import os
import sys
from visionlit import Visionlit


if __name__ == "__main__":
    key = "56daa10355169608ce4b179286ef6860661f6a3820b98"
    vision = Visionlit(key)
    try:
        result = vision.segment_image("test_image.jpg")
        print(result)
    except ValueError as e:
        print(e)


