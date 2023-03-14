import logging
from flask import Flask, request
from models.plate_reader import PlateReader
import logging
import io
import requests


IM_HOST = 'http://51.250.83.169:7878/images'


app = Flask(__name__)
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')


# <url>:8080/readOneImage?img_id=10022
@app.route('/readOneImage')
def read_one_image():
    """
        Handler for reading plate number
        from an image

        :return: res: dict
    """
    if not str(request.args['img_id']).isdecimal():
        return {'error': 'invalid image id'}, 400

    im_url = f"{IM_HOST}/{request.args['img_id']}"
    im = requests.get(im_url, stream=True)

    try:
        im.raise_for_status()
    except requests.exceptions.HTTPError as error:
        if 400 <= error.response.status_code < 500:
            return {'error': 'invalid image'}, 400
        elif error.response.status_code >= 500:
            return {'error': 'server error'}, 500

    im = io.BytesIO(im.content)
    res = plate_reader.read_text(im)

    return {
        'plate_number': res,
    }


# <url>:8080/readFewImages?img_1=10022&img_2=9965
@app.route('/readFewImages')
def read_few_images():
    """
        Few images handler for reading plate numbers
        from a batch of images

        :return: res: dict
    """
    res = {}
    for key, value in request.args.items():
        if str(value).isdecimal():
            im_url = f"{IM_HOST}/{value}"
            im = requests.get(im_url)

            try:
                im.raise_for_status()
            except requests.exceptions.HTTPError as error:
                if 400 <= error.response.status_code < 500:
                    res[f'{key}_plate_number'] = 'invalid image'
                    continue
                elif error.response.status_code >= 500:
                    res[f'{key}_plate_number'] = 'server error'
                    continue

            im = io.BytesIO(im.content)
            url_res = plate_reader.read_text(im)
            res[f'{key}_plate_number'] = url_res
        else:
            res[f'{key}_plate_number'] = 'invalid image id'

    return res


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)