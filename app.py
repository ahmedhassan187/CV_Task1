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
            new_img = Functions.gaussian_filter(Functions,img,int(kernal),1)
            Functions.display_image(Functions,new_img,'filtered_img')
        elif filtertype == "avg-filter":
            new_img = Functions.average_filter(Functions,image_data=img,filter_size=int(kernal))
            Functions.display_image(Functions,new_img,'filtered_img')
        elif filtertype == "mad-filter":
            new_img = Functions.median_filter(Functions,img,int(kernal))
            Functions.display_image(Functions,new_img,'filtered_img')
        elif filtertype == "hp-filter":
            new_img = Functions.low_high_pass(Functions,img,'high',int(raduis))
            Functions.display_image(Functions,new_img,'filtered_img')
        elif filtertype == "lp-filter":
            new_img = Functions.low_high_pass(Functions,img,'low',int(raduis))
            Functions.display_image(Functions,new_img,'filtered_img')
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
        print(noiseType)
        img = cv2.imread("./static/imgs/original_img.jpg",cv2.IMREAD_GRAYSCALE)
        if noiseType == "uniform-noise":
            new_img = Functions.noisy('uniform',img)
            Functions.display_image(Functions,new_img,'original_img')
        elif noiseType == "gaussian-noise":
            new_img = Functions.noisy('gaussian',img)
            Functions.display_image(Functions,new_img,'original_img')
        elif noiseType == "sp-noise":
            new_img = Functions.noisy('s&p',img)
            Functions.display_image(Functions,new_img,'original_img')
        return render_template("main.html")
    else:
        return render_template("main.html")

@app.route('/hybrid' , methods = ['POST', 'GET'] )
def hybrid():
    if request.method == 'POST':
        img1 = request.files.get('firstimg')
        img2 = request.files.get('secondimg')
        if img1 != None:
            name = './static/imgs/' + img1.filename + '.jpg'
            img1.save(name)
        if img2 != None:
            name = './static/imgs/' + img2.filename + '.jpg'
            img2.save(name)

        print(img1)
        print(img2)
        return render_template("main.html")
    else:
        return render_template("main.html")
@app.route('/hybridraduis' , methods = ['POST', 'GET'] )
def hybrid_raduis():
    if request.method == 'POST':
        raduis1 = request.json['img1_raduis']
        raduis2 = request.json['img2_raduis']
        print(raduis1)
        print(raduis2)
        img1 = cv2.imread('./static/imgs/firstimg.jpg',cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread('./static/imgs/secondimg.jpg',cv2.IMREAD_GRAYSCALE)
        img1 = Functions.low_high_pass(Functions,img1,'low',int(raduis1))
        img2 = Functions.low_high_pass(Functions,img2,'high',int(raduis2))
        new_img = img1+img2 
        # new_img = Functions.hybrid(Functions,img1,img2,int(raduis1),int(raduis2))
        Functions.display_image(Functions,new_img,'hybrid_img')
        return render_template("main.html")
    else:
        return render_template("main.html")
if __name__ == '__main__':
    app.run(debug=True , port=3500)