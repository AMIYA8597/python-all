"""
# ==============================================================================
# LABORATORY: NUMERICAL CALCULUS (SCIPY.INTEGRATE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the `sympy` laboratory, you learned how to perform Analytical Calculus. 
# SymPy mathematically calculates the exact equation for an Integral.
# 
# However, many functions in the real world (especially in Physics and Biology) 
# CANNOT be integrated analytically. There is no mathematical equation for the 
# area under their curves.
# 
# `scipy.integrate` performs NUMERICAL Calculus. It does not try to find an 
# equation. It uses highly advanced computational algorithms (like Gaussian 
# Quadrature and Runge-Kutta) to slice the area into millions of microscopic 
# rectangles, calculating the exact numerical Area under the curve in milliseconds.
#
# Furthermore, it provides `solve_ivp` (Solve Initial Value Problem), which is 
# the industry standard for simulating complex physics and differential equations 
# (like the trajectory of a SpaceX rocket or the spread of a pandemic virus).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Compute Definite Integrals using `quad` (Quadrature).
# - Compute Double Integrals for 3D surfaces using `dblquad`.
# - Simulate physical systems using `solve_ivp` (Ordinary Differential Equations).
#
# ==============================================================================
"""

import numpy as np
from scipy import integrate

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. NUMERICAL INTEGRATION (DEFINITE INTEGRALS)
# ==============================================================================
def demonstrate_quadrature():
    section_header("Definite Integrals (Gaussian Quadrature)")
    
    # 1. SIMPLE INTEGRAL
    # Let's calculate the area under the curve f(x) = x^2 from x=0 to x=3.
    # Mathematically, the integral of x^2 is (x^3)/3. Evaluated at 3, it is 27/3 = 9.
    
    def f(x):
        return x**2
        
    # `quad` returns a tuple: (Estimated Area, Upper Bound of the Error)
    area, error = integrate.quad(f, 0, 3)
    
    print("Function: f(x) = x^2")
    print(f"Area [0 to 3] : {area:.6f} (Mathematically exact!)")
    print(f"Error Bound   : {error:.2e} (Virtually zero)")
    
    # 2. IMPOSSIBLE INTEGRALS
    # The Gaussian curve e^(-x^2) has NO analytical integral. You cannot solve 
    # this using SymPy or High School Calculus! It must be computed numerically.
    # Let's integrate it from -Infinity to +Infinity!
    
    def gauss_curve(x):
        return np.exp(-x**2)
        
    # We can literally use `np.inf` as the integration bounds!
    area_gauss, error_gauss = integrate.quad(gauss_curve, -np.inf, np.inf)
    
    print("\nFunction: f(x) = e^(-x^2) (The Gaussian Bell Curve)")
    print(f"Area [-inf to +inf] : {area_gauss:.6f}")
    print(f"Mathematical Truth  : sqrt(pi) = {np.sqrt(np.pi):.6f}")
    print("(SciPy successfully integrated across infinity in milliseconds!)")


# ==============================================================================
# 4. SOLVING ORDINARY DIFFERENTIAL EQUATIONS (ODEs)
# ==============================================================================
def demonstrate_ode():
    section_header("Solving ODEs (Physics Simulation)")
    
    print("Simulating Exponential Decay (e.g., Radioactive Uranium).")
    print("Differential Equation: dy/dt = -k * y")
    print("(The rate of decay is proportional to the current amount of material).")
    
    # 1. DEFINE THE DIFFERENTIAL EQUATION
    # The function signature must ALWAYS be `f(t, y)`.
    # It must return the DERIVATIVE (dy/dt) at the current time `t`.
    k = 0.5  # Decay constant
    
    def decay_derivative(t, y):
        return -k * y
        
    # 2. INITIAL CONDITIONS
    t_span = (0.0, 10.0) # Simulate from Time=0 to Time=10 seconds
    y0 = [100.0]         # Start with 100 grams of Uranium
    
    # We want to extract the simulated data at exactly these time intervals
    t_eval = np.linspace(0, 10, 6) 
    
    # 3. SOLVE THE ODE
    # `solve_ivp` automatically uses the RK45 (Runge-Kutta) algorithm, dynamically 
    # adjusting its time steps to guarantee mathematical stability!
    solution = integrate.solve_ivp(
        decay_derivative, 
        t_span, 
        y0, 
        t_eval=t_eval
    )
    
    print("\nSimulation Results:")
    for time_point, amount in zip(solution.t, solution.y[0]):
        print(f"Time: {time_point:4.1f}s | Uranium Remaining: {amount:6.2f} grams")
        
    print("\nNotice how the material decays rapidly at first, then slows down ")
    print("as the total mass decreases. SciPy simulated this physics perfectly!")


