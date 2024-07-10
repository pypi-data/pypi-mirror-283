import numpy as np
from scipy.optimize import fsolve

def GetParametersPseudo(MWblackoil, MW_pseudo, z_pseudo, SGo, flag_code):
    """
    Calculate the thermodynamic properties of pseudocomponents.
    
    Args:
    MWblackoil (float): Average molar mass of the pseudocomponents.
    MW_pseudo (list): List of molecular weights for each pseudocomponent.
    z_pseudo (list): List of molar fractions for each pseudocomponent.
    SGo (float): Specific gravity of oil at standard conditions.
    flag_code (int): Code indicating the procedure for numerical calculations.
    
    Returns:
    dict: Dictionary containing estimated properties for pseudocomponents.
    """
    # Determine the coefficient Cf based on flag_code
    if flag_code == 1:
        Cf = 0.3
    else:
        def equation(Cf):
            return SGo - MWblackoil / np.sum(z_pseudo * MW_pseudo / (0.28554 + Cf * (MW_pseudo - 65.94185) ** 0.129969))
        Cf, = fsolve(equation, 0.3)

    # Calculate specific gravity for each pseudocomponent
    SG_pseudo = 0.28554 + Cf * (MW_pseudo - 65.94185) ** 0.129969

    # Calculate boiling temperature (assuming Raoult's law and corrections)
    Tb_pseudo = 1928.3 - 1.695 * 1e5 * np.exp(-4.922 * 1e-3 * MW_pseudo - 4.7685 * SG_pseudo +
                                              3.462 * 1e-3 * MW_pseudo * SG_pseudo) * MW_pseudo ** (-0.03522) * SG_pseudo ** 3.266

    # Calculate critical properties using Lee-Kesler correlations
    Tc = 341.7 + 811.0 * SG_pseudo + (0.4244 + 0.1174 * SG_pseudo) * Tb_pseudo + \
         (0.4669 - 3.2623 * SG_pseudo) * 1e5 / Tb_pseudo
    Tc = Tc * 5 / 9  # Convert Rankine to Kelvin
    
    Pc = np.exp(8.3634 - 0.0566 / SG_pseudo - (0.24244 + 2.2898 / SG_pseudo + 0.11857 / SG_pseudo ** 2) * 1e-3 * Tb_pseudo +
                (1.4685 + 3.648 / SG_pseudo + 0.47227 / SG_pseudo ** 2) * 1e-7 * Tb_pseudo ** 2 -
                (0.42019 + 1.6977 / SG_pseudo ** 2) * 1e-10 * Tb_pseudo ** 3)
    Pc = Pc * 6894.76  # Convert psi to Pa
    Tb_pseudo = Tb_pseudo * 5/9 

    # Calculate acentric factor
    acentric = (3 / 7) * np.log10(Pc / 101325) / ((Tc / Tb_pseudo) - 1) - 1

    # Calculate critical volume using Hall-Yarborough correlation
    Vc = 0.025 * MW_pseudo ** 1.15 * SG_pseudo ** -0.7935
    Vc = Vc * 6.242796057614462e-05  # Convert cubic feet per pound-mole to cubic meters per gram-mole
    Vc = Vc / MW_pseudo * 1000  # Convert from m^3/gmol to m^3/kgmol

    # Volume-shift parameter
    s = 1 - 2.258 / MW_pseudo ** 0.1823

    # Aggregate properties into a dictionary
    pseudo_properties = {
        'N': len(MW_pseudo),
        'MW': MW_pseudo,
        'Tb': Tb_pseudo,
        'Tc': Tc,
        'Pc': Pc,
        'Vc': Vc,
        'Acentric': acentric,
        's': s
    }

    return pseudo_properties
