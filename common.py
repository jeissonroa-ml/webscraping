import yaml

#la libreria yaml que es la que nos servira de ayuda para 
#convertir el archivo de configuracion en un diccionario 
#(objeto que podemos manejar facilmente en Python)


__config = None


def config():
    global __config
    if not __config:
        #Para realizar nuestra “conversion” se hace uso de la funcion yaml.
        #load([archivo.yaml]) que recibe el archivo como parametro y retorna
        # un diccionario.
        with open('config.yaml', mode='r') as f:
            __config = yaml.load(f, Loader=yaml.FullLoader)
            #config = yaml.safe_load(f)

    return __config
