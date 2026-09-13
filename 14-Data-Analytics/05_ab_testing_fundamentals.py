"""
05_ab_testing_fundamentals.py

## A. Concept Name
A/B Testing Fundamentals

## B. Concept Explanation
A/B testing is a randomized experimentation process wherein two or more versions of a variable are shown to different segments of users to determine which version leaves the maximum impact and drives business metrics. It fundamentally relies on statistical hypothesis testing.

## C. Why It's Important
It removes guesswork from decision-making, allowing teams to make data-driven decisions that improve key metrics while mitigating risks associated with deploying new changes.

## D. Code Analogy
Imagine testing two sorting algorithms on live data. The Control is your current sort, and Treatment is a new proposed sort. You split the incoming arrays to be sorted between the two. If the Treatment consistently runs faster without errors (and we prove it wasn't just due to random chance), we adopt the Treatment.

## E. Example Output
The script outputs simulated data counts, observed conversion rates, the Z-Statistic and P-Value from a hypothesis test, and a 95% Confidence Interval for the uplift.

## F. Related Concepts
- Hypothesis Testing (Null vs. Alternative)
- Z-tests and P-values
- Statistical Significance and Alpha
- Confidence Intervals

## X. Project Connection
Understanding A/B testing is crucial for evaluating model performance and business decisions in data analytics projects. It bridges the gap between raw data predictions and actionable business intelligence.
"""
import numpy as np
import pandas as pd
import scipy.stats as stats

def run_ab_testing_tutorial():
    print("--- 1. Simulating A/B Test Data ---")
    # Scenario: Testing a new checkout button color (Red vs. Green)
    # Control (A): Old color, Treatment (B): New color
    
    np.random.seed(42)
    sample_size_A = 5000
    sample_size_B = 5000
    
    # True conversion rates (unknown in reality)
    true_conv_A = 0.10  # 10%
    true_conv_B = 0.12  # 12% (The new button is actually better)
    
    # Simulate conversions (1 for conversion, 0 for no conversion)
    conversions_A = np.random.binomial(1, true_conv_A, sample_size_A)
    conversions_B = np.random.binomial(1, true_conv_B, sample_size_B)
    
    df_A = pd.DataFrame({'Group': 'Control', 'Converted': conversions_A})
    df_B = pd.DataFrame({'Group': 'Treatment', 'Converted': conversions_B})
    df = pd.concat([df_A, df_B], ignore_index=True)
    
    print("Simulated Data Overview:")
    print(df.groupby('Group')['Converted'].agg(['count', 'sum', 'mean']))

    print("\n--- 2. Calculating Observed Metrics ---")
    conv_rate_A = df[df['Group'] == 'Control']['Converted'].mean()
    conv_rate_B = df[df['Group'] == 'Treatment']['Converted'].mean()
    
    n_A = df[df['Group'] == 'Control']['Converted'].count()
    n_B = df[df['Group'] == 'Treatment']['Converted'].count()
    
    successes_A = df[df['Group'] == 'Control']['Converted'].sum()
    successes_B = df[df['Group'] == 'Treatment']['Converted'].sum()
    
    print(f"Observed Conversion Rate A (Control): {conv_rate_A:.4f} ({conv_rate_A*100:.2f}%)")
    print(f"Observed Conversion Rate B (Treatment): {conv_rate_B:.4f} ({conv_rate_B*100:.2f}%)")
    print(f"Absolute Uplift: {(conv_rate_B - conv_rate_A)*100:.2f}%")
    print(f"Relative Uplift: {((conv_rate_B - conv_rate_A)/conv_rate_A)*100:.2f}%")

    print("\n--- 3. Hypothesis Testing (Z-Test for Proportions) ---")
    # H0 (Null Hypothesis): Conversion Rate A == Conversion Rate B
    # H1 (Alternative Hypothesis): Conversion Rate A != Conversion Rate B
    
    # Calculate pooled probability
    p_pool = (successes_A + successes_B) / (n_A + n_B)
    
    # Calculate Standard Error
    se_pool = np.sqrt(p_pool * (1 - p_pool) * (1/n_A + 1/n_B))
    
    # Calculate Z-statistic
    z_stat = (conv_rate_B - conv_rate_A) / se_pool
    
    # Calculate p-value (Two-tailed test)
    p_value = stats.norm.sf(abs(z_stat)) * 2
    
    print(f"Z-Statistic: {z_stat:.4f}")
    print(f"P-Value: {p_value:.4e}")

    print("\n--- 4. Interpreting Results ---")
    alpha = 0.05  # Significance level (5%)
    print(f"Significance Level (Alpha): {alpha}")
    
    if p_value < alpha:
        print("Result: REJECT the null hypothesis.")
        print("Conclusion: There is a statistically significant difference between Control and Treatment.")
    else:
        print("Result: FAIL TO REJECT the null hypothesis.")
        print("Conclusion: There is NOT a statistically significant difference between Control and Treatment.")

    print("\n--- 5. Confidence Intervals ---")
    # Calculate 95% CI for the difference in conversion rates
    z_critical = stats.norm.ppf(1 - alpha/2)  # For 95% CI, z is approx 1.96
    
    # Standard error for the difference
    se_diff = np.sqrt( (conv_rate_A * (1-conv_rate_A) / n_A) + (conv_rate_B * (1-conv_rate_B) / n_B) )
    
    diff = conv_rate_B - conv_rate_A
    margin_of_error = z_critical * se_diff
    
    ci_lower = diff - margin_of_error
    ci_upper = diff + margin_of_error
    
    print(f"95% Confidence Interval for the Uplift: [{ci_lower:.4f}, {ci_upper:.4f}]")
    if ci_lower > 0:
        print("The confidence interval does not contain 0, which aligns with our significant p-value.")

if __name__ == "__main__":
    run_ab_testing_tutorial()
