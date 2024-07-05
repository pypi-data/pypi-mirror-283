import requests
import json
from pypercorn.utilities import Utilities


class Satellite:
    def __init__(self):
        self.ip_server = "https://hypercornapi-1.azurewebsites.net"
        self.utilities = Utilities()

    def ndvi(self, x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4, date):
        response = json.loads(requests.get(
            f"{self.ip_server}/algorithms/images/satellite/ndvi/", params={"x_1": x_1, "y_1": y_1, "x_2": x_2, "y_2": y_2, "x_3": x_3, "y_3": y_3, "x_4": x_4, "y_4": y_4, "date": date}).content)
        if "image" in response.keys():
            response = self.utilities.numpy_response(response, "image")
        return response

    def visible(self, x_1, y_1, x_2, y_2,  x_3, y_3, x_4, y_4, date):
        response = json.loads(requests.get(
            f"{self.ip_server}/algorithms/images/satellite/visible/", params={"x_1": x_1, "y_1": y_1, "x_2": x_2, "y_2": y_2, "x_3": x_3, "y_3": y_3, "x_4": x_4, "y_4": y_4, "date": date}).content)
        if "image" in response.keys():
            response = self.utilities.numpy_response(response, "image")
        return response
