def FlashCalculation(z, K):
    """
    Solving the isothermal flash calculation for the oil-gas mixture
    according to the successive substitution algorithm proposed by Rachford-Rice (1952).
    
    Inputs:
    z - Molar composition in the feed flow (numpy array)
    K - Ratio between the molar fractions of the gas and oil phase for each
        component in the mixture (numpy array)
        
    Outputs:
    Beta_posterior - Vapor fraction (V/F)
    """
    Beta_prior = 0
    Beta_posterior = 0.5
    tol = 1e-6  # Tolerance for convergence
    
    while abs(Beta_prior - Beta_posterior) >= tol:
        Beta_prior = Beta_posterior
        f = sum(z * (K - 1) / (1 + Beta_prior * (K - 1)))
        df = -sum(z * (K - 1) ** 2 / (1 + Beta_prior * (K - 1)) ** 2)
        Beta_posterior = Beta_prior - f / df

        # Saturation to avoid convergence errors due to infeasible sets of z and K
        Beta_posterior = max(min(Beta_posterior, 1 - 1e-10), 1e-10)

    return Beta_posterior