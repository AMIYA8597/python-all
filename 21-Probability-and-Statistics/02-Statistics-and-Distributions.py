"""
# 02 - Statistics: Distributions, Z-Scores, and Hypothesis Testing

## A. Concept Name
Descriptive Statistics, The Normal Distribution, Z-Scores, and A/B Testing (Hypothesis Testing).

## B. One-Sentence Definition
Statistics provides the tools to summarize massive datasets (Mean, Variance) and mathematically prove whether an observed improvement in an AI model's performance is real or just random luck (Hypothesis Testing).

## C. Why Does This Exist?
In ML, you constantly make changes. You change the architecture, and accuracy goes from 90.1% to 90.4%. 
Is your new model actually better? Or did it just get lucky on the test set?
Statistics provides the **p-value**, the ultimate metric for separating signal from noise.
Additionally, many ML algorithms (like Linear Regression and Gaussian Naive Bayes) fundamentally assume that the underlying data follows a Normal (Gaussian) Distribution.

## D. Intuition & Real-World Analogy
Imagine you are testing a new website layout to see if it increases sales (A/B Testing).
Group A (old layout) has an average order value of $50.
Group B (new layout) has an average order value of $52.
Did the layout work?
If only 5 people visited the site, $52 means nothing. It's just random noise.
If 5,000,000 people visited the site, $52 is a massive, definitive victory.
Statistics formalizes this intuition using Variance and Sample Size.

## E. Core Mathematical Concepts

### 1. Mean and Variance
- **Mean (mu)**: The center of the data.
- **Variance (sigma^2)**: How spread out the data is. High variance means the data is unpredictable and noisy.
- **Standard Deviation (sigma)**: The square root of variance. It's in the same units as the original data.

### 2. The Normal Distribution (Bell Curve)
The most important shape in statistics. Due to the Central Limit Theorem, almost everything in nature (height, test scores, measurement errors) forms a bell curve.
- 68% of data falls within 1 standard deviation of the mean.
- 95% falls within 2 standard deviations.
- 99.7% falls within 3 standard deviations.

### 3. Z-Scores (Standardization)
A Z-score tells you exactly how many standard deviations a data point is from the mean.
Formula: `Z = (X - Mean) / Standard_Deviation`
In AI: We use this exact formula to "Standardize" our data before feeding it into a neural network (e.g., `StandardScaler` in scikit-learn).

### 4. Hypothesis Testing & p-values
- **Null Hypothesis (H0)**: "Your new ML model is NOT better. Any difference is just luck."
- **Alternative Hypothesis (H1)**: "Your new ML model IS better."
- **p-value**: The probability of seeing a 90.4% accuracy IF the Null Hypothesis were true. If the p-value is tiny (e.g., < 0.05), we reject the Null Hypothesis and declare victory.

## F. Common Mistakes & Anti-Patterns
1. **p-hacking**: Running 50 different A/B tests, finding one that randomly gets a p-value < 0.05, and publishing it as a breakthrough. At 0.05 (5%), 1 in 20 tests will pass purely by chance!
2. **Assuming Normality**: Using statistical tests that assume a bell curve on data that is heavily skewed (like income distribution). Always visualize your data first!

## G. Interview Connection
**Q: "Why do we scale/standardize data before training a Neural Network?"**
A: "Features often have drastically different scales (e.g., Age 0-100 vs Income 0-1,000,000). If we don't scale, the gradients for Income will explode, and the model will ignore Age. By converting everything to Z-scores (Mean=0, Std=1), we put all features on a level playing field, creating a smooth, spherical loss landscape that Gradient Descent can traverse easily."

## H. Implementation & Guided Practice
"""

import math
import random

# ==========================================
# 1. Descriptive Statistics (From Scratch)
# ==========================================
def calculate_statistics(data):
    print("--- 1. Descriptive Statistics ---")
    
    n = len(data)
    mean = sum(data) / n
    
    # Variance = sum((x - mean)^2) / n
    variance = sum((x - mean)**2 for x in data) / n
    
    # Standard Deviation
    std_dev = math.sqrt(variance)
    
    print(f"Data: {data[:5]}... (Total {n} items)")
    print(f"Mean: {mean:.2f}")
    print(f"Variance: {variance:.2f}")
    print(f"Standard Deviation: {std_dev:.2f}")
    
    return mean, std_dev


