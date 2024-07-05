from easyRTML.process import Processor
from easyRTML.extract import Extractor
from easyRTML.xg import XGML
import re
import os
import pickle
import numpy as np


class pyRTML:
    def __init__(self, processor: Processor, extractor: Extractor, xgml_model: XGML):
        self.processor = processor
        self.extractor = extractor
        self.xgml_model = xgml_model
        self.extractor.process_data(self.processor.normalized_df)  # Process data using normalized DataFrame

        # Retrieve selected features from XGML model
        self.selected_features = xgml_model.selected_features
        # Retrieve inverse_label_mapping from XGML model
        self.inverse_label_mapping = xgml_model.inverse_label_mapping

        # Initialize variables from Processor and Extractor
        self.offsets = self.processor.get_offsets()
        self.scales = self.processor.get_scales()
        self.num_columns = self.processor.get_num_columns()
        self.buffer_length = self.extractor.get_variables()['buffer_length']
        self.shift_length = self.extractor.get_variables()['shift_length']
        self.rem_length = self.extractor.get_variables()['rem_length']
        self.column_numbers = self.processor.get_column_numbers()
        self.window_length = self.extractor.get_variables()['window_length']
        self.hop_size = self.extractor.get_variables()['hop_size']

    def easyRTML_python_generate(self, model_file="xgboost.pkl", serial_port='COM5', baud_rate=9600):
        # Function to interpret feature names and generate statements indicating the calculation to be performed
        def generate_calculation_statements(selected_features):
            statements = []
            for feature in selected_features:
                parts = feature.split('_')
                col_name = '_'.join(parts[:-1])  # Extract the feature name
                calculation = parts[-1]  # Extract the calculation to be performed
                col_num = self.column_numbers.get(col_name, None)  # Get the column number
                if col_num is not None:
                    if calculation == 'max':
                        statements.append(f"For the {col_num}th iteration, calculate the maximum value.")
                    elif calculation == 'min':
                        statements.append(f"For the {col_num}th iteration, calculate the minimum value.")
                    elif calculation == 'mean':
                        statements.append(f"For the {col_num}th iteration, calculate the mean value.")
                    elif calculation == 'rms':
                        statements.append(f"For the {col_num}th iteration, calculate the rms value.")
                    # Add more conditions as needed
                else:
                    print(f"Error: Could not find column number for feature '{col_name}'.")
            return statements

        # Generate calculation statements for selected features
        calculation_statements = generate_calculation_statements(self.selected_features)

        code = [
            "import serial",
            "import numpy as np",
            "import pickle",
            "import time",
            "import warnings",
            "import xgboost as xgb",
            "from sklearn.ensemble import RandomForestClassifier",
            "warnings.filterwarnings('ignore')",
            "",
            "",
            "class Step0:",
            "    def __init__(self, offset=None, scale=None):",
            f"        self.offset = np.array({self.offsets})",
            f"        self.scale = np.array({self.scales})",
            "",
            "    def transform(self, X):",
            f"        if X.shape[0] != {len(self.offsets)}:",
            f"            raise ValueError(f\"Input data must have {len(self.offsets)} features,\")",
            "        X = (X - self.offset) * self.scale",
            "        X[X < 0] = 0",
            "        X[X > 1] = 1",
            "        return X",
            "",
            "",
            "class Window:",
            "    def __init__(self):",
            f"        self.queue = np.zeros({self.buffer_length})",
            "        self.head = 0",
            "",
            "    def transform(self, x):",
            f"        self.queue[self.head:self.head + {self.num_columns}] = x",
            f"        self.head += {self.num_columns}",
            "",
            f"        if self.head == {self.buffer_length}:",
            "            transformed_array = self.queue.copy()",
            f"            self.queue[:{self.rem_length}] = self.queue[{self.shift_length}:]",
            f"            self.queue[{self.rem_length}:] = 0",
            f"            self.head -= {self.shift_length}",
            "            return transformed_array",
            "",
            "",
        ]

        # Regular expression pattern to match iteration numbers in words
        iteration_pattern = re.compile(r'(\d+)(?:st|nd|rd|th)')

        iteration_numbers = []
        feature_names = []

        for statement in calculation_statements:
            parts = statement.split()
            iteration_match = iteration_pattern.search(statement)
            if iteration_match:
                iteration_num = int(iteration_match.group(1))
                feature_name = parts[-2]  # Extract feature name
                iteration_numbers.append(iteration_num)
                feature_names.append(feature_name)

        code.extend([
            "class Step2:",
            "    def __init__(self):",
            "        pass",
            "",
            "    def transform(self, x):",
            "        features = []",
            f"        for iteration in range(1, {self.num_columns + 1}):",
            f"            x_subset = x[iteration-1::{self.num_columns}]",
            "            x_subset = np.asarray(x_subset)",
            "",
        ])

        prev_iteration = None
        for iteration, feature_name in zip(iteration_numbers, feature_names):
            if prev_iteration is None:
                code.append(f"            if iteration == {iteration}:")
            elif prev_iteration != iteration:
                code.append(f"            elif iteration == {iteration}:")
            prev_iteration = iteration
            if feature_name == 'mean':
                code.append("                features.append(np.mean(x_subset))")
            elif feature_name == 'minimum':
                code.append("                features.append(np.min(x_subset))")
            elif feature_name == 'maximum':
                code.append("                features.append(np.max(x_subset))")
            elif feature_name == 'rms':
                code.append("                features.append(np.sqrt(np.mean(x_subset ** 2)))")

        code.extend([
            "",
            "        return np.array(features)",
            "",
            "# Load the trained model from a file",
            f"with open('{model_file}', 'rb') as model_file:",
            "    model_selected = pickle.load(model_file)",
            "",
            "#pipeline",
            "step0 = Step0()",
            "window = Window()",
            "step2 = Step2()",
            "",
            "# Initialize serial port",
            f"serial_port = '{serial_port}'",
            f"baud_rate = {baud_rate}",
            "ser = serial.Serial(serial_port, baud_rate)",
            "",
            "last_10_features = []",
            "",
            "start_time_overall = time.time()",
            "",
            "prediction_made = False",
            f"inverse_label_mapping = {self.inverse_label_mapping}",
            "",
            "# Loop to read data from serial port, perform transformations, and predict the label",
            "while True:",
            "    try:",
            "        current_time = time.time()",
            "        elapsed_time = current_time - start_time_overall",
            "        if elapsed_time > 10:",
            "            if not prediction_made:",
            "                print('Error: Run code again')",
            "                break",
            "",
            "",
            "        try:",
            "            line = ser.readline().decode('utf-8', errors='ignore').strip()",
            "            if not line:",
            "                continue",
            "            data = [float(x) for x in line.split(',')]  # Assuming data is comma-separated float values",
            "        except (UnicodeDecodeError, ValueError) as e:",
            "            print(f'Error reading data: {e}')",
            "            continue",
            "",
            "        try:",
            "            transformed_data_step0 = step0.transform(np.array(data))",
            "        except ValueError as e:",
            "            print(f'Transformation error: {e}')",
            "            continue",
            "",
            "        transformed_array = window.transform(transformed_data_step0)",
            "",
            "        if transformed_array is not None:",
            "            feature_output = step2.transform(transformed_array)",
            "#            print('Feature Output:', feature_output)",
            "",
            "            last_10_features.append(feature_output)",
            "            if len(last_10_features) > 10:",
            "                last_10_features.pop(0)",
            "            if len(last_10_features) == 10 and all(np.array_equal(last_10_features[0], f) for f in last_10_features):",
            "                print('Error: Run again')  ",
            "                break",
            "",
            "            feature_output_reshaped = feature_output.reshape(1, -1)",
            "            start_time = time.time()  # Record start time for prediction",
            "            predicted_label = model_selected.predict(feature_output_reshaped)[0] ",
            "            predicted_label_name = inverse_label_mapping[predicted_label]",
            "            print('Predicted Label:', predicted_label_name)",
            "",
            "            prediction_made = True",
            "            end_time = time.time()  ",
            "            elapsed_time = end_time - start_time",
            "            print(f'Time taken for prediction: {1000 * elapsed_time:.2f} ms')",
            "",
            "            print()",
            "    except KeyboardInterrupt:",
            "        print('Interrupted by user')",
            "        break",
            "ser.close()",
            "",
        ])

        return "\n".join(code)
    
    def execute_generated_code(self, model_file="xgboost.pkl", serial_port='COM5', baud_rate=9600):
        # Generate the Python code
        generated_code = self.easyRTML_python_generate(model_file=model_file, serial_port=serial_port, baud_rate=baud_rate)

        # Execute the generated code
        try:
            exec(generated_code, globals())
        except Exception as e:
            print(f"Error executing generated code: {e}")


    def save_code_to_file(self, code, folder_name="easyRTML", file_name="easyRTML_python_code.py"):
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Define the file path
        file_path = os.path.join(folder_name, file_name)

        # Save the code to the file
        with open(file_path, 'w') as file:
            file.write(code)
            
