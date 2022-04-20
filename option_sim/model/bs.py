import sympy as sp
from sympy.stats import Normal, cdf
from sympy.solvers import nsolve


# Defining all variables
S, X, T, sigma, r, cp = sp.symbols('S X T sigma r cp')

d1 = (sp.ln(S / X) + (r + sigma ** 2 * sp.Rational(1, 2)) * T) / \
    (sigma * sp.sqrt(T))
d2 = d1 - sigma * sp.sqrt(T)

N = Normal('N', 0.0, 1.0)

bs = cp * S * cdf(N)(cp * d1) - cp * X * sp.exp(-r * T) * cdf(N)(cp * d2)

bs_opt = sp.lambdify(
                    (S, X, T, sigma, r, cp),
                    bs,
                    modules=['numpy', 'sympy']
                    )

# First Order Greeks
delta = sp.lambdify(
                    (S, X, T, sigma, r, cp),
                    bs.diff(S),
                    modules=['numpy', 'sympy']
                    )

vega = sp.lambdify(
                    (S, X, T, sigma, r, cp),
                    bs.diff(sigma) / 100,
                    modules=['numpy', 'sympy']
                    )

theta = sp.lambdify(
                    (S, X, T, sigma, r, cp),
                    bs.diff(T) / (-365),
                    modules=['numpy', 'sympy']
                    )

rho = sp.lambdify(
                    (S, X, T, sigma, r, cp),
                    bs.diff(r) / 100,
                    modules=['numpy', 'sympy']
                    )

# Second Order Greeks
gamma = sp.lambdify(
                    (S, X, T, sigma, r, cp),
                    bs.diff(S, 2),
                    modules=['numpy', 'sympy']
                    )

vanna = sp.lambdify(
                    (S, X, T, sigma, r, cp),
                    bs.diff(S, sigma),
                    modules=['numpy', 'sympy']
                    )

vomma = sp.lambdify(
                    (S, X, T, sigma, r, cp),
                    bs.diff(sigma, 2),
                    modules=['numpy', 'sympy']
                    )

charm = sp.lambdify(
                    (S, X, T, sigma, r, cp),
                    bs.diff(S, T),
                    modules=['numpy', 'sympy']
                    )

def implied_vol(s, x, t, R, CP, price):
    """Returns implied volatility from derivative market price"""

    imp_vol = nsolve(bs.subs([(S, s), (X, x), (T, t), (r,R), (cp, CP)]) - price, sigma, 1)
    return imp_vol

bs_opt.__doc__ = \
                    """
                        Black and Scholes formula

                        Parameters
                        ----------
                        S : Spot price

                        X : Strike price

                        T : days to maturity / 365

                        sigma : volatility

                        r : risk free interest rate

                        cp : 1 for call
                            -1 for put

                        Returns
                        -------
                            Derivative price
                    """
