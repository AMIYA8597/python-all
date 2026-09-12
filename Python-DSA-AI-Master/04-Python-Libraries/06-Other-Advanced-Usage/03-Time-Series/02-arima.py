"""
Module: 02-arima
Description: A textbook-grade, interactive lesson on ARIMA (AutoRegressive Integrated Moving Average) models.

===========================================================================
                      ARIMA (AutoRegressive Integrated Moving Average)
===========================================================================

Learning Objectives:
1. Understand the core components of ARIMA: AR (Autoregression), I (Integration), and MA (Moving Average).
2. Grasp the mathematical background of time series modeling.
3. Learn how to simulate AR, MA, and ARIMA processes from scratch.
4. Understand the Big-O time and space complexities associated with parameter estimation and forecasting.
5. Apply real-world forecasting techniques using Python (statsmodels) and custom implementations.

---------------------------------------------------------------------------
1. Mathematical Background
---------------------------------------------------------------------------
ARIMA is characterized by three parameters: (p, d, q)

- **AR(p) - Autoregression**:
  The current value is a linear combination of its past `p` values.
  Equation:
      Y_t = c + φ_1 Y_{t-1} + φ_2 Y_{t-2} + ... + φ_p Y_{t-p} + ε_t
  where φ_i are the parameters, c is a constant, and ε_t is white noise.

- **I(d) - Integration**:
  The number of non-seasonal differences needed to make the time series stationary.
  If d=1, we model the difference: Y'_t = Y_t - Y_{t-1}.
  A stationary series has a constant mean and variance over time.

- **MA(q) - Moving Average**:
  The current value is a linear combination of past `q` error terms (white noise).
  Equation:
      Y_t = μ + ε_t + θ_1 ε_{t-1} + θ_2 ε_{t-2} + ... + θ_q ε_{t-q}
  where θ_i are the parameters and μ is the expectation of Y_t.

Combined ARIMA(p, d, q):
  (1 - Σ(φ_i B^i)) (1 - B)^d Y_t = c + (1 + Σ(θ_j B^j)) ε_t
  where B is the backshift operator: B Y_t = Y_{t-1}.

---------------------------------------------------------------------------
2. Big-O Analysis (Computational Complexity)
---------------------------------------------------------------------------
- **Parameter Estimation**:
  Estimating ARIMA parameters typically uses Maximum Likelihood Estimation (MLE) or 
  Conditional Sum of Squares (CSS) optimized via algorithms like L-BFGS or Powell's method.
  - Time Complexity: O(I * (p+q)^2 * N) or worse, where I is the number of iterations,
    (p+q) is the number of parameters, and N is the length of the time series. The use of Kalman 
    filters for exact likelihood computation takes O(N * (p+q)^3).
  - Space Complexity: O(N) for storing the series and residuals. Kalman filter state 
    matrices take O((p+q)^2) space.

- **Forecasting**:
  Once parameters are known, predicting `h` steps ahead:
  - Time Complexity: O(h * (p+q))
  - Space Complexity: O(h) to store predictions.

---------------------------------------------------------------------------
3. Real-World Applications
---------------------------------------------------------------------------
- **Financial Markets**: Forecasting stock prices, exchange rates, and market volatility.
- **Supply Chain**: Demand forecasting to optimize inventory levels.
- **Energy Sector**: Predicting electricity demand or renewable energy production.
- **Meteorology**: Short-term weather forecasting and climate trend analysis.
"""

import math
import random
from typing import List, Tuple, Optional, Union


