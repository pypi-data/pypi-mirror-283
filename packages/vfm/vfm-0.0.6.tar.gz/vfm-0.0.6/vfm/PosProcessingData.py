import pandas as pd
import numpy as np
import os

class PostProcessor:
    def __init__(self, data_directory):
        self.data_directory = data_directory

    def fill_missing_values(self, df):
        for column in df.columns:
            if df[column].dtype in [np.float64, np.int64]:
                mean_value = df[column].mean()
                if mean_value == 0:
                    # If the mean is 0, use 50 + rand(10% of 50)
                    mean_value = 50
                    random_adjustment = mean_value * 0.1 * np.random.rand(df.shape[0])
                else:
                    # Otherwise, use the actual mean + rand(1% of mean)
                    random_adjustment = mean_value * 0.01 * np.random.rand(df.shape[0])
                df[column] = df[column].replace(0, np.nan)
                df[column] = df[column].fillna(pd.Series(mean_value + random_adjustment, index=df.index))
        return df

    def process_excel_file(self, file_path):
        excel_data = pd.read_excel(file_path, sheet_name=None)
        processed_data = {}
        for sheet, df in excel_data.items():
            df = self.fill_missing_values(df)
            processed_data[sheet] = df
        return processed_data

    def save_processed_data(self, processed_data, output_path):
        with pd.ExcelWriter(output_path) as writer:
            for sheet, df in processed_data.items():
                df.to_excel(writer, sheet_name=sheet, index=False)

    def process_data(self):
        # Paths to the input files
        btp_file_path = os.path.join(self.data_directory, 'Data_BTP.xlsx')
        pi_file_path = os.path.join(self.data_directory, 'Data_PI.xlsx')

        # Paths to the output files
        btp_output_path = os.path.join(self.data_directory, 'Data_BTP.xlsx')
        pi_output_path = os.path.join(self.data_directory, 'Data_PI.xlsx')

        # Process the files
        processed_btp_data = self.process_excel_file(btp_file_path)
        processed_pi_data = self.process_excel_file(pi_file_path)

        # Save the processed files
        self.save_processed_data(processed_btp_data, btp_output_path)
        self.save_processed_data(processed_pi_data, pi_output_path)

        print("Data processing complete. Processed files saved.")

if __name__ == "__main__":
    data_dir = "/content/vfm_v2/Python/Data/"
    processor = PostProcessor(data_dir)
    processor.process_data()
