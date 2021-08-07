import json

from pylab import rcParams

import general

rcParams['figure.figsize'] = 10, 20


def _init_procedure(image_path):
	global result_object
	with open('vision_api.json') as f:
		data = json.load(f)
	
	result = general.http_request(data["api_key"], image_path)
	
	if result.status_code != 200 or result.json().get('error'):
		print("Error")
	else:
		result_object = result.json()['responses'][0]['textAnnotations']
	
	global text_array
	text_array = []
	for index in range(len(result_object)):
		if index > 0:
			text_array.append(result_object[index]["description"])
	
	def fetch_text(result_object):
		return result_object["description"]
	
	result_object = {"text": fetch_text(result_object[0]), "text_segments": text_array}
	return result_object
