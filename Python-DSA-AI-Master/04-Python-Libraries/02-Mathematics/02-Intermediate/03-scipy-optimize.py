"""
Module: 03-scipy-optimize
Description: A comprehensive, textbook-grade interactive lesson on `scipy.optimize`.

================================================================================
# MASTERING SCIPY.OPTIMIZE: A COMPREHENSIVE TEXTBOOK
================================================================================

## 1. Introduction
The `scipy.optimize` module provides a vast collection of algorithms for function 
minimization (scalar or multivariate), curve fitting, and root finding. Optimization 
is the mathematical discipline of finding the "best" available values of some objective 
function given a defined domain (and potentially constraints).

Whether you are training a machine learning model (minimizing a loss function), 
finding equilibrium states in physics (minimizing energy), or maximizing profit 
in economics (linear programming), optimization is the core computational engine.

## 2. Mathematical Background and Theory
Optimization problems generally take the form:
    Minimize:  f(x)
    Subject to: 
        g_i(x) >= 0  (Inequality constraints)
        h_j(x) == 0  (Equality constraints)
        x_L <= x <= x_U (Bounds)

### A. Root Finding
Root finding solves the equation f(x) = 0.
- **Bisection Method**: A bracketing method that repeatedly halves an interval 
  [a, b] where f(a) and f(b) have opposite signs. 
  * Time Complexity: O(log((b-a)/tol)) steps. 
  * Guaranteed to converge but relatively slow.
- **Newton-Raphson Method**: Uses the first derivative (gradient) to iteratively 
  find better approximations. x_{n+1} = x_n - f(x_n) / f'(x_n).
  * Time Complexity: Quadratic convergence near the root.
  * Can diverge if the derivative is close to zero or initial guess is poor.
- **Secant / Brent's Method**: Combines bisection, secant, and inverse quadratic 
  interpolation. This is the default in many SciPy functions because it offers 
  the robustness of bisection with the superlinear convergence of secant.

### B. Unconstrained Minimization
- **Nelder-Mead (Simplex)**: A derivative-free heuristic algorithm. It maintains 
  a simplex of n+1 points in n-dimensional space and iteratively updates the 
  worst point. Good for noisy or non-differentiable functions.
- **BFGS (Broyden-Fletcher-Goldfarb-Shanno)**: A quasi-Newton method that 
  builds an approximation to the Hessian matrix (second derivatives) iteratively 
  using gradient evaluations. Very fast for smooth functions. O(N^2) space complexity.
- **CG (Conjugate Gradient)**: Uses gradients but avoids storing the full Hessian 
  matrix, making it suitable for very large-scale problems (O(N) space).

### C. Constrained Minimization
- **SLSQP (Sequential Least SQuares Programming)**: Solves non-linear programming 
  problems with equality and inequality constraints. It iteratively solves quadratic 
  approximations of the objective, subject to linearizations of the constraints.

### D. Global Optimization
Local minimizers can get stuck in local valleys. Global optimizers attempt to find 
the absolute minimum over a domain.
- **Differential Evolution**: A stochastic population-based method inspired by genetics.
- **Dual Annealing / Simulated Annealing**: Inspired by metallurgy, uses a temperature 
  parameter to occasionally accept worse solutions to escape local minima.

### E. Linear Programming
Special case where both the objective function and constraints are strictly linear.
- **Simplex Algorithm**: Moves along the edges of the feasible convex polytope.
- **Interior-Point Methods**: Traverses the interior of the feasible region, 
  which has polynomial time complexity in the worst case (unlike Simplex).

## 3. Learning Objectives
By the end of this module, you will be able to:
1. Find roots of scalar and multivariate functions.
2. Minimize complex, multi-variable objective functions without constraints.
3. Formulate and solve constrained optimization problems.
4. Perform robust curve fitting using least squares techniques.
5. Use global optimization algorithms to escape local minima.
6. Solve real-world supply chain and resource allocation problems via linear programming.

================================================================================
"""

import time
import math
import typing
from typing import List, Tuple, Callable, Dict, Any, Optional

