import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test_classes import TestMessage

# Add your test classes to this list
test_classes = [TestMessage]

# Load the tests from each test class
test_suite = unittest.TestSuite()
for test_class in test_classes:
    tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
    test_suite.addTests(tests)

# Run the tests
unittest.TextTestRunner(verbosity=2).run(test_suite)