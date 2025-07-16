import unittest
import os
import sys
import fnmatch

def discover_and_run_tests():
    base_dir = os.path.dirname(__file__)
    sys.path.insert(0, base_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(base_dir, '..')))
    test_files = []
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if fnmatch.fnmatch(filename, '*test*.py'):
                test_files.append(os.path.join(root, filename))

    suite = unittest.TestSuite()
    for test_file in test_files:
        rel_path = os.path.relpath(test_file, base_dir)
        module_name = rel_path.replace(os.sep, '.')[:-3]  # strip .py
        try:
            module = __import__(module_name, fromlist=[''])
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
                    tests = unittest.defaultTestLoader.loadTestsFromTestCase(obj)
                    suite.addTests(tests)
        except Exception as e:
            print(f"[SKIP] {module_name}: {e}")
            continue

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result

if __name__ == '__main__':
    discover_and_run_tests()
