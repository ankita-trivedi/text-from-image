import json
import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import general as fx
import model_easyocr as e_ocr
import model_google_vision as gv

app = Flask(__name__, template_folder="templates")

uploads_dir = os.path.join(app.root_path, os.path.join('files', 'uploads'))

def fetch_text_from_image(image_path=""):
	if image_path != "":
		result = {
			"e_ocr":e_ocr._init_procedure(image_path),
			"gv_ocr": gv._init_procedure(image_path)
		}
		return json.dumps(result)
	else:
		return "NO Path Given"


@app.route('/', methods=['GET'])
def upload_form():
	return render_template('home.html')


@app.route('/upload', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		file_sub_dir = fx.current_milli_time()
		file_dir_path = os.path.join(uploads_dir, file_sub_dir)
		os.makedirs(os.path.join(uploads_dir, file_sub_dir))
		full_file_path = os.path.join(file_dir_path, secure_filename(file.filename))
		file.save(full_file_path)
		text_from_image = fetch_text_from_image(full_file_path)
		return text_from_image
	else:
		return "Method Not Allowed"


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=443)
