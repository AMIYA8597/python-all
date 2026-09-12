"""
Module: 04-scipy-integrate
Description: Comprehensive textbook-grade educational script for SciPy Integration (scipy.integrate).

=========================================================================================
PYTHON DSA & AI MASTERCLASS: SCIPY INTEGRATE (Numerical Integration & ODE Solvers)
=========================================================================================

Learning Objectives:
1. Understand the theoretical foundations of numerical integration and its necessity.
2. Master single and multiple integrals using continuous functions (`quad`, `dblquad`, etc.).
3. Master integration of fixed data points using `trapezoid`, `simpson`, and `romb`.
4. Solve Ordinary Differential Equations (ODEs) using modern solvers like `solve_ivp`.
5. Model complex systems (like Lotka-Volterra Predator-Prey and Lorenz Attractor).
6. Analyze computational complexity and select appropriate integration methods.
7. Handle edge cases: improper integrals, discontinuities, and stiff ODEs.

Mathematical Background:
------------------------
1. DEFINITE INTEGRALS:
   The definite integral of f(x) from a to b represents the signed area under the curve.
   Analytical integration uses antiderivatives, but many functions (e.g., e^(-x^2)) 
   lack elementary antiderivatives, making numerical integration essential.

2. QUADRATURE (Gaussian Quadrature & QUADPACK):
   SciPy's `quad` relies on the Fortran library QUADPACK. It uses adaptive quadrature 
   methods (like Gauss-Kronrod) which dynamically evaluate the function more frequently
   where the function varies rapidly, ensuring high accuracy.
   
3. FIXED-SAMPLE INTEGRATION:
   When we only have discrete data points (x_i, y_i), we estimate the integral using:
   - Trapezoidal Rule: Approximates the area as a series of trapezoids. Error ~ O(h^2)
   - Simpson's Rule: Approximates using parabolic arcs. Error ~ O(h^4). Needs odd number of points.
   - Romberg Integration: Extrapolates trapezoidal approximations. Error ~ O(h^(2m)).

4. ORDINARY DIFFERENTIAL EQUATIONS (ODEs):
   An ODE relates a function to its derivatives. E.g., dy/dt = f(t, y).
   Initial Value Problems (IVPs) start with a known y(t0) and step forward in time.
   Methods include Runge-Kutta (RK45 - explicit, good for non-stiff) and 
   BDF/Radau (implicit, good for stiff equations).

Complexity Analysis (Big-O):
----------------------------
Time and Space complexity in numerical integration depend heavily on the method, 
the error tolerance (atol, rtol), and the dimension of integration.

- `scipy.integrate.quad`: 
    Time: O(N * C), where N is the number of function evaluations, C is cost of f(x).
    Space: O(N) to store intervals in memory.
- `scipy.integrate.simpson`:
    Time: O(N), where N is the number of data points.
    Space: O(1) auxiliary space beyond the input arrays.
- `scipy.integrate.solve_ivp`:
    Time: O(S * C * D), where S is the number of steps, C is cost per step, D is dimension.
    Space: O(S * D) to store the solution trajectory.
"""

import math
import time
import warnings
from typing import Callable, Tuple, List, Dict, Any, Optional

import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt

# Type aliases for clarity
Func1D = Callable[[float], float]
Func2D = Callable[[float, float], float]


