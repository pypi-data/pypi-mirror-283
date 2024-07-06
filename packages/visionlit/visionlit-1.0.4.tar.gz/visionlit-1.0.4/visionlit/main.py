import os
import requests

class Visionlit:

    def __init__(self, key: str):
        self.key = key
        self.validation_url = "https://refworkers.io/functions/getpremium_api.php?api_key="


    def _is_key_valid(self):
        try:
            key = self.validation_url + self.key
            response = requests.get(key)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            data = response.json()  # This will raise a ValueError if the response is not JSON
            reqs = int(data.get('request_nr', 0))
            if reqs < 1:
                return data.get('valid', False)
            else:
                return data.get('valid', True)
        except (requests.RequestException, ValueError) as e:
            return False

    def segment_image(self,  image_path: str):
        """
        Segment an image using the provided model.
        """
        if not self._is_key_valid():
            raise ValueError("Invalid key. Access denied.")
        # Placeholder for image segmentation logic
        return "Image segmentation not implemented yet."

