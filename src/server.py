from flask import Flask, request, flash, send_file, Response
from flask_cors import CORS
import app as insta

app = Flask(__name__)
CORS(app)
app.secret_key = b'_5#y3L"G6Q8d\n\xec]/'

ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_csv():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return Response("No File", 404)
        file = request.files['file']
        if file.filename == '':
            return Response("No File", 404)
        if file and allowed_file(file.filename):
            res = insta.run(file)

    return send_file(res)


@app.route('/version', methods=['GET'])
def version():
    return Response("1.1", 200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
