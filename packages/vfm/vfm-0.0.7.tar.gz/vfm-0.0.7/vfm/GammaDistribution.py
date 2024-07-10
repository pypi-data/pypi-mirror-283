import numpy as np
import math
from scipy.special import gamma, gammainc

def GammaDistribution(MWblackoil, eta, Lambda, N_pseudo, M_b):
    """
    Split of the black oil in pseudocomponents according to the Gamma-distribution model.
    
    Args:
    MWblackoil (float): Average molar mass of the pseudocomponents.
    eta (float): Molar mass of the heaviest pure component considered.
    Lambda (float): Shape parameter of the gamma distribution.
    N_pseudo (int): Number of pseudocomponents.
    M_b (list): Molecular-weight boundaries of each pseudocomponent.
    
    Returns:
    tuple: Tuple containing:
        MW_pseudo (numpy array): Estimated molecular weights for the pseudocomponents.
        z_pseudo (numpy array): Molar fractions of each pseudocomponent.
    """
    # Initializing output variables
    MW_pseudo = np.zeros(N_pseudo)
    z_pseudo = np.zeros(N_pseudo)

    # Calculation of the dependent parameter Beta
    Beta = (MWblackoil - eta) / Lambda

    # Calculating properties of pseudocomponents
    for j in range(N_pseudo - 1):
        yplus = (M_b[j] - eta) / Beta
        P_plus = p_aprox(M_b[j], eta, Lambda, Beta)  # Cumulative density function of M_b(j)
        
        if j == 0:
            yminus = 0  # (eta - eta) / Beta
            P_minus = 0  # Cumulative density function of M_b(j-1)
        else:
            yminus = (M_b[j-1] - eta) / Beta
            P_minus = p_aprox(M_b[j-1], eta, Lambda, Beta)
        
        # Calculation of the output properties
        z_pseudo[j] = P_plus - P_minus
        MW_pseudo[j] = eta + Lambda * Beta * (1 - (np.exp(-yplus) * yplus**Lambda - np.exp(-yminus) * yminus**Lambda) / (z_pseudo[j] * gamma(Lambda + 1)))

    # Calculations for the heaviest pseudocomponent
    yminus = (M_b[-1] - eta) / Beta
    z_pseudo[-1] = 1 - np.sum(z_pseudo[:-1])
    MW_pseudo[-1] = eta + Lambda * Beta * (1 + np.exp(-yminus) * yminus**Lambda / (z_pseudo[-1] * gamma(Lambda + 1)))

    return MW_pseudo, z_pseudo

def p_aprox(M_b, eta, Lambda, Beta):
    """
    Calculates the cumulative density function for a given molecular weight boundary.
    
    Args:
    M_b (float): Molecular-weight boundary of the pseudocomponent.
    eta (float): Molar mass of the heaviest pure component considered.
    Lambda (float): Shape parameter of the gamma distribution.
    Beta (float): Model parameter derived from black oil properties.
    
    Returns:
    float: Approximated cumulative density function value.
    """
    y = (M_b - eta) / Beta
    S = 1/Lambda*y/y
    j = 1
    while True:
        prod = Lambda
        for mm in range(1,j+1):
            prod = prod*(mm+Lambda)
        if prod > math.inf:
            break

        S = S + (y ** j)/prod
        j = j + 1


    return S * np.exp(-y) * y**Lambda / gamma(Lambda)
