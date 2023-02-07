from flask import Flask, jsonify, request
import os
import openai
import requests
from flask_cors import CORS, cross_origin
import threading

openai_key = os.environ.get("OPENAI_KEY")

printful_key = os.environ.get("PRINTFUL_KEY")

prompt = None

task_lock = threading.Lock()
task_key = None


headers = {
    'Authorization': 'Bearer ' + printful_key,
    'Content-Type': 'application/json'
}

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/generate_product/": {"origins": "*"},
                     r"/view_product/": {"origins": "*"},
                     r"/get_all_products/<input_value>": {"origins": "*"},
                     r"/load_ai/<input_value>": {"origins": "*"},
                     r"/generate_text/<input_value>": {"origins": "*"}})


@ app.route("/load_ai/<input_value>", methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def load_ai(input_value):
    prompt = input_value
    if prompt is None or prompt == "":
        return jsonify({"error": "prompt parameter is required"}), 400
    openai.api_key = openai_key
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256"
        )
    except openai.error.InvalidRequestError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"image_url": response['data'][0]['url']})


@ app.route("/generate_text/<input_value>", methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def generate_text(input_value):
    with prompt_lock:
        prompt = input_value
    if prompt is None or prompt == "":
        return jsonify({"error": "prompt parameter is required"}), 400

    openai.api_key = openai_key
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Give an alternative prompt for the following that would have yielded a better image: " + prompt,
            max_tokens=1000,
            temperature=0.9)
    except openai.error.InvalidRequestError as e:
        return jsonify({"error": str(e)}), 400
    return response.choices[0].text


@app.route("/generate_product", methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def generate_product():
    chest_logo = "https://gateway.pinata.cloud/ipfs/QmXKu3kbkksCJsHaoJ2N5KUsRF3HFWuvacZTP7arhD3rVS?_gl=1*oadv6z*_ga*MjE0MjEyNjU3NC4xNjc1MDE0NTg2*_ga_5RMPXG14TE*MTY3NTYzMTAyOC43LjAuMTY3NTYzMTAyOC42MC4wLjA.&__cf_chl_tk=seoLwhAI3lVqOMpaODAvbQo6Ct_mfWGsiaO52TMpjPU-1675631030-0-gaNycGzNDdE"

    data = request.json
    image_url = data['imageUrl']

    data = {
        "sync_product": {
            "name": prompt
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
        ]
    }
    external_api_response = requests.post(
        'https://api.printful.com/store/products', headers=headers, json=data)

    response = external_api_response.json()

    id = response['result']['id']
    name = response['result']['name']

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
        ]
    }
    task_key = None
    max_retries = 3
    retry_count = 0
    while task_key is None and retry_count < max_retries:
        mock_results = requests.post(mock_url, headers=headers, json=data)
        data = mock_results.json()
        with task_lock:
            task_key = data.get('result', {}).get('task_key')
        retry_count += 1

    if task_key is None:
        raise Exception("Failed to retrieve task_key after multiple retries")

    return jsonify({"task_key": task_key, "id": str(id), "name": name}).json


@ app.route("/view_product", methods=['POST'])
@ cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def view_product():
    try:
        data = request.json
        task_key = data['task_key']
        new_url = f'https://api.printful.com/mockup-generator/task?task_key={task_key}'

        y = requests.get(url=new_url, headers=headers)
        data = y.json()
        mockups = data['result']['mockups']
        print(data)
        new_url = mockups[0]['mockup_url']
        return jsonify({"image_url": new_url})

    except openai.error.InvalidRequestError as e:
        return jsonify({"error": str(e)}), 400


@ app.route("/get_all_products/<input_value>", methods=['GET'])
@ cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_all_products(input_value):
    try:
        url = f'https://api.printful.com/sync/products/{input_value}'

        y = requests.get(url=url, headers=headers)
        data = y.json()
        return jsonify(data)

    except openai.error.InvalidRequestError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(port=8000, debug=True)
