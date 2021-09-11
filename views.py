from flask import Flask,request,jsonify,url_for, render_template, redirect,send_file,abort
from datetime import datetime as dt
import os

os.system("color")

app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def main():
    files = os.listdir('./notes')
    return render_template("index.html",files=files)

@app.route('/save_note',methods=["POST"])
def save_note():
    title = request.form['title']
    print(title)
    if not os.path.exists('./notes'):
        os.mkdir('./notes')
    if title:
        open(f'./notes/{str(title)}.txt','w').write('')
    return redirect("/")

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = './notes'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)
    # abs_path = req_path
    print(abs_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('index.html', files=files)

app.run(host="0.0.0.0",port=1024,debug=True)