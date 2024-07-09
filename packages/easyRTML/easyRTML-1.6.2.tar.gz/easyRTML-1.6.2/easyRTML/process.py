# easyRTML/process.py

import pandas as pd

class Processor:
    def __init__(self, file_name):
        self.df = pd.read_csv(file_name)
        self.feature_info = {}
        self.clean_data()
        self.calculate_feature_info()
        self.normalized_df = self.normalize_data()

    def clean_column(self, col_data):
        col_data = pd.to_numeric(col_data, errors='coerce')
        col_data.fillna(col_data.mean(), inplace=True)
        return col_data

    def clean_data(self):
        for col_name in self.df.columns:
            if col_name not in ['label', 'label_name']:
                self.df[col_name] = self.clean_column(self.df[col_name])

    def calculate_feature_info(self):
        col_number = 1
        for col_name in self.df.columns:
            if col_name not in ['label', 'label_name']:
                col_data = self.df[col_name]
                max_val = col_data.max()
                min_val = col_data.min()
                scale = 1 / (max_val - min_val)
                offset = min_val
                self.feature_info[col_name] = {'offset': offset, 'scale': scale, 'number': col_number}
                col_number += 1

    def normalize_data(self):
        normalized_df = pd.DataFrame({'label': self.df['label'], 'label_name': self.df['label_name']})
        for col_name in self.df.columns:
            if col_name not in ['label', 'label_name']:
                offset = self.feature_info[col_name]['offset']
                scale = self.feature_info[col_name]['scale']
                normalized_df[col_name] = (self.df[col_name] - offset) * scale
        return normalized_df

    def get_offsets(self):
        return [self.feature_info[col]['offset'] for col in self.feature_info]

    def get_scales(self):
        return [self.feature_info[col]['scale'] for col in self.feature_info]

    def get_columns_except_label(self):
        return [col for col in self.df.columns if col not in ['label', 'label_name']]

    def get_num_columns(self):
        return len(self.get_columns_except_label())

    def get_column_numbers(self):
        return {col: self.feature_info[col]['number'] for col in self.feature_info}
