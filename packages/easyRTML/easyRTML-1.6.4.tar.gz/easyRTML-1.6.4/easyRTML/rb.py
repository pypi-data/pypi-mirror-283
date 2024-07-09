# import pandas as pd
# import numpy as np
# from sklearn.model_selection import StratifiedKFold
# from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.ensemble import RandomForestClassifier
# import pickle
# import warnings

# warnings.filterwarnings('ignore', category=UserWarning)

# class RBML:
#     def __init__(self, shuffled_df, random_state=42):
#         self.shuffled_df = shuffled_df
#         self.X = shuffled_df.drop(['label', 'label_name'], axis=1, errors='ignore')
#         self.y = shuffled_df['label_name']
#         self.label_mapping, self.inverse_label_mapping = self.create_label_mappings(self.y)
#         self.y_mapped = self.y.map(self.label_mapping)
#         self.random_state = random_state
        
#         # Initialize attributes to store selected features and label mapping
#         self.selected_features = None
#         self.label_mapping = self.label_mapping
#         self.inverse_label_mapping = self.inverse_label_mapping

#     def create_label_mappings(self, y):
#         """
#         Create label mappings for the target variable.
#         """
#         labels = y.unique()
#         label_mapping = {label: idx for idx, label in enumerate(labels)}
#         inverse_label_mapping = {idx: label for label, idx in label_mapping.items()}
#         return label_mapping, inverse_label_mapping

#     def arrange_features(self, selected_features):
#         """
#         Arrange selected features based on a naming convention.
#         """
#         arranged_features = []
#         feature_groups = {}

#         for feature in selected_features:
#             feature_name, _, indicator = feature.partition('_')
#             feature_groups.setdefault(feature_name, []).append((indicator, feature))

#         for feature_name, features in feature_groups.items():
#             features.sort(key=lambda x: x[0])
#             arranged_features.extend(feature for _, feature in features)

#         return arranged_features

#     def get_cross_validated_accuracy(self, X, y_mapped, selected_features, rf_params, cv_params):
#         """
#         Train Random Forest model and return cross-validated accuracy.
#         """
#         if not selected_features:
#             return 0  # No features selected, return 0 accuracy

#         kf = StratifiedKFold(**cv_params)
#         accuracies = []

#         for train_index, test_index in kf.split(X, y_mapped):
#             X_train_cv, X_test_cv = X.iloc[train_index], X.iloc[test_index]
#             y_train_cv, y_test_cv = y_mapped.iloc[train_index], y_mapped.iloc[test_index]

#             model = RandomForestClassifier(**rf_params)
#             model.fit(X_train_cv[selected_features], y_train_cv)
#             y_pred_cv = model.predict(X_test_cv[selected_features])
#             accuracy = accuracy_score(y_test_cv, y_pred_cv)
#             accuracies.append(accuracy)

#         return np.mean(accuracies)

#     def feature_selection(self, X, y_mapped, rf_params, cv_params, accuracy_improvement_threshold=0.01):
#         """
#         Perform feature selection using cross-validation.
#         """
#         selected_features = []
#         best_accuracy = 0
#         available_features = list(X.columns)

#         while available_features:
#             best_feature = None
#             for feature in available_features:
#                 current_features = selected_features + [feature]
#                 accuracy = self.get_cross_validated_accuracy(X, y_mapped, current_features, rf_params, cv_params)
#                 print(f"Testing feature: {feature}, Cross-Validated Accuracy: {accuracy}")
#                 if accuracy > best_accuracy + accuracy_improvement_threshold:
#                     best_accuracy = accuracy
#                     best_feature = feature

#             if best_feature is None:
#                 break  # No feature improved the accuracy significantly
#             selected_features.append(best_feature)
#             available_features.remove(best_feature)
#             print(f"Selected features: {selected_features}, Best cross-validated accuracy: {best_accuracy}")

#         selected_features = self.arrange_features(selected_features)  # Arrange selected features
#         self.selected_features = selected_features  # Store selected features
#         print(f"Final selected features: {selected_features}")
#         print(f"Best cross-validated accuracy achieved: {best_accuracy}")

#         return selected_features, best_accuracy

#     def train_final_model(self, X, y_mapped, selected_features, inverse_label_mapping, rf_params, cv_params):
#         """
#         Train the final Random Forest model with the selected features using cross-validation.
#         """
#         kf = StratifiedKFold(**cv_params)
#         accuracies = []
#         all_y_true = []
#         all_y_pred = []

#         for train_index, test_index in kf.split(X, y_mapped):
#             X_train_cv, X_test_cv = X.iloc[train_index], X.iloc[test_index]
#             y_train_cv, y_test_cv = y_mapped.iloc[train_index], y_mapped.iloc[test_index]

#             model = RandomForestClassifier(**rf_params)
#             model.fit(X_train_cv[selected_features], y_train_cv)

#             y_pred_cv = model.predict(X_test_cv[selected_features])
#             all_y_true.extend(y_test_cv)
#             all_y_pred.extend(y_pred_cv)

