from flask import Flask, render_template , request , jsonify , json
from functions import Functions
import numpy as np
import cv2
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
        filtertype = request.json['type']
        kernal = request.json['kernalsize']
        raduis= request.json['raduissize']

        img = cv2.imread("./static/imgs/original_img.jpg",cv2.IMREAD_GRAYSCALE)
        # print(img.shape)
        if filtertype == "gaussian-filter":
            new_img = Functions.gaussian_filter(Functions,img,3,1)
            Functions.display_image(Functions,new_img)
        elif filtertype == "avg-filter":
            new_img = Functions.average_filter(Functions,image_data=img,filter_size=9)
            Functions.display_image(Functions,new_img)
        elif filtertype == "mad-filter":
            new_img = Functions.median_filter(Functions,img,7)
            Functions.display_image(Functions,new_img)
        elif filtertype == "hp-filter":
            new_img = Functions.low_high_pass(Functions,img,'high',10)
            Functions.display_image(Functions,new_img)
        elif filtertype == "lp-filter":
            new_img = Functions.low_high_pass(Functions,img,'low',20)
            Functions.display_image(Functions,new_img)
        print(filtertype)
        print(kernal)
        print(raduis)        
        return render_template("main.html")
    else:
        return render_template("main.html")

@app.route('/noise' , methods =['POST','GET'])
def noise():
    if request.method == 'POST':
        noiseType = request.json['type']
        snr = request.json['snr']
        print(noiseType)
        print(snr)
        return render_template("main.html")
    else:
        return render_template("main.html")
#@app.route('/SNR' , methods =['POST','GET'])
#def snr():
    #if request.method == 'POST':
        #snr = request.json
        #print(snr)
        
        #return render_template("main.html")
    #else:
        #return render_template("main.html")

if __name__ == '__main__':
    app.run(debug=True)