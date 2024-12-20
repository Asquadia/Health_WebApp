import unittest
from unittest.mock import patch
import sys
import os

# Adjust the path to include the project root directory
test_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(test_dir)
sys.path.insert(0, project_dir)

# Import using direct module names since they are in the project root
from backend.app import app as backend_app
from bmi_service.bmi import bmi
from bmr_service.bmr import bmr

class TestBackendAPI(unittest.TestCase):
    def setUp(self):
        """Setup test client before each test."""
        self.backend_app = backend_app.test_client()
        self.backend_app.testing = True

    def print_test_info(self, service, endpoint, input_values, expected_value, returned_value):
        """Prints detailed information about the test."""
        print(f"---------------------------------------")
        print(f"Service: {service}")
        print(f"Endpoint: {endpoint}")
        print(f"Input Values: {input_values}")
        print(f"Expected Value: {expected_value}")
        print(f"Returned Value: {returned_value}")
        if isinstance(expected_value, type) and issubclass(expected_value, BaseException):
            test_result = 'PASSED' if isinstance(returned_value, expected_value) else 'FAILED'
        elif isinstance(expected_value, float) and isinstance(returned_value, float):
            test_result = 'PASSED' if abs(returned_value - expected_value) < 1e-6 else 'FAILED'
        else:
            test_result = 'PASSED' if returned_value == expected_value else 'FAILED'
        print(f"Test Result: {test_result}")
        print(f"---------------------------------------")

    def test_api_calculate_bmi_success(self):
        """Test the /api/bmi endpoint with successful external API call."""
        service = "BMI Service"
        endpoint = "/api/bmi"
        input_values = {'weight': 70, 'height': 1.75}
        expected_value = {'bmi': 22.857142857142858} 
        
        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}')
        returned_value = response.json

        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(returned_value['bmi'], expected_value['bmi'])

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_api_calculate_bmi_missing_params(self):
        """Test the /api/bmi endpoint with missing parameters."""
        service = "BMI Service"
        endpoint = "/api/bmi"
        input_values = {'weight': 70}
        expected_value = {'error': 'Weight and height are required parameters.'}

        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}')
        returned_value = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(returned_value, expected_value)

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_api_calculate_bmr_success(self):
        """Test the /api/bmr endpoint with successful external API call."""
        service = "BMR Service"
        endpoint = "/api/bmr"
        input_values = {'weight': 70, 'height': 175, 'age': 30, 'gender': 'male'}
        expected_value = {'bmr': 1695.667}

        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}&age={input_values["age"]}&gender={input_values["gender"]}')
        returned_value = response.json

        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(returned_value['bmr'], expected_value['bmr'], places=3)

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_bmi_calculation(self):
        """Test the bmi function with valid inputs."""
        service = "BMI Function"
        endpoint = "N/A"
        input_values = {'weight': 70, 'height': 1.75}
        expected_value = 22.857142857142858

        returned_value = bmi(**input_values)

        self.assertAlmostEqual(returned_value, expected_value)

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_bmr_calculation(self):
        """Test the bmr function with valid inputs."""
        service = "BMR Function"
        endpoint = "N/A"
        input_values = {'weight': 70, 'height': 175, 'age': 30, 'gender': 'male'}
        expected_value = 1695.667

        returned_value = bmr(**input_values)

        self.assertAlmostEqual(returned_value, expected_value, places=6)

        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

    def test_bmi_type_check(self):
        """Test the bmi function with invalid input types."""
        service = "BMI Function"
        endpoint = "N/A"
        invalid_inputs = [
            ({'weight': '70', 'height': 1.75}, TypeError),
            ({'weight': 70, 'height': '1.75'}, TypeError),
            ({'weight': None, 'height': 1.75}, TypeError),
            ({'weight': 70, 'height': None}, TypeError),
        ]
        for inputs, expected_exception in invalid_inputs:
            with self.assertRaises(expected_exception) as context:
                bmi(**inputs)
            self.assertIsInstance(context.exception, expected_exception)
            self.print_test_info(service, endpoint, inputs, expected_exception, context.exception)

    def test_bmr_type_check(self):
        """Test the bmr function with invalid input types."""
        service = "BMR Function"
        endpoint = "N/A"
        invalid_inputs = [
            ({'weight': '70', 'height': 175, 'age': 30, 'gender': 'male'}, TypeError),
            ({'weight': 70, 'height': '175', 'age': 30, 'gender': 'male'}, TypeError),
            ({'weight': 70, 'height': 175, 'age': '30', 'gender': 'male'}, TypeError),
            ({'weight': 70, 'height': 175, 'age': 30, 'gender': 123}, TypeError),
            ({'weight': None, 'height': 175, 'age': 30, 'gender': 'male'}, TypeError),
            ({'weight': 70, 'height': None, 'age': 30, 'gender': 'male'}, TypeError),
            ({'weight': 70, 'height': 175, 'age': None, 'gender': 'male'}, TypeError),
            ({'weight': 70, 'height': 175, 'age': 30, 'gender': None}, TypeError),
        ]
        for inputs, expected_exception in invalid_inputs:
            with self.assertRaises(expected_exception) as context:
                bmr(**inputs)
            self.assertIsInstance(context.exception, expected_exception)
            self.print_test_info(service, endpoint, inputs, expected_exception, context.exception)

    def test_bmi_value_check(self):
        """Test the bmi function with invalid input values (negative or zero)."""
        service = "BMI Function"
        endpoint = "N/A"
        invalid_inputs = [
            {'weight': 0, 'height': 1.75},
            {'weight': -70, 'height': 1.75},
            {'weight': 70, 'height': 0},
            {'weight': 70, 'height': -1.75},
        ]
        for inputs in invalid_inputs:
            with self.assertRaises(ValueError) as context:
                bmi(**inputs)
            self.assertIsInstance(context.exception, ValueError)
            self.print_test_info(service, endpoint, inputs, ValueError, context.exception)

    def test_bmr_value_check(self):
        """Test the bmr function with invalid input values (negative or zero)."""
        service = "BMR Function"
        endpoint = "N/A"
        invalid_inputs = [
            {'weight': 0, 'height': 175, 'age': 30, 'gender': 'male'},
            {'weight': -70, 'height': 175, 'age': 30, 'gender': 'male'},
            {'weight': 70, 'height': 0, 'age': 30, 'gender': 'male'},
            {'weight': 70, 'height': -175, 'age': 30, 'gender': 'male'},
            {'weight': 70, 'height': 175, 'age': 0, 'gender': 'male'},
            {'weight': 70, 'height': 175, 'age': -30, 'gender': 'male'},
        ]
        for inputs in invalid_inputs:
            with self.assertRaises(ValueError) as context:
                bmr(**inputs)
            self.assertIsInstance(context.exception, ValueError)
            self.print_test_info(service, endpoint, inputs, ValueError, context.exception)

    def test_bmr_invalid_gender(self):
        """Test the bmr function with an invalid gender."""
        service = "BMR Function"
        endpoint = "N/A"
        input_values = {'weight': 70, 'height': 175, 'age': 30, 'gender': 'other'}
        with self.assertRaises(ValueError) as context:
            bmr(**input_values)
        self.assertEqual(str(context.exception), 'Invalid gender. Please specify "male" or "female".')
        self.print_test_info(service, endpoint, input_values, ValueError, context.exception)

    def test_api_calculate_bmi_invalid_input(self):
        """Test the /api/bmi endpoint with invalid input values."""
        service = "BMI Service"
        endpoint = "/api/bmi"
        invalid_inputs = [
            ({'weight': 0, 'height': 1.75}, {'error': 'Weight must be a positive value.'}),
            ({'weight': -70, 'height': 1.75}, {'error': 'Weight must be a positive value.'}),
            ({'weight': 70, 'height': 0}, {'error': 'Height must be a positive value.'}),
            ({'weight': 70, 'height': -1.75}, {'error': 'Height must be a positive value.'}),
            ({'weight': 'abc', 'height': 1.75}, {'error': 'Weight and height are required parameters.'}),
            ({'weight': 70, 'height': 'abc'}, {'error': 'Weight and height are required parameters.'}),
            ({'weight': None, 'height': 1.75}, {'error': 'Weight and height are required parameters.'}),
            ({'weight': 70, 'height': None}, {'error': 'Weight and height are required parameters.'}),
        ]
        for inputs, expected_error in invalid_inputs:
            response = self.backend_app.get(f'{endpoint}?weight={inputs.get("weight")}&height={inputs.get("height")}')
            returned_value = response.json
            self.assertEqual(response.status_code, 400)
            self.assertEqual(returned_value, expected_error)
            self.print_test_info(service, endpoint, inputs, expected_error, returned_value)

    def test_api_calculate_bmr_invalid_input(self):
        """Test the /api/bmr endpoint with invalid input values."""
        service = "BMR Service"
        endpoint = "/api/bmr"
        invalid_inputs = [
            ({'weight': 0, 'height': 175, 'age': 30, 'gender': 'male'}, {'error': 'Weight must be a positive value.'}),
            ({'weight': -70, 'height': 175, 'age': 30, 'gender': 'male'}, {'error': 'Weight must be a positive value.'}),
            ({'weight': 70, 'height': 0, 'age': 30, 'gender': 'male'}, {'error': 'Height must be a positive value.'}),
            ({'weight': 70, 'height': -175, 'age': 30, 'gender': 'male'}, {'error': 'Height must be a positive value.'}),
            ({'weight': 70, 'height': 175, 'age': 0, 'gender': 'male'}, {'error': 'Age must be a positive value.'}),
            ({'weight': 70, 'height': 175, 'age': -30, 'gender': 'male'}, {'error': 'Age must be a positive value.'}),
            ({'weight': 'abc', 'height': 175, 'age': 30, 'gender': 'male'}, {'error': 'Weight, height, age, and gender are required parameters.'}),
            ({'weight': 70, 'height': 'abc', 'age': 30, 'gender': 'male'}, {'error': 'Weight, height, age, and gender are required parameters.'}),
            ({'weight': 70, 'height': 175, 'age': 'abc', 'gender': 'male'}, {'error': 'Weight, height, age, and gender are required parameters.'}),
            ({'weight': 70, 'height': 175, 'age': 30, 'gender': 123}, {'error': 'Invalid gender. Please specify "male" or "female".'}),
            ({'weight': 70, 'height': 175, 'age': 30, 'gender': 'other'}, {'error': 'Invalid gender. Please specify "male" or "female".'}),
            ({'weight': None, 'height': 175, 'age': 30, 'gender': 'male'}, {'error': 'Weight, height, age, and gender are required parameters.'}),
            ({'weight': 70, 'height': None, 'age': 30, 'gender': 'male'}, {'error': 'Weight, height, age, and gender are required parameters.'}),
            ({'weight': 70, 'height': 175, 'age': None, 'gender': 'male'}, {'error': 'Weight, height, age, and gender are required parameters.'}),
            ({'weight': 70, 'height': 175, 'age': 30, 'gender': None}, {'error': 'Invalid gender. Please specify "male" or "female".'}),
        ]
        for inputs, expected_error in invalid_inputs:
            response = self.backend_app.get(f'{endpoint}?weight={inputs.get("weight")}&height={inputs.get("height")}&age={inputs.get("age")}&gender={inputs.get("gender")}')
            returned_value = response.json
            self.assertEqual(response.status_code, 400)
            self.assertEqual(returned_value, expected_error)
            self.print_test_info(service, endpoint, inputs, expected_error, returned_value)

    def test_api_calculate_bmr_missing_params(self):
        """Test the /api/bmr endpoint with missing parameters."""
        service = "BMR Service"
        endpoint = "/api/bmr"
        input_values = {'weight': 70, 'height': 175}
        expected_value = {'error': 'Weight, height, age, and gender are required parameters.'}

        response = self.backend_app.get(f'{endpoint}?weight={input_values["weight"]}&height={input_values["height"]}')
        returned_value = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(returned_value, {'error': 'Weight, height, age, and gender are required parameters.'})
        self.print_test_info(service, endpoint, input_values, expected_value, returned_value)

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()

    # Add all tests from the TestBackendAPI class to the suite
    suite.addTest(unittest.makeSuite(TestBackendAPI))

    # Create a test runner
    runner = unittest.TextTestRunner()

    # Run the tests and capture the results in a TestResult object
    result = runner.run(suite)

    # Print the summary
    print("\nTest Results Summary:")
    print("---------------------")
    print(f"Ran: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.errors) - len(result.failures)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