# ==========================================
# 2. Z-Scores (Data Standardization)
# ==========================================
def demonstrate_z_scores(data, mean, std_dev):
    print("\n--- 2. Z-Scores (StandardScaler) ---")
    
    # We want to know how "extreme" the first data point is.
    val = data[0]
    z_score = (val - mean) / std_dev
    
    print(f"Value: {val}")
    print(f"Z-Score: {z_score:.2f}")
    
    if abs(z_score) > 3:
        print("This is an OUTLIER! (> 3 standard deviations away)")
    elif abs(z_score) > 2:
        print("This is highly unusual. (> 2 std dev)")
    else:
        print("This is completely normal. (< 2 std dev)")
        
    # Standardize the whole array
    standardized_data = [(x - mean) / std_dev for x in data]
    
    print(f"\nOriginal Data:     {data[:4]}")
    print(f"Standardized Data: {[round(x, 2) for x in standardized_data[:4]]}")
    print("Notice the standardized data now centers around 0.0!")


# ==========================================
# 3. Hypothesis Testing (A/B Testing simulation)
# ==========================================
def simulate_ab_test():
    """
    Simulates a Z-test to compare two ML models.
    """
    print("\n--- 3. A/B Testing (Z-Test) ---")
    
    # Model A (Baseline)
    n_a = 1000        # Test set size
    acc_a = 0.85      # 85% accuracy
    
    # Model B (New Model)
    n_b = 1000        # Test set size
    acc_b = 0.88      # 88% accuracy
    
    print(f"Model A Accuracy: {acc_a * 100}% on {n_a} samples.")
    print(f"Model B Accuracy: {acc_b * 100}% on {n_b} samples.")
    
    # Calculate Pooled Proportion
    p_pool = ((acc_a * n_a) + (acc_b * n_b)) / (n_a + n_b)
    
    # Standard Error
    se = math.sqrt(p_pool * (1 - p_pool) * ((1/n_a) + (1/n_b)))
    
    # Z-statistic
    z = (acc_b - acc_a) / se
    
    print(f"\nZ-Statistic: {z:.2f}")
    
    # A Z-score of 1.96 corresponds to a p-value of 0.05 (95% confidence)
    if z > 1.96:
        print("Result: STATISTICALLY SIGNIFICANT! (p < 0.05)")
        print("Conclusion: Model B is genuinely better. Deploy to production!")
    else:
        print("Result: NOT statistically significant.")
        print("Conclusion: Model B just got lucky. Do not deploy.")


## I. Active Recall Questions
"""
1. What does it mean if a data point has a Z-score of 0?
   *Answer: It means the data point is exactly equal to the mean of the dataset.*
2. Why is the Normal Distribution so ubiquitous in AI and nature?
   *Answer: Because of the Central Limit Theorem. When you add together many independent random variables (like the thousands of genetic factors that determine height, or thousands of random errors), their normalized sum tends toward a normal distribution.*
3. What is a p-value?
   *Answer: The probability of obtaining test results at least as extreme as the results actually observed, under the assumption that the null hypothesis is correct. A low p-value (< 0.05) means the null hypothesis is highly unlikely.*
"""

if __name__ == "__main__":
    print("========== STATISTICS & DISTRIBUTIONS MASTERCLASS ==========\n")
    
    # Generate some fake data (e.g., lengths of user sessions on a website in seconds)
    # Mean = 300, StdDev = 50
    fake_data = [random.gauss(300, 50) for _ in range(1000)]
    
    # Let's inject one crazy outlier!
    fake_data.insert(0, 800.0) 
    
    mean, std_dev = calculate_statistics(fake_data)
    demonstrate_z_scores(fake_data, mean, std_dev)
    simulate_ab_test()
    print("\n========== MASTERCLASS COMPLETE ==========")
