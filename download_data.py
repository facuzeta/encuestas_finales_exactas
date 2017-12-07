# -*- coding: utf-8 -*-
import bs4
import urllib2
import json
import datetime
import os

host='http://encuestas_finales.exactas.uba.ar/'

def get_url(url): return urllib2.urlopen(url)

def parse_docentes(dt):
	rds=[]
	for d in dt.find_all('td')[1].find_all('div'):
		rd={}
		rd['docente_link']=host+d.find('a').attrs['href'][3:]
		rd['docente_img_score_link']=host+d.find('img').attrs['src'][3:]
		rd['docente_img_score']=get_url(rd['docente_img_score_link']).read().encode('base64')
		rd['docente_nombre']=d.find('a').text
		rd['docente_cargo']=d.find('span').text
		rds.append(rd)
	return rds

def parse_turnos(scores_turnos,docentes_turnos):
	r_turnos=[]
	for st,dt in zip(scores_turnos,docentes_turnos):
		score_turno_img= st.find('img').attrs['src']
		r_t={}
		r_t['turno_score_img_link']=host+score_turno_img[3:]
		r_t['turno_score_img']=get_url(r_t['turno_score_img_link']).read().encode('base64')
		try: 
			r_t['turno_comentarios_link']=host+'cmt/t'+st.find('a').attrs['onclick'].split(", ")[1][:-2]+".html"
			r_t['turno_comentarios']=[c.text for c in bs4.BeautifulSoup(get_url(r_t['turno_comentarios_link']).read()).find_all('div',{'class':'cm'})]
		except: 
			r_t['turno_comentarios_link']=''
			r_t['turno_comentarios']=[]
		r_t['turno_docentes']=parse_docentes(dt)
		r_turnos.append(r_t)
	return r_turnos
	

def get_materia(mat_id):
	url_mat ='http://encuestas_finales.exactas.uba.ar/mat/m'+str(mat_id)+".html"
	html =get_url(url_mat).read()
	cursadas =(bs4.BeautifulSoup(html).find_all('tr'))[1::3]
	res=[]
	for tr in cursadas:
		cuat, raw_info = tr.find_all('td')
		link_scores= host+raw_info.find_all('img')[0].attrs['src'][3:]
		link_curso=host+raw_info.find_all('a')[1].attrs['href'][3:]
		link_comentarios=host+'cma/'+link_curso.split("/")[-1]
		r={}
		r['mat_id']=mat_id
		r['cuat']=cuat.text
		print "\t",r
		r['link_scores']=link_scores
		r['link_curso']=link_curso
		r['materia_img_scores']=get_url(link_scores).read().encode('base64')
		html_curso=get_url(link_curso).read()

		trs=bs4.BeautifulSoup(html_curso).find_all('tr')
		curso_scores=trs[1].find('img').attrs['src']
		docentes_turnos=trs[1:][0::3][1:]
		scores_turnos=trs[1:][1::3]
		r['cursos']=parse_turnos(scores_turnos,docentes_turnos)
		res.append(r)
	return res

def get_all_materias_ids():		
	all_materias_ids=[]
	for d in range(0,62):
		html=get_url("http://encuestas_finales.exactas.uba.ar/lists/l_mats_%d.html" %d).read()
		all_materias_ids+=[(a.attrs['href'][5:-5],a.text) for a in bs4.BeautifulSoup(html).find_all('a') if "mat" in a.attrs['href']]
	return all_materias_ids

path_materias='materias_dump'	
try: os.mkdir(path_materias)
except: pass

all_materias_ids= get_all_materias_ids()
for mat_id,mat_name in all_materias_ids:
	try: 
		print mat_id, datetime.datetime.now()
		mat =get_materia(mat_id)
		for mi in range(len(mat)):
			mat[mi]['mat_nombre']=mat_name
		fout=open(os.path.join(path_materias,mat_id+'.json'),'w')
		json.dump(mat,fout)
		fout.close()
	except:
		fout = open('log.error','a')
		fout.write('fallo mat_id:'+mat_id+"\n")
		fout.close()
		
