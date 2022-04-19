import sympy as sp
from sympy.stats import Normal, cdf
import numpy as np


#Defining all variables
S,X,T,sigma,r, cp = sp.symbols('S X T sigma r cp')

d1 = ( sp.ln(S / X) + (r + sigma ** 2 * sp.Rational(1,2))* T ) / ( sigma * sp.sqrt(T))
d2 = d1 - sigma * sp.sqrt(T)

N = Normal('N',0.0, 1.0)

bs = cp * S * cdf(N)(cp * d1) - cp * X * sp.exp(-r * T) * cdf(N)(cp * d2)
bs_opt = sp.lambdify(
                    (S,X,T,sigma,r,cp),
                    bs,
                    modules=['numpy', 'sympy']
                    )

#1st Order Greeks
delta = sp.lambdify((S,X,T,sigma,r,cp),bs.diff(S), modules=['numpy', 'sympy'])
vega = sp.lambdify((S,X,T,sigma,r,cp),bs.diff(sigma), modules=['numpy', 'sympy']) 
theta = sp.lambdify((S,X,T,sigma,r,cp),bs.diff(T)/365, modules=['numpy', 'sympy'])
rho = sp.lambdify((S,X,T,sigma,r,cp),bs.diff(r), modules=['numpy', 'sympy'])

#2nd Order Greeks
gamma = sp.lambdify((S,X,T,sigma,r,cp),bs.diff(S,2), modules=['numpy', 'sympy'])
vanna = sp.lambdify((S,X,T,sigma,r,cp),bs.diff(S,sigma), modules=['numpy', 'sympy'])
vomma = sp.lambdify((S,X,T,sigma,r,cp),bs.diff(sigma,2), modules=['numpy', 'sympy']) 
charm = sp.lambdify((S,X,T,sigma,r,cp),bs.diff(S,T), modules=['numpy', 'sympy']) 


print(bs_opt(100,100,30/365,.6,.05,1))
print(theta(100,100,30/365,.6,.05,1))
print(gamma(100,100,30/365,.6,.05,1))