try:
    import numpy as np
    from scipy import optimize
    from scipy.optimize import OptimizeResult
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    print("WARNING: NumPy and/or SciPy are not installed.")
    print("Please install them using: pip install numpy scipy")
    print("The code will use mock data or raise NotImplementedError if run without them.")


# ==============================================================================
# SECTION 1: SCALAR ROOT FINDING
# ==============================================================================

def underlying_theory_bisection(func: Callable[[float], float], a: float, b: float, tol: float = 1e-6, max_iter: int = 100) -> Tuple[float, int]:
    """
    To appreciate SciPy's root finding, we first implement a foundational algorithm manually.
    The Bisection Method requires f(a) and f(b) to have opposite signs.
    
    Args:
        func: The continuous scalar function f(x).
        a: Left boundary of the interval.
        b: Right boundary of the interval.
        tol: Tolerance for the root approximation.
        max_iter: Maximum number of iterations to prevent infinite loops.
        
    Returns:
        A tuple (root_estimate, number_of_iterations).
        
    Raises:
        ValueError: If f(a) and f(b) do not have opposite signs.
    """
    fa, fb = func(a), func(b)
    if fa * fb > 0:
        raise ValueError(f"Root not bracketed. f({a})={fa}, f({b})={fb}")
    
    for i in range(max_iter):
        mid = (a + b) / 2.0
        fmid = func(mid)
        
        # Check if we have found the root exactly or if the interval is small enough
        if abs(fmid) < tol or (b - a) / 2.0 < tol:
            return mid, i + 1
            
        # Narrow the bracket
        if fa * fmid < 0:
            b = mid
            fb = fmid
        else:
            a = mid
            fa = fmid
            
    return (a + b) / 2.0, max_iter


def demonstrate_scalar_root_finding() -> None:
    """
    Demonstrates `scipy.optimize.root_scalar`, which provides a unified interface
    for scalar root finding algorithms (Brent, Newton, Bisect, etc.).
    """
    print("\n" + "="*50)
    print("1. SCALAR ROOT FINDING (root_scalar)")
    print("="*50)
    
    if not HAS_SCIPY:
        print("Skipping - SciPy not installed.")
        return

    # Objective function: A cubic polynomial f(x) = x^3 - 2x^2 - 11x + 12
    # Roots are at x = -3, 1, 4
    def cubic_function(x: float) -> float:
        return x**3 - 2*x**2 - 11*x + 12
        
    # Derivative: f'(x) = 3x^2 - 4x - 11
    def cubic_derivative(x: float) -> float:
        return 3*x**2 - 4*x - 11

    # Method 1: Brent's Method (Default for bracketed roots in SciPy)
    # Brent's method does not require derivatives. We provide an interval [bracket].
    bracket = (2.5, 5.0) # Should bracket the root at x=4
    res_brent = optimize.root_scalar(cubic_function, bracket=bracket, method='brentq')
    print(f"Brent's Method (Bracket {bracket}):")
    print(f"  Root found at x = {res_brent.root:.6f}")
    print(f"  Iterations: {res_brent.iterations}")
    print(f"  Function calls: {res_brent.function_calls}")
    print(f"  Converged: {res_brent.converged}\n")

    # Method 2: Newton-Raphson Method
    # Newton's method requires a starting point (x0) and a first derivative (fprime).
    x0 = 0.0 # Starting close to x=1
    res_newton = optimize.root_scalar(cubic_function, x0=x0, fprime=cubic_derivative, method='newton')
    print(f"Newton-Raphson Method (Initial guess x0={x0}):")
    print(f"  Root found at x = {res_newton.root:.6f}")
    print(f"  Iterations: {res_newton.iterations}")
    print(f"  Function calls: {res_newton.function_calls}")
    print(f"  Converged: {res_newton.converged}\n")

    # Let's compare with our manual bisection
    try:
        manual_root, iters = underlying_theory_bisection(cubic_function, 2.5, 5.0)
        print(f"Manual Bisection Method (Bracket 2.5 to 5.0):")
        print(f"  Root found at x = {manual_root:.6f}")
        print(f"  Iterations: {iters}\n")
        # Notice that Bisection typically takes more iterations (~20-25) compared to Brent (~6-8).
    except ValueError as e:
        print(f"Bisection failed: {e}")