#             accuracy = accuracy_score(y_test_cv, y_pred_cv)
#             accuracies.append(accuracy)

#             print(f"Fold Accuracy: {accuracy:.4f}")

#         mean_accuracy = np.mean(accuracies)
#         print(f"Mean Accuracy: {mean_accuracy:.4f}")
#         print()
#         print("Cross-validation scores:", accuracies)
#         print(f"Mean cross-validation accuracy: {mean_accuracy:.4f}")
#         print(f"Training accuracy: {accuracy_score(y_train_cv, model.predict(X_train_cv[selected_features])):.4f}")
#         print(f"Test accuracy: {accuracy_score(y_test_cv, model.predict(X_test_cv[selected_features])):.4f}")

#         all_y_true = [inverse_label_mapping[label] for label in all_y_true]
#         all_y_pred = [inverse_label_mapping[label] for label in all_y_pred]

#         print("Classification Report:")
#         print(classification_report(all_y_true, all_y_pred))

#         conf_matrix = confusion_matrix(all_y_true, all_y_pred)
#         plt.figure(figsize=(5, 3))
#         sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=inverse_label_mapping.values(), yticklabels=inverse_label_mapping.values())
#         plt.xlabel("Predicted labels")
#         plt.ylabel("True labels")
#         plt.title("Confusion Matrix")
#         plt.show()

#         plt.figure(figsize=(5, 3))
#         corr_matrix = X[selected_features].corr()
#         sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
#         plt.title("Correlation Matrix of Selected Features")
#         plt.show()

#         sns.pairplot(self.shuffled_df[selected_features + ['label_name']], hue='label_name')
#         plt.show()

#         return model

#     def save_model(self, model, filename='random_forest.pkl'):
#         """
#         Save the trained model to a file.
#         """
#         with open(filename, 'wb') as f:
#             pickle.dump(model, f)

#     def Random_forest(self, **kwargs):
#         """
#         Set Random Forest parameters and CV parameters using kwargs, perform feature selection, and train the final model.
#         """
#         default_rf_params = {
#             'n_estimators': 20,
#             'max_depth': 3,
#             'min_samples_leaf': 1,
#             'min_samples_split': 2,
#             'bootstrap' : True,
#             'max_samples': 0.8,
#             'max_features': 'log2',
#             'random_state': 42
#         }
#         default_cv_params = {'n_splits': 5, 'shuffle': True, 'random_state': 42}

#         rf_params = {**default_rf_params, **kwargs.get('rf_params', {})}
#         cv_params = {**default_cv_params, **kwargs.get('cv_params', {})}

#         selected_features, best_accuracy = self.feature_selection(self.X, self.y_mapped, rf_params, cv_params)
#         model = self.train_final_model(self.X, self.y_mapped, selected_features, self.inverse_label_mapping, rf_params, cv_params)

#         # Save the model using only the filename parameter
#         self.save_model(model, filename=kwargs.get('filename', 'random_forest.pkl'))



import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
import pickle
import warnings

warnings.filterwarnings('ignore', category=UserWarning)

