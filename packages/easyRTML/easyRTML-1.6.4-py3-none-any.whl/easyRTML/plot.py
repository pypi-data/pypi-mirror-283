# easyRTML/plot.py

import matplotlib.pyplot as plt
import os

class Plot:
    @staticmethod
    def plot(df):
        plt.figure(figsize=(12, 3))
        df.plot(ax=plt.gca())
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Plot')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_normalized(normalized_df):
        plt.figure(figsize=(12, 3))
        ax = normalized_df.drop(columns=['label_name']).plot(ax=plt.gca())
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Normalized Plot')
        plt.tight_layout()
        plt.show()

    @staticmethod

    def plot_separated(normalized_df):
        if not os.path.exists('plots'):
            os.makedirs('plots')

        unique_labels = normalized_df['label_name'].unique()
        for label_name in unique_labels:
            subset_df = normalized_df[normalized_df['label_name'] == label_name]
            plt.figure(figsize=(12, 3))
            for col_name in subset_df.columns.drop(['label', 'label_name']):
                plt.plot(subset_df.index, subset_df[col_name], label=col_name)
            plt.title(f'Plot for {label_name}')
            plt.xlabel('Samples')
            plt.ylabel('Normalized Value')
            plt.legend()
            plt.tight_layout()
            plt.show()
            plt.close()