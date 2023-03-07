from flask import Flask, render_template , request , jsonify , json


app = Flask(__name__)
@app.route('/' , methods = ['POST', 'GET'] )
def main():
    if request.method == 'POST':
        img = request.files.get('original_img')
        name = './static/imgs/' + img.filename + '.jpg'
        img.save(name)
        print(img)
        return render_template("main.html")
    else:
        return render_template("main.html")


@app.route('/filter' , methods =['POST','GET'])
def filter():
    if request.method == 'POST':
        filtertype = request.json
        print(filtertype)
        return render_template("main.html")
    else:
        return render_template("main.html")

@app.route('/noise' , methods =['POST','GET'])
def noise():
    if request.method == 'POST':
        noise = request.json
        print(noise)
        return render_template("main.html")
    else:
        return render_template("main.html")


if __name__ == '__main__':
    app.run(debug=True)