# ==============================================================================
# SECTION 2: MULTIVARIATE ROOT FINDING
# ==============================================================================

def demonstrate_multivariate_root_finding() -> None:
    """
    Demonstrates `scipy.optimize.root` for solving systems of non-linear equations.
    """
    print("\n" + "="*50)
    print("2. MULTIVARIATE ROOT FINDING (root)")
    print("="*50)
    
    if not HAS_SCIPY:
        return

    # System of non-linear equations:
    # 1. x^2 + y^2 = 1 (A circle of radius 1 centered at origin)
    # 2. y - x^2 = 0   (A parabola opening upwards)
    # We want to find the intersection points. 
    # Expected roots approx: (+-0.786, 0.618)
    
    def system_of_equations(vars_array: np.ndarray) -> np.ndarray:
        x, y = vars_array[0], vars_array[1]
        eq1 = x**2 + y**2 - 1.0
        eq2 = y - x**2
        return np.array([eq1, eq2])

    # Initial guess
    guess = np.array([0.5, 0.5])
    
    # Using the default hybr method (MINPACK's Powell hybrid method)
    result = optimize.root(system_of_equations, guess)
    
    print("System: x^2 + y^2 = 1 AND y - x^2 = 0")
    print(f"Initial Guess: {guess}")
    print(f"Converged: {result.success}")
    if result.success:
        print(f"Solution: x = {result.x[0]:.5f}, y = {result.x[1]:.5f}")
        # Verify the solution
        residuals = system_of_equations(result.x)
        print(f"Residuals (should be near 0): {residuals}")
    else:
        print(f"Failed to converge: {result.message}")


# ==============================================================================
# SECTION 3: UNCONSTRAINED OPTIMIZATION (MINIMIZATION)
# ==============================================================================

def demonstrate_unconstrained_minimization() -> None:
    """
    Demonstrates minimizing scalar and multivariate functions without constraints.
    """
    print("\n" + "="*50)
    print("3. UNCONSTRAINED MINIMIZATION")
    print("="*50)

    if not HAS_SCIPY:
        return

    # --- 3A: SCALAR MINIMIZATION ---
    print("--- 3A. Scalar Minimization (minimize_scalar) ---")
    # Objective: Minimize the Rosenbrock valley in 1D, or a simpler function
    # Let's use f(x) = (x - 3.14)^2 + 2 * sin(x)
    def scalar_objective(x: float) -> float:
        return (x - 3.14)**2 + 2 * math.sin(x)

    # Using Brent's method to find local minimum
    res_scalar = optimize.minimize_scalar(scalar_objective, method='brent')
    print("Objective: f(x) = (x - 3.14)^2 + 2 * sin(x)")
    print(f"Minimum found at x = {res_scalar.x:.5f}")
    print(f"Function value at minimum = {res_scalar.fun:.5f}")
    print(f"Function evaluations = {res_scalar.nfev}\n")


    # --- 3B: MULTIVARIATE MINIMIZATION ---
    print("--- 3B. Multivariate Minimization (minimize) ---")
    # The Rosenbrock function is the classic non-convex test case for optimization algorithms.
    # It features a long, narrow, parabolic valley. Finding the valley is easy, 
    # but converging to the global minimum (at 1,1,...,1) is difficult.
    # f(x, y) = (a - x)^2 + b(y - x^2)^2 (where typically a=1, b=100)
    
    def rosenbrock(x: np.ndarray) -> float:
        """The Rosenbrock function."""
        return sum(100.0 * (x[1:] - x[:-1]**2.0)**2.0 + (1 - x[:-1])**2.0)
        
    def rosenbrock_der(x: np.ndarray) -> np.ndarray:
        """First derivative (gradient) of the Rosenbrock function."""
        xm = x[1:-1]
        xm_m1 = x[:-2]
        xm_p1 = x[2:]
        der = np.zeros_like(x)
        der[1:-1] = 200 * (xm - xm_m1**2) - 400 * (xm_p1 - xm**2) * xm - 2 * (1 - xm)
        der[0] = -400 * x[0] * (x[1] - x[0]**2) - 2 * (1 - x[0])
        der[-1] = 200 * (x[-1] - x[-2]**2)
        return der

    x0 = np.array([-1.2, 1.0, -1.5, 2.0]) # 4D Rosenbrock initial guess
    print(f"Objective: 4D Rosenbrock Function")
    print(f"Initial guess: {x0}")

    # Method 1: Nelder-Mead (Simplex)
    # Does not use gradients. Slower but robust to noise.
    start = time.time()
    res_nm = optimize.minimize(rosenbrock, x0, method='Nelder-Mead', options={'disp': False})
    t_nm = time.time() - start
    print("\nAlgorithm: Nelder-Mead (Derivative-Free)")
    print(f"  Success: {res_nm.success}")
    print(f"  Minimum x: {np.round(res_nm.x, 4)}")
    print(f"  Min Value: {res_nm.fun:.2e}")
    print(f"  Evaluations: {res_nm.nfev}, Time: {t_nm:.4f} sec")

    # Method 2: BFGS (Quasi-Newton)
    # Uses gradient (approximated numerically if not provided). Much faster.
    start = time.time()
    res_bfgs = optimize.minimize(rosenbrock, x0, method='BFGS', jac=rosenbrock_der, options={'disp': False})
    t_bfgs = time.time() - start
    print("\nAlgorithm: BFGS (Using Analytical Jacobian/Gradient)")
    print(f"  Success: {res_bfgs.success}")
    print(f"  Minimum x: {np.round(res_bfgs.x, 4)}")
    print(f"  Min Value: {res_bfgs.fun:.2e}")
    print(f"  Evaluations: {res_bfgs.nfev}, Time: {t_bfgs:.4f} sec")
    print("  (Notice how BFGS with explicit gradients requires far fewer evaluations than Nelder-Mead)")


