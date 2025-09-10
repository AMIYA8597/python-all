# Complete Guide to Python Libraries for AI, ML, and Data Science

## Comprehensive Reference with Examples and Best Practices

**Author:** Python DSA Master  
**Version:** 1.0  
**Date:** September 2025  

---

## Table of Contents

1. [Introduction](#chapter-1) - Page 1
2. [Core Data Science Libraries](#chapter-2) - Page 8
3. [Machine Learning Frameworks](#chapter-3) - Page 35
4. [Deep Learning Frameworks](#chapter-4) - Page 62
5. [Computer Vision Libraries](#chapter-5) - Page 89
6. [Natural Language Processing](#chapter-6) - Page 106
7. [Data Visualization](#chapter-7) - Page 123
8. [Statistical Analysis](#chapter-8) - Page 140
9. [Big Data & Distributed Computing](#chapter-9) - Page 152
10. [Specialized ML Libraries](#chapter-10) - Page 164
11. [Deployment & Production](#chapter-11) - Page 176
12. [Best Practices & Workflows](#chapter-12) - Page 188
13. [Appendices](#chapter-13) - Page 195

---

## Chapter 1: Introduction to Python Libraries Ecosystem

### Why Python for Data Science and AI?


Python has become the de facto language for data science, machine learning, and artificial intelligence due to several key advantages:

• **Simplicity and Readability**: Python's clean syntax makes it easy to learn and use
• **Rich Ecosystem**: Thousands of specialized libraries for every domain
• **Community Support**: Large, active community contributing to open-source projects  
• **Performance**: Optimized libraries built on C/C++ for computational efficiency
• **Versatility**: From data analysis to web development to AI research
• **Industry Adoption**: Used by major tech companies and research institutions

The Python data science stack consists of several layers:
- **Foundation Layer**: NumPy (numerical computing), Pandas (data manipulation)
- **Visualization Layer**: Matplotlib, Seaborn, Plotly (data visualization)
- **Machine Learning Layer**: Scikit-learn, XGBoost (traditional ML)
- **Deep Learning Layer**: TensorFlow, PyTorch (neural networks)
- **Specialized Layer**: OpenCV (computer vision), NLTK/spaCy (NLP)
- **Production Layer**: FastAPI, Streamlit (deployment)


### Installation and Environment Setup


**Setting Up Your Python Environment**

1. **Install Python** (version 3.8+ recommended)
   - Download from python.org
   - Use Anaconda for data science (recommended)

2. **Virtual Environment Setup**
   ```bash
   # Using venv
   python -m venv ml_env
   source ml_env/bin/activate  # Linux/Mac
   ml_env\Scripts\activate   # Windows
   
   # Using conda
   conda create -n ml_env python=3.9
   conda activate ml_env
   ```

3. **Essential Package Installation**
   ```bash
   # Core data science stack
   pip install numpy pandas matplotlib seaborn jupyter
   
   # Machine learning
   pip install scikit-learn xgboost lightgbm
   
   # Deep learning
   pip install tensorflow torch torchvision
   
   # Additional tools
   pip install plotly opencv-python nltk spacy
   ```

4. **Development Environment**
   - **Jupyter Notebook**: Interactive development
   - **JupyterLab**: Advanced notebook interface  
   - **VS Code**: Full IDE with Python extensions
   - **PyCharm**: Professional Python IDE


## Chapter 2: Core Data Science Libraries

*Essential libraries that form the foundation of data science in Python*

### NumPy (1.24+)

**Description:** The fundamental package for scientific computing with Python

**Installation:** `pip install numpy`

**Import:** `import numpy as np`

**Key Features:**
- N-dimensional array objects
- Broadcasting functions
- Linear algebra operations
- Fourier transform functions
- Random number generation


**NumPy: The Foundation of Scientific Computing**

NumPy (Numerical Python) provides the foundation for nearly all data science and machine learning libraries in Python. It introduces the powerful N-dimensional array object (ndarray) and functions to work with these arrays.

**Core Concepts:**

1. **NDArray Object**
   - Homogeneous array of elements (all same data type)
   - More efficient than Python lists for numerical operations
   - Support for broadcasting (operations on arrays of different shapes)

2. **Array Creation**
   ```python
   import numpy as np
   
   # From lists
   arr1d = np.array([1, 2, 3, 4, 5])
   arr2d = np.array([[1, 2, 3], [4, 5, 6]])
   
   # Using built-in functions
   zeros = np.zeros((3, 4))        # 3x4 array of zeros
   ones = np.ones((2, 3))          # 2x3 array of ones
   identity = np.eye(3)            # 3x3 identity matrix
   range_arr = np.arange(0, 10, 2) # [0, 2, 4, 6, 8]
   linspace = np.linspace(0, 1, 5) # 5 points from 0 to 1
   ```

3. **Array Operations**
   ```python
   a = np.array([1, 2, 3, 4])
   b = np.array([5, 6, 7, 8])
   
   # Element-wise operations
   print(a + b)      # [6, 8, 10, 12]
   print(a * b)      # [5, 12, 21, 32]
   print(a ** 2)     # [1, 4, 9, 16]
   
   # Universal functions (ufuncs)
   print(np.sqrt(a))     # Square root
   print(np.exp(a))      # Exponential
   print(np.sin(a))      # Sine
   ```

4. **Linear Algebra**
   ```python
   # Matrix operations
   A = np.array([[1, 2], [3, 4]])
   B = np.array([[5, 6], [7, 8]])
   
   # Matrix multiplication
   C = np.dot(A, B)  # or A @ B
   
   # Eigenvalues and eigenvectors
   eigenvals, eigenvecs = np.linalg.eig(A)
   
   # Matrix inverse
   A_inv = np.linalg.inv(A)
   
   # Singular Value Decomposition
   U, s, Vt = np.linalg.svd(A)
   ```

5. **Statistical Operations**
   ```python
   data = np.random.randn(1000)  # Random normal distribution
   
   # Descriptive statistics
   mean = np.mean(data)
   median = np.median(data)
   std = np.std(data)
   var = np.var(data)
   
   # Along specific axes
   matrix = np.random.randn(5, 3)
   col_means = np.mean(matrix, axis=0)  # Mean of each column
   row_means = np.mean(matrix, axis=1)  # Mean of each row
   ```

**Real-World Example: Image Processing**
```python
import numpy as np
import matplotlib.pyplot as plt

# Create a simple image (2D array)
height, width = 100, 100
image = np.zeros((height, width))

# Add some patterns
for i in range(height):
    for j in range(width):
        image[i, j] = np.sin(i/10) * np.cos(j/10)

# Apply filters
# Gaussian blur (simplified)
kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16
# In real applications, use scipy.ndimage or OpenCV for convolution

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.subplot(1, 2, 2)
plt.imshow(image, cmap='hot')
plt.title('With Different Colormap')
plt.show()
```

**Performance Tips:**
- Use vectorized operations instead of loops
- Leverage broadcasting for operations on different shaped arrays
- Use appropriate data types (float32 vs float64) to save memory
- Utilize NumPy's built-in functions which are optimized in C


---

### Pandas (2.0+)

**Description:** Powerful data structures and data analysis tools

**Installation:** `pip install pandas`

**Import:** `import pandas as pd`

**Key Features:**
- DataFrame and Series objects
- Data cleaning and transformation
- File I/O operations
- Grouping and aggregation
- Time series analysis


**Pandas: Data Manipulation and Analysis**

Pandas is the cornerstone library for data manipulation and analysis in Python. It provides two main data structures: DataFrame (2D) and Series (1D), which are built on top of NumPy arrays but offer much more functionality for data analysis.

**Core Data Structures:**

1. **Series - 1D labeled array**
   ```python
   import pandas as pd
   import numpy as np
   
   # Create Series
   s = pd.Series([1, 3, 5, np.nan, 6, 8])
   print(s)
   
   # Series with custom index
   s2 = pd.Series({'a': 1, 'b': 2, 'c': 3})
   print(s2['a'])  # Access by label
   ```

2. **DataFrame - 2D labeled data structure**
   ```python
   # Create DataFrame from dictionary
   data = {
       'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
       'Age': [25, 30, 35, 28],
       'City': ['New York', 'London', 'Tokyo', 'Paris'],
       'Salary': [50000, 60000, 70000, 55000]
   }
   df = pd.DataFrame(data)
   print(df)
   
   # DataFrame info
   print(df.info())        # Data types and memory usage
   print(df.describe())    # Statistical summary
   print(df.shape)         # Dimensions
   ```

**Data Loading and I/O:**
```python
# Reading data from various sources
df_csv = pd.read_csv('data.csv')
df_excel = pd.read_excel('data.xlsx', sheet_name='Sheet1')
df_json = pd.read_json('data.json')
df_sql = pd.read_sql('SELECT * FROM table', connection)

# Writing data
df.to_csv('output.csv', index=False)
df.to_excel('output.xlsx', index=False)
df.to_json('output.json')
df.to_sql('table_name', connection, if_exists='replace')
```

**Data Selection and Indexing:**
```python
# Column selection
print(df['Name'])           # Single column (Series)
print(df[['Name', 'Age']])  # Multiple columns (DataFrame)

# Row selection
print(df.iloc[0])           # By integer position
print(df.loc[0])            # By label
print(df.iloc[0:3])         # Slice by position
print(df.loc[0:2])          # Slice by label

# Conditional selection
young_employees = df[df['Age'] < 30]
high_earners = df[df['Salary'] > 55000]
complex_filter = df[(df['Age'] > 25) & (df['Salary'] > 50000)]
```

**Data Cleaning and Transformation:**
```python
# Handling missing values
df_with_nan = df.copy()
df_with_nan.loc[1, 'Salary'] = np.nan

# Check for missing values
print(df_with_nan.isnull().sum())

# Fill missing values
df_filled = df_with_nan.fillna({
    'Salary': df_with_nan['Salary'].mean()
})

# Drop rows with missing values
df_cleaned = df_with_nan.dropna()

# Data type conversion
df['Age'] = df['Age'].astype('int32')
df['City'] = df['City'].astype('category')  # Save memory for categorical data

# String operations
df['Name_Upper'] = df['Name'].str.upper()
df['Name_Length'] = df['Name'].str.len()

# Apply custom functions
def salary_category(salary):
    if salary < 55000:
        return 'Low'
    elif salary < 65000:
        return 'Medium'
    else:
        return 'High'

df['Salary_Category'] = df['Salary'].apply(salary_category)
```

**Grouping and Aggregation:**
```python
# Add more data for grouping example
extended_data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
    'Department': ['IT', 'HR', 'IT', 'Finance', 'IT', 'HR'],
    'Age': [25, 30, 35, 28, 32, 45],
    'Salary': [50000, 60000, 70000, 55000, 65000, 80000]
}
df_ext = pd.DataFrame(extended_data)

# Group by department
dept_stats = df_ext.groupby('Department').agg({
    'Age': ['mean', 'min', 'max'],
    'Salary': ['mean', 'sum'],
    'Name': 'count'
}).round(2)
print(dept_stats)

# Multiple grouping
age_salary_stats = df_ext.groupby(['Department'])['Salary'].describe()
```

**Time Series Analysis:**
```python
# Create time series data
dates = pd.date_range('2023-01-01', periods=100, freq='D')
ts_data = pd.DataFrame({
    'Date': dates,
    'Value': np.random.randn(100).cumsum()
})
ts_data.set_index('Date', inplace=True)

# Time-based operations
monthly_avg = ts_data.resample('M').mean()  # Monthly average
weekly_sum = ts_data.resample('W').sum()    # Weekly sum

# Moving averages
ts_data['MA_7'] = ts_data['Value'].rolling(window=7).mean()
ts_data['MA_30'] = ts_data['Value'].rolling(window=30).mean()
```

**Merging and Joining:**
```python
# Create sample datasets
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'city': ['NY', 'LA', 'Chicago', 'Boston']
})

orders = pd.DataFrame({
    'order_id': [101, 102, 103, 104, 105],
    'customer_id': [1, 2, 2, 3, 1],
    'amount': [100, 150, 200, 175, 300]
})

# Different types of joins
inner_join = pd.merge(customers, orders, on='customer_id', how='inner')
left_join = pd.merge(customers, orders, on='customer_id', how='left')
right_join = pd.merge(customers, orders, on='customer_id', how='right')
outer_join = pd.merge(customers, orders, on='customer_id', how='outer')
```

**Real-World Example: Sales Data Analysis**
```python
# Load and analyze sales data
# (In practice, you'd load from CSV/database)
sales_data = pd.DataFrame({
    'Date': pd.date_range('2023-01-01', periods=365, freq='D'),
    'Product': np.random.choice(['A', 'B', 'C'], 365),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 365),
    'Sales': np.random.uniform(100, 1000, 365),
    'Units': np.random.randint(1, 50, 365)
})

# Add derived columns
sales_data['Month'] = sales_data['Date'].dt.month
sales_data['Quarter'] = sales_data['Date'].dt.quarter
sales_data['Revenue_per_Unit'] = sales_data['Sales'] / sales_data['Units']

# Monthly sales analysis
monthly_sales = sales_data.groupby(['Month', 'Product']).agg({
    'Sales': 'sum',
    'Units': 'sum'
}).reset_index()

# Top performing products
top_products = sales_data.groupby('Product')['Sales'].sum().sort_values(ascending=False)

# Regional performance
regional_performance = sales_data.groupby('Region').agg({
    'Sales': ['sum', 'mean'],
    'Units': 'sum'
})

print("Monthly Sales by Product:")
print(monthly_sales.head())
print("\nTop Products by Revenue:")
print(top_products)
print("\nRegional Performance:")
print(regional_performance)
```

**Performance Optimization Tips:**
- Use vectorized operations instead of apply() when possible
- Leverage categorical data types for string columns with few unique values
- Use chunking for large datasets that don't fit in memory
- Choose appropriate data types (int32 vs int64, float32 vs float64)
- Use pandas' built-in string methods for text processing


---

## Chapter 3: Machine Learning Frameworks

*Libraries for traditional machine learning algorithms and techniques*

### Scikit-learn (1.3+)

**Description:** Simple and efficient tools for predictive data analysis

**Installation:** `pip install scikit-learn`

**Import:** `from sklearn import *`

**Key Features:**
- Wide range of ML algorithms
- Model evaluation and selection
- Data preprocessing utilities
- Pipeline construction
- Cross-validation tools


**Scikit-learn: The Complete Machine Learning Toolkit**

Scikit-learn is the most popular machine learning library in Python, providing simple and efficient tools for data mining and data analysis. It's built on NumPy, SciPy, and matplotlib and follows a consistent API design across all algorithms.

**Core Philosophy:**
- **Consistency**: All objects share a common interface
- **Inspection**: Parameter values are accessible as public attributes
- **Limited object hierarchy**: Only algorithms are represented as classes
- **Composition**: Many tasks can be expressed as sequences of more fundamental algorithms
- **Sensible defaults**: Most parameters have default values

**Key Components:**

1. **Estimators**: Objects that fit models to data
2. **Predictors**: Estimators that can make predictions
3. **Transformers**: Estimators that can transform data
4. **Model selection**: Tools for comparing, validating and choosing parameters

**Classification Algorithms:**

```python
from sklearn.datasets import load_iris, make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# Load sample data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. Logistic Regression
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)
y_pred_lr = log_reg.predict(X_test)
print("Logistic Regression Accuracy:", log_reg.score(X_test, y_test))

# 2. Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
print("Random Forest Accuracy:", rf.score(X_test, y_test))

# Feature importance
feature_importance = rf.feature_importances_
print("Feature Importance:", feature_importance)

# 3. Support Vector Machine
svm = SVC(kernel='rbf', C=1.0)
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)
print("SVM Accuracy:", svm.score(X_test, y_test))

# 4. K-Nearest Neighbors
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)
print("KNN Accuracy:", knn.score(X_test, y_test))

# Detailed evaluation
print("\nDetailed Classification Report (Random Forest):")
print(classification_report(y_test, y_pred_rf))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred_rf))
```

**Regression Algorithms:**

```python
from sklearn.datasets import load_boston, make_regression
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

# Generate sample regression data
X, y = make_regression(n_samples=1000, n_features=5, noise=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. Linear Regression
linear_reg = LinearRegression()
linear_reg.fit(X_train, y_train)
y_pred_linear = linear_reg.predict(X_test)
print("Linear Regression R²:", r2_score(y_test, y_pred_linear))
print("Linear Regression RMSE:", np.sqrt(mean_squared_error(y_test, y_pred_linear)))

# 2. Ridge Regression (L2 regularization)
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
y_pred_ridge = ridge.predict(X_test)
print("Ridge Regression R²:", r2_score(y_test, y_pred_ridge))

# 3. Lasso Regression (L1 regularization)
lasso = Lasso(alpha=1.0)
lasso.fit(X_train, y_train)
y_pred_lasso = lasso.predict(X_test)
print("Lasso Regression R²:", r2_score(y_test, y_pred_lasso))
print("Lasso Coefficients:", lasso.coef_)  # Some will be exactly 0

# 4. Random Forest Regression
rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg.fit(X_train, y_train)
y_pred_rf = rf_reg.predict(X_test)
print("Random Forest R²:", r2_score(y_test, y_pred_rf))
```

**Data Preprocessing:**

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif
import pandas as pd

# Sample data with missing values and categorical features
data = pd.DataFrame({
    'age': [25, 30, np.nan, 35, 28],
    'income': [50000, np.nan, 75000, 80000, 60000],
    'education': ['Bachelor', 'Master', 'PhD', 'Bachelor', 'Master'],
    'target': [0, 1, 1, 1, 0]
})

# 1. Handling Missing Values
imputer = SimpleImputer(strategy='mean')
data[['age', 'income']] = imputer.fit_transform(data[['age', 'income']])

# 2. Scaling Numerical Features
scaler = StandardScaler()
data[['age', 'income']] = scaler.fit_transform(data[['age', 'income']])

# 3. Encoding Categorical Features
le = LabelEncoder()
data['education_encoded'] = le.fit_transform(data['education'])

# One-hot encoding (alternative approach)
education_dummies = pd.get_dummies(data['education'], prefix='education')
data = pd.concat([data, education_dummies], axis=1)

print("Preprocessed Data:")
print(data)
```

**Model Selection and Evaluation:**

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Sample data
X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)

# 1. Cross-Validation
rf = RandomForestClassifier(random_state=42)
cv_scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean CV score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

# 2. Grid Search for Hyperparameter Tuning
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, None],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X, y)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best cross-validation score: {grid_search.best_score_:.3f}")

# 3. Pipeline with Preprocessing
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Grid search with pipeline
param_grid_pipeline = {
    'classifier__n_estimators': [50, 100],
    'classifier__max_depth': [5, 10]
}

grid_pipeline = GridSearchCV(pipeline, param_grid_pipeline, cv=5, scoring='accuracy')
grid_pipeline.fit(X, y)

print(f"Best pipeline score: {grid_pipeline.best_score_:.3f}")
```

**Clustering Algorithms:**

```python
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

# Generate sample clustering data
X, y_true = make_blobs(n_samples=300, centers=4, n_features=2, 
                      random_state=42, cluster_std=1.0)

# 1. K-Means Clustering
kmeans = KMeans(n_clusters=4, random_state=42)
y_kmeans = kmeans.fit_predict(X)
print(f"K-Means Silhouette Score: {silhouette_score(X, y_kmeans):.3f}")

# 2. DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
y_dbscan = dbscan.fit_predict(X)
print(f"DBSCAN Silhouette Score: {silhouette_score(X, y_dbscan):.3f}")

# 3. Hierarchical Clustering
hierarchical = AgglomerativeClustering(n_clusters=4)
y_hierarchical = hierarchical.fit_predict(X)
print(f"Hierarchical Silhouette Score: {silhouette_score(X, y_hierarchical):.3f}")

# 4. Gaussian Mixture Model
gmm = GaussianMixture(n_components=4, random_state=42)
y_gmm = gmm.fit_predict(X)
print(f"GMM Silhouette Score: {silhouette_score(X, y_gmm):.3f}")

# Visualize results
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
algorithms = [('K-Means', y_kmeans), ('DBSCAN', y_dbscan), 
              ('Hierarchical', y_hierarchical), ('GMM', y_gmm)]

for i, (name, labels) in enumerate(algorithms):
    row, col = i // 2, i % 2
    axes[row, col].scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
    axes[row, col].set_title(name)

plt.tight_layout()
plt.show()
```

**Dimensionality Reduction:**

```python
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt

# Load sample high-dimensional data
digits = load_digits()
X, y = digits.data, digits.target

print(f"Original data shape: {X.shape}")

# 1. Principal Component Analysis (PCA)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
print(f"PCA explained variance ratio: {pca.explained_variance_ratio_}")
print(f"Total explained variance: {pca.explained_variance_ratio_.sum():.3f}")

# 2. t-SNE
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X)

# 3. Linear Discriminant Analysis (supervised)
lda = LinearDiscriminantAnalysis(n_components=2)
X_lda = lda.fit_transform(X, y)

# Visualize results
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
techniques = [('PCA', X_pca), ('t-SNE', X_tsne), ('LDA', X_lda)]

for i, (name, X_reduced) in enumerate(techniques):
    axes[i].scatter(X_reduced[:, 0], X_reduced[:, 1], c=y, cmap='tab10')
    axes[i].set_title(f'{name} of Digits Dataset')

plt.tight_layout()
plt.show()
```

**Real-World Example: Complete ML Pipeline**

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score
import pandas as pd

# Load breast cancer dataset
data = load_breast_cancer()
X, y = data.data, data.target

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create pipelines for different algorithms
pipelines = {
    'Logistic Regression': Pipeline([
        ('scaler', StandardScaler()),
        ('feature_selection', SelectKBest(f_classif, k=10)),
        ('classifier', LogisticRegression(random_state=42))
    ]),
    
    'Random Forest': Pipeline([
        ('feature_selection', SelectKBest(f_classif, k=15)),
        ('classifier', RandomForestClassifier(random_state=42))
    ]),
    
    'SVM': Pipeline([
        ('scaler', StandardScaler()),
        ('feature_selection', SelectKBest(f_classif, k=10)),
        ('classifier', SVC(probability=True, random_state=42))
    ])
}

# Hyperparameter grids
param_grids = {
    'Logistic Regression': {
        'classifier__C': [0.1, 1, 10],
        'feature_selection__k': [5, 10, 15]
    },
    'Random Forest': {
        'classifier__n_estimators': [50, 100, 200],
        'classifier__max_depth': [5, 10, None],
        'feature_selection__k': [10, 15, 20]
    },
    'SVM': {
        'classifier__C': [0.1, 1, 10],
        'classifier__gamma': ['scale', 'auto'],
        'feature_selection__k': [5, 10, 15]
    }
}

# Evaluate each pipeline
results = {}
for name, pipeline in pipelines.items():
    # Grid search
    grid_search = GridSearchCV(pipeline, param_grids[name], 
                              cv=5, scoring='roc_auc', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    # Best model evaluation
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    
    results[name] = {
        'best_params': grid_search.best_params_,
        'best_cv_score': grid_search.best_score_,
        'test_auc': roc_auc_score(y_test, y_pred_proba),
        'classification_report': classification_report(y_test, y_pred)
    }

# Display results
for name, result in results.items():
    print(f"\n{'='*50}")
    print(f"Algorithm: {name}")
    print(f"{'='*50}")
    print(f"Best Parameters: {result['best_params']}")
    print(f"Best CV AUC Score: {result['best_cv_score']:.4f}")
    print(f"Test AUC Score: {result['test_auc']:.4f}")
    print("\nClassification Report:")
    print(result['classification_report'])
```

**Best Practices:**

1. **Always use train/validation/test splits** or cross-validation
2. **Preprocess data consistently** between training and testing
3. **Use pipelines** to prevent data leakage
4. **Start with simple models** before trying complex ones
5. **Tune hyperparameters systematically** using grid search or random search
6. **Evaluate with appropriate metrics** for your problem type
7. **Consider feature scaling** for distance-based algorithms
8. **Handle imbalanced data** with appropriate techniques
9. **Document your preprocessing steps** for reproducibility
10. **Validate your model** on truly unseen data


---

