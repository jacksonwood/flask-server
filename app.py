from flask import Flask, jsonify, Response, url_for, redirect, request
import os
import openai
import requests
import time
from flask_cors import CORS, cross_origin
from io import BytesIO
from PIL import Image


openai_key = os.environ.get("OPENAI_KEY")

printful_key = os.environ.get("PRINTFUL_KEY")


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/load_ai/<input_value>": {"origins": "*"}})
headers = {
    'Authorization': 'Bearer ' + printful_key,
    'Content-Type': 'application/json'
}


@ app.route("/load_ai/<input_value>", methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def load_ai(input_value):
    # Create a session
    session = requests.Session()
    # Set the headers for the session

    session.headers.update(headers)

    openai.api_key = openai_key
    try:
        response = openai.Image.create(
            prompt=input_value,
            n=1,
            size="256x256"
        )
    except openai.error.InvalidRequestError as e:
        return jsonify({"error": str(e)}), 400

    image_url = response['data'][0]['url']

    # image_url = 'https://gateway.pinata.cloud/ipfs/QmeXSVnT8BGyxA39zERiEijFwEfgsbFmEUDKRc49pBX3Uo?_gl=1*pkq9dw*_ga*MjE0MjEyNjU3NC4xNjc1MDE0NTg2*_ga_5RMPXG14TE*MTY3NTk0ODcyNC45LjAuMTY3NTk0ODcyNi41OC4wLjA.'

    chest_logo = "https://gateway.pinata.cloud/ipfs/QmXKu3kbkksCJsHaoJ2N5KUsRF3HFWuvacZTP7arhD3rVS?_gl=1*oadv6z*_ga*MjE0MjEyNjU3NC4xNjc1MDE0NTg2*_ga_5RMPXG14TE*MTY3NTYzMTAyOC43LjAuMTY3NTYzMTAyOC42MC4wLjA.&__cf_chl_tk=seoLwhAI3lVqOMpaODAvbQo6Ct_mfWGsiaO52TMpjPU-1675631030-0-gaNycGzNDdE"

    # Make a POST request to another API
    external_api_url = 'https://api.printful.com/store/products'

    data = {
        "sync_product": {
            "name": input_value
        },
        "sync_variants": [
            {
                "variant_id": 11576,
                "retail_price": 39.99,
                "files": [
                    {
                        "type": "back",
                        "url": image_url,
                        "position": {
                            "area_width": 1800,
                            "area_height": 2400,
                            "width": 1800,
                            "height": 1800,
                            "top": 600,
                            "left": 0
                        }
                    },
                    {
                        "type": "embroidery_chest_left",
                        "url": chest_logo,
                        "options": [
                            {
                                "id": "auto_thread_color",
                                "value": True
                            }
                        ]
                    }
                ]
            },
            {
                "variant_id": 11577,
                "retail_price": 39.99,
                "files": [
                    {
                        "type": "back",
                        "url": image_url,
                        "position": {
                            "area_width": 1800,
                            "area_height": 2400,
                            "width": 1800,
                            "height": 1800,
                            "top": 600,
                            "left": 0
                        }
                    },
                    {
                        "type": "embroidery_chest_left",
                        "url": chest_logo,
                        "options": [
                            {
                                "id": "auto_thread_color",
                                "value": True
                            }
                        ]
                    }
                ]
            },
            {
                "variant_id": 11578,
                "retail_price": 39.99,
                "files": [
                    {
                        "type": "back",
                        "url": image_url,
                        "position": {
                            "area_width": 1800,
                            "area_height": 2400,
                            "width": 1800,
                            "height": 1800,
                            "top": 600,
                            "left": 0
                        }
                    },
                    {
                        "type": "embroidery_chest_left",
                        "url": chest_logo,
                        "options": [
                            {
                                "id": "auto_thread_color",
                                "value": True
                            }
                        ]
                    }
                ]
            },
            {
                "variant_id": 11579,
                "retail_price": 39.99,
                "files": [
                    {
                        "type": "back",
                        "url": image_url,
                        "position": {
                            "area_width": 1800,
                            "area_height": 2400,
                            "width": 1800,
                            "height": 1800,
                            "top": 600,
                            "left": 0
                        }
                    },
                    {
                        "type": "embroidery_chest_left",
                        "url": chest_logo,
                        "options": [
                            {
                                "id": "auto_thread_color",
                                "value": True
                            }
                        ]
                    }
                ]
            }
        ],
    }
    external_api_response = session.post(
        external_api_url, headers=headers, json=data)

    response = external_api_response.json()

    id = response['result']['id']

    try:
        get_product_url = f'https://api.printful.com/sync/products/{id}'

        y = session.get(url=get_product_url, headers=headers)
        data = y.json()

    except openai.error.InvalidRequestError as e:
        return jsonify({"error": str(e)}), 400

    print(data)

    return (jsonify({"product": data, 'url': image_url}))


@app.route("/image/<id>", methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def image(id):
    session = requests.Session()
    url1 = 'https://gateway.pinata.cloud/ipfs/Qmc3z8LknwWpYJdakPsmuHZ6zZtCXowkqJmHbFFzxTyvKV'

    url_post = 'https://api.printful.com/store/products/' + str(id)
    y = session.get(url=url_post, headers=headers)
    data = y.json()
    url2 = data['result']['sync_variants'][0]['files'][1]['url']

    response1 = session.get(url1)
    response2 = session.get(url2)

    # Open the two images using PIL
    img1 = Image.open(BytesIO(response1.content))
    img2 = Image.open(BytesIO(response2.content))

    # Scale up the second image
    scale_factor = 1.55
    img2 = img2.resize((int(img2.width * scale_factor),
                       int(img2.height * scale_factor)), Image.ANTIALIAS)
    # Paste image2 onto image1 at position (0, 0)
    img1.paste(img2, (225, 140))

    # Convert the image to RGB mode
    img1 = img1.convert("RGB")

    # Save the result as a JPEG file
    img1.save('result.jpg', 'JPEG')

    with open('result.jpg', 'rb') as f:
        image_data = f.read()
    return Response(image_data, content_type='image/jpeg')


if __name__ == "__main__":
    app.run(port=8000, debug=True)