# ==============================================================================
# SECTION 4: CONSTRAINED OPTIMIZATION
# ==============================================================================

def demonstrate_constrained_minimization() -> None:
    """
    Demonstrates solving optimization problems subject to constraints and bounds.
    Algorithm typically used: SLSQP (Sequential Least SQuares Programming).
    """
    print("\n" + "="*50)
    print("4. CONSTRAINED MINIMIZATION (SLSQP)")
    print("="*50)

    if not HAS_SCIPY:
        return

    # Let's solve a practical geometric problem:
    # Maximize the volume of a rectangular box (V = x * y * z),
    # subject to a constraint on its surface area (A = 2xy + 2xz + 2yz <= 100)
    # Since SciPy only *minimizes*, we minimize the negative volume.
    
    def objective(vars_array: np.ndarray) -> float:
        x, y, z = vars_array
        volume = x * y * z
        return -volume  # Negative for maximization
        
    def surface_area_constraint(vars_array: np.ndarray) -> float:
        x, y, z = vars_array
        # The constraint is formulated such that C(x) >= 0.
        # So: 100 - (2xy + 2xz + 2yz) >= 0
        return 100.0 - 2.0 * (x*y + x*z + y*z)

    # We also have bounds: dimensions must be strictly positive.
    # Let's say at least 0.1, and practically bounded above by 10
    bounds = ((0.1, 10.0), (0.1, 10.0), (0.1, 10.0))
    
    # Define constraints dictionary for SciPy
    cons = ({
        'type': 'ineq', 
        'fun': surface_area_constraint
    })

    # Initial guess
    x0 = np.array([1.0, 1.0, 1.0])
    
    print("Problem: Maximize volume of 3D box (minimize -x*y*z)")
    print("Subject to: Surface Area <= 100, and 0.1 <= x,y,z <= 10")
    
    res = optimize.minimize(
        objective, 
        x0, 
        method='SLSQP', 
        bounds=bounds, 
        constraints=cons
    )
    
    if res.success:
        x, y, z = res.x
        max_vol = -res.fun
        surf_area = 2*(x*y + x*z + y*z)
        print(f"\nOptimization Successful: {res.message}")
        print(f"Optimal Dimensions: x={x:.3f}, y={y:.3f}, z={z:.3f}")
        print(f"Maximum Volume: {max_vol:.3f}")
        print(f"Surface Area Used: {surf_area:.3f} (Max allowed was 100)")
        print("Note: The cube (x=y=z) is the optimal shape for maximizing volume for a given surface area.")
    else:
        print(f"Optimization Failed: {res.message}")


