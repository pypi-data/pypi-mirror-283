import os
import pickle
import re
import xgboost as xgb
from easyRTML import XGML

def parse_tree(tree):
    lines = tree.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    return lines

def extract_feature_index(feature_name, class_names):
    if feature_name in class_names:
        return class_names.index(feature_name)
    else:
        raise ValueError(f"Feature name '{feature_name}' not found in class_names.")

def tree_to_code(tree, class_names, class_label):
    def recurse(lines, depth):
        if not lines:
            return ""
        
        line = lines.pop(0)
        indent = " " * depth * 4
        
        if re.match(r'\d+:\[.*<.*\] yes=\d+,no=\d+,missing=\d+', line):
            split_info = re.search(r'(\d+):\[(.*)<(.*)\] yes=(\d+),no=(\d+),missing=(\d+)', line)
            if split_info:
                feature_name = split_info.group(2)
                operator = '<='
                threshold = float(split_info.group(3))
                feature_index = extract_feature_index(feature_name, class_names)
                code = f"{indent}if (x[{feature_index}] {operator} {threshold}) {{\n"
                code += recurse(lines, depth + 1)
                code += f"{indent}}}\n{indent}else {{\n"
                code += recurse(lines, depth + 1)
                code += f"{indent}}}\n"
                return code
            else:
                raise ValueError(f"Unexpected line format: {line}")
        
        elif re.match(r'\d+:leaf.*', line):
            leaf_value = float(line.split('=')[1])
            return f"{indent}votes[{class_label}] += {leaf_value};\n"
        
        else:
            raise ValueError(f"Unexpected line format: {line}")

    lines = parse_tree(tree)
    return recurse(lines, 1)

def model_to_code(model, class_names, label_mapping):
    trees = model.get_booster().get_dump()
    num_classes = len(model.classes_)  # Number of classes
    code = "#ifndef CLASSIFIER_H\n"
    code += "#define CLASSIFIER_H\n"
    code += "#include <Arduino.h>\n"
    code += "#include <vector>\n"
    code += "#include <string>\n\n"
    code += "class easyRTML_classifier {\n"
    code += "public:\n"
    code += "    /**\n"
    code += "     * Predict class for features vector\n"
    code += "     */\n"
    code += "     String predict(float *x) {\n"
    code += f"        float votes[{num_classes}] = {{ 0.0f }};\n"

    for i, tree in enumerate(trees):
        class_index = i % num_classes
        label_name = next(key for key, value in label_mapping.items() if value == class_index)
        code += f"        // Tree #{i + 1}\n"
        code += tree_to_code(tree, class_names, class_index)
    
    code += "         String predictedLabel;\n"
    code += "        float maxVotes = -999999999;\n\n"

    for label, index in label_mapping.items():
        code += f"        // Compare votes for {label} class\n"
        code += f"        if (votes[{index}] > maxVotes) {{\n"
        code += f"            predictedLabel = \"{label}\";\n"
        code += f"            maxVotes = votes[{index}];\n"
        code += "        }\n\n"

    code += "        return predictedLabel;\n"
    code += "    }\n"
    code += "};\n"
    code += "#endif\n"

    return code

def Port_model(model_type, load_the_model, xgml_instance):
    if model_type != "easyRTML_Xgboost":
        raise ValueError("Only Xgboost model type is supported")

    # Extract selected_features and label_mapping from XGML instance
    selected_features = xgml_instance.selected_features
    label_mapping = xgml_instance.label_mapping

    # Load the model
    with open(load_the_model, 'rb') as f:
        model = pickle.load(f)
    
    # Generate the C++ code
    cpp_code = model_to_code(model, selected_features, label_mapping)

    # Ensure the directory structure exists
    output_dir = os.path.join("easyRTML", "Xgboost_Classifier_easyRTML")
    os.makedirs(output_dir, exist_ok=True)

    # Save the C++ code to Classifier.h
    output_file = os.path.join(output_dir, "classifier.h")
    with open(output_file, 'w') as f:
        f.write(cpp_code)
    
    return cpp_code

def generate_code(model_type, model_filename, xgml_instance):
    cpp_code = Port_model(model_type, model_filename, xgml_instance)
    return cpp_code



import os
import pickle
import re
import xgboost as xgb
from easyRTML import XGML
import numpy as np
from sklearn.tree import _tree

def parse_tree(tree):
    lines = tree.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    return lines

def extract_feature_index(feature_name, class_names):
    if feature_name in class_names:
        return class_names.index(feature_name)
    else:
        raise ValueError(f"Feature name '{feature_name}' not found in class_names.")

