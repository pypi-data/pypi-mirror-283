import os
import numpy as np
import pandas as pd

class UpdateDataDelumping:
    def __init__(self, data_directory):
        self.data_directory = data_directory
        self.wells = ['RJS-680', 'LL-60', 'LL-69', 'LL-90', 'LL-97', 'LL-100', 'LL-102']
        self.data_btp = {well: pd.DataFrame() for well in self.wells}
        self.data_pi = {well: pd.DataFrame() for well in self.wells}
        self.data_bdo = pd.DataFrame()

    def read_btp_data(self):
        btp_file_path = os.path.join(self.data_directory, 'Data_BTP.xlsx')
        for well in self.wells:
            self.data_btp[well] = pd.read_excel(btp_file_path, sheet_name=well)
            self.data_btp[well]['Time'] = pd.to_datetime(self.data_btp[well]['Time'], errors='coerce')
            if self.data_btp[well]['Time'].isnull().any():
                print(f"Warning: NaT values found in 'Time' column of BTP data for well {well}.")

    def read_pi_data(self):
        pi_file_path = os.path.join(self.data_directory, 'Data_PI.xlsx')
        for well in self.wells:
            self.data_pi[well] = pd.read_excel(pi_file_path, sheet_name=well)
            self.data_pi[well]['Time'] = pd.to_datetime(self.data_pi[well]['Time'], errors='coerce')
            if self.data_pi[well]['Time'].isnull().any():
                print(f"Warning: NaT values found in 'Time' column of PI data for well {well}.")

    def read_bdo_data(self):
        bdo_file_path = os.path.join(self.data_directory, 'Data_BDO.csv')
        self.data_bdo = pd.read_csv(bdo_file_path, delimiter=';', decimal=',')
        self.data_bdo['Time'] = pd.to_datetime(self.data_bdo['Time'], errors='coerce')
        if self.data_bdo['Time'].isnull().any():
            print("Warning: NaT values found in 'Time' column of BDO data.")

    def merge_data(self):
        merged_data = {}
        for well in self.wells:
            # Merge BTP and PI data on Time
            merged_df = pd.merge_asof(self.data_btp[well].sort_values('Time'), 
                                      self.data_pi[well].sort_values('Time'), 
                                      on='Time', 
                                      direction='nearest')
            merged_data[well] = merged_df
        return merged_data

    def save_data(self, merged_data):
        output_file_path = os.path.join(self.data_directory, 'DataDelumping.xlsx')
        with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
            for well in self.wells:
                merged_data[well].to_excel(writer, sheet_name=well, index=False)
        print("DataDelumping.xlsx has been created.")

    def read_and_process_data(self):
        self.read_btp_data()
        self.read_pi_data()
        self.read_bdo_data()
        merged_data = self.merge_data()
        self.save_data(merged_data)

# Example usage:
# update_data_delumping = UpdateDataDelumping(data_directory="/content/vfm_v2/Python/Data/")
# update_data_delumping.read_and_process_data()