# ==============================================================================
# SECTION 5: GLOBAL OPTIMIZATION
# ==============================================================================

def demonstrate_global_optimization() -> None:
    """
    Demonstrates Global Optimization algorithms.
    Standard local optimizers get trapped in the nearest local minimum.
    Global optimizers explore the space more broadly to find the global minimum.
    """
    print("\n" + "="*50)
    print("5. GLOBAL OPTIMIZATION")
    print("="*50)

    if not HAS_SCIPY:
        return

    # We use the Eggholder function, a notorious function for optimization testing
    # because it is characterized by an immense number of local minima.
    # Global minimum is at f(x,y) ≈ -959.6407, for x=512, y=404.2319
    
    def eggholder(v: np.ndarray) -> float:
        x, y = v
        term1 = -(y + 47.0) * np.sin(np.sqrt(abs(x / 2.0 + (y + 47.0))))
        term2 = -x * np.sin(np.sqrt(abs(x - (y + 47.0))))
        return term1 + term2

    bounds = [(-512, 512), (-512, 512)]
    
    print("Objective: Eggholder Function (Highly non-convex, many local minima)")
    print(f"Search space bounds: {bounds}")
    
    # 1. Using standard local minimization (will likely fail to find the global minimum)
    print("\nAttempting with Local Optimizer (BFGS)...")
    res_local = optimize.minimize(eggholder, x0=[0, 0], bounds=bounds, method='L-BFGS-B')
    print(f"  Local Minimum found at: x={res_local.x[0]:.2f}, y={res_local.x[1]:.2f}")
    print(f"  Function value: {res_local.fun:.2f} (Far from true global min ~ -959.64)")

    # 2. Using Differential Evolution (Global)
    print("\nAttempting with Global Optimizer (Differential Evolution)...")
    start = time.time()
    res_de = optimize.differential_evolution(eggholder, bounds, seed=42)
    t_de = time.time() - start
    print(f"  Global Minimum found at: x={res_de.x[0]:.2f}, y={res_de.x[1]:.2f}")
    print(f"  Function value: {res_de.fun:.2f}")
    print(f"  Evaluations: {res_de.nfev}, Time: {t_de:.4f} sec")


# ==============================================================================
# SECTION 6: CURVE FITTING & LEAST SQUARES
# ==============================================================================

def demonstrate_curve_fitting() -> None:
    """
    Demonstrates `scipy.optimize.curve_fit` for fitting a parameterized mathematical
    model to experimental data, utilizing non-linear least squares.
    """
    print("\n" + "="*50)
    print("6. CURVE FITTING (curve_fit)")
    print("="*50)

    if not HAS_SCIPY:
        return

    # Simulate some noisy data that follows an exponential decay model:
    # y = A * exp(-B * x) + C
    np.random.seed(0)
    x_data = np.linspace(0, 4, 50)
    true_A, true_B, true_C = 2.5, 1.3, 0.5
    y_true = true_A * np.exp(-true_B * x_data) + true_C
    
    # Add random Gaussian noise
    y_noise = 0.2 * np.random.normal(size=x_data.size)
    y_data = y_true + y_noise

    # Define the model function to fit
    def decay_model(x: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
        return a * np.exp(-b * x) + c

    print("Model: y = A * exp(-B * x) + C")
    print(f"True parameters: A={true_A}, B={true_B}, C={true_C}")
    print("Adding Gaussian noise to generate mock experimental data...")

    # Perform the curve fit
    # popt: Optimal values for the parameters so that the sum of the squared residuals 
    #       of f(xdata, *popt) - ydata is minimized.
    # pcov: The estimated covariance of popt. The diagonals provide the variance.
    try:
        popt, pcov = optimize.curve_fit(decay_model, x_data, y_data)
        
        # Calculate standard deviations of the fitted parameters
        perr = np.sqrt(np.diag(pcov))
        
        print("\nFitted Parameters:")
        print(f"  A = {popt[0]:.3f} +/- {perr[0]:.3f}")
        print(f"  B = {popt[1]:.3f} +/- {perr[1]:.3f}")
        print(f"  C = {popt[2]:.3f} +/- {perr[2]:.3f}")
        
        # Calculate R-squared to see goodness of fit
        residuals = y_data - decay_model(x_data, *popt)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y_data - np.mean(y_data))**2)
        r_squared = 1 - (ss_res / ss_tot)
        print(f"\nGoodness of Fit (R^2): {r_squared:.4f}")
        
    except Exception as e:
        print(f"Curve fitting failed: {e}")


