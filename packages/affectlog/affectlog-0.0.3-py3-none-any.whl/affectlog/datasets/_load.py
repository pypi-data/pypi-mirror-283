import os
import pandas as pd

def load_data_scientist_jobs():
    """Load the preprocessed 'Data Scientist Jobs' dataset

    Returns
    -----------
    pd.DataFrame
    """
    abs_dir_path = os.path.dirname(os.path.abspath(__file__))
    abs_datasets_path = os.path.join(abs_dir_path, 'data', 'DataScientist.csv')

    dataset = pd.read_csv(abs_datasets_path)

    return dataset

def load_online_courses():
    """Load the preprocessed 'Online Courses' dataset

    Returns
    -----------
    pd.DataFrame
    """
    abs_dir_path = os.path.dirname(os.path.abspath(__file__))
    abs_datasets_path = os.path.join(abs_dir_path, 'data', 'Online_Courses.csv')

    dataset = pd.read_csv(abs_datasets_path)

    return dataset

def load_hr_analytics():
    """Load the preprocessed 'HR Analytics' dataset

    Returns
    -----------
    pd.DataFrame
    """
    abs_dir_path = os.path.dirname(os.path.abspath(__file__))
    abs_datasets_path = os.path.join(abs_dir_path, 'data', 'HR-Employee-Attrition.csv')

    dataset = pd.read_csv(abs_datasets_path)

    return dataset

def load_ds_salaries():
    """Load the preprocessed 'Data Science Job Salaries' dataset

    Returns
    -----------
    pd.DataFrame
    """
    abs_dir_path = os.path.dirname(os.path.abspath(__file__))
    abs_datasets_path = os.path.join(abs_dir_path, 'data', 'ds_salaries.csv')

    dataset = pd.read_csv(abs_datasets_path)

    return dataset

def load_salary_prediction():
    """Load the preprocessed 'Salary Prediction for Beginners' dataset

    Returns
    -----------
    pd.DataFrame
    """
    abs_dir_path = os.path.dirname(os.path.abspath(__file__))
    abs_datasets_path = os.path.join(abs_dir_path, 'data', 'Salary-Data.csv')

    dataset = pd.read_csv(abs_datasets_path)

    return dataset
