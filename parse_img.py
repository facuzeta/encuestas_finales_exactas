import cv2
import base64
import json
import os
import random
from PIL import Image
import cv2
from StringIO import StringIO
import numpy as np
from collections import Counter
from collections import  defaultdict

FNAME_SCALE= 'scale.json'
IMG_WIDTH=29

def readb64(base64_string):
	sbuf = StringIO()
	sbuf.write(base64.b64decode(base64_string))
	pimg = Image.open(sbuf)
	return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

def most_popular_color(img):
	cn =Counter(["_".join(map(str,l)) for pix in img.tolist() for l in pix if not min(l)==255 and np.mean(l)<200])
	return map(int,cn.most_common(1)[0][0].split("_"))

def split_list_of_circles(img): return [img[:,i*IMG_WIDTH:(i+1)*IMG_WIDTH,:] for i in range( int(np.ceil(img.shape[1]/float(IMG_WIDTH))))]
		

def create_scale():
	res =[]
	scale=cv2.imread('scale.png')
	for i in range(27):
		w=IMG_WIDTH
		sub_img= scale[:,i*w:(i+1)*w,:]
		#~ cv2.imwrite(str(i)+".png",sub_img)
		pix = most_popular_color(sub_img)
		pattern=np.array([[pix for ii in range(10)] for _ in range(10)])
		#~ cv2.imwrite('pattern_%d.png' % i , pattern)
		res.append(pix)
	
	fout = open(FNAME_SCALE,'w')
	json.dump(res,fout)
	fout.close()
	

def parse_scale(img):
	scales=[1,1.2,1.3,1.5,1.6,1.8,1.9,2.1,2.2,2.4,2.5,2.7,2.8,3.0,3.2,3.3,3.5,3.6,3.8,3.9,4.1,4.2,4.4,4.5,4.7,4.8,5.0]
	fl = open(FNAME_SCALE)
	pix_colors=np.array(json.load(fl))
	fl.close()
	color_per_score = map(most_popular_color,split_list_of_circles(img))
	return [scales[np.argmin(abs(pix_colors-a).sum(1))] for a in color_per_score]
	


