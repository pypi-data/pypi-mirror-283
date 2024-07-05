# easyRTML/extract.py

import pandas as pd
import numpy as np

class Extractor:
    def __init__(self, sampling_freq=273, mean_gesture_duration=1000, shift=0.3):
        self.sampling_freq = sampling_freq
        self.mean_gesture_duration = mean_gesture_duration
        self.shift = shift
        self.variables = {}

    def calculate_features(self, window):
        min_val = np.min(window)
        max_val = np.max(window)
        mean_val = np.mean(window)
        rms_val = np.sqrt(np.mean(window ** 2))
        return min_val, max_val, mean_val, rms_val

    def extract_features(self, dataframe, window_length, hop_size):
        features_dict = {'label': [], 'label_name': []}
        for col_name in dataframe.columns:
            if col_name not in ['label', 'label_name']:
                features_dict[f"{col_name}_min"] = []
                features_dict[f"{col_name}_max"] = []
                features_dict[f"{col_name}_mean"] = []
                features_dict[f"{col_name}_rms"] = []
                for i in range(0, len(dataframe[col_name]) - window_length + 1, hop_size):
                    window = dataframe[col_name].iloc[i:i + window_length]
                    min_val, max_val, mean_val, rms_val = self.calculate_features(window)
                    features_dict[f"{col_name}_min"].append(min_val)
                    features_dict[f"{col_name}_max"].append(max_val)
                    features_dict[f"{col_name}_mean"].append(mean_val)
                    features_dict[f"{col_name}_rms"].append(rms_val)

        features_dict['label'] = [dataframe['label'].iloc[0]] * len(features_dict[f"{col_name}_min"])
        features_dict['label_name'] = [dataframe['label_name'].iloc[0]] * len(features_dict[f"{col_name}_min"])
        return pd.DataFrame(features_dict)

    def process_data(self, normalized_df):
        window_length = self.sampling_freq * self.mean_gesture_duration // 1000
        hop_size = int(self.shift * window_length)

        num_columns = len(normalized_df.columns) - 2
        buffer_length = num_columns * window_length
        rem_length = buffer_length - (num_columns * hop_size)
        shift_length = num_columns * hop_size

        unique_labels = normalized_df['label_name'].unique()
        features_dfs = []
        for label_name in unique_labels:
            subset_df = normalized_df[normalized_df['label_name'] == label_name]
            features_df = self.extract_features(subset_df, window_length, hop_size)
            features_dfs.append(features_df)

        features_df = pd.concat(features_dfs, ignore_index=True)
        pd.set_option('display.max_columns', None)  # Show all columns in the DataFrame
        pd.set_option('display.max_rows', None)  # Show all columns in the DataFrame

        self.variables = {
            'num_columns': num_columns,
            'window_length': window_length,
            'hop_size': hop_size,
            'buffer_length': buffer_length,
            'rem_length': rem_length,
            'shift_length': shift_length
        }

        self.features_df = features_df
        self.shuffled_df = self.shuffle_dataframe(features_df)

        return self.features_df, self.shuffled_df, self.variables

    def shuffle_dataframe(self, features_df):
        shuffled_df = features_df.sample(frac=1, random_state=42).reset_index(drop=True)
        pd.set_option('display.max_columns', None)  # Show all columns in the DataFrame
        pd.set_option('display.max_rows', None)  # Show all columns in the DataFrame
        return shuffled_df

    def get_variables(self):
        return self.variables

    def get_shuffled_df(self):
        return self.shuffled_df
