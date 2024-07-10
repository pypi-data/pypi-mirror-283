import numpy as np

def HeuristicBinaryInteractions(MW_comp, Vc_comp, k_bin_pure):
    """
    Calculate the binary interaction parameters of the Peng-Robinson equation
    based on the Chueh-Prausnitz equation, and aggregate these with existing pure component parameters.
    
    Args:
    MW_comp (list): Molecular weights of the components considered in the calculations.
    Vc_comp (list): Critical volumes of the components considered in the calculations.
    k_bin_pure (numpy array): Binary interaction parameters of the pure components.
    
    Returns:
    numpy array: Matrix comprising the binary interaction parameters of the components.
    """
    n_comp = len(MW_comp)
    k_bin = np.zeros((n_comp, n_comp))

    # Assume k_bin_pure is a square matrix for the first 10 components
    k_bin[:10, :10] = k_bin_pure[:10, :10]

    # Conversion of critical volume from m³/mol to ft³/lb-mol
    Vc_comp_ft = Vc_comp * MW_comp * 0.001 / 6.242796057614462e-05

    # Calculate binary interaction parameters for new components
    for j in range(10, n_comp):
        for i in range(n_comp):
            k_bin[j, i] = (1.0 - ((2.0 * ((Vc_comp_ft[i] * Vc_comp_ft[j]) ** (1.0/6.0))) /
                         (Vc_comp_ft[i] ** (1.0/3.0) + Vc_comp_ft[j] ** (1.0/3.0))) ** 3.0)
    k_bin[:,10:] = k_bin[10:,:].T

    # Zero out interactions among new pseudocomponents beyond the original matrix
    if n_comp > 10:
        k_bin[10:n_comp, 10:n_comp] = 0

    return k_bin