# ==============================================================================
# 5. SYSTEMS OF ODEs (PREDATOR-PREY MODEL)
# ==============================================================================
def demonstrate_sir_model():
    section_header("Systems of ODEs (The SIR Pandemic Model)")
    
    print("How do Epidemiologists predict the peak of a viral pandemic?")
    print("They use a System of Differential Equations (SIR Model):")
    print("- Susceptible (S): People who can catch the virus.")
    print("- Infected (I): People spreading the virus.")
    print("- Recovered (R): People who are immune.")
    
    # Mathematical constants
    beta = 0.3  # Infection rate
    gamma = 0.1 # Recovery rate
    
    # The ODE system returns a list of 3 derivatives! [dS/dt, dI/dt, dR/dt]
    def sir_derivatives(t, state):
        S, I, R = state
        
        # New infections occur when S meets I
        dS_dt = -beta * S * I
        
        # Infections go UP from new cases, but DOWN as people recover
        dI_dt = (beta * S * I) - (gamma * I)
        
        # Recoveries go UP constantly
        dR_dt = gamma * I
        
        return [dS_dt, dI_dt, dR_dt]
        
    # Initial Conditions (A city of 1,000,000 people)
    # We scale the population to 1.0 (100%) for mathematical simplicity.
    S0 = 0.99  # 99% susceptible
    I0 = 0.01  # 1% initially infected (Patient Zero)
    R0 = 0.00  # 0% recovered
    state_0 = [S0, I0, R0]
    
    t_span = (0, 50) # Simulate 50 days
    t_eval = np.linspace(0, 50, 6) # Output data every 10 days
    
    solution = integrate.solve_ivp(sir_derivatives, t_span, state_0, t_eval=t_eval)
    
    print("\nPandemic Simulation (50 Days):")
    print(f"{'Day':>5} | {'Susceptible':>12} | {'Infected':>10} | {'Recovered':>10}")
    print("-" * 45)
    
    for i in range(len(solution.t)):
        day = solution.t[i]
        s = solution.y[0][i] * 100
        inf = solution.y[1][i] * 100
        r = solution.y[2][i] * 100
        print(f"{day:5.0f} | {s:11.1f}% | {inf:9.1f}% | {r:9.1f}%")
        
    print("\nConclusion: The infection peaks, herd immunity triggers (S drops), ")
    print("and the virus mathematically burns itself out! ")


def run_all_labs():
    demonstrate_quadrature()
    demonstrate_ode()
    demonstrate_sir_model()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between `scipy.integrate.quad` and SymPy integration?
   Answer: SymPy performs Analytical Integration (manipulating algebra to return an exact mathematical equation, like $\frac{1}{3}x^3$). It will crash if the equation has no analytical solution (like $e^{-x^2}$). `scipy.integrate.quad` performs Numerical Quadrature. It does not look for an equation; it uses heavily optimized $C$ algorithms to slice the graph into microscopic rectangles and compute the raw physical Area under the curve in milliseconds.

2. What is an Initial Value Problem (IVP)?
   Answer: In physics and engineering, you usually know the *rules* of how a system changes over time (the Differential Equation / Derivative), and you know the *exact starting state* at Time=0 (the Initial Values). `solve_ivp` takes the starting state and iteratively steps forward in time, continuously applying the derivative rules to simulate exactly how the system evolves into the future. 

3. Why do we return an Array of derivatives in the SIR model?
   Answer: Because it is a *System* of Ordinary Differential Equations (ODEs). The equations are heavily coupled (the infection rate `dI/dt` directly depends on the current Susceptible population `S`). You cannot solve them sequentially! You must return the derivatives of all 3 variables simultaneously, so the Runge-Kutta solver can mathematically step them all forward in time together in perfect synchrony.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Numerical Integration & ODEs Completed.")
