from flask import Flask, render_template , request , jsonify , json
from functions import Functions
import numpy as np
import cv2
import os
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
        if os.path.exists("./static/imgs/noisy.jpg") != True:
            img = cv2.imread("./static/imgs/original_img.jpg",cv2.IMREAD_GRAYSCALE)
        else:
            img = cv2.imread("./static/imgs/noisy.jpg",cv2.IMREAD_GRAYSCALE)
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
            Functions.display_image(Functions,new_img,'noisy')
        elif noiseType == "gaussian-noise":
            new_img = Functions.noisy('gaussian',img)
            Functions.display_image(Functions,new_img,'noisy')
        elif noiseType == "sp-noise":
            new_img = Functions.noisy('s&p',img)
            Functions.display_image(Functions,new_img,'noisy')
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
@app.route('/histogram' , methods = ['POST', 'GET'] )
def histogram():
    if request.method == 'POST':
        img = request.files.get('inputimg')
        if img != None:
            name = './static/imgs/' + img.filename + '.jpg'
            img.save(name)
        print(img)
        read_img = cv2.imread('./static/imgs/inputimg.jpg')
        RGB_hist = Functions.RGB_histogram(Functions,read_img)
        Functions.Plot_RGBHistogram(Functions,RGB_hist,"./static/imgs/RGB_histogram.jpg")
        Gray_hist =Functions.Gray_histogram_Compute(Functions,read_img)
        Functions.Gray_histogram_Plot(Functions,Gray_hist,"./static/imgs/Gray_histogram.jpg")
        equalizedImg = Functions.img_equalize(Functions,read_img)
        Functions.display_image(Functions,equalizedImg,'equalized_img')
        RGB_equalized = Functions.RGB_histogram(Functions,equalizedImg)
        Functions.Plot_RGBHistogram(Functions,RGB_equalized,"./static/imgs/RGB_histogram_equalized.jpg")
        Gray_equalized =Functions.Gray_histogram_Compute(Functions,equalizedImg)
        Functions.Gray_histogram_Plot(Functions,Gray_equalized,"./static/imgs/Gray_histogram_equalized.jpg")
        return render_template("main.html")
    else:
        return render_template("main.html")

@app.route('/edge' , methods = ['POST', 'GET'] )
def edge():
    if request.method == 'POST':
        img = request.files.get('inputedge')
        if img != None:
            name = './static/imgs/' + img.filename + '.jpg'
            img.save(name)
        print(img)

        return render_template("main.html")
    else:
        return render_template("main.html")
@app.route('/edgetype' , methods = ['POST', 'GET'] )
def edgetype():
    if request.method == 'POST':
        type = request.json
        print(type)
        img = cv2.imread('./static/imgs/inputedge.jpg',cv2.IMREAD_GRAYSCALE)
        new_img = Functions.edge_detection(Functions,img,str(type))
        new_img = new_img*150
        Functions.display_image(Functions,new_img,"outputedge")
        return render_template("main.html")
    else:
        return render_template("main.html")
@app.route('/threshold' , methods = ['POST', 'GET'] )
def threshold():
    if request.method == 'POST':
        type = request.json
        print(type)
        img = cv2.imread('./static/imgs/inputedge.jpg',cv2.IMREAD_GRAYSCALE)
        vv1 = Functions.thres_finder(Functions,img, thres=30, delta_T=1.0)
        # threshold the image
        if str(type) == 'localthreshold':
            local_thresh = Functions.local_threshold(Functions,img, 7)
            Functions.display_image(Functions,local_thresh,"threshold")
        if str(type) == 'globalthreshold':
            global_thresh = Functions.global_threshold(Functions,img, vv1, 255, 0)
            Functions.display_image(Functions,global_thresh,"threshold")
        return render_template("main.html")
    else:
        return render_template("main.html")
if __name__ == '__main__':
    app.run(debug=True , port=3500)