class RBML:
    def __init__(self, shuffled_df, random_state=42):
        self.shuffled_df = shuffled_df
        self.X = shuffled_df.drop(['label', 'label_name'], axis=1, errors='ignore')
        self.y = shuffled_df['label_name']
        self.label_mapping, self.inverse_label_mapping = self.create_label_mappings(self.y)
        self.y_mapped = self.y.map(self.label_mapping)
        self.random_state = random_state
        
        # Initialize attributes to store selected features and label mapping
        self.selected_features = None
        self.label_mapping = self.label_mapping
        self.inverse_label_mapping = self.inverse_label_mapping

    def create_label_mappings(self, y):
        """
        Create label mappings for the target variable.
        """
        labels = y.unique()
        label_mapping = {label: idx for idx, label in enumerate(labels)}
        inverse_label_mapping = {idx: label for label, idx in label_mapping.items()}
        return label_mapping, inverse_label_mapping

    def arrange_features(self, selected_features):
        """
        Arrange selected features based on a naming convention.
        """
        arranged_features = []
        feature_groups = {}

        for feature in selected_features:
            feature_name, _, indicator = feature.partition('_')
            feature_groups.setdefault(feature_name, []).append((indicator, feature))

        for feature_name, features in feature_groups.items():
            features.sort(key=lambda x: x[0])
            arranged_features.extend(feature for _, feature in features)

        return arranged_features

    def get_cross_validated_accuracy(self, X, y_mapped, selected_features, rf_params, cv_params):
        """
        Train Random Forest model and return cross-validated accuracy.
        """
        if not selected_features:
            return 0  # No features selected, return 0 accuracy

        kf = StratifiedKFold(**cv_params)
        accuracies = []

        for train_index, test_index in kf.split(X, y_mapped):
            X_train_cv, X_test_cv = X.iloc[train_index], X.iloc[test_index]
            y_train_cv, y_test_cv = y_mapped.iloc[train_index], y_mapped.iloc[test_index]

            model = RandomForestClassifier(**rf_params)
            model.fit(X_train_cv[selected_features], y_train_cv)
            y_pred_cv = model.predict(X_test_cv[selected_features])
            accuracy = accuracy_score(y_test_cv, y_pred_cv)
            accuracies.append(accuracy)

        return np.mean(accuracies)

    def feature_selection(self, X, y_mapped, rf_params, cv_params, accuracy_improvement_threshold=0.01):
        """
        Perform feature selection using cross-validation.
        """
        selected_features = []
        best_accuracy = 0
        available_features = list(X.columns)

        while available_features:
            best_feature = None
            for feature in available_features:
                current_features = selected_features + [feature]
                accuracy = self.get_cross_validated_accuracy(X, y_mapped, current_features, rf_params, cv_params)
                # print(f"Testing feature: {feature}, Cross-Validated Accuracy: {accuracy}")
                if accuracy > best_accuracy + accuracy_improvement_threshold:
                    best_accuracy = accuracy
                    best_feature = feature

            if best_feature is None:
                break  # No feature improved the accuracy significantly
            selected_features.append(best_feature)
            available_features.remove(best_feature)
            print(f"Selected features: {selected_features}, Best cross-validated accuracy: {best_accuracy}")

        selected_features = self.arrange_features(selected_features)  # Arrange selected features
        self.selected_features = selected_features  # Store selected features
        print(f"Final selected features: {selected_features}")
        print(f"Best cross-validated accuracy achieved: {best_accuracy}")

        return selected_features, best_accuracy

    def train_final_model(self, X, y_mapped, selected_features, inverse_label_mapping, rf_params, cv_params):
        """
        Train the final Random Forest model with the selected features using cross-validation.
        """
        kf = StratifiedKFold(**cv_params)
        accuracies = []
        all_y_true = []
        all_y_pred = []

        for train_index, test_index in kf.split(X, y_mapped):
            X_train_cv, X_test_cv = X.iloc[train_index], X.iloc[test_index]
            y_train_cv, y_test_cv = y_mapped.iloc[train_index], y_mapped.iloc[test_index]

            model = RandomForestClassifier(**rf_params)
            model.fit(X_train_cv[selected_features], y_train_cv)

            y_pred_cv = model.predict(X_test_cv[selected_features])
            all_y_true.extend(y_test_cv)
            all_y_pred.extend(y_pred_cv)

            accuracy = accuracy_score(y_test_cv, y_pred_cv)
            accuracies.append(accuracy)

            print(f"Fold Accuracy: {accuracy:.4f}")

        mean_accuracy = np.mean(accuracies)
        print(f"Mean Accuracy: {mean_accuracy:.4f}")
        print()
        print("Cross-validation scores:", accuracies)
        print(f"Mean cross-validation accuracy: {mean_accuracy:.4f}")
        print(f"Training accuracy: {accuracy_score(y_train_cv, model.predict(X_train_cv[selected_features])):.4f}")
        print(f"Test accuracy: {accuracy_score(y_test_cv, model.predict(X_test_cv[selected_features])):.4f}")

        all_y_true = [inverse_label_mapping[label] for label in all_y_true]
        all_y_pred = [inverse_label_mapping[label] for label in all_y_pred]

        print("Classification Report:")
        print(classification_report(all_y_true, all_y_pred))

        conf_matrix = confusion_matrix(all_y_true, all_y_pred)
        plt.figure(figsize=(5, 3))
        sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=inverse_label_mapping.values(), yticklabels=inverse_label_mapping.values())
        plt.xlabel("Predicted labels")
        plt.ylabel("True labels")
        plt.title("Confusion Matrix")
        plt.show()

        plt.figure(figsize=(5, 3))
        corr_matrix = X[selected_features].corr()
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
        plt.title("Correlation Matrix of Selected Features")
        plt.show()

        sns.pairplot(self.shuffled_df[selected_features + ['label_name']], hue='label_name')
        plt.show()

        return model

    def save_model(self, model, filename='random_forest.pkl'):
        """
        Save the trained model to a file.
        """
        with open(filename, 'wb') as f:
            pickle.dump(model, f)

    def Random_forest(self, **kwargs):
        """
        Set Random Forest parameters and CV parameters using kwargs, perform feature selection, and train the final model.
        """
        default_rf_params = {
            'n_estimators': 20,
            'max_depth': 3,
            'min_samples_leaf': 1,
            'min_samples_split': 2,
            'bootstrap' : True,
            'max_samples': 0.8,
            'max_features': 'log2',
            'random_state': 42
        }
        default_cv_params = {'n_splits': 5, 'shuffle': True, 'random_state': 42}

        rf_params = {**default_rf_params, **kwargs.get('rf_params', {})}
        cv_params = {**default_cv_params, **kwargs.get('cv_params', {})}

        selected_features, best_accuracy = self.feature_selection(self.X, self.y_mapped, rf_params, cv_params)
        model = self.train_final_model(self.X, self.y_mapped, selected_features, self.inverse_label_mapping, rf_params, cv_params)

        # Save the model using only the filename parameter
        self.save_model(model, filename=kwargs.get('filename', 'random_forest.pkl'))

