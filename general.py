from base64 import b64encode

import constant
import json
import requests
import time


def current_milli_time():
	return str(round(time.time() * 1000))


def prepare_image_data(image_path):
	img_object = None
	with open(image_path, 'rb') as f:
		image_content_txt = b64encode(f.read()).decode()
		img_object = {
			'image': {
				'content': image_content_txt
			},
			'features': [{
				'type': 'DOCUMENT_TEXT_DETECTION',
				'maxResults': 1
			}]
		}
	return json.dumps({"requests": img_object}).encode()


def http_request(api_key, image_path):
	response = requests.post(constant.API_ENDPOINT,
	                         data=prepare_image_data(image_path),
	                         params={'key': api_key},
	                         headers={'Content-Type': 'application/json'})
	return response
