import unittest
from tests.model_manager.test_model_manager import TestModelManager

def suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestModelManager)
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())