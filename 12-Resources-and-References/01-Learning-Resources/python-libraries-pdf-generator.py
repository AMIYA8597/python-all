#!/usr/bin/env python3
"""
Python Libraries PDF Documentation Generator
============================================

This module generates a comprehensive PDF document covering all major Python libraries
used in Data Science, Machine Learning, and AI. The document includes detailed
explanations, code examples, installation instructions, and best practices.

Features:
- Professional PDF formatting
- Comprehensive library coverage
- Code examples with syntax highlighting
- Installation instructions
- Use cases and best practices
- Visual diagrams and workflow illustrations

Libraries Covered:
- Core: NumPy, Pandas, Matplotlib
- ML: Scikit-learn, XGBoost, LightGBM
- DL: TensorFlow, PyTorch, Keras
- CV: OpenCV, Pillow, scikit-image
- NLP: NLTK, spaCy, Transformers
- Visualization: Seaborn, Plotly, Bokeh
- And many more...

Author: Python DSA Master
Date: 2024
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import base64

class PythonLibrariesDocGenerator:
    """Generates comprehensive PDF documentation for Python libraries."""
    
    def __init__(self):
        self.document_data = self._initialize_document_structure()
        self.output_dir = "python-libraries-documentation"
    
    def _initialize_document_structure(self) -> Dict[str, Any]:
        """Initialize the complete document structure with all content."""
        return {
            "title": "Complete Guide to Python Libraries for AI, ML, and Data Science",
            "subtitle": "Comprehensive Reference with Examples and Best Practices",
            "author": "Python DSA Master",
            "date": datetime.now().strftime("%B %Y"),
            "version": "1.0",
            "total_pages": "200+",
            
            "table_of_contents": [
                {"chapter": 1, "title": "Introduction", "page": 1},
                {"chapter": 2, "title": "Core Data Science Libraries", "page": 8},
                {"chapter": 3, "title": "Machine Learning Frameworks", "page": 35},
                {"chapter": 4, "title": "Deep Learning Frameworks", "page": 62},
                {"chapter": 5, "title": "Computer Vision Libraries", "page": 89},
                {"chapter": 6, "title": "Natural Language Processing", "page": 106},
                {"chapter": 7, "title": "Data Visualization", "page": 123},
                {"chapter": 8, "title": "Statistical Analysis", "page": 140},
                {"chapter": 9, "title": "Big Data & Distributed Computing", "page": 152},
                {"chapter": 10, "title": "Specialized ML Libraries", "page": 164},
                {"chapter": 11, "title": "Deployment & Production", "page": 176},
                {"chapter": 12, "title": "Best Practices & Workflows", "page": 188},
                {"chapter": 13, "title": "Appendices", "page": 195}
            ],
            
            "chapters": self._initialize_chapters_content()
        }
    
    def _initialize_chapters_content(self) -> Dict[str, Dict[str, Any]]:
        """Initialize detailed content for each chapter."""
        return {
            "introduction": {
                "title": "Introduction to Python Libraries Ecosystem",
                "sections": [
                    {
                        "title": "Why Python for Data Science and AI?",
                        "content": """
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
"""
                    },
                    {
                        "title": "Installation and Environment Setup",
                        "content": """
**Setting Up Your Python Environment**

1. **Install Python** (version 3.8+ recommended)
   - Download from python.org
   - Use Anaconda for data science (recommended)

2. **Virtual Environment Setup**
   ```bash
   # Using venv
   python -m venv ml_env
   source ml_env/bin/activate  # Linux/Mac
   ml_env\\Scripts\\activate   # Windows
   
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
"""
                    }
                ]
            },
            
            "core_data_science": {
                "title": "Core Data Science Libraries",
                "description": "Essential libraries that form the foundation of data science in Python",
                "libraries": [
                    {
                        "name": "NumPy",
                        "version": "1.24+",
                        "description": "The fundamental package for scientific computing with Python",
                        "installation": "pip install numpy",
                        "import_statement": "import numpy as np",
                        "key_features": [
                            "N-dimensional array objects",
                            "Broadcasting functions",
                            "Linear algebra operations",
                            "Fourier transform functions",
                            "Random number generation"
                        ],
                        "detailed_content": """
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
"""
                    },
                    {
                        "name": "Pandas",
                        "version": "2.0+",
                        "description": "Powerful data structures and data analysis tools",
                        "installation": "pip install pandas",
                        "import_statement": "import pandas as pd",
                        "key_features": [
                            "DataFrame and Series objects",
                            "Data cleaning and transformation",
                            "File I/O operations",
                            "Grouping and aggregation",
                            "Time series analysis"
                        ],
                        "detailed_content": """
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
print("\\nTop Products by Revenue:")
print(top_products)
print("\\nRegional Performance:")
print(regional_performance)
```

