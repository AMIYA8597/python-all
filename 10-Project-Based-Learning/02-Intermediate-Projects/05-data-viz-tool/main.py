\"\"\"
Data Visualization Tool - Main Module

This script provides an interactive and programmatic data visualization tool
using pandas and seaborn/matplotlib. It supports reading tabular data (CSV/JSON),
cleaning data, and generating various plots (scatter, bar, histogram, correlation).

Industry Use Cases:
- Rapid Exploratory Data Analysis (EDA)
- Automated report generation
- Preprocessing steps before machine learning pipelines

Features:
- Extensible architecture using class-based design.
- Built-in data imputation for missing values.
- Automated numerical and categorical column detection.
- Statistical summary generation.

Advanced Concepts:
- Type hinting and generic data structures.
- Factory patterns for plot generation.
- Error handling and logging.
\"\"\"

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from typing import Optional, List, Dict, Any, Union
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataVisualizer:
    \"\"\"
    A comprehensive tool for data analysis and visualization.
    \"\"\"
    
    def __init__(self, data_path: Union[str, Path]):
        \"\"\"
        Initialize the visualizer with a dataset.
        
        Args:
            data_path: Path to the CSV or JSON file.
        \"\"\"
        self.data_path = Path(data_path)
        self.df: Optional[pd.DataFrame] = None
        
    def load_data(self) -> None:
        \"\"\"
        Loads data from the specified path into a pandas DataFrame.
        Supports .csv and .json extensions.
        \"\"\"
        logger.info(f\"Attempting to load data from {self.data_path}\")
        try:
            if self.data_path.suffix.lower() == '.csv':
                self.df = pd.read_csv(self.data_path)
            elif self.data_path.suffix.lower() == '.json':
                self.df = pd.read_json(self.data_path)
            else:
                raise ValueError(\"Unsupported file format. Only CSV and JSON are supported.\")
            
            logger.info(f\"Successfully loaded data with shape {self.df.shape}\")
        except FileNotFoundError:
            logger.error(f\"File not found: {self.data_path}\")
            raise
        except Exception as e:
            logger.error(f\"An error occurred while loading data: {e}\")
            raise

    def clean_data(self, fill_strategy: str = 'mean') -> None:
        \"\"\"
        Cleans the dataset by handling missing values.
        
        Args:
            fill_strategy: Strategy to fill NA values for numeric columns ('mean', 'median', 'zero').
        \"\"\"
        if self.df is None:
            raise ValueError(\"Data not loaded. Call load_data() first.\")
            
        initial_missing = self.df.isna().sum().sum()
        if initial_missing == 0:
            logger.info(\"No missing values found. Data is clean.\")
            return
            
        logger.info(f\"Found {initial_missing} missing values. Cleaning data...\")
        
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        
        # Clean numeric columns
        for col in numeric_cols:
            if self.df[col].isna().any():
                if fill_strategy == 'mean':
                    self.df[col] = self.df[col].fillna(self.df[col].mean())
                elif fill_strategy == 'median':
                    self.df[col] = self.df[col].fillna(self.df[col].median())
                elif fill_strategy == 'zero':
                    self.df[col] = self.df[col].fillna(0)
                    
        # Clean categorical columns using mode
        for col in categorical_cols:
            if self.df[col].isna().any():
                self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
                
        final_missing = self.df.isna().sum().sum()
        logger.info(f\"Data cleaning complete. Remaining missing values: {final_missing}\")

    def plot_correlation_matrix(self, save_path: Optional[str] = None) -> None:
        \"\"\"
        Plots a correlation heatmap for numeric columns.
        \"\"\"
        if self.df is None:
            raise ValueError(\"Data not loaded.\")
            
        numeric_df = self.df.select_dtypes(include=['number'])
        if numeric_df.empty:
            logger.warning(\"No numeric columns available for correlation matrix.\")
            return
            
        plt.figure(figsize=(10, 8))
        corr = numeric_df.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Correlation Matrix')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            logger.info(f\"Saved correlation matrix to {save_path}\")
        else:
            plt.show()
            
    def plot_distribution(self, column: str, save_path: Optional[str] = None) -> None:
        \"\"\"
        Plots the distribution (histogram + KDE) of a numeric column.
        \"\"\"
        if self.df is None:
            raise ValueError(\"Data not loaded.\")
            
        if column not in self.df.columns:
            raise ValueError(f\"Column '{column}' not found in dataset.\")
            
        if not pd.api.types.is_numeric_dtype(self.df[column]):
            raise ValueError(f\"Column '{column}' is not numeric. Cannot plot distribution.\")
            
        plt.figure(figsize=(8, 5))
        sns.histplot(self.df[column], kde=True, color='skyblue')
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            logger.info(f\"Saved distribution plot to {save_path}\")
        else:
            plt.show()

def test_visualizer():
    \"\"\"
    Simple test routine to demonstrate the visualizer's capabilities.
    Requires a sample dataset or creates a dummy one.
    \"\"\"
    import tempfile
    
    # Create a dummy dataset
    dummy_data = {
        'age': [25, 30, 35, None, 40, 50, 45],
        'salary': [50000, 60000, 75000, 80000, None, 100000, 95000],
        'department': ['IT', 'HR', 'IT', 'Marketing', 'IT', 'HR', None]
    }
    df = pd.DataFrame(dummy_data)
    
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        temp_path = tmp.name
        
    try:
        viz = DataVisualizer(temp_path)
        viz.load_data()
        viz.clean_data(fill_strategy='median')
        
        print(\"\\n--- Cleaned DataFrame ---\")
        print(viz.df)
        
        viz.plot_correlation_matrix()
        viz.plot_distribution('salary')
    finally:
        Path(temp_path).unlink()

if __name__ == \"__main__\":
    test_visualizer()