class ARIMASimulator:
    """
    A class to simulate AR, MA, and ARIMA processes from scratch.
    Useful for generating synthetic data and understanding the mechanics
    of the underlying mathematical equations.
    """

    @staticmethod
    def generate_white_noise(n: int, mean: float = 0.0, std_dev: float = 1.0) -> List[float]:
        """
        Generates Gaussian white noise.

        Time Complexity: O(N)
        Space Complexity: O(N)

        :param n: Number of samples.
        :param mean: Mean of the normal distribution.
        :param std_dev: Standard deviation.
        :return: A list of white noise values.
        """
        return [random.gauss(mean, std_dev) for _ in range(n)]

    @staticmethod
    def simulate_ar(p_params: List[float], n: int, c: float = 0.0) -> List[float]:
        """
        Simulates an Autoregressive AR(p) process.

        Time Complexity: O(N * p)
        Space Complexity: O(N)

        :param p_params: List of phi parameters [φ_1, φ_2, ..., φ_p].
        :param n: Number of time steps to simulate.
        :param c: Constant term.
        :return: A list of simulated AR(p) values.
        """
        p = len(p_params)
        noise = ARIMASimulator.generate_white_noise(n)
        
        # Initialize the series with noise (assuming past values were 0)
        series = [c + noise[i] for i in range(p)]

        for t in range(p, n):
            ar_term = sum(p_params[i] * series[t - 1 - i] for i in range(p))
            val = c + ar_term + noise[t]
            series.append(val)

        return series

    @staticmethod
    def simulate_ma(q_params: List[float], n: int, mu: float = 0.0) -> List[float]:
        """
        Simulates a Moving Average MA(q) process.

        Time Complexity: O(N * q)
        Space Complexity: O(N)

        :param q_params: List of theta parameters [θ_1, θ_2, ..., θ_q].
        :param n: Number of time steps to simulate.
        :param mu: Mean of the series.
        :return: A list of simulated MA(q) values.
        """
        q = len(q_params)
        noise = ARIMASimulator.generate_white_noise(n + q)  # generate extra past noise
        
        series = []
        for t in range(q, n + q):
            ma_term = sum(q_params[i] * noise[t - 1 - i] for i in range(q))
            val = mu + noise[t] + ma_term
            series.append(val)

        return series
    
    @staticmethod
    def integrate_series(series: List[float], d: int) -> List[float]:
        """
        Integrates (undifferences) a time series `d` times.
        For d=1, Y_t = Y_{t-1} + Y'_t

        Time Complexity: O(d * N)
        Space Complexity: O(N)

        :param series: The differenced time series.
        :param d: Order of integration.
        :return: Integrated time series.
        """
        if d == 0:
            return series

        integrated = series.copy()
        for _ in range(d):
            new_series = [integrated[0]]
            for t in range(1, len(integrated)):
                new_series.append(new_series[t-1] + integrated[t])
            integrated = new_series

        return integrated


class SimpleARIMAForecaster:
    """
    A naive ARIMA forecaster that assumes parameters are already known (no MLE fitting).
    This demonstrates how predictions are made given a historical series and (p, d, q) parameters.
    """
    
    def __init__(self, p_params: List[float], d: int, q_params: List[float], c: float = 0.0):
        self.p_params = p_params
        self.d = d
        self.q_params = q_params
        self.c = c
        self.p = len(p_params)
        self.q = len(q_params)
        
    def difference(self, series: List[float]) -> List[float]:
        """
        Differences the series `d` times to make it stationary.
        """
        diffed = series.copy()
        for _ in range(self.d):
            diffed = [diffed[i] - diffed[i-1] for i in range(1, len(diffed))]
        return diffed

    def forecast(self, history: List[float], steps: int) -> List[float]:
        """
        Forecasts `steps` ahead.
        Note: True ARIMA forecasting involves updating residuals (errors).
        Here, for future steps, expected future errors are 0.

        Time Complexity: O(steps * p)
        Space Complexity: O(steps + d)
        """
        # Step 1: Difference the data if d > 0
        working_series = self.difference(history) if self.d > 0 else history.copy()
        
        # Step 2: Forecast the stationary series
        forecast_diff = []
        for step in range(steps):
            # AR component based on past values
            ar_term = 0.0
            for i in range(self.p):
                idx = len(working_series) - 1 - i
                if idx >= 0:
                    ar_term += self.p_params[i] * working_series[idx]
            
            # MA component for future steps is generally 0 because future noise E[e_t] = 0.
            # (If predicting step 1, we might use past residuals, but we simplify here).
            ma_term = 0.0 
            
            next_val = self.c + ar_term + ma_term
            working_series.append(next_val)
            forecast_diff.append(next_val)
            
        # Step 3: Integrate back to original scale if d > 0
        if self.d == 0:
            return forecast_diff
            
        # To integrate forecasts, we need the last values of the series at each differencing level
        # A simpler way is to append forecasts to the original series and take the difference backwards
        # Reconstruct from history + forecast_diff
        reconstructed = history[-1:] # Start with last known value
        
        # Assuming d=1 for simplicity in this reconstruction logic:
        # Y_{t+1} = Y_t + Y'_{t+1}
        # If d > 1, reconstruction is more complex. We'll handle d=1 here.
        if self.d == 1:
            for fd in forecast_diff:
                next_real = reconstructed[-1] + fd
                reconstructed.append(next_real)
            return reconstructed[1:]
        else:
            raise NotImplementedError("Forecasting integration for d > 1 is omitted for brevity.")