def tree_to_code(tree, class_names, class_label):
    def recurse(lines, depth):
        if not lines:
            return ""
        
        line = lines.pop(0)
        indent = " " * depth * 4
        
        if re.match(r'\d+:\[.*<.*\] yes=\d+,no=\d+,missing=\d+', line):
            split_info = re.search(r'(\d+):\[(.*)<(.*)\] yes=(\d+),no=(\d+),missing=(\d+)', line)
            if split_info:
                feature_name = split_info.group(2)
                operator = '<='
                threshold = float(split_info.group(3))
                feature_index = extract_feature_index(feature_name, class_names)
                code = f"{indent}if (x[{feature_index}] {operator} {threshold}) {{\n"
                code += recurse(lines, depth + 1)
                code += f"{indent}}}\n{indent}else {{\n"
                code += recurse(lines, depth + 1)
                code += f"{indent}}}\n"
                return code
            else:
                raise ValueError(f"Unexpected line format: {line}")
        
        elif re.match(r'\d+:leaf.*', line):
            leaf_value = float(line.split('=')[1])
            return f"{indent}votes[{class_label}] += {leaf_value};\n"
        
        else:
            raise ValueError(f"Unexpected line format: {line}")

    lines = parse_tree(tree)
    return recurse(lines, 1)

def multi_feature_tree_to_arduino(tree, feature_names, class_names):
    tree_ = tree.tree_
    feature_names = list(feature_names)
    class_names = list(class_names)

    def recurse(node, depth):
        indent = "    " * (depth + 2)  # Adjusted for the method indentation
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_names[tree_.feature[node]]
            threshold = tree_.threshold[node]
            code = []
            code.append(f"{indent}if (features[{feature_names.index(name)}] <= {threshold}) {{")
            code.extend(recurse(tree_.children_left[node], depth + 1))
            code.append(f"{indent}}} else {{")
            code.extend(recurse(tree_.children_right[node], depth + 1))
            code.append(f"{indent}}}")
            return code
        else:
            class_probs = tree_.value[node][0]  # Multiclass probabilities at the leaf node
            class_idx = np.argmax(class_probs)
            class_name = class_names[class_idx]
            return [f'{indent}votes[{class_idx}] += {class_probs[class_idx]};']

    code = recurse(0, 1)
    return "\n".join(code)

def model_to_code(model, selected_features, label_mapping, model_type):
    inverse_label_mapping = {v: k for k, v in label_mapping.items()}
    num_classes = len(model.classes_) if model_type == "easyRTML_RandomForest" else len(model.classes_)
    
    code = "#ifndef CLASSIFIER_H\n"
    code += "#define CLASSIFIER_H\n"
    code += "#include <Arduino.h>\n"
    code += "#include <vector>\n"
    code += "#include <string>\n\n"
    code += "class easyRTML_classifier {\n"
    code += "public:\n"
    code += "    /**\n"
    code += "     * Predict class for features vector\n"
    code += "     */\n"
    code += "    String predict(float *features) {\n"
    code += f"        float votes[{num_classes}] = {{ 0.0f }};\n"

    if model_type == "easyRTML_Xgboost":
        trees = model.get_booster().get_dump()
        for i, tree in enumerate(trees):
            class_index = i % num_classes
            label_name = next(key for key, value in label_mapping.items() if value == class_index)
            code += f"        // Tree #{i + 1}\n"
            code += tree_to_code(tree, selected_features, class_index)
    else:
        for i, estimator in enumerate(model.estimators_):
            code += f"        // Tree {i + 1}\n"
            tree_code = multi_feature_tree_to_arduino(estimator, model.feature_names_in_, model.classes_)
            code += tree_code
            code += "\n\n"

    code += "        String predictedLabel;\n"
    code += "        float maxVotes = -999999999;\n\n"

    for idx, class_name in enumerate(model.classes_):
        code += f"        if (votes[{idx}] > maxVotes) {{\n"
        code += f"            predictedLabel = \"{inverse_label_mapping[class_name]}\";\n"
        code += f"            maxVotes = votes[{idx}];\n"
        code += "        }\n\n"

    code += "        return predictedLabel;\n"
    code += "    }\n"
    code += "};\n"
    code += "#endif\n"

    return code

def Port_model(model_type, load_the_model, xgml_instance):
    if model_type not in ["easyRTML_Xgboost", "easyRTML_RandomForest"]:
        raise ValueError("Only Xgboost and RandomForest model types are supported")

    # Extract selected_features and label_mapping from XGML instance
    selected_features = xgml_instance.selected_features
    label_mapping = xgml_instance.label_mapping

    # Load the model
    with open(load_the_model, 'rb') as f:
        model = pickle.load(f)
    
    # Generate the C++ code
    cpp_code = model_to_code(model, selected_features, label_mapping, model_type)

    # Ensure the directory structure exists
    output_dir = os.path.join("easyRTML", f"{model_type}_Classifier_easyRTML")
    os.makedirs(output_dir, exist_ok=True)

    # Save the C++ code to Classifier.h
    output_file = os.path.join(output_dir, "classifier.h")
    with open(output_file, 'w') as f:
        f.write(cpp_code)
    
    return cpp_code

def generate_code(model_type, model_filename, xgml_instance):
    cpp_code = Port_model(model_type, model_filename, xgml_instance)
    return cpp_code