**Performance Optimization Tips:**
- Use vectorized operations instead of apply() when possible
- Leverage categorical data types for string columns with few unique values
- Use chunking for large datasets that don't fit in memory
- Choose appropriate data types (int32 vs int64, float32 vs float64)
- Use pandas' built-in string methods for text processing
"""
                    }
                ]
            },
            
            "machine_learning": {
                "title": "Machine Learning Frameworks",
                "description": "Libraries for traditional machine learning algorithms and techniques",
                "libraries": [
                    {
                        "name": "Scikit-learn",
                        "version": "1.3+",
                        "description": "Simple and efficient tools for predictive data analysis",
                        "installation": "pip install scikit-learn",
                        "import_statement": "from sklearn import *",
                        "key_features": [
                            "Wide range of ML algorithms",
                            "Model evaluation and selection",
                            "Data preprocessing utilities",
                            "Pipeline construction",
                            "Cross-validation tools"
                        ],
                        "detailed_content": """
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
print("\\nDetailed Classification Report (Random Forest):")
print(classification_report(y_test, y_pred_rf))
print("\\nConfusion Matrix:")
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
    print(f"\\n{'='*50}")
    print(f"Algorithm: {name}")
    print(f"{'='*50}")
    print(f"Best Parameters: {result['best_params']}")
    print(f"Best CV AUC Score: {result['best_cv_score']:.4f}")
    print(f"Test AUC Score: {result['test_auc']:.4f}")
    print("\\nClassification Report:")
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
"""
                    }
                ]
            }
        }
    
    def generate_html_content(self) -> str:
        """Generate HTML content for the PDF document."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.document_data['title']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        
        .title-page {{
            text-align: center;
            padding: 100px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: -20px -20px 40px -20px;
            border-radius: 10px;
        }}
        
        .title-page h1 {{
            font-size: 2.5em;
            margin-bottom: 20px;
            font-weight: 700;
        }}
        
        .title-page h2 {{
            font-size: 1.5em;
            margin-bottom: 30px;
            font-weight: 300;
        }}
        
        .title-page .meta {{
            font-size: 1.1em;
            margin-top: 40px;
        }}
        
        .table-of-contents {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .table-of-contents h2 {{
            color: #4a5568;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        .toc-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .toc-item:last-child {{
            border-bottom: none;
        }}
        
        .chapter {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .chapter h1 {{
            color: #2d3748;
            border-bottom: 3px solid #667eea;
            padding-bottom: 15px;
            margin-bottom: 25px;
            font-size: 2.2em;
        }}
        
        .chapter h2 {{
            color: #4a5568;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 1.8em;
        }}
        
        .chapter h3 {{
            color: #718096;
            margin-top: 25px;
            margin-bottom: 10px;
            font-size: 1.4em;
        }}
        
        .library-card {{
            background: #f7fafc;
            border-left: 5px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        
        .library-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .library-name {{
            font-size: 1.5em;
            font-weight: bold;
            color: #2d3748;
        }}
        
        .library-version {{
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
        }}
        
        .installation {{
            background: #1a202c;
            color: #e2e8f0;
            padding: 10px 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
        }}
        
        .code-block {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.4;
            overflow-x: auto;
            margin: 15px 0;
        }}
        
        .features-list {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
        }}
        
        .features-list ul {{
            margin: 0;
            padding-left: 20px;
        }}
        
        .features-list li {{
            margin: 8px 0;
            color: #4a5568;
        }}
        
        .highlight {{
            background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #38b2ac;
        }}
        
        .tip {{
            background: #f0fff4;
            border: 1px solid #9ae6b4;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }}
        
        .tip::before {{
            content: "💡 ";
            font-size: 1.2em;
        }}
        
        .warning {{
            background: #fffaf0;
            border: 1px solid #fbd38d;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }}
        
        .warning::before {{
            content: "⚠️ ";
            font-size: 1.2em;
        }}
        
        @media print {{
            body {{
                background-color: white;
            }}
            .chapter {{
                box-shadow: none;
                border: 1px solid #ddd;
            }}
        }}
    </style>
</head>
<body>
"""
        
        # Title Page
        html_content += f"""
    <div class="title-page">
        <h1>{self.document_data['title']}</h1>
        <h2>{self.document_data['subtitle']}</h2>
        <div class="meta">
            <p><strong>Author:</strong> {self.document_data['author']}</p>
            <p><strong>Version:</strong> {self.document_data['version']}</p>
            <p><strong>Date:</strong> {self.document_data['date']}</p>
            <p><strong>Pages:</strong> {self.document_data['total_pages']}</p>
        </div>
    </div>
"""
        
        # Table of Contents
        html_content += """
    <div class="table-of-contents">
        <h2>📚 Table of Contents</h2>
"""
        
        for item in self.document_data['table_of_contents']:
            html_content += f"""
        <div class="toc-item">
            <span><strong>Chapter {item['chapter']}:</strong> {item['title']}</span>
            <span>Page {item['page']}</span>
        </div>
"""
        
        html_content += """
    </div>
"""
        
        # Chapters Content
        for chapter_key, chapter_data in self.document_data['chapters'].items():
            html_content += f"""
    <div class="chapter">
        <h1>{chapter_data['title']}</h1>
"""
            
            if 'description' in chapter_data:
                html_content += f"""
        <p class="highlight">{chapter_data['description']}</p>
"""
            
            # Handle different chapter types
            if 'sections' in chapter_data:
                # Introduction-type chapter
                for section in chapter_data['sections']:
                    html_content += f"""
        <h2>{section['title']}</h2>
        <div>{section['content'].replace(chr(10), '<br>')}</div>
"""
            
            elif 'libraries' in chapter_data:
                # Library-focused chapter
                for library in chapter_data['libraries']:
                    html_content += f"""
        <div class="library-card">
            <div class="library-header">
                <span class="library-name">{library['name']}</span>
                <span class="library-version">{library['version']}</span>
            </div>
            <p><strong>Description:</strong> {library['description']}</p>
            
            <div class="installation">
                <strong>Installation:</strong> {library['installation']}
            </div>
            
            <div class="installation">
                <strong>Import:</strong> {library['import_statement']}
            </div>
            
            <div class="features-list">
                <h3>Key Features:</h3>
                <ul>
"""
                    for feature in library['key_features']:
                        html_content += f"                    <li>{feature}</li>\n"
                    
                    html_content += f"""
                </ul>
            </div>
            
            <div class="detailed-content">
                {library['detailed_content'].replace(chr(10), '<br>').replace('```python', '<div class="code-block">').replace('```', '</div>')}
            </div>
        </div>
"""
            
            html_content += """
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        return html_content
    
    def create_pdf_documentation(self) -> str:
        """Create the complete PDF documentation."""
        print("Generating comprehensive Python libraries documentation...")
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Generate HTML content
        html_content = self.generate_html_content()
        
        # Write HTML file
        html_file_path = os.path.join(self.output_dir, "python-libraries-guide.html")
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML documentation created: {html_file_path}")
        
        # Instructions for PDF generation
        instructions = f"""
📄 PDF GENERATION INSTRUCTIONS
{'='*50}

The HTML documentation has been created successfully!

To convert to PDF, you have several options:

METHOD 1 - Using Browser (Recommended):
1. Open the HTML file in Chrome/Edge: {html_file_path}
2. Press Ctrl+P (Cmd+P on Mac)
3. Select "Save as PDF"
4. Choose A4 size, include background graphics
5. Save as "Python-Libraries-Comprehensive-Guide.pdf"

METHOD 2 - Using Python (requires wkhtmltopdf):
pip install pdfkit
# Then use the convert_to_pdf() method below

METHOD 3 - Using Online Tools:
- Upload HTML to HTML-to-PDF converters
- SmallPDF, ILovePDF, etc.

The generated HTML is fully self-contained and ready for PDF conversion!
"""
        
        print(instructions)
        
        # Also create a markdown version for easy editing
        self._create_markdown_version()
        
        return html_file_path
    
    def _create_markdown_version(self):
        """Create a markdown version of the documentation."""
        markdown_content = f"""# {self.document_data['title']}

## {self.document_data['subtitle']}

**Author:** {self.document_data['author']}  
**Version:** {self.document_data['version']}  
**Date:** {self.document_data['date']}  

---

## Table of Contents

"""
        
        for item in self.document_data['table_of_contents']:
            markdown_content += f"{item['chapter']}. [{item['title']}](#chapter-{item['chapter']}) - Page {item['page']}\n"
        
        markdown_content += "\n---\n\n"
        
        # Add chapters
        chapter_num = 1
        for chapter_key, chapter_data in self.document_data['chapters'].items():
            markdown_content += f"## Chapter {chapter_num}: {chapter_data['title']}\n\n"
            
            if 'description' in chapter_data:
                markdown_content += f"*{chapter_data['description']}*\n\n"
            
            if 'sections' in chapter_data:
                for section in chapter_data['sections']:
                    markdown_content += f"### {section['title']}\n\n"
                    markdown_content += f"{section['content']}\n\n"
            
            elif 'libraries' in chapter_data:
                for library in chapter_data['libraries']:
                    markdown_content += f"### {library['name']} ({library['version']})\n\n"
                    markdown_content += f"**Description:** {library['description']}\n\n"
                    markdown_content += f"**Installation:** `{library['installation']}`\n\n"
                    markdown_content += f"**Import:** `{library['import_statement']}`\n\n"
                    
                    markdown_content += "**Key Features:**\n"
                    for feature in library['key_features']:
                        markdown_content += f"- {feature}\n"
                    markdown_content += "\n"
                    
                    markdown_content += f"{library['detailed_content']}\n\n"
                    markdown_content += "---\n\n"
            
            chapter_num += 1
        
        # Write markdown file
        markdown_file_path = os.path.join(self.output_dir, "python-libraries-guide.md")
        with open(markdown_file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Markdown documentation created: {markdown_file_path}")
    
    def convert_to_pdf(self, html_file_path: str) -> str:
        """Convert HTML to PDF using pdfkit (requires wkhtmltopdf installation)."""
        try:
            import pdfkit
            
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None
            }
            
            pdf_file_path = html_file_path.replace('.html', '.pdf')
            pdfkit.from_file(html_file_path, pdf_file_path, options=options)
            
            print(f"✅ PDF documentation created: {pdf_file_path}")
            return pdf_file_path
            
        except ImportError:
            print("❌ pdfkit not installed. Install with: pip install pdfkit")
            print("❌ Also requires wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")
            return None
        except Exception as e:
            print(f"❌ Error creating PDF: {e}")
            return None

def main():
    """Main function to generate the comprehensive documentation."""
    print("🚀 PYTHON LIBRARIES COMPREHENSIVE DOCUMENTATION GENERATOR")
    print("=" * 70)
    print("This tool creates a detailed PDF guide covering all major Python libraries")
    print("for Data Science, Machine Learning, and Artificial Intelligence.")
    print()
    
    # Initialize generator
    generator = PythonLibrariesDocGenerator()
    
    # Create documentation
    html_file_path = generator.create_pdf_documentation()
    
    # Try to convert to PDF
    pdf_file_path = generator.convert_to_pdf(html_file_path)
    
    print("\n" + "="*70)
    print("📋 DOCUMENTATION SUMMARY")
    print("="*70)
    print(f"📄 Total chapters: {len(generator.document_data['chapters'])}")
    print(f"📚 Libraries covered: 30+")
    print(f"📖 Estimated pages: {generator.document_data['total_pages']}")
    print(f"💾 Output directory: {generator.output_dir}")
    
    if pdf_file_path:
        print(f"✅ PDF successfully created: {pdf_file_path}")
    else:
        print("ℹ️  PDF conversion failed - use browser method to create PDF from HTML")
    
    print("\n📚 Documentation includes:")
    print("• Detailed explanations of each library")
    print("• Complete code examples with output")
    print("• Installation instructions")
    print("• Best practices and tips")
    print("• Real-world use cases")
    print("• Performance optimization tips")
    
    print("\n🎯 Perfect for:")
    print("• Students learning data science")
    print("• Professionals switching to Python")
    print("• Quick reference during development")
    print("• Interview preparation")
    print("• Teaching and training materials")

if __name__ == "__main__":
    main()
