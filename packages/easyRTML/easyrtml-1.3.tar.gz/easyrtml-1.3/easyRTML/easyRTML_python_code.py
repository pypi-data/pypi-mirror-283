import serial
import numpy as np
import pickle
import time
import warnings
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
warnings.filterwarnings('ignore')


class Step0:
    def __init__(self, offset=None, scale=None):
        self.offset = np.array([-19.05, -15.34, -3.22, -7.36, -3.71, -8.73])
        self.scale = np.array([0.022696323195642305, 0.031201248049921998, 0.04258943781942078, 0.08257638315441784, 0.14662756598240467, 0.0572737686139748])

    def transform(self, X):
        if X.shape[0] != 6:
            raise ValueError(f"Input data must have 6 features,")
        X = (X - self.offset) * self.scale
        X[X < 0] = 0
        X[X > 1] = 1
        return X


class Window:
    def __init__(self):
        self.queue = np.zeros(1638)
        self.head = 0

    def transform(self, x):
        self.queue[self.head:self.head + 6] = x
        self.head += 6

        if self.head == 1638:
            transformed_array = self.queue.copy()
            self.queue[:1152] = self.queue[486:]
            self.queue[1152:] = 0
            self.head -= 486
            return transformed_array


class Step2:
    def __init__(self):
        pass

    def transform(self, x):
        features = []
        for iteration in range(1, 7):
            x_subset = x[iteration-1::6]
            x_subset = np.asarray(x_subset)

            if iteration == 1:
                features.append(np.max(x_subset))
            elif iteration == 2:
                features.append(np.max(x_subset))
            elif iteration == 3:
                features.append(np.max(x_subset))
            elif iteration == 6:
                features.append(np.min(x_subset))

        return np.array(features)

# Load the trained model from a file
with open('XgBoost.pkl', 'rb') as model_file:
    model_selected = pickle.load(model_file)

#pipeline
step0 = Step0()
window = Window()
step2 = Step2()

# Initialize serial port
serial_port = '/dev/cu.usbserial-0001'
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)

last_10_features = []

start_time_overall = time.time()

prediction_made = False
inverse_label_mapping = {0: 'ideal', 1: 'ud', 2: 'leftr'}

# Loop to read data from serial port, perform transformations, and predict the label
while True:
    try:
        current_time = time.time()
        elapsed_time = current_time - start_time_overall
        if elapsed_time > 10:
            if not prediction_made:
                print('Error: Run code again')
                break


        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue
            data = [float(x) for x in line.split(',')]  # Assuming data is comma-separated float values
        except (UnicodeDecodeError, ValueError) as e:
            print(f'Error reading data: {e}')
            continue

        try:
            transformed_data_step0 = step0.transform(np.array(data))
        except ValueError as e:
            print(f'Transformation error: {e}')
            continue

        transformed_array = window.transform(transformed_data_step0)

        if transformed_array is not None:
            feature_output = step2.transform(transformed_array)
#            print('Feature Output:', feature_output)

            last_10_features.append(feature_output)
            if len(last_10_features) > 10:
                last_10_features.pop(0)
            if len(last_10_features) == 10 and all(np.array_equal(last_10_features[0], f) for f in last_10_features):
                print('Error: Run again')  
                break

            feature_output_reshaped = feature_output.reshape(1, -1)
            start_time = time.time()  # Record start time for prediction
            predicted_label = model_selected.predict(feature_output_reshaped)[0] 
            predicted_label_name = inverse_label_mapping[predicted_label]
            print('Predicted Label:', predicted_label_name)

            prediction_made = True
            end_time = time.time()  
            elapsed_time = end_time - start_time
            print(f'Time taken for prediction: {1000 * elapsed_time:.2f} ms')

            print()
    except KeyboardInterrupt:
        print('Interrupted by user')
        break
ser.close()