# ==============================================================================
# SECTION 7: LINEAR PROGRAMMING
# ==============================================================================

def demonstrate_linear_programming() -> None:
    """
    Demonstrates `scipy.optimize.linprog` for linear programming.
    Linear programming solves problems where the objective and constraints are all linear.
    """
    print("\n" + "="*50)
    print("7. LINEAR PROGRAMMING (linprog)")
    print("="*50)

    if not HAS_SCIPY:
        return

    # Scenario: A factory produces two products, P1 and P2.
    # Profit per unit: P1=$30, P2=$20. (We want to maximize 30*x1 + 20*x2)
    # Since linprog minimizes, our objective is to minimize (-30*x1 - 20*x2).
    # 
    # Constraints (Resource limits):
    # 1. Machine A time: 2*x1 + 1*x2 <= 100 hours
    # 2. Machine B time: 1*x1 + 1*x2 <= 80 hours
    # 3. Machine C time: 1*x1 + 0*x2 <= 40 hours
    # 
    # Bounds: x1 >= 0, x2 >= 0
    
    # Objective coefficients (minimize -30*x1 - 20*x2)
    c = [-30, -20]
    
    # Inequality constraints matrix (left-hand side)
    A_ub = [
        [2, 1], # Machine A
        [1, 1], # Machine B
        [1, 0]  # Machine C
    ]
    
    # Inequality constraints vector (right-hand side)
    b_ub = [100, 80, 40]
    
    # Bounds for variables
    x1_bounds = (0, None)
    x2_bounds = (0, None)

    print("Factory Production Problem (Maximize Profit):")
    print("  Maximize: 30*P1 + 20*P2")
    print("  Subject to:")
    print("    2*P1 + 1*P2 <= 100")
    print("    1*P1 + 1*P2 <= 80")
    print("    1*P1 <= 40")
    print("    P1 >= 0, P2 >= 0")

    # Solve using the highs-ds method (default dual simplex for SciPy modern versions)
    res = optimize.linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[x1_bounds, x2_bounds], method='highs')
    
    if res.success:
        p1, p2 = res.x
        max_profit = -res.fun # Reverse the sign back to positive profit
        print(f"\nSolution Found:")
        print(f"  Produce {p1:.1f} units of P1")
        print(f"  Produce {p2:.1f} units of P2")
        print(f"  Maximum Profit = ${max_profit:.2f}")
    else:
        print(f"Linear Programming failed: {res.message}")


# ==============================================================================
# SECTION 8: PERFORMANCE, EDGE CASES & BEST PRACTICES
# ==============================================================================

def analyze_performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks, edge cases, and best practices 
    when working with numerical optimization.
    """
    print("\n" + "="*50)
    print("8. PERFORMANCE, EDGE CASES & BEST PRACTICES")
    print("="*50)
    
    print("""
1. Provide Gradients (Jacobians) where possible:
   - Algorithms like BFGS use the derivative to determine the direction of descent.
   - If you do not provide `jac=gradient_func`, SciPy approximates it using finite 
     differences. This requires additional objective function calls per iteration, 
     drastically slowing down large multidimensional problems and introducing 
     floating-point inaccuracies.

2. Scaling / Preconditioning:
   - If your variables operate on vastly different scales (e.g., x1 is in millions, 
     x2 is in decimals), optimization algorithms struggle to converge. 
   - Always normalize or scale your variables to be roughly O(1).

3. Local vs. Global Minima:
   - Gradient-descent based methods (BFGS, Newton) find the *nearest* local minimum.
   - If your function is non-convex (like the Eggholder function), the result depends 
     entirely on the initial guess `x0`.
   - Use multi-start (running local minimization from multiple random `x0`) or global 
     algorithms (`differential_evolution`, `basinhopping`) for non-convex functions.

