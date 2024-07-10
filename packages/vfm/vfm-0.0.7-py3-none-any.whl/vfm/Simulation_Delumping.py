import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import gamma
from scipy.optimize import minimize, differential_evolution
import os
from vfm.vfm import UpdateDataDelumping, GetDataPure, ExtendCG, DelumpingMethod, BisectionMethod, Plotting_Delumping



class OilWellAnalysis:
    def __init__(self, data_directory, result_directory, flag_code, flag_init):
        self.data_directory = data_directory
        self.result_directory = result_directory
        self.flag_code = flag_code
        self.flag_init = flag_init
        self.ID_Wells = ["RJS-680", "LL-60", "LL-69", "LL-90", "LL-97", "LL-100", "LL-102"]
        self.Tag = ["N2", "CO2", "C1", "C2", "C3", "iC4", "nC4", "iC5", "nC5", "nC6",
                    "nC7", "nC8", "nC9", "nC10"]      
        self.data = None
        self.pure_properties = None
        self.CG_vectors = {}  # Dictionary to store CG vectors for each well
        self.load_data()
        self.setup_directories()


    def load_data(self):
        # Define the file path for the updated data
        file_path = os.path.join(self.data_directory, "Data_Delumping_updated.csv") 
        # Load the CSV file into a DataFrame
        self.data = pd.read_csv(file_path)
        # Convert date strings to datetime objects if necessary
        if 'Time' in self.data.columns:
            self.data['Time'] = pd.to_datetime(self.data['Time'])  
        # Gather pure component properties; assumes GetDataPure returns a DataFrame or similar structure
        self.pure_properties = GetDataPure(self.Tag)
        # Convert necessary columns to numeric types and handle missing values
        cols_to_convert = ['rhoo_SC', 'Qo_SC', 'Qg_SC', 'Qw_SC', 'Rs', 'Bo', 'SGg', 'T_sep', 'P_sep', 'Bg']
        for col in cols_to_convert:
            self.data[col] = pd.to_numeric(self.data[col], errors='coerce')

    def setup_directories(self):
        # Set up directories based on flag_code and flag_init, as done in MATLAB
        base_path = os.path.join(self.result_directory, 'Delumping_case')
        self.dirs = {code: os.path.join(base_path, f"{code}_init{self.flag_init}") for code in self.flag_code}
        for path in self.dirs.values():
            os.makedirs(path, exist_ok=True)
            

    def initialize_parameters(self):
        # Initialize parameters based on flag_init
        self.data['rhow_SC'] = 1000  # Water density at standard conditions [kg/m^3]
        if 'API' not in self.data.columns:
            self.data['SGo_meas'] = self.data['rhoo_SC'] / 1000
            self.data['API'] = 141.5 / self.data['SGo_meas'] - 131.5
        
        for code in self.flag_code:
            if code % 2 == 1:  # Odd code uses Lasater correlation
                self.data[f'MWblackoil_{code}'] = np.exp(-(self.data['API'] - 202.99) / 29.95)
            else:  # Even code uses Standing correlation
                self.data[f'MWblackoil_{code}'] = 630 - 10 * self.data['API']

    def process_data(self):
        for well_id in self.ID_Wells:
            well_data = self.data[self.data['Well_ID'] == well_id]
            self.handle_well_data(well_data, well_id)

    def handle_well_data(self, well_data, well_id):
        well_path = self.result_directory + '/' + well_id
        os.makedirs(well_path, exist_ok=True)
        
        N_data = len(well_data)
        CG_vector = np.empty(N_data, dtype=object)
        SGg_meas = well_data['SGg'].copy()

        for i, row in well_data.iterrows():
            if not pd.isna(row['Qo_SC']) and not pd.isna(row['Y_N2']):
                if not pd.isna(row['SGg']):
                    CG_vector[i], SGg_meas[i] = ExtendCG(well_data, self.pure_properties, i)
                elif self.flag_init == 3:
                    CG_vector[i], SGg_meas[i] = ExtendCG(well_data, self.pure_properties, i)

        # Store processed CG vector and other data for later use
        self.CG_vectors[well_id] = CG_vector

        # Store processed data
        processed_data = {
            'SGo_meas': well_data['rhoo_SC'] / well_data['rhow_SC'],
            'API_meas': 141.5 / well_data['SGo_meas'] - 131.5,
            'GOR_meas': well_data['Qg_SC'] / well_data['Qo_SC'],
            'SGg_meas': SGg_meas,
            'Qg_SC': well_data['Qg_SC'],
            'Qo_SC': well_data['Qo_SC'],
            'T_sep': well_data['T_sep'],
            'P_sep': well_data['P_sep'],
        }
        processed_df = pd.DataFrame(processed_data)
        processed_df.to_csv(os.path.join(well_path, f'processed_{well_id}.csv'))

    def calculate_wellstream_compositions(self):
        Lambda = 0.5  # Simplified value for Gamma distribution

        # Preparing output structures
        N_data_max = max(self.data['N_data'])
        n_wells = len(self.ID_Wells)
        n_code = len(self.flag_code)

        # Initializing arrays for the results
        API_est = np.zeros((N_data_max, n_wells, n_code))
        GOR_est = np.zeros((N_data_max, n_wells, n_code))
        SGg_est = np.zeros((N_data_max, n_wells, n_code))
        x_est = np.empty((N_data_max, n_wells, n_code), dtype=object)
        y_est = np.empty((N_data_max, n_wells, n_code), dtype=object)
        z_est = np.empty((N_data_max, n_wells, n_code), dtype=object)
        MW_est = np.empty((N_data_max, n_wells, n_code), dtype=object)
        pseudo_est = np.empty((N_data_max, n_wells, n_code), dtype=object)
        PRE_API = np.zeros((N_data_max, n_wells, n_code))
        PRE_GOR = np.zeros((N_data_max, n_wells, n_code))
        PRE_SGg = np.zeros((N_data_max, n_wells, n_code))
        FO = np.zeros((N_data_max, n_wells, n_code))

        # Process each flag code
        for k, code in enumerate(self.flag_code):
            if code == 1:
                # Example: Set specific molecular weights and bounds for flag_code 1
                eta = self.pure_properties['MW'][-1]  # Example: use the last entry
                M_b = np.array([156.31, 170.34, 184.37, 198.39, 212.42, 226.45, 240.47, 1100])
                ub_var, lb_var = 250, 144
            else:
                # Set for other flag codes
                eta = self.pure_properties['MW'][10]  # Example: specific index
                M_b = self.pure_properties['MW'][11:]  # Example: subset
                ub_var, lb_var = M_b[-1], M_b[0]

    def run_simulation(self):
        Lambda = 0.5  # Gamma distribution simplified value
        # Prepare matrices for results
        self.prepare_simulation_structures()

        # Timing simulation start
        import time
        start_time = time.time()

        # Simulation over each flag code and well
        for k, code in enumerate(self.flag_code):
            for j, well_id in enumerate(self.ID_Wells):
                N_data = self.data[self.data['Well_ID'] == well_id]['N_data'].iloc[0]
                for i in range(N_data):
                    results = self.optimize_well(i, j, k, code)
                    self.store_results(i, j, k, results)

        # Timing simulation end
        elapsed_time = time.time() - start_time
        print(f"Simulation took {elapsed_time:.2f} seconds.")

    def prepare_simulation_structures(self):
        # Get dimensions for result structures
        N_data_max = self.data['N_data'].max()
        n_wells = len(self.ID_Wells)
        n_code = len(self.flag_code)

        # Initialize output structures
        self.API_est = np.zeros((N_data_max, n_wells, n_code))
        self.GOR_est = np.zeros((N_data_max, n_wells, n_code))
        self.SGg_est = np.zeros((N_data_max, n_wells, n_code))
        self.x_est = np.empty((N_data_max, n_wells, n_code), dtype=object)
        self.y_est = np.empty((N_data_max, n_wells, n_code), dtype=object)
        self.z_est = np.empty((N_data_max, n_wells, n_code), dtype=object)
        self.MW_est = np.empty((N_data_max, n_wells, n_code), dtype=object)
        self.pseudo_est = np.empty((N_data_max, n_wells, n_code), dtype=object)
        self.PRE_API = np.zeros((N_data_max, n_wells, n_code))
        self.PRE_GOR = np.zeros((N_data_max, n_wells, n_code))
        self.PRE_SGg = np.zeros((N_data_max, n_wells, n_code))
        self.FO = np.zeros((N_data_max, n_wells, n_code))

    def optimize_well(self, i, j, k, code):
        # Select optimization parameters based on code
        if code == 1:
            eta = self.pure_properties['MW'][-1]  # Example: last molecular weight
            M_b = np.array([156.31, 170.34, 184.37, 198.39, 212.42, 226.45, 240.47, 1100])
            ub_var, lb_var = 250, 144
        else:
            eta = self.pure_properties['MW'][10]  # Example: specific molecular weight
            M_b = self.pure_properties['MW'][11:]  # Subsetting
            ub_var, lb_var = M_b[-1], M_b[0]

        # Define the function to optimize
        def objective_function(var):
            # Assume DelumpingMethod now also returns PRE values in addition to the objective value
            obj_value, PRE_API, PRE_GOR, PRE_SGg = DelumpingMethod(var, eta, self.Lambda, M_b, self.pure_properties,
                                       self.CG_vector[i][self.pos_wells[j]], self.T_sep[i][j], self.P_sep[i][j],
                                       self.Qg_SC[i][j], self.Qo_SC[i][j], self.SGo_meas[i][j],
                                       self.API_meas[i][j], self.GOR_meas[i][j], self.SGg_meas[i][j], code)
            return obj_value, PRE_API, PRE_GOR, PRE_SGg  # Adjust based on actual return structure

        # Conduct optimization
        if code == 1:
            result = minimize(lambda var: objective_function(var)[0], self.MWblackoil[i][j][k], bounds=[(lb_var, ub_var)], method='L-BFGS-B')
        else:
            result = differential_evolution(lambda var: objective_function(var)[0], bounds=[(lb_var, ub_var)])

        # Assuming result.x contains the optimized variables and additional statistics are returned by objective_function
        _, PRE_API, PRE_GOR, PRE_SGg = objective_function(result.x)
        return result.x, result.fun, (PRE_API, PRE_GOR, PRE_SGg)

    def store_results(self, i, j, k, optimization_results):
        # Unpack results from the optimization and additional computations
        optimized_value, optimization_fun, additional_results = optimization_results
        PRE_API, PRE_GOR, PRE_SGg = additional_results

        # Update the model results matrices
        self.MWblackoil[i][j][k] = optimized_value
        self.API_est[i][j][k] = self.API_meas[i][j] + (PRE_API * self.API_meas[i][j] / 100)
        self.GOR_est[i][j][k] = self.GOR_meas[i][j] + (PRE_GOR * self.GOR_meas[i][j] / 100)
        self.SGg_est[i][j][k] = self.SGg_meas[i][j] + (PRE_SGg * self.SGg_meas[i][j] / 100)
        self.x_est[i][j][k] = x_comp
        self.y_est[i][j][k] = y_comp

        # Manage position tracking if needed
        if not hasattr(self, 'pos_cont'):
            self.pos_cont = 0  # Initialize if it doesn't exist
        if not hasattr(self, 'pos_cons'):
            self.pos_cons = np.zeros((self.data['N_data'].sum(),), dtype=int)  # Assuming sum of all N_data as the size

        # Store the index position adjusted for flattened indexing across wells
        self.pos_cons[self.pos_cont] = i + (j * self.data['N_data'].max())  # Adjust for maximum possible data length per well
        self.pos_cont += 1
        
    def plotting_delumping(self):
        # This function needs to be defined to plot the results
        fig, ax = plt.subplots(2, 1, figsize=(10, 8))
        ax[0].plot(self.API_est.flatten(), label='Estimated API')
        ax[0].plot(self.API_meas.flatten(), label='Measured API', linestyle='--')
        ax[0].set_title('API Comparison')
        ax[0].legend()

        ax[1].plot(self.GOR_est.flatten(), label='Estimated GOR')
        ax[1].plot(self.GOR_meas.flatten(), label='Measured GOR', linestyle='--')
        ax[1].set_title('GOR Comparison')
        ax[1].legend()

        plt.tight_layout()
        plt.show()

    def save_results(self):
        # Save all results into a CSV file for simplicity
        results = {
            "MWblackoil": self.MWblackoil.flatten(),
            "API_meas": self.API_meas.flatten(),
            "API_est": self.API_est.flatten(),
            "GOR_meas": self.GOR_meas.flatten(),
            "GOR_est": self.GOR_est.flatten(),
            "SGg_meas": self.SGg_meas.flatten(),
            "SGg_est": self.SGg_est.flatten(),
        }
        results_df = pd.DataFrame(results)
        results_df.to_csv(f"{self.dirs[self.flag_code[0]]}/Results.csv", index=False)


    def run_full_simulation(self):
        self.initialize_parameters()
        self.process_data()
        self.calculate_wellstream_compositions()
        self.run_simulation()
        self.plotting_delumping()
        self.save_results()

# Usage
# data_directory = "../Dados/"
# result_directory = "../Resultados/Delumping_case"
# flag_code = [1, 2, 3]
# flag_init = 1

# simulation = OilWellAnalysis(data_directory, result_directory, flag_code, flag_init)
# simulation.run_full_simulation()