# =========================================================================
# Test Cases and Executions
# =========================================================================
def run_tests():
    """
    Validates the mathematical operations of AR, MA, and Integration.
    """
    print("--- Running ARIMA Core Mechanics Tests ---")
    
    # Test 1: Integration (Undifferencing)
    # Series of 1s: [1, 1, 1, 1] integrated 1 time should be [1, 2, 3, 4]
    series_ones = [1.0, 1.0, 1.0, 1.0]
    integrated = ARIMASimulator.integrate_series(series_ones, d=1)
    assert integrated == [1.0, 2.0, 3.0, 4.0], f"Integration failed, got {integrated}"
    print("Integration Test Passed.")

    # Test 2: AR Simulation Size
    n = 100
    ar_sim = ARIMASimulator.simulate_ar(p_params=[0.5], n=n)
    assert len(ar_sim) == n, "AR simulation length mismatch."
    print("AR Simulation Test Passed.")

    # Test 3: MA Simulation Size
    ma_sim = ARIMASimulator.simulate_ma(q_params=[0.4, -0.2], n=n)
    assert len(ma_sim) == n, "MA simulation length mismatch."
    print("MA Simulation Test Passed.")
    
    # Test 4: Simple Forecasting AR(1), d=1
    history = [10.0, 12.0, 15.0, 19.0] # Diff: [2.0, 3.0, 4.0]
    # Let's say AR(1) with phi=1.0 on the differenced data
    forecaster = SimpleARIMAForecaster(p_params=[1.0], d=1, q_params=[])
    # Next diff should be 1.0 * 4.0 = 4.0. Next value = 19.0 + 4.0 = 23.0
    preds = forecaster.forecast(history, steps=1)
    assert abs(preds[0] - 23.0) < 1e-6, f"Forecasting failed, expected 23.0 got {preds[0]}"
    print("ARIMA Simple Forecasting Test Passed.")
    
    print("All internal mechanism tests passed successfully!\n")


def real_world_application():
    """
    Demonstrates a mock real-world application of predicting weekly server load.
    """
    print("--- Real-World Application: Server Load Forecasting ---")
    print("Context: We have past weekly server CPU utilization (differenced data) and we want to predict the next 3 weeks.")
    
    # Historical load trend (simulated as an AR(2) process + some noise)
    # The true parameters are phi1 = 0.6, phi2 = -0.2
    server_load = ARIMASimulator.simulate_ar(p_params=[0.6, -0.2], n=50, c=50.0)
    
    print(f"Latest 5 weeks of historical load: {[round(x, 2) for x in server_load[-5:]]}")
    
    # Instantiate forecaster assuming we already used MLE to find parameters
    forecaster = SimpleARIMAForecaster(p_params=[0.6, -0.2], d=0, q_params=[], c=50.0)
    
    # Forecast next 3 weeks
    predictions = forecaster.forecast(server_load, steps=3)
    
    print(f"Forecast for the next 3 weeks: {[round(x, 2) for x in predictions]}")
    print("Observation: The model uses the autoregressive nature of the server load to gracefully revert to the mean (c=50.0).")
    print("-" * 60 + "\n")


if __name__ == "__main__":
    print("=" * 60)
    print(" " * 15 + "ARIMA MODELING LESSON")
    print("=" * 60)
    
    run_tests()
    real_world_application()
    
    print("Summary:")
    print("1. ARIMA comprises Autoregression (AR), Differencing (I), and Moving Average (MA).")
    print("2. It fundamentally transforms non-stationary data to stationary before applying linear combinations of past values and errors.")
    print("3. Time complexity of fitting real ARIMA models is high due to non-convex optimization required for MA parameters.")
    print("=" * 60)
