import os
import pandas as pd

def load_DataScientist():
    """Load the preprocessed 'DataScientist' dataset

    Source: https://www.kaggle.com/datasets/andrewmvd/data-scientist-jobs
    
    License: see file ./data/LICENSE-DATA.txt
    
    Returns
    -----------
    pd.DataFrame
    """
    abs_dir_path = os.path.dirname(os.path.abspath(__file__))
    abs_datasets_path = os.path.join(abs_dir_path, 'data', 'DataScientist.csv')
    dataset = pd.read_csv(abs_datasets_path)
    return dataset

def load_ds_salaries():
    """Load the preprocessed 'ds_salaries' dataset

    Source: https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries
    
    License: see file ./data/LICENSE-DATA.txt
    
    Returns
    -----------
    pd.DataFrame
    """
    abs_dir_path = os.path.dirname(os.path.abspath(__file__))
    abs_datasets_path = os.path.join(abs_dir_path, 'data', 'ds_salaries.csv')
    dataset = pd.read_csv(abs_datasets_path)
    return dataset

def load_HR_Employee_Attrition():
    """Load the preprocessed 'HR-Employee-Attrition' dataset

    Source: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
    
    License: see file ./data/LICENSE-DATA.txt
    
    Returns
    -----------
    pd.DataFrame
    """
    abs_dir_path = os.path.dirname(os.path.abspath(__file__))
    abs_datasets_path = os.path.join(abs_dir_path, 'data', 'HR-Employee-Attrition.csv')
    dataset = pd.read_csv(abs_datasets_path)
    return dataset

def load_Online_Courses():
    """Load the preprocessed 'Online_Courses' dataset

    Source: https://www.kaggle.com/datasets/khaledatef1/online-courses
    
    License: see file ./data/LICENSE-DATA.txt
    
    Returns
    -----------
    pd.DataFrame
    """
    abs_dir_path = os.path.dirname(os.path.abspath(__file__))
    abs_datasets_path = os.path.join(abs_dir_path, 'data', 'Online_Courses.csv')
    dataset = pd.read_csv(abs_datasets_path)
    return dataset

def load_Salary_Data():
    """Load the preprocessed 'Salary-Data' dataset

    Source: https://www.kaggle.com/datasets/rkiattisak/salaly-prediction-for-beginer
    
    License: see file ./data/LICENSE-DATA.txt
    
    Returns
    -----------
    pd.DataFrame
    """
    abs_dir_path = os.path.dirname(os.path.abspath(__file__))
    abs_datasets_path = os.path.join(abs_dir_path, 'data', 'Salary-Data.csv')
    dataset = pd.read_csv(abs_datasets_path)
    return dataset
