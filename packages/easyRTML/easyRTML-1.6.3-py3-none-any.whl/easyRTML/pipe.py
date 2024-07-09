# from easyRTML.process import Processor
# from easyRTML.extract import Extractor
# from easyRTML.xg import XGML  

# class Pipe:
#     def __init__(self, processor: Processor, extractor: Extractor, xgml_model: XGML):
#         self.processor = processor
#         self.extractor = extractor
#         self.xgml_model = xgml_model
#         self.extractor.process_data(self.processor.normalized_df)  # Process data using normalized DataFrame

#         # Retrieve selected features from XGML model
#         self.selected_features = xgml_model.selected_features
#         # Retrieve inverse_label_mapping from XGML model
#         self.inverse_label_mapping = xgml_model.inverse_label_mapping

#         self.print_variables()

#     def print_variables(self):
#         # Variables from Processor
#         variables = self.extractor.get_variables()

#         offsets = self.processor.get_offsets()
#         scales = self.processor.get_scales()
#         num_columns = self.processor.get_num_columns()
#         buffer_length = variables['buffer_length']
#         shift_length = variables['shift_length']
#         column_numbers = self.processor.get_column_numbers()
#         total_num_features = len(self.selected_features)
#         hop_size = variables['hop_size']
#         rem_length = variables['rem_length']
#         window_length = variables['window_length']
#         # Print all variables
#         print("Selected Features:", self.selected_features)
#         print("Offsets:", offsets)
#         print("Scales:", scales)
#         print("Columns except 'label' and 'label_name':", self.processor.get_columns_except_label())
#         print("Number of columns except 'label' and 'label_name':", num_columns)
#         print("Column numbers:", column_numbers)
#         print("Window length:", window_length)
#         print("Hop size:", hop_size)
#         print("Buffer length:", buffer_length)
#         print("Remaining length:", rem_length)
#         print("Shift length:", shift_length)
#         print("Total number of features:", total_num_features)
#         print("Inverse Label Mapping:", self.inverse_label_mapping)

import os
import re
from easyRTML.process import Processor
from easyRTML.extract import Extractor
from easyRTML.xg import XGML