# =========================================================================================
# SECTION 1: SINGLE VARIABLE INTEGRATION (CONTINUOUS FUNCTIONS)
# =========================================================================================
def demonstrate_single_integration() -> None:
    """
    Demonstrates 1D integration using `scipy.integrate.quad`.
    `quad` is the general-purpose workhorse for 1D integrals.
    """
    print("\n" + "="*60)
    print("SECTION 1: 1D INTEGRATION WITH `quad`")
    print("="*60)

    # 1. Standard Definite Integral
    # Let's integrate f(x) = x^2 from 0 to 3. (Analytically: x^3/3 => 27/3 = 9.0)
    def f_polynomial(x: float) -> float:
        return x**2

    result, error_estimate = spi.quad(f_polynomial, 0, 3)
    print(f"1. Integral of x^2 from 0 to 3:")
    print(f"   Value: {result:.6f} | Error Estimate: {error_estimate:.2e}")

    # 2. Infinite Bounds (Improper Integrals)
    # The Gaussian integral: Integral of e^(-x^2) from -inf to inf = sqrt(pi)
    def f_gaussian(x: float) -> float:
        return np.exp(-x**2)

    result_gauss, error_gauss = spi.quad(f_gaussian, -np.inf, np.inf)
    expected_gauss = np.sqrt(np.pi)
    print(f"\n2. Improper Integral of e^(-x^2) from -inf to inf:")
    print(f"   Value: {result_gauss:.6f} (Expected: {expected_gauss:.6f})")
    print(f"   Error Estimate: {error_gauss:.2e}")

    # 3. Passing Arguments to the Integrand
    # Often, functions have parameters. E.g., f(x) = a * x^b
    def f_parameterized(x: float, a: float, b: float) -> float:
        return a * (x ** b)
    
    a_val, b_val = 2.0, 3.0
    result_param, err_param = spi.quad(f_parameterized, 0, 2, args=(a_val, b_val))
    # Integral of 2 * x^3 from 0 to 2 is [2*x^4/4] from 0 to 2 = 16/2 = 8.0
    print(f"\n3. Parameterized Integral 2*x^3 from 0 to 2:")
    print(f"   Value: {result_param:.6f} | Error Estimate: {err_param:.2e}")

    # 4. Handling singularities
    # f(x) = 1/sqrt(x). At x=0, the function goes to infinity.
    def f_singular(x: float) -> float:
        return 1.0 / np.sqrt(x) if x > 0 else 0.0 # Guard against divide by zero

    # quad can often handle endpoint singularities automatically
    res_sing, err_sing = spi.quad(f_singular, 0, 1)
    # Integral is [2*sqrt(x)] from 0 to 1 = 2.0
    print(f"\n4. Singularity at lower bound (1/sqrt(x) from 0 to 1):")
    print(f"   Value: {res_sing:.6f} | Error Estimate: {err_sing:.2e}")


# =========================================================================================
# SECTION 2: MULTIPLE INTEGRATION (DOUBLE, TRIPLE, N-DIMENSIONAL)
# =========================================================================================
def demonstrate_multiple_integration() -> None:
    """
    Demonstrates double (`dblquad`), triple (`tplquad`), and N-dimensional (`nquad`) integration.
    """
    print("\n" + "="*60)
    print("SECTION 2: MULTIPLE INTEGRATION (`dblquad`, `tplquad`)")
    print("="*60)

    # 1. Double Integral using `dblquad`
    # Let's integrate f(y, x) = x * y over x in [0, 2] and y in [0, 1]
    # Note the signature for dblquad integrand is f(y, x) - y is first argument!
    def f_xy(y: float, x: float) -> float:
        return x * y

    # The bounds for y can be functions of x. Here they are constant.
    res_dbl, err_dbl = spi.dblquad(f_xy, 0, 2, lambda x: 0, lambda x: 1)
    # Analytically: Integral (x*y dx dy) = (x^2/2) * (y^2/2) = (4/2)*(1/2) = 1.0
    print("1. Double Integral of x*y (x: [0, 2], y: [0, 1]):")
    print(f"   Value: {res_dbl:.6f} | Error Estimate: {err_dbl:.2e}")

    # 2. Double Integral with functional boundaries
    # Area of a circle: Integrate f(y, x) = 1 over x^2 + y^2 <= R^2
    # x goes from -R to R. y goes from -sqrt(R^2-x^2) to sqrt(R^2-x^2)
    R = 2.0
    def f_circle(y: float, x: float) -> float:
        return 1.0
    
    def lower_y(x: float) -> float:
        return -np.sqrt(R**2 - x**2)
    
    def upper_y(x: float) -> float:
        return np.sqrt(R**2 - x**2)

    res_circ, err_circ = spi.dblquad(f_circle, -R, R, lower_y, upper_y)
    expected_circ = np.pi * R**2
    print("\n2. Area of Circle (R=2) via Double Integration:")
    print(f"   Value: {res_circ:.6f} (Expected: {expected_circ:.6f})")

    # 3. Triple Integral using `tplquad`
    # Volume of a sphere (R=1). Integrate 1 over z, y, x.
    # Signature: f(z, y, x)
    def f_sphere(z: float, y: float, x: float) -> float:
        return 1.0

    res_sphere, err_sphere = spi.tplquad(
        f_sphere,
        -1, 1,                                            # x bounds
        lambda x: -np.sqrt(1 - x**2),                     # y lower bound (func of x)
        lambda x: np.sqrt(1 - x**2),                      # y upper bound (func of x)
        lambda x, y: -np.sqrt(max(0, 1 - x**2 - y**2)),   # z lower bound (func of x, y)
        lambda x, y: np.sqrt(max(0, 1 - x**2 - y**2))     # z upper bound (func of x, y)
    )
    expected_sphere = (4/3) * np.pi * 1**3
    print("\n3. Volume of Sphere (R=1) via Triple Integration:")
    print(f"   Value: {res_sphere:.6f} (Expected: {expected_sphere:.6f})")


