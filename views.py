from flask import Flask,request,jsonify,url_for, render_template, redirect,send_file,abort
from datetime import datetime as dt
import requests as req
import os
import re

os.system("color")

app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def main():
    #files = [file.replace('.txt','') for file in os.listdir('./notes')]
    files = [file[:-4] for file in os.listdir('./notes')]
    return render_template("index.html",files=files)

@app.route('/create_note',methods=["POST"])
def create_note(name=None):
    name = request.form.get('note_name') or name
    print(name)
    if not os.path.exists('./notes'):
        os.mkdir('./notes')
    if name:
        open(f'./notes/{str(name)}.txt','w').write('')
    return redirect("/")

# @app.route('/save/', defaults={'note_title': ''})
# @app.route('/<path:note_title>')

def br2n(html: str, mobile: bool = False) -> str:
    replacing = {}
    n = html.replace('<div><br></div>','\n')
    
    for s in re.findall('(</div>(\\n)*<div>)',n):
        replacing[s[0]] = re.sub('<div>|</div>','',s[0]) +'\n'
    
    for prev,new in replacing.items():
        n = n.replace(prev,new)
    
    if mobile:
        n = n.replace('<div>','\n')

    n = re.sub('<div>|</div>|<br>','',n)

    print(replacing)
    
    return n

@app.route('/sync_note',methods=["POST"])
def sync_note():
    # request = request.form['asdad']
    print(request)
    name = request.form.get('name')
    content = request.form.get('content')
    mobile = request.form.get('mobile').lower().strip() == 'true'

    print(f"Mobile: {mobile}")
    print(f'Raw content: {str(content)}')
    content = br2n(html=str(content),mobile=mobile)
    # content = content.replace('<br>','\n')
    print(f'Converted: {content}')

    # content = content.lstrip('<div>')
    # content = content.replace('<div><br></div>','\n')
    # content = content.replace('<br><div>','\n')
    # content = content.replace('</div><div>','\n')
    # content = content.replace('<br>','\n')
    # content = content.replace('<div>','\n')
    # content = content.replace('</div>','')
    # title = request.form['title']
    # print(name,content)
    if not os.path.exists('./notes'):
        os.mkdir('./notes')
    if name:
        open(f'./notes/{str(name)}.txt','w',encoding='utf-8').write(content)
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success':False, 'message': '*** NO NAME PROVIDED ***'}), 400
    

@app.route('/', defaults={'note_name': ''})
@app.route('/<path:note_name>')
def get_note_name(note_name):
    BASE_DIR = './notes'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, f"{note_name}.txt")
    # abs_path = req_path
    print(abs_path)

    # Return 404 if path doesn't exist
    # if not os.path.exists(abs_path):
    #     return abort(404)

    # Check if path is a file and serve
    if not os.path.isfile(abs_path):
        # note_content = open(abs_path,'r',encoding="utf-8").read()
        
    # else:
        create_note(name=note_name)
    
    return render_template('note.html', note_name=f'{note_name}')


@app.route('/get_note_content',methods=["POST"])
def get_note_content():
    # print(request.json)
    # request = request.json
    note_name = request.form.get('name')
    print(f"Note name: {note_name}")

    if not note_name:
        return jsonify({'note_content': '*** NO NAME PROVIDED ***'}), 400

    BASE_DIR = './notes'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, f"{note_name}.txt")
    # abs_path = req_path
    print(abs_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    note_content = open(abs_path,'r',encoding="utf-8").read()
        
    return jsonify({'note_content':note_content}), 200

# @app.route('/', defaults={'note_title': ''})
# @app.route('/<path:note_title>')
# def get_note(note_title):
#     BASE_DIR = './notes'

#     # Joining the base and the requested path
#     abs_path = os.path.join(BASE_DIR, f"{note_title}.txt")
#     # abs_path = req_path
#     print(abs_path)

#     # Return 404 if path doesn't exist
#     if not os.path.exists(abs_path):
#         return abort(404)

#     # Check if path is a file and serve
#     if os.path.isfile(abs_path):
#         note_content = open(abs_path,'r',encoding="utf-8").read()
#         return render_template('note.html', note_content=note_content)
#         # return send_file(abs_path)

#     # Show directory contents
#     files = os.listdir(abs_path)
#     return render_template('index.html', files=files)

app.run(host="0.0.0.0",port=1024,debug=True)