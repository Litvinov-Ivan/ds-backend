import requests
from typing import List


class PlateReaderClient:
    """
    Plate number reader Client Class constructor

    Attributes
    ----------
    host: IP of the client

    Methods
    -------
    __init__(self, host: str):
        host: IP of the client

    read_one_plate_number(self, img_id: int):
        Method for reading the plate number from the input image

        Returns JSON with result of model reading the
        plate number from the image.

        :input: img_id: int
        :return: res.json(): dict

    read_few_plate_number(self, img_id: int):
        Method for reading the plate number from the input images

        Returns JSON with result of model reading the
        plate number from the images.

        :input: img_list: list
        :return: res.json(): dict
    """

    def __init__(self, host: str):
        """
            Method for reading the plate number from the input image

            Returns JSON with result of model reading the
            plate number from the image.
        :param host: int
        :return: res.json(): dict
        """
        self.host = host

    def read_one_plate_number(self, img_id: int) -> dict:
        res = requests.get(
            f'{self.host}/readOneImage',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            params={
                'img_id': img_id,
            },
        )

        return res.json()

    def read_few_plate_numbers(self, img_list: List[int]) -> dict:
        """
            Method for reading the plate number from the input images

            Returns JSON with result of model reading the
            plate number from the images.

        :param img_list: list[int]
        :return: res.json(): dict
        """
        res = requests.get(
            f'{self.host}/readFewImages',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            params={
                f'img_{i[0] + 1}': i[1] for i in enumerate(img_list)
            },
        )

        return res.json()



if __name__ == '__main__':
    client = PlateReaderClient(host='http://127.0.0.1:8080')

    img_id = 10022
    img_list = [10022, 9965, 9966, '10022', '1002a']

    res_1 = client.read_one_plate_number(img_id)
    res_2 = client.read_few_plate_numbers(img_list)
    print(res_1)
    print(res_2)