# =========================================================================================
# SECTION 3: FIXED SAMPLE INTEGRATION (DISCRETE DATA)
# =========================================================================================
def demonstrate_discrete_integration() -> None:
    """
    Demonstrates integration of sampled data using Trapezoidal and Simpson's rules.
    This is highly relevant for real-world data (sensors, time-series) where the 
    continuous function is unknown.
    """
    print("\n" + "="*60)
    print("SECTION 3: DISCRETE DATA INTEGRATION")
    print("="*60)

    # Let's create some synthetic sampled data for f(x) = sin(x)
    x = np.linspace(0, np.pi, 11)  # 11 points => 10 intervals
    y = np.sin(x)

    print(f"Integrating sampled data (11 points) of sin(x) from 0 to pi.")
    print("Expected Exact Value: 2.0")

    # 1. Trapezoidal Rule
    # Uses linear interpolation between points.
    # Formula: sum( (x[i] - x[i-1]) * (y[i] + y[i-1]) / 2 )
    res_trapz = spi.trapezoid(y, x)
    err_trapz = abs(2.0 - res_trapz)
    print(f"\n1. Trapezoidal Rule (`trapezoid`):")
    print(f"   Value: {res_trapz:.6f} | Absolute Error: {err_trapz:.6f}")

    # 2. Simpson's Rule
    # Uses quadratic (parabolic) interpolation. Usually more accurate if the underlying
    # function is smooth. Requires an odd number of points (even number of intervals).
    # If points are even, SciPy handles the last interval via trapezoidal or modified simpson.
    res_simpson = spi.simpson(y, x=x)
    err_simpson = abs(2.0 - res_simpson)
    print(f"\n2. Simpson's Rule (`simpson`):")
    print(f"   Value: {res_simpson:.6f} | Absolute Error: {err_simpson:.6f}")
    
    # Observe that Simpson's rule provides a much smaller error for smooth functions
    print("\nInsight: Simpson's rule is generally preferred over Trapezoidal for smooth")
    print("curves because it fits parabolas instead of straight lines, resulting in O(h^4) error.")


# =========================================================================================
# SECTION 4: ORDINARY DIFFERENTIAL EQUATIONS (ODEs) - INITIAL VALUE PROBLEMS
# =========================================================================================
def demonstrate_ode_solvers() -> None:
    """
    Demonstrates solving ordinary differential equations using `solve_ivp`.
    """
    print("\n" + "="*60)
    print("SECTION 4: ORDINARY DIFFERENTIAL EQUATIONS (`solve_ivp`)")
    print("="*60)

    # 1. Simple 1D ODE: Exponential Decay
    # dy/dt = -k * y. Initial condition: y(0) = 5.
    # Analytical solution: y(t) = 5 * e^(-kt)
    k = 0.5
    def decay_model(t: float, y: np.ndarray) -> np.ndarray:
        return -k * y

    t_span = (0.0, 10.0) # Time span to solve for
    y0 = [5.0]           # Initial state (must be array-like, even for 1D)
    
    # We specify t_eval to get the solution at specific time points
    t_eval = np.linspace(t_span[0], t_span[1], 20)
    
    sol = spi.solve_ivp(decay_model, t_span, y0, t_eval=t_eval, method='RK45')
    
    print("1. Solving Exponential Decay: dy/dt = -0.5*y, y(0) = 5")
    print(f"   Solver Success: {sol.success}")
    print(f"   Number of function evaluations: {sol.nfev}")
    print(f"   y(10) numerical: {sol.y[0, -1]:.4f}")
    print(f"   y(10) analytical: {5 * np.exp(-0.5 * 10):.4f}")

    # 2. System of ODEs: Lotka-Volterra Predator-Prey Model
    # dx/dt = alpha*x - beta*x*y   (Prey dynamics)
    # dy/dt = delta*x*y - gamma*y  (Predator dynamics)
    alpha, beta, delta, gamma = 2.0/3.0, 4.0/3.0, 1.0, 1.0

    def lotka_volterra(t: float, state: List[float]) -> List[float]:
        x, y = state
        dx_dt = alpha * x - beta * x * y
        dy_dt = delta * x * y - gamma * y
        return [dx_dt, dy_dt]
    
    t_span_lv = (0.0, 15.0)
    initial_populations = [10.0, 5.0] # 10 prey, 5 predators
    sol_lv = spi.solve_ivp(lotka_volterra, t_span_lv, initial_populations, 
                           method='RK45', dense_output=True)
    
    print("\n2. System of ODEs: Lotka-Volterra Predator-Prey Model")
    print(f"   Solver Success: {sol_lv.success}")
    print(f"   Evaluated {sol_lv.nfev} times to solve over t in [0, 15]")
    
    # Dense output allows us to evaluate the solution at any continuous time t
    t_interp = 7.5
    state_interp = sol_lv.sol(t_interp)
    print(f"   Continuous interpolation at t=7.5:")
    print(f"     Prey population: {state_interp[0]:.2f}")
    print(f"     Predator population: {state_interp[1]:.2f}")


