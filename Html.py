
class Titulo: 
    def __init__(self, texto, posicion, tamanio, color) -> None:
        self.texto = texto
        self.posicion = posicion
        self.tamanio = tamanio 
        self.color = color
    
    
    def agregar_texto(self, texto):
        self.texto = texto

    def agregar_posicion(self, posicion):
        self.texto = posicion

    def agregar_tamanio(self, tamanio):
        self.texto = tamanio

    def agregar_color(self, color):
        self.texto = color
    
    def __str__(self):
        return f'<h1 sytle="text-align:{self.posicion}; font-size:{self.agregar_tamanio}; color: {self.color}"> {self.texto} </h1> '
    

def obtener_titulo(lista):
    for lexema in lista:
        if lexema.tipo == "Titulo"



html_inicio = "<html>"

html_cuerpo = "todas tus etiquetas"

html_cierre = "</html>"

html_final = html_inicio + html_cuerpo+ html_cierre







