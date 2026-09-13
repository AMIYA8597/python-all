"""
Numerical Algorithms in Python

===============================================================================
Learning Objectives:
1. Understand the foundation of numerical computing and its applications.
2. Implement fundamental numerical algorithms from scratch (e.g., Root Finding, Integration).
3. Recognize the limitations of floating-point arithmetic and numerical stability.
4. Utilize standard libraries (`math`, `numpy`, `scipy`) for robust numerical computation.

Concept Explanation:
Numerical Algorithms are step-by-step mathematical procedures used to solve problems
involving continuous variables (unlike discrete math). They are essential when exact
analytical solutions are impossible or too computationally expensive.

Key Areas of Numerical Computing:
- **Root Finding**: Finding the solutions to f(x) = 0. (e.g., Newton-Raphson, Bisection).
- **Numerical Integration**: Approximating the definite integral of a function (e.g., Trapezoidal Rule).
- **Interpolation & Extrapolation**: Estimating unknown values that fall within or outside known data points.
- **Differential Equations**: Approximating solutions to ODEs and PDEs.

Performance & Stability:
- **Precision**: Due to IEEE 754 floating-point representation, numbers are approximations.
  Always use `math.isclose()` instead of `==` for float comparisons.
- **Stability**: Algorithms that compound errors over iterations are unstable. Care must
  be taken to structure computations to minimize round-off errors.

Industry Use Cases:
- Quantitative finance for pricing derivatives (Black-Scholes).
- Physics simulations and computer graphics.
- Machine Learning optimization (Gradient Descent).
===============================================================================
"""

import math
from typing import Callable, Tuple

# =============================================================================
# 1. Root Finding Algorithms
# =============================================================================

def bisection_method(func: Callable[[float], float], a: float, b: float, tol: float = 1e-6, max_iter: int = 100) -> float:
    """
    Finds a root of func(x) = 0 within the interval [a, b] using the Bisection Method.
    
    Args:
        func: The continuous function for which the root is sought.
        a: Lower bound of the interval.
        b: Upper bound of the interval.
        tol: Tolerance for the root approximation.
        max_iter: Maximum number of iterations.
        
    Returns:
        The approximated root x where func(x) is approximately 0.
        
    Raises:
        ValueError: If the root is not bracketed in [a, b] (i.e., func(a) * func(b) >= 0).
    """
    if func(a) * func(b) >= 0:
        raise ValueError("The root is not bracketed in the given interval [a, b].")
        
    for _ in range(max_iter):
        midpoint = (a + b) / 2.0
        
        # Check if we have found the root or reached the desired tolerance
        if abs(func(midpoint)) < tol or (b - a) / 2.0 < tol:
            return midpoint
            
        # Decide which half to keep
        if func(midpoint) * func(a) < 0:
            b = midpoint
        else:
            a = midpoint
            
    return (a + b) / 2.0


def newton_raphson(func: Callable[[float], float], deriv: Callable[[float], float], x0: float, tol: float = 1e-6, max_iter: int = 100) -> float:
    """
    Finds a root of func(x) = 0 using the Newton-Raphson method.
    Requires the derivative of the function.
    
    Args:
        func: The function f(x).
        deriv: The derivative f'(x).
        x0: Initial guess.
        tol: Tolerance.
        max_iter: Maximum iterations.
    """
    x = x0
    for i in range(max_iter):
        fx = func(x)
        dfx = deriv(x)
        
        if abs(fx) < tol:
            return x
            
        if dfx == 0:
            raise ZeroDivisionError(f"Derivative is zero at x = {x}. Method fails.")
            
        # Newton-Raphson update step: x_{n+1} = x_n - f(x_n)/f'(x_n)
        x = x - fx / dfx
        
    raise ValueError("Newton-Raphson did not converge within the maximum iterations.")

# =============================================================================
# 2. Numerical Integration
# =============================================================================

def trapezoidal_rule(func: Callable[[float], float], a: float, b: float, n: int) -> float:
    """
    Approximates the definite integral of func from a to b using the Trapezoidal Rule.
    
    Args:
        func: The integrand function.
        a: Lower limit of integration.
        b: Upper limit of integration.
        n: Number of trapezoids (subintervals).
    """
    h = (b - a) / n
    integral = 0.5 * (func(a) + func(b))
    
    for i in range(1, n):
        integral += func(a + i * h)
        
    return integral * h

# =============================================================================
# Main Execution and Tests
# =============================================================================

if __name__ == "__main__":
    print("--- Numerical Algorithms ---")
    
    # 1. Bisection Method
    # Solve x^2 - 4 = 0. Root is exactly 2.0 (for x > 0)
    def f(x: float) -> float: return x**2 - 4
    
    root_bisect = bisection_method(f, 0, 5)
    print(f"Bisection Method Root for x^2 - 4: {root_bisect}")
    assert math.isclose(root_bisect, 2.0, abs_tol=1e-5), "Bisection failed!"
    
    # 2. Newton-Raphson
    # Solve x^3 - x - 2 = 0
    def g(x: float) -> float: return x**3 - x - 2
    def dg(x: float) -> float: return 3*x**2 - 1
    
    root_newton = newton_raphson(g, dg, x0=1.5)
    print(f"Newton-Raphson Root for x^3 - x - 2: {root_newton}")
    assert math.isclose(g(root_newton), 0.0, abs_tol=1e-5), "Newton-Raphson failed!"
    
    # 3. Numerical Integration
    # Integrate x^2 from 0 to 1. Analytical answer is 1/3 ~ 0.333333
    def h(x: float) -> float: return x**2
    
    integral_approx = trapezoidal_rule(h, 0.0, 1.0, 1000)
    print(f"Trapezoidal Rule Integral of x^2 from 0 to 1: {integral_approx}")
    assert math.isclose(integral_approx, 1/3, abs_tol=1e-4), "Integration failed!"
    
    print("All numerical algorithm tests passed successfully!")

"""
===============================================================================
Interview Challenge:
The Secant Method is a root-finding algorithm that uses a succession of roots
of secant lines to better approximate a root of a function. It does not require
the derivative of the function, unlike Newton-Raphson, making it useful when
the derivative is hard to compute.

Challenge:
Implement the `secant_method(func, x0, x1, tol)` function.
Hint: The update formula is x_n = x_{n-1} - f(x_{n-1}) * (x_{n-1} - x_{n-2}) / (f(x_{n-1}) - f(x_{n-2})).

What happens if f(x_{n-1}) == f(x_{n-2})? How would you handle this case?
===============================================================================
"""