4. Edge Cases - Discontinuous or Noisy Functions:
   - Gradient methods fail completely on non-differentiable or noisy functions.
   - Fallback to derivative-free methods like `Nelder-Mead` or Powell's method.

5. Dimensionality Curse:
   - Global optimization time scales exponentially with dimensionality. Do not expect 
     `differential_evolution` to quickly solve a 10,000-dimensional neural network 
     parameter space. For extreme dimensionalities, specialized stochastic gradient 
     descent (SGD, Adam) implemented in PyTorch/TensorFlow are required.
    """)


# ==============================================================================
# SECTION 9: REAL-WORLD / INTERVIEW CHALLENGE
# ==============================================================================

def real_world_challenge() -> None:
    """
    A common algorithmic challenge framed as a mathematical optimization problem:
    The Facility Location Problem (Weber Problem / Geometric Median).
    
    Problem Statement:
    Given a set of N customer coordinates on a 2D grid, find the optimal coordinates
    for a single warehouse that minimizes the sum of Euclidean distances to all customers.
    """
    print("\n" + "="*50)
    print("9. INTERVIEW / REAL-WORLD CHALLENGE: FACILITY LOCATION")
    print("="*50)

    if not HAS_SCIPY:
        return

    # 5 Customer locations on a grid (x, y)
    customers = np.array([
        [2, 3],
        [4, 8],
        [8, 1],
        [9, 6],
        [5, 5]
    ])
    
    print("Customer Locations (x, y):")
    for idx, (x, y) in enumerate(customers):
        print(f"  C{idx+1}: ({x}, {y})")

    # Objective Function: Sum of Euclidean distances
    def sum_of_distances(warehouse_pos: np.ndarray) -> float:
        # warehouse_pos is [x, y]
        # np.linalg.norm computes Euclidean distance across the axis
        distances = np.linalg.norm(customers - warehouse_pos, axis=1)
        return float(np.sum(distances))
        
    # Initial guess (Centroid/mean of all customer locations)
    # The mean minimizes squared distances, but we want to minimize absolute distances.
    # It serves as an excellent starting guess.
    initial_guess = np.mean(customers, axis=0)
    
    print(f"\nInitial Guess (Centroid): x={initial_guess[0]:.2f}, y={initial_guess[1]:.2f}")
    initial_cost = sum_of_distances(initial_guess)
    print(f"Cost at Centroid: {initial_cost:.2f}")

    # Run optimization (Nelder-Mead is great here because the absolute distance 
    # derivative can be undefined if the warehouse lands exactly on a customer).
    res = optimize.minimize(sum_of_distances, initial_guess, method='Nelder-Mead')
    
    if res.success:
        opt_x, opt_y = res.x
        print(f"\nOptimized Warehouse Location (Geometric Median):")
        print(f"  x={opt_x:.2f}, y={opt_y:.2f}")
        print(f"  Minimized Cost (Sum of Distances): {res.fun:.2f}")
        print("Notice how the Geometric Median provides a slightly lower total distance than the simple centroid.")
    else:
        print("Optimization failed.")


# ==============================================================================
# MAIN EXECUTION BLOCK
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "#" * 70)
    print(" " * 20 + "SCIPY.OPTIMIZE MASTERCLASS")
    print("#" * 70)

    # 1. Root Finding
    demonstrate_scalar_root_finding()
    demonstrate_multivariate_root_finding()

    # 2. Unconstrained Minimization
    demonstrate_unconstrained_minimization()

    # 3. Constrained Minimization
    demonstrate_constrained_minimization()

    # 4. Global Optimization
    demonstrate_global_optimization()

    # 5. Curve Fitting
    demonstrate_curve_fitting()

    # 6. Linear Programming
    demonstrate_linear_programming()

    # 7. Real World Challenge
    real_world_challenge()

    # 8. Best Practices
    analyze_performance_and_edge_cases()

    print("\n" + "#" * 70)
    print(" " * 20 + "LESSON COMPLETE")
    print("#" * 70 + "\n")
