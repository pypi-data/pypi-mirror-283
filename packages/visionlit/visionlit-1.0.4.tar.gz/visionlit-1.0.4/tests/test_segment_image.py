import unittest
import requests_mock
import os
import sys
from visionlit import Visionlit

class TestVisionlit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the key from the environment variable


        # Create a Visionlit instance to derive and set the Fernet key

        # Get the derived key from the environment variable
        cls.derived_key = os.getenv('FERNET_KEY')
        if not cls.derived_key:
            raise ValueError("Environment variable FERNET_KEY not set")

        cls.validation_url = "https://refworkers.io/functions/getpremium_api.php?api_key="
        cls.visionlit = Visionlit(cls.derived_key)

    @requests_mock.Mocker()
    def test_is_key_valid(self, mock):
        # Mock the API response for a valid key
        mock.get(self.validation_url + self.visionlit.key, json={'valid': True, 'request_nr': '0'})

        # Check if the key is valid
        is_valid = self.visionlit._is_key_valid()

        # Print the result
        if is_valid:
            print(f"The derived: {self.derived_key}) is valid.")
        else:
            print(f"The key {self.key} (derived: {self.derived_key}) is not valid.")

        # Assert that the key is valid
        self.assertTrue(is_valid)

    @requests_mock.Mocker()
    def test_is_key_invalid(self, mock):
        # Mock the API response for an invalid key
        mock.get(self.validation_url + self.visionlit.key, json={'valid': False, 'request_nr': '1'})

        # Check if the key is invalid
        is_valid = self.visionlit._is_key_valid()

        # Print the result
        if is_valid:
            print(f"The key derived: {self.derived_key} is valid.")
        else:
            print(f"The key derived: {self.derived_key} is not valid.")

        # Assert that the key is invalid
        self.assertFalse(is_valid)

    @requests_mock.Mocker()
    def test_segment_image_valid_key(self, mock):
        # Mock the API response for a valid key
        mock.get(self.validation_url + self.visionlit.key, json={'valid': True, 'request_nr': '0'})

        # Call the segment_image method
        result = self.visionlit.segment_image( "dummy_image_path.jpg")

        # Print the result
        print(f"The key derived: {self.derived_key} is valid. Segment image result: {result}")

        # Assert the result
        self.assertEqual(result, "Image segmentation not implemented yet.")

    @requests_mock.Mocker()
    def test_segment_image_invalid_key(self, mock):
        # Mock the API response for an invalid key
        mock.get(self.validation_url + self.visionlit.key, json={'valid': False, 'request_nr': '1'})

        # Call the segment_image method and expect a ValueError
        with self.assertRaises(ValueError) as context:
            self.visionlit.segment_image( "dummy_image_path.jpg")

        # Print the result
        print(f"The key derived: {self.derived_key} is not valid. Error: {str(context.exception)}")

        self.assertTrue("Invalid key. Access denied." in str(context.exception))

if __name__ == '__main__':
    unittest.main(argv=sys.argv[:1])
