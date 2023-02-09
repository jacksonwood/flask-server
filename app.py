from flask import Flask, jsonify
import os
import openai
import requests
import time
from flask_cors import CORS, cross_origin

openai_key = os.environ.get("OPENAI_KEY")

printful_key = os.environ.get("PRINTFUL_KEY")


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/load_ai/<input_value>": {"origins": "*"}})


@ app.route("/load_ai/<input_value>", methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def load_ai(input_value):
    # Create a session
    session = requests.Session()

    # Set the headers for the session
    headers = {
        'Authorization': 'Bearer ' + printful_key,
        'Content-Type': 'application/json'
    }
    session.headers.update(headers)
    '''

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
    print(image_url)
    '''
    image_url = 'https://www.twitter.com'

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

    mock_url = 'https://api.printful.com/mockup-generator/create-task/438'

    data = {
        "variant_ids": [11576, 11577, 11578, 11579],

        "product_options": {
            "lifelike": False
        },
        "files": [
            {
                "placement": "back",
                "image_url": image_url,
                "position": {
                    "area_width": 1800,
                    "area_height": 2400,
                    "width": 1800,
                    "height": 1800,
                    "top": 600,
                    "left": 0
                }
            }
        ],
        "options": ["Back"]
    }
    mock_results = session.post(mock_url, headers=headers, json=data)
    data = mock_results.json()
    print(data)
    task_key = data['result']['task_key']
    id = str(id)
    print(id)
    try:
        print(task_key)
        new_url = f'https://api.printful.com/mockup-generator/task?task_key={task_key}'

        while True:
            y = session.get(url=new_url, headers=headers)
            if y.status_code == 200:
                new_data = y.json()
                if new_data['result']['status'] != 'pending':
                    try:
                        mockups = new_data['result']['mockups']
                        new_url = mockups[0]['mockup_url']
                        break
                    except KeyError:
                        print("The key 'mockups' was not found in the response data")
                else:
                    print("The task is still pending, waiting...")
                    time.sleep(4)
            else:
                print(
                    f"The request was unsuccessful, status code: {y.status_code}")
                break
    except Exception as e:
        print(f"An error occurred while trying to get the mockup URL: {e}")

    final_mock = new_url

    try:
        get_product_url = f'https://api.printful.com/sync/products/{id}'

        y = session.get(url=get_product_url, headers=headers)
        data = y.json()

    except openai.error.InvalidRequestError as e:
        return jsonify({"error": str(e)}), 400

    return (jsonify({"mockup": final_mock, "product": data}))


if __name__ == "__main__":
    app.run(port=8000, debug=True)
