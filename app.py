from flask import Flask, render_template


app = Flask(__name__)
@app.route('/')
def main():
    return render_template("main.html")
@app.route('/filter')
def filter():
    return render_template("main.html")
@app.route('/noise')
def noise():
    return render_template("main.html")
if __name__ == '__main__':
    app.run(debug=True)