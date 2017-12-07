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
import datetime 
import multiprocessing

""" map con multiprocessing"""
def map_multi( f, l, cpu_n= multiprocessing.cpu_count()):
        pool = multiprocessing.Pool(cpu_n)
        res = pool.map( f, l)
        pool.close()
        pool.join()
        return res



""" str base64 -> img opencv """
def readb64(base64_string):
	sbuf = StringIO()
	sbuf.write(base64.b64decode(base64_string))
	pimg = Image.open(sbuf)
	return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

""" obtener el color mas popular de una imagen, sacando blancos"""
def most_popular_color(img):
	try:
		cn =Counter(["_".join(map(str,l)) for pix in img.tolist() for l in pix if not min(l)==255 and np.mean(l)<200])
		return map(int,cn.most_common(1)[0][0].split("_"))
	except: return [np.nan,np.nan,np.nan]

def split_list_of_circles(img): return [img[:,i*IMG_WIDTH:(i+1)*IMG_WIDTH,:] for i in range( int(np.ceil(img.shape[1]/float(IMG_WIDTH))))]
		
""" para generar escala """
def create_scale():
	path_colors_pattern='color_patrones'
	return np.array([cv2.imread(os.path.join(path_colors_pattern,fn))[0] for fn in sorted(os.listdir(path_colors_pattern))])
	

""" dada img devuelvo una lista con valores, error <0.11"""
def parse_scale(img):
	scales=np.linspace(1,5,41)
	color_per_score = map(most_popular_color,split_list_of_circles(img))
	def rate(a):
		try: return scales[np.nanargmin((abs(pix_colors-np.array(a))).sum(2).sum(1))]
		except: return np.nan		
	return [rate(a) for a in color_per_score]
	
""" data una materias con los scores en imagenes en base64, las
reemplazo por lista de numeros
"""
def process_materia(fn):	
	try:
		fin=open(os.path.join(path,fn))
		d=json.load(fin)
		fin.close()
		for a_i in range(len(d)):
			d[a_i]['materia_scores']=parse_scale(readb64(d[a_i]['materia_img_scores']))
			del d[a_i]['materia_img_scores']
			for curso_i in range(len(d[a_i]['cursos'])):
				r= d[a_i]['cursos'][curso_i]
				r['turno_score']=parse_scale(readb64(r['turno_score_img']))
				del r['turno_score_img']
				for turno_doc_i in range(len(d[a_i]['cursos'][curso_i]['turno_docentes'])):
					r=d[a_i]['cursos'][curso_i]['turno_docentes'][turno_doc_i]
					r['docente_score']=parse_scale(readb64(r['docente_img_score']))
					del r['docente_img_score']
		return d
	except:
		fout = open('fallo_parsing.log','a')
		fout.write(fn+"\n")
		fout.close()

def process_all_files():
	pix_colors = create_scale()
	all_mats=[]
	
	for ipack in range(100):
		pack = sorted(os.listdir(path))[ipack::100]
		print ipack,100,datetime.datetime.now()
		all_mats+=map_multi(process_materia,pack)
	
	fout=open('data.json','w')
	json.dump(all_mats,fout)
	fout.close()

IMG_WIDTH=29
path='materias_dump'
	
process_all_files()


