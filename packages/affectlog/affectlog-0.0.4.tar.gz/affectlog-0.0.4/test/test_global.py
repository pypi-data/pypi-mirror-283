import unittest
from affectlog._global_checks import global_check_import


class Global(unittest.TestCase):
    
    def setUp(self):
        pass

    def test(self):
        # Test to ensure ImportError is raised for non-existent package
        with self.assertRaises(ImportError):
            global_check_import("error_package", "error")
        
        # Test to ensure ImportWarning is raised for specific warning condition
        with self.assertRaises(ImportWarning):
            global_check_import("affectlog", "warning")
        
        # Test to check the successful import of existing packages
        global_check_import("shap", "test")
        global_check_import("statsmodels")
        global_check_import("scikit-learn")
        global_check_import("lime")
        
        # Test to ensure an invalid import check raises a BaseException
        with self.assertRaises(BaseException):
            global_check_import("sklearn", "this won't work")


if __name__ == '__main__':
    unittest.main()
