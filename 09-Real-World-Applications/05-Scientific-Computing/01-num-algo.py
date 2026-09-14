"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (SCIENTIFIC COMPUTING & SCIPY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A quantitative analyst needs to model the aerodynamic drag of a rocket re-entering 
# the atmosphere. The math involves finding the Area Under a Curve (Integration) 
# and predicting future states based on rates of change (Differential Equations). 
# A junior analyst attempts to write a custom Python `while` loop using the 
# Euler Method. The float precision drifts by 0.0001% per loop. Over 10 million 
# iterations, the cumulative drift is so catastrophic the simulation mathematically 
# believes the rocket crashed into the moon instead of Earth.
#
# A senior Data Scientist understands "Numerical Stability". They install `SciPy`. 
# They use the battle-tested Fortran 77 backend (`ODEPACK`) to mathematically 
# execute an explicit Runge-Kutta (RK45) integration algorithm. The C/Fortran 
# solver dynamically scales its own time steps to mathematically guarantee an 
# error bound of 1e-8. It flawlessly models the trajectory in 0.2 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the mathematical architecture of `SciPy` (Scientific Python).
# - Execute Numerical Integration (Calculating the Area Under a Curve).
# - Execute Numerical Optimization (Finding the mathematical Minimum).
#
# ==============================================================================
"""

import math
import timeit

# Gracefully handle missing SciPy/NumPy dependencies
try:
    import numpy as np
    from scipy.integrate import quad
    from scipy.optimize import minimize_scalar
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. NUMERICAL INTEGRATION (AREA UNDER A CURVE)
# ==============================================================================
# We want to find the exact Area Under the Curve for the mathematical function:
# f(x) = x^2 * sin(x)
# Bounded between x = 0 and x = 5.

def mathematical_function(x: float) -> float:
    """The continuous mathematical curve."""
    return (x**2) * math.sin(x)

def demonstrate_numerical_integration():
    section_header("Scientific Calculus: Numerical Integration (scipy.integrate)")
    
    if not HAS_SCIPY:
        print("  [ERROR] SciPy is not installed. Run `pip install scipy numpy`.")
        return
        
    print("  [SCENARIO] Calculating the Definite Integral of f(x) = x^2 * sin(x) from 0 to 5.")
    
    # 1. The Naive Approach (Riemann Sum / Rectangle Method)
    # We chop the area into 1,000,000 tiny rectangles and sum them up!
    print("\n  [NAIVE PYTHON EXECUTION (Riemann Sum)]")
    start_naive = timeit.default_timer()
    
    N = 1_000_000
    a = 0.0
    b = 5.0
    dx = (b - a) / N
    
    total_area = 0.0
    for i in range(N):
        x_i = a + (i * dx)
        # Area of rectangle = width * height
        total_area += dx * mathematical_function(x_i)
        
    end_naive = timeit.default_timer()
    print(f"    -> Area Calculated:  {total_area:.8f}")
    print(f"    -> Execution Time:   {end_naive - start_naive:.4f} seconds")


    # 2. The Professional Approach (QUADPACK Fortran Library)
    print("\n  [PROFESSIONAL SCIPY EXECUTION (quad)]")
    # `quad` calls a highly optimized Fortran 77 algorithm (QUADPACK).
    # It uses adaptive Gaussian quadrature math to achieve infinite precision instantly!
    start_scipy = timeit.default_timer()
    
    # quad(function, lower_bound, upper_bound)
    area, error_bound = quad(mathematical_function, 0.0, 5.0)
    
    end_scipy = timeit.default_timer()
    print(f"    -> Area Calculated:  {area:.8f}")
    print(f"    -> Error Bound:      ±{error_bound:.2e} (Absolute Mathematical Perfection)")
    print(f"    -> Execution Time:   {end_scipy - start_scipy:.4f} seconds")


# ==============================================================================
# 4. NUMERICAL OPTIMIZATION (FINDING THE MINIMUM)
# ==============================================================================
# We want to find the exact optimal price to sell a product to maximize profit.
# The mathematical Profit Curve is given by:
# Profit(x) = - (x - 25)^2 + 500  (This is a parabola peaking at x=25)
# Because scipy.optimize finds the MINIMUM, we must mathematically INVERT the 
# function by multiplying by -1 to find the MAXIMUM!

def inverted_profit_function(x: float) -> float:
    """The inverted parabolic profit curve."""
    # We want to maximize: -(x-25)^2 + 500
    # Therefore, we minimize: (x-25)^2 - 500
    return ((x - 25) ** 2) - 500

def demonstrate_numerical_optimization():
    section_header("Scientific Calculus: Numerical Optimization (scipy.optimize)")
    
    if not HAS_SCIPY:
        return
        
    print("  [SCENARIO] Finding the exact optimal Price (X) to maximize Profit(X).")
    print("  Profit Curve: f(x) = -(x-25)^2 + 500")
    
    print("\n  [EXECUTING BRENT'S METHOD OPTIMIZATION]")
    # We mathematically constrain the algorithm to search between prices 0 and 100.
    # Brent's method is a root-finding algorithm combining the bisection method, 
    # the secant method, and inverse quadratic interpolation.
    
    result = minimize_scalar(inverted_profit_function, bounds=(0, 100), method='bounded')
    
    print(f"    -> Algorithm Success: {result.success}")
    print(f"    -> Optimal Price (X): ${result.x:.2f}")
    
    # We invert the math back to calculate the real profit!
    optimal_profit = -result.fun
    print(f"    -> Max Profit (Y):    ${optimal_profit:.2f}")
    print(f"    -> CPU Iterations:    {result.nfev} evaluations (Lightning Fast!)")


def run_all_labs():
    demonstrate_numerical_integration()
    demonstrate_numerical_optimization()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why shouldn't you write your own mathematical integration or optimization algorithms in raw Python using `while` loops?"
   Senior Answer: "Numerical Stability and Float Drifting. In Calculus, integrating a curve requires slicing the data into infinitely small steps (e.g., $dx = 0.0000001$). Because CPUs use IEEE 754 Floating Point binary architecture, $0.1 + 0.2$ mathematically evaluates to $0.30000000000000004$. If you loop $10$ million times, these microscopic float precision errors compound violently, completely corrupting the final answer. Professional libraries like SciPy interface directly with battle-tested C and Fortran 77 libraries (like QUADPACK for integration or LAPACK for linear algebra). These underlying libraries contain decades of advanced mathematical heuristics specifically designed to dynamically adjust step sizes to mathematically counter IEEE 754 precision drifting, guaranteeing stable, scientifically viable results."

2. Interviewer: "When executing numerical optimization using `scipy.optimize.minimize`, why did we have to 'invert' the mathematical profit function?"
   Senior Answer: "Because of standardized algorithmic architecture. All standard optimization algorithms in Calculus (like Gradient Descent, Newton-CG, or BFGS) are mathematically architected to find the 'Global Minimum' (the lowest physical point in a valley on the graph). If you have a Profit Curve that looks like a mountain (a Parabola opening downwards), and you tell the algorithm to minimize it, it will run to $-\\infty$ (Negative Infinity) and crash. By mathematically multiplying the entire function by $-1$, we physically invert the mountain into a valley. The algorithm flawlessly finds the lowest point in the valley, which mathematically corresponds precisely to the peak of the original mountain."

3. Interviewer: "What is 'Brent's Method' (`method='bounded'`), and why is it superior to simply plotting 100 points on a graph and picking the highest one (Grid Search)?"
   Senior Answer: "Grid Search (plotting 100 points) is highly inefficient and mathematically inaccurate. If you check Price = $24$ and Price = $25$, you completely miss the possibility that the absolute perfect mathematical maximum was $24.782$. Brent's Method is an advanced root-finding algorithm that combines three distinct mathematical concepts: the Bisection Method (chopping the search space in half repeatedly), the Secant Method, and Inverse Quadratic Interpolation. It behaves intelligently; it rapidly narrows down the mathematical search space without evaluating the entire curve. It evaluates the function only $10$ or $15$ times in total, converging on the absolute perfect float value (e.g., $24.9999999$) in microseconds, vastly outperforming Grid Search in both speed and mathematical precision."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Scientific Computing (SciPy) Completed.")
