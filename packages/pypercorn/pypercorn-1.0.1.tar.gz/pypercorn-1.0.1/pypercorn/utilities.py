from numpy import ndarray
import msgpack_numpy as m
from numpy import array


class Utilities:
    def decoding_file_image(self, image):
        if type(image) == str:
            path = image
            file = open(path, 'rb')
            files = {"file": file}
        elif type(image) == list or isinstance(image, ndarray):
            array = image
            encoding = m.packb(array)
            files = {"file": ("array.msgpack", encoding)}

        return files

    def numpy_response(self, response, key):
        numpy_array = array(response[key])
        response[key] = numpy_array
        return response
