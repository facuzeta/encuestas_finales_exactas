# encuestas_finales_exactas
Codigo para bajar la data y parsearla de http://encuestas_finales.exactas.uba.ar/

- download_data.py: baja los datos por materia guardandolos en JSONs. Como los puntajes de las encuestas estan guardadas como imagenes en la web, este script las guarda en formato base64 para poder incluirlas en los JSONs.

- parse_img.py: toma los JSONs generados por el script download_data y los junta todos reemplazando las imagenes por listas de numeros correspondientes a las imagenes. Uso el color de los cicurlos de las encuetas para inferir el numero, este metodo tiene un error estimado < 0.1. Deberia hacerse algo de digit recognition pero fue mas facil hacerlo asi.

- req.txt: es la lista de paquetes de python necesario para correr los scripts (pip install -r req.txt para instalarlos)

- color_patrones: contiene varios PNGs etiquetados con la valoración por color.

- data.json.zip: Es la data de todas las encuentas (hasta 2017-12-07) parseada generada con los scripts anteriores.

