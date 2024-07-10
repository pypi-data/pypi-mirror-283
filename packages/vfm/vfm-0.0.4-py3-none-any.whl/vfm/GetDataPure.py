import numpy as np

def GetDataPure(tag_in):
    """
    Transcription and storage of the thermodynamic properties from the pure components.
    
    Args:
    tag_in (list): List of the desired ordering of the pure components considered.
    
    Returns:
    dict: Dictionary containing the thermodynamic properties of the pure components.
    """
    # Definition of component tags according to gas chromatography data ordering
    tag_data = ["N2", "CO2", "C1", "C2", "C3", "iC4", "nC4", "iC5", "nC5", "nC6",
                "nC7", "nC8", "nC9", "nC10"]

    # Technical data transcription from sources
    mw_ref = [28.01, 44.01, 16.04, 30.07, 44.10, 58.12, 58.12, 72.15,
              72.15, 86.18, 100.2, 114.23, 128.26, 142.29]  # Molecular weight [g/mol]
    tb_ref = [-320.45, -109.26, -258.68, -127.48, -43.67, 10.90, 31.10,
              82.12, 96.93, 155.71, 209.17, 258.22, 303.48, 345.48]  # Boiling temperature [°F]
    tc_ref = [-232.51, 87.91, -116.66, 89.91, 206.02, 274.98, 305.55,
              369.10, 385.79, 454.01, 512.69, 563.99, 610.61, 652.19]  # Critical temperature [°F]
    pc_ref = [493.14, 1070.83, 667.04, 706.64, 616.13, 529.11, 550.57,
              490.38, 488.79, 438.75, 397.41, 361.15, 332.14, 306.03]  # Critical pressure [psia]
    vc_ref = [0.0510, 0.0342, 0.0985, 0.0775, 0.0727, 0.0724, 0.0703,
              0.0679, 0.0695, 0.0690, 0.0684, 0.0682, 0.0679, 0.0675]  # Critical volume [ft^3/lb]
    acentric_ref = [0.0377, 0.2236, 0.0115, 0.0995, 0.1523, 0.1808,
                    0.2002, 0.2275, 0.2515, 0.3013, 0.3495, 0.3996, 0.4435, 0.4923]  # Acentric factor
    s_ref = [-0.1927, -0.0817, -0.1595, -0.1134, -0.0863, -0.0844, -0.0675,
             -0.0608, -0.0390, -0.0080, 0.0033, 0.0314, 0.0408, 0.0655]  # Volume-shift parameter
    k_bin_ref = np.array([
        [0, -0.017, 0.031, 0.0577999, 0.07248, 0.0885824, 0.0864354, 0.10012, 0.0995857, 0.117182, 0.133912, 0.148509, 0.165069, 0.17983],
        [-0.017, 0, 0.092, 0.11337, 0.11203, 0.11056, 0.11075, 0.1095, 0.10955, 0.107948, 0.106421, 0.105089, 0.103577, 0.10223],
        [0.031, 0.092, 0, 0.0154511, 0.0203843, 0.0247469, 0.0247469, 0.0286086, 0.0286086, 0.03203, 0.0350654, 0.0377621, 0.0401605, 0.0422974],
        [0.0577999, 0.11337, 0.0154511, 0, 0, 0.024297, 0.024297, 0.0281586, 0.0281586, 0.0315799, 0.0346154, 0.0373121, 0.0397105, 0.0418474],
        [0.07248, 0.11203, 0.0203843, 0, 0, 0, 0, 0.0271865, 0.0271865, 0.0306075, 0.0336429, 0.0363396, 0.038738, 0.0408749],
        [0.0885824, 0.11056, 0.0247469, 0.024297, 0, 0, 0, 0, 0, 0.0278318, 0.0308673, 0.033564, 0.0359624, 0.0380993],
        [0.0864354, 0.11075, 0.0247469, 0.024297, 0, 0, 0, 0, 0, 0.0278318, 0.0308673, 0.033564, 0.0359624, 0.0380993],
        [0.10012, 0.1095, 0.0286086, 0.0281586, 0.0271865, 0, 0, 0, 0, 0, 0.015873, 0.0185697, 0.0209682, 0.0231051],
        [0.0995857, 0.10955, 0.0286086, 0.0281586, 0.0271865, 0, 0, 0, 0, 0, 0.015873, 0.0185697, 0.0209682, 0.0231051],
        [0.117182, 0.107948, 0.03203, 0.0315799, 0.0306075, 0.0278318, 0.0278318, 0, 0, 0, 0, 0, 0, 0],
        [0.133912, 0.106421, 0.0350654, 0.0346154, 0.0336429, 0.0308673, 0.0308673, 0.015873, 0.015873, 0, 0, 0, 0, 0],
        [0.148509, 0.105089, 0.0377621, 0.0373121, 0.0363396, 0.033564, 0.033564, 0.0185697, 0.0185697, 0, 0, 0, 0, 0],
        [0.165069, 0.103577, 0.0401605, 0.0397105, 0.038738, 0.0359624, 0.0359624, 0.0209682, 0.0209682, 0, 0, 0, 0, 0],
        [0.17983, 0.10223, 0.0422974, 0.0418474, 0.0408749, 0.0380993, 0.0380993, 0.0231051, 0.0231051, 0, 0, 0, 0, 0]
    ])  # Binary interaction parameters

    # Find positions for the desired ordering
    pos_data = [tag_data.index(tag) for tag in tag_in]

    # Transcription of properties according to the found positions
    PureProperties = {
        'N': len(tag_in),
        'MW': [mw_ref[i] for i in pos_data],
        'Tb': [tb_ref[i] for i in pos_data],
        'Tc': [tc_ref[i] for i in pos_data],
        'Pc': [pc_ref[i] for i in pos_data],
        'Vc': [vc_ref[i] for i in pos_data],
        'Acentric': [acentric_ref[i] for i in pos_data],
        's': [s_ref[i] for i in pos_data],
        'k_bin': k_bin_ref[:, pos_data][pos_data, :]  # Subset matrix
    }

    # Conversion of the output variables to SI units
    PureProperties['Tb'] = [(Tb - 32) * 5/9 + 273.15 for Tb in PureProperties['Tb']]  # [K]
    PureProperties['Tc'] = [(Tc - 32) * 5/9 + 273.15 for Tc in PureProperties['Tc']]  # [K]
    PureProperties['Pc'] = [Pc * 6894.75728 for Pc in PureProperties['Pc']]  # [Pa]
    PureProperties['Vc'] = [Vc / 16.018463 for Vc in PureProperties['Vc']]  # [m^3/mol]

    return PureProperties

# Example usage:
# tag_in = ["N2", "CO2", "C1", "C2", "C3", "iC4", "nC4", "iC5", "nC5", "nC6", "nC7", "nC8", "nC9", "nC10"]
# PureProperties = get_data_pure(tag_in)
