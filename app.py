import os
import pathlib
from datetime import datetime
from os.path import isfile, join, isdir

from flask import Flask, request, render_template, send_file
import html
import shutil
import humanize
import mimetypes

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/h1')
def hoofdstuk1():
    # 1
    # a = 10
    # if a > 0:
    #     return "boodschap"
    #
    # return ""

    # 2
    # a = 16
    # if 10 > a > 0:
    #     return "boodschap"
    # return ""

    # 3
    a = 12.3
    if 10 > a > 0:
        if a >= 5.5:
            return "voldoende"
        else:
            return "onvoldoende"
    else:
        return "ongeldige invoer"


@app.route('/h2')
def hoofdstuk2():
    # 4
    # out = ""
    # for a in range(1, 11, 2):
    #     out += f'{a}<br>'
    # return out

    # 5
    # html = ""
    # tafel = 4
    # for a in range(1, 11):
    #     html += f'{a} x {tafel} = {a * tafel}<br>'
    # return html

    # 6
    out = ""
    fib = 0
    tmp1 = 0
    tmp2 = 1
    while fib < 1000:
        out += f'{fib}, '
        fib = tmp1 + tmp2
        tmp1 = tmp2
        tmp2 = fib

    return out


@app.route('/h3', methods=['GET', 'POST'])
def hoofdstuk3():
    # 7
    # out = ""
    # if request.method == "POST":
    #     color = request.form.get("color")
    #     out += f"Color: {color}<br>"
    #     out += ('<style>'
    #              'body {'
    #              f"  background-color: {color};"
    #              '}'
    #              '</style>')
    #
    # out += ('<form method="POST" action="/h3">'
    #          'Kleur: <input type="text" name="color">'
    #          '<input type="submit" value="Stel in"></form>')
    #
    # return out

    # 8
    # out = ""
    # out += ('<form method="POST" action="/h3">'
    #          'Naam: <input type="text" name="name"><br>'
    #          'Leeftijd: <input type="text" name="age"><br>'
    #          '<input type="submit" value="Invoeren"></form>')
    #
    # if request.method == "POST":
    #     age = int(request.form.get('age'))
    #     name = request.form.get('name')
    #
    #     for i in range(age):
    #         out += f'{name}<br>'
    #
    # return html

    # 9
    out = ""
    out += ('<form method="POST" action="/h3">'
            'Tafel: <input type="text" name="table"><br>'
            '<input type="submit" value="Invoeren"></form>')

    if request.method == "POST":
        table = int(request.form.get('table'))

        for i in range(1, 11):
            out += f'{i} x {table} = {i * table}<br>'

    return out


@app.route('/h4', methods=['GET', 'POST'])
def hoofdstuk4():
    # 10

    # 13
    # f = open("img/content.txt")
    # out = f.read()
    # return out

    # 14
    # f = open("img/content.txt")
    # out = f'<textarea>{f.read()}</textarea>'
    # return out

    # 15
    f = open("app.py")
    out = f'<textarea>{html.escape(f.read())}</textarea>'
    return out


@app.route('/h5', methods=['GET', 'POST'])
def hoofdstuk5():
    # 16
    # shutil.copy2('img/content.txt', 'img/kopie.txt')
    # return "done"

    # 17
    out = ""
    if request.method == "POST":
        f = open("opdracht17.txt", "w")
        o17 = request.form.get("o17").replace("\n", "")
        f.write(o17)

    f = open("opdracht17.txt")
    out += ('<form method="POST" action="/h5">'
            f'<textarea rows="20" cols="50" name="o17">{f.read()}</textarea><br>'
            '<input type="submit" value="Opslaan">'
            '</form>')

    return out


@app.route('/filebrowser', methods=['GET', 'POST'])
def end():
    cwd = os.getcwd()
    link_cwd = ""
    file = ""
    file_size = ""
    file_read = "Nee"
    file_time = ""
    img = ""
    text = ""

    if request.method == "POST":
        file = request.args.get("file")
        file_loc = cwd + "\\" + file
        content = request.form.get("file").replace("\n", "")
        f = open(file_loc, "w")
        f.write(content)

    if request.args.get("cwd"):
        link_cwd += request.args.get("cwd")
        cwd = cwd + "\\" + link_cwd
        cwd = cwd.replace("\\\\", "\\")

    if request.args.get("file"):
        file = request.args.get("file")
        file_loc = cwd + "\\" + file

        if pathlib.Path(file_loc).is_file():
            f = open(file_loc, "a")

            file_size = humanize.naturalsize(os.path.getsize(file_loc))

            if f.writable():
                file_read = "Ja"

            diff = datetime.now() - datetime.fromtimestamp(os.path.getmtime(file_loc))
            file_time = humanize.naturaltime(diff)

            mime = mimetypes.guess_type(file_loc)[0].split("/")[0]
            if mime == "image":
                img = link_cwd + "\\" + file

            if mime == "text":
                f = open(file_loc, "r")
                text = html.escape(f.read())

    # crumbs
    crumbs = ""
    parts = link_cwd.lstrip("\\").split("\\")
    link = ""
    if len(parts) > 0:
        for p in parts:
            link += "\\" + p
            crumbs += f' > <a href="/filebrowser?cwd={link}">{p}</a>'

    files = [f for f in os.listdir(cwd) if isfile(join(cwd, f))]
    dirs = [f for f in os.listdir(cwd) if isdir(join(cwd, f))]

    return render_template('filebrowser.html', cwd=cwd, files=files, dirs=dirs, link_cwd=link_cwd,
                           file=file, file_size=file_size, file_read=file_read, file_time=file_time, img=img, text=text,
                           crumbs=crumbs)


@app.route('/image/<path:file>')
def photo(file=""):
    if pathlib.Path(file).is_file():
        return send_file(file)
    return ""


if __name__ == '__main__':
    app.run()