# =========================================================================================
# SECTION 5: ADVANCED TOPICS - STIFF ODEs & LORENZ ATTRACTOR
# =========================================================================================
def demonstrate_stiff_odes_and_chaos() -> None:
    """
    Demonstrates handling of stiff ODEs (where standard methods like RK45 fail or are 
    incredibly slow) and chaotic systems like the Lorenz Attractor.
    """
    print("\n" + "="*60)
    print("SECTION 5: STIFF ODES & CHAOTIC SYSTEMS")
    print("="*60)

    # 1. Stiff ODE Example (Van der Pol Oscillator with high mu)
    # d^2x/dt^2 - mu * (1 - x^2) * dx/dt + x = 0
    # Let y1 = x, y2 = dx/dt
    # dy1/dt = y2
    # dy2/dt = mu * (1 - y1^2) * y2 - y1
    mu = 1000.0 # High mu makes the system stiff

    def vanderpol(t: float, y: List[float]) -> List[float]:
        y1, y2 = y
        return [y2, mu * (1 - y1**2) * y2 - y1]
    
    t_span_vdp = (0, 3000)
    y0_vdp = [2.0, 0.0]
    
    print(f"Solving stiff Van der Pol oscillator (mu={mu})...")
    print("Using Radau method (implicit, designed for stiff systems).")
    start_time = time.time()
    
    # Standard RK45 would take forever and likely fail. We must use a stiff solver.
    # 'Radau' or 'BDF' are appropriate for stiff problems.
    sol_stiff = spi.solve_ivp(vanderpol, t_span_vdp, y0_vdp, method='Radau', rtol=1e-6)
    
    print(f"   Solved in {time.time() - start_time:.4f} seconds.")
    print(f"   Number of evaluations: {sol_stiff.nfev} (Very efficient for stiff systems)")


# =========================================================================================
# SECTION 6: INTERVIEW CHALLENGE
# =========================================================================================
def interview_challenge() -> None:
    """
    INTERVIEW CHALLENGE: 
    Given an array of non-negative integers representing an elevation map where the width 
    of each bar is 1, compute how much water it can trap after raining using numerical
    integration concepts (area calculations).
    
    While this is traditionally solved via a two-pointer array algorithm (Trapping Rain Water),
    it conceptually aligns with calculating the area bounded between curves!
    We will solve it using the traditional O(N) array approach but explain it via the lens
    of discrete integration boundaries.
    """
    print("\n" + "="*60)
    print("SECTION 6: INTERVIEW CHALLENGE (Integration Context)")
    print("="*60)
    
    def trap_water(heights: List[int]) -> int:
        """
        Calculates trapped water.
        Time Complexity: O(N)
        Space Complexity: O(1)
        
        Concept: The water trapped at index i is the area between the curve of the water 
        surface and the terrain curve. The water surface at i is min(max_left, max_right).
        Thus, Water_Area = Integral( Water_Surface(x) - Terrain(x) dx ) 
        Since dx=1 for each block, we sum the discrete differences.
        """
        if not heights:
            return 0
            
        left, right = 0, len(heights) - 1
        left_max, right_max = heights[left], heights[right]
        total_water = 0
        
        while left < right:
            if left_max < right_max:
                left += 1
                left_max = max(left_max, heights[left])
                total_water += left_max - heights[left]
            else:
                right -= 1
                right_max = max(right_max, heights[right])
                total_water += right_max - heights[right]
                
        return total_water

    test_terrain = [0,1,0,2,1,0,1,3,2,1,2,1]
    water = trap_water(test_terrain)
    print(f"Terrain elevations: {test_terrain}")
    print(f"Total Water Trapped: {water} units")
    print("Concept mapping: Water volume is a discrete integral of the bounded region.")


# =========================================================================================
# MAIN EXECUTION & TESTS
# =========================================================================================
def run_all_demonstrations() -> None:
    """
    Executes the entire lesson plan.
    """
    try:
        demonstrate_single_integration()
        demonstrate_multiple_integration()
        demonstrate_discrete_integration()
        demonstrate_ode_solvers()
        demonstrate_stiff_odes_and_chaos()
        interview_challenge()
        print("\n" + "="*60)
        print("ALL SCIPY.INTEGRATE MODULES COMPLETED SUCCESSFULLY.")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred during execution: {e}")


if __name__ == "__main__":
    # Suppress specific scipy warnings if necessary for clean output
    warnings.filterwarnings("ignore", category=spi.IntegrationWarning)
    
    run_all_demonstrations()
