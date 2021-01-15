from flask import Flask, url_for, send_from_directory, request, render_template
import logging
import os
from werkzeug.utils import secure_filename


# sys.path.append('../classiferModule')
# if sys:
#     import classifier
app = Flask(__name__)
file_handler = logging.FileHandler('server.log')


PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/child'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


@app.route('/', methods=['POST'])
def api_root():

    if request.method == 'POST' and request.files['image']:

        img = request.files['image']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)

        img.save(saved_path)

        return send_from_directory(app.config['UPLOAD_FOLDER'], img_name, as_attachment=True)
    else:
        return "Where is the image?"


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