class Pipe:
    def __init__(self, processor: Processor, extractor: Extractor, xgml_model: XGML):
        self.processor = processor
        self.extractor = extractor
        self.xgml_model = xgml_model
        self.extractor.process_data(self.processor.normalized_df)  # Process data using normalized DataFrame

        # Retrieve selected features from XGML model
        self.selected_features = xgml_model.selected_features

    def print_variables(self):
        # Variables from Processor and Extractor
        variables = self.extractor.get_variables()
        offsets = self.processor.get_offsets()
        scales = self.processor.get_scales()
        num_columns = self.processor.get_num_columns()
        buffer_length = variables['buffer_length']
        shift_length = variables['shift_length']
        column_numbers = self.processor.get_column_numbers()
        total_num_features = len(self.selected_features)
        hop_size = variables['hop_size']
        rem_length = variables['rem_length']
        window_length = variables['window_length']

        # Print all variables
        # print("Selected Features:", self.selected_features)
        # print("Offsets:", offsets)
        # print("Scales:", scales)
        # print("Columns except 'label' and 'label_name':", self.processor.get_columns_except_label())
        # print("Number of columns except 'label' and 'label_name':", num_columns)
        # print("Column numbers:", column_numbers)
        # print("Window length:", window_length)
        # print("Hop size:", hop_size)
        # print("Buffer length:", buffer_length)
        # print("Remaining length:", rem_length)
        # print("Shift length:", shift_length)
        # print("Total number of features:", total_num_features)

        # Return variables for use in generating C++ code
        return {
            'offsets': offsets,
            'scales': scales,
            'num_columns': num_columns,
            'buffer_length': buffer_length,
            'shift_length': shift_length,
            'column_numbers': column_numbers,
            'total_num_features': total_num_features,
            'hop_size': hop_size,
            'rem_length': rem_length,
            'window_length': window_length,
            'selected_features': self.selected_features
        }

    def generate_cpp_code(self):
        variables = self.print_variables()  # Retrieve variables from print_variables method
        offsets = variables['offsets']
        scales = variables['scales']
        num_columns = variables['num_columns']
        buffer_length = variables['buffer_length']
        shift_length = variables['shift_length']
        column_numbers = variables['column_numbers']
        total_num_features = variables['total_num_features']
        selected_features = variables['selected_features']

        # Function to generate calculation statements
        def generate_calculation_statements(selected_features):
            statements = []
            for feature in selected_features:
                parts = feature.split('_')
                col_name = '_'.join(parts[:-1])  # Extract the feature name
                calculation = parts[-1]   # Extract the calculation to be performed
                col_num = column_numbers.get(col_name, None)  # Get the column number from the column_numbers dictionary
                if col_num is not None:
                    calc_dict = {
                        'max': 'maximum',
                        'min': 'minimum',
                        'mean': 'mean',
                        'rms': 'rms'
                    }
                    if calculation in calc_dict:
                        statements.append(f"For the {col_num}th iteration, calculate the {calc_dict[calculation]} value.")
                else:
                    print(f"Error: Could not find column number for feature '{col_name}'.")
            return statements

        # Regular expression pattern to match iteration numbers in words
        iteration_pattern = re.compile(r'(\d+)(?:st|nd|rd|th)')

        calculation_statements = generate_calculation_statements(selected_features)
        iteration_numbers = []
        feature_names = []

        # Extract iteration numbers and feature names from calculation statements
        for statement in calculation_statements:
            iteration_match = iteration_pattern.search(statement)
            if iteration_match:
                iteration_num = int(iteration_match.group(1))
                feature_name = statement.split()[-2]  # Extract feature name
                iteration_numbers.append(iteration_num)
                feature_names.append(feature_name)

        # Map long feature names to their short forms
        name_map = {
            'minimum': 'min',
            'maximum': 'max'
        }
        feature_names = [name_map.get(name, name) for name in feature_names]

        # Function to generate the output C++ code
        def generate_output(offsets, scales):
            offset_str = ""
            scale_str = ""

            # Generate offset assignments
            for i in range(len(offsets)):
                offset_str += f"offset[{i}] = {offsets[i]}; "
                if i % 3 == 2:
                    offset_str += "\n      "

            offset_str = offset_str.strip()  # Remove trailing whitespace and newlines

            # Generate scale assignments
            for i in range(len(scales)):
                scale_str += f"scale[{i}] = {scales[i]}; "
                if i % 2 == 1:
                    scale_str += "\n      "

            scale_str = scale_str.strip()  # Remove trailing whitespace and newlines

            # Prepare final output
            output = f"      {offset_str}\n\n      // Initialize scale array with pre-determined values\n      {scale_str}"

            return output

        # Function to generate the calculation of features part of the C++ code
        def generate_feature_calculation(iteration_numbers, feature_names, total_num_features):
            output = ""

            # Function to determine if we need to calculate mean or rms for a given iteration
            def calculate_extras(iter_num):
                features_for_iter = [f for i, f in zip(iteration_numbers, feature_names) if i == iter_num]
                extras = ""
                if 'mean' in features_for_iter:
                    extras += "        float meanVal = sum / count;\n"
                if 'rms' in features_for_iter:
                    extras += "        float rmsVal = sqrt(sumSquares / count);\n"
                return extras

            # Collect unique iteration numbers
            unique_iters = sorted(set(iteration_numbers))

            # Iterate through the unique iteration numbers
            for unique_iter in unique_iters:
                if_clause = "if" if unique_iter == unique_iters[0] else "else if"
                output += f"      {if_clause} (iteration == {unique_iter - 1}) {{ // Calculate features for iteration {unique_iter}\n"
                output += calculate_extras(unique_iter)
                for idx, (iter_num, feature) in enumerate(zip(iteration_numbers, feature_names)):
                    if iter_num == unique_iter:
                        output += f"        features[{idx}] = {feature}Val; // {feature.capitalize()}\n"
                output += "      }\n"

            return output

        # Assemble the final C++ code
        generated_cpp_code = ""
        generated_cpp_code += f"#ifndef PIPELINE_H\n"
        generated_cpp_code += f"#define PIPELINE_H\n"
        generated_cpp_code += f"\n"
        generated_cpp_code += f"#include <Arduino.h>\n"
        generated_cpp_code += f"#include <float.h>\n"
        generated_cpp_code += f"#include <stdint.h> \n"
        generated_cpp_code += f"#include \"classifier.h\"\n"
        generated_cpp_code += f"\n"
        generated_cpp_code += f"class Pipeline {{\n"
        generated_cpp_code += f"  public:\n"
        generated_cpp_code += f"    Pipeline() : bufferIndex(0) {{\n"
        generated_cpp_code += generate_output(offsets, scales)
        generated_cpp_code += f"    }}\n"
        generated_cpp_code += f"    void reset() {{\n"
        generated_cpp_code += f"      bufferIndex = 0;\n"
        generated_cpp_code += f"      memset(buffer, 0, sizeof(buffer));\n"
        generated_cpp_code += f"    }}\n"
        generated_cpp_code += f"    bool normalizeAndBuffer(float rawData[{num_columns}]) {{\n"
        generated_cpp_code += f"      if (!rawData) {{\n"
        generated_cpp_code += f"        Serial.println(\"Error: Input data is null\");\n"
        generated_cpp_code += f"        return false;\n"
        generated_cpp_code += f"      }}\n"
        generated_cpp_code += f"      if (bufferIndex + {num_columns} > bufferSize) {{\n"
        generated_cpp_code += f"        Serial.println(\"Error: Buffer overflow\");\n"
        generated_cpp_code += f"        return false;\n"
        generated_cpp_code += f"      }}\n"
        generated_cpp_code += f"      for (int i = 0; i < {num_columns}; i++) {{\n"
        generated_cpp_code += f"        float normalizedValue = (rawData[i] - offset[i]) * scale[i];\n"
        generated_cpp_code += f"        normalizedValue = constrain(normalizedValue, 0.0, 1.0);\n"
        generated_cpp_code += f"        buffer[bufferIndex++] = normalizedValue;\n"
        generated_cpp_code += f"      }}\n"
        generated_cpp_code += f"      if (bufferIndex >= bufferSize) {{\n"
        generated_cpp_code += f"        calculateFeatures();\n"
        generated_cpp_code += f"        shiftBuffer();\n"
        generated_cpp_code += f"        bufferIndex = bufferSize - shiftSize;\n"
        generated_cpp_code += f"      }}\n"
        generated_cpp_code += f"      return true;\n"
        generated_cpp_code += f"    }}\n"
        generated_cpp_code += f"    String getPrediction() {{\n"
        generated_cpp_code += f"      return currentPrediction;\n"
        generated_cpp_code += f"    }}\n"
        generated_cpp_code += f"  private:\n"
        generated_cpp_code += f"    static const uint32_t bufferSize = {buffer_length};\n"
        generated_cpp_code += f"    static const uint32_t shiftSize = {shift_length};\n"
        generated_cpp_code += f"    float buffer[bufferSize];\n"
        generated_cpp_code += f"    uint32_t bufferIndex;\n"
        generated_cpp_code += f"    float offset[{num_columns}];\n"
        generated_cpp_code += f"    float scale[{num_columns}];\n"
        generated_cpp_code += f"    easyRTML_classifier classifier;\n"
        generated_cpp_code += f"    uint32_t predictionTime;\n"
        generated_cpp_code += f"    String currentPrediction;\n"
        generated_cpp_code += f"    void shiftBuffer() {{\n"
        generated_cpp_code += f"      memmove(buffer, buffer + shiftSize, (bufferSize - shiftSize) * sizeof(float));\n"
        generated_cpp_code += f"      memset(buffer + (bufferSize - shiftSize), 0, shiftSize * sizeof(float));\n"
        generated_cpp_code += f"    }}\n"
        generated_cpp_code += f"    void calculateFeatures() {{\n"
        generated_cpp_code += f"      float features[{total_num_features}];\n"
        generated_cpp_code += f"      int featureCount = 0;\n"
        generated_cpp_code += f"      for (int iteration = 0; iteration < {num_columns}; iteration++) {{\n"
        generated_cpp_code += f"        int count = 0;\n"
        generated_cpp_code += f"        float sum = 0.0, sumSquares = 0.0;\n"
        generated_cpp_code += f"        float maxVal = -FLT_MAX, minVal = FLT_MAX;\n"
        generated_cpp_code += f"        float featureArray[bufferSize / {num_columns}];\n"
        generated_cpp_code += f"        int featureIndex = 0;\n"
        generated_cpp_code += "         // The loop should calculate maxVal and minVal\n";
        generated_cpp_code += "         for (uint32_t i = iteration; i < bufferSize; i += 6) {\n";
        generated_cpp_code += "         float value = buffer[i];\n";
        generated_cpp_code += "         sum += value;\n";
        generated_cpp_code += "         sumSquares += value * value;\n";
        generated_cpp_code += "         if (value > maxVal) maxVal = value; // This line is correct\n";
        generated_cpp_code += "         if (value < minVal) minVal = value; // This line is correct\n";
        generated_cpp_code += "         featureArray[featureIndex++] = value;\n";
        generated_cpp_code += "       }\n";

        generated_cpp_code += generate_feature_calculation(iteration_numbers, feature_names, total_num_features)
        generated_cpp_code += f"     }}\n"
        generated_cpp_code += f"     classifyFeatures(features);\n"
        generated_cpp_code += f"    }}\n"
        generated_cpp_code += f"    void classifyFeatures(float features[]) {{\n"
        generated_cpp_code += f"      uint32_t startTime = micros();\n"
        generated_cpp_code += f"      currentPrediction = classifier.predict(features);\n"
        generated_cpp_code += f"      predictionTime = micros() - startTime;\n"
        generated_cpp_code += f"      Serial.print(\"Prediction: \");\n"
        generated_cpp_code += f"      Serial.print(currentPrediction);\n"
        generated_cpp_code += f"      Serial.print(\" Prediction Time: \");\n"
        generated_cpp_code += f"      Serial.print(predictionTime);\n"
        generated_cpp_code += f"      Serial.println(\"μs\");\n"
        generated_cpp_code += f"    }}\n"
        generated_cpp_code += f"}};\n"
        generated_cpp_code += f"\n"
        generated_cpp_code += f"#endif\n"

        return generated_cpp_code

    def save_cpp_code(self):
        # Ensure the directory structure exists
        output_dir = os.path.join("easyRTML", "Pipeline_easyRTML")
        os.makedirs(output_dir, exist_ok=True)

        # Save the C++ code to pipeline.h
        output_file = os.path.join(output_dir, "pipeline.h")
        with open(output_file, 'w') as f:
            f.write(self.generate_cpp_code())


        print(self.generate_cpp_code())


# Example usage:
# if __name__ == "__main__":
#     processor = Processor()  # Initialize Processor instance
#     extractor = Extractor()  # Initialize Extractor instance
#     xgml_model = XGML()  # Initialize XGML instance

#     pipe = Pipe(processor, extractor, xgml_model)  # Initialize Pipe instance
#     pipe.save_cpp_code()  # Generate and save C++ code
