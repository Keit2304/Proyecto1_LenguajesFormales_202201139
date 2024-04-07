from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import webbrowser
import os


lexemas = []
errores = []

class Lexema:
    def __init__(self, tipo, valor, columna, fila):
        self.tipo = tipo
        self.valor = valor
        self.columna = columna
        self.fila = fila

class Error:
    def __init__(self, mensaje, columna, fila):
        self.mensaje = mensaje
        self.columna = columna
        self.fila = fila
        

def analizadorLexico(textAreaInicial, textAreaFinal, reportArea):
    
    caracteres_invalidos = ""
   
    texto = textAreaInicial.get("1.0", "end")
    
    palabra = ""
    fila = 1
    columna = 0
    

    # Obtenemos el texto del text area
    texto = textAreaInicial.get("1.0", "end")
    
    # Iteramos sobre cada caracter del texto
    i = 0
    while i < len(texto):
        char = texto[i]
        columna += 1


        # Verificamos que el caracter sea una letra o un dígito
        if char.isalnum():
            # Iteramos los caracteres para obtener la palabra completa
            while i < len(texto) and texto[i].isalnum():
                palabra += texto[i]
                i += 1

            # Verificar si la palabra es una palabra reservada
            if palabra.lower() in ['doctype', 'html', 'head', 'title', 'body', 'h1', 'p', 'h2']:
                lexemas.append(Lexema("PALABRA_RESERVADA", palabra.lower(), columna, fila))
            elif palabra.isdigit():
                lexemas.append(Lexema("NUMERO", palabra, columna, fila))
            else:
                lexemas.append(Lexema("PALABRA", palabra, columna, fila))
            palabra = ""

        # Verificamos otros caracteres especiales
        elif char in [',']:
            lexemas.append(Lexema("COMA", char, columna, fila))
        elif char in ['.']:
            lexemas.append(Lexema("PUNTO", char, columna, fila))
        elif char in ['+', '-', '*', '/', '<', '>', '!']:
            lexemas.append(Lexema("ESPECIAL", char, columna, fila))
        elif char == '"':  # Verificar si es un inicio de cadena
            cadena = char
            i += 1
            columna += 1
            while i < len(texto) and texto[i] != '"':
                cadena += texto[i]
                i += 1
                columna += 1
            if i < len(texto) and texto[i] == '"':  # Si encontramos el final de la cadena
                cadena += '"'
                lexemas.append(Lexema("CADENA", cadena, columna, fila))
            else:  # Si no encontramos el final de la cadena, hay un error
                errores.append(Error("Cadena sin cerrar", columna, fila))
        # Ignoramos estos caracteres
        elif char in [' ', '\n', '\t', '\r']:
            if char == '\n':
                fila += 1
            columna = 0
        else:
            errores.append(Error(char, columna, fila))

        i += 1
    
    for lexema in lexemas:
        print(f'Tipo: {lexema.tipo}, Valor: {lexema.valor}, Columna: {lexema.columna}, Fila: {lexema.fila}')

    imprimirLexemasYErrores(lexemas, errores, textAreaFinal)
    reportArea.delete("1.0", END)
    reportArea.insert(END, caracteres_invalidos)

def cargarArchivo(textArea):
    archivo = filedialog.askopenfilename(filetypes=[("Archivo de texto", "*.txt, *.html")])

    if archivo:
        with open(archivo, 'r') as f:
            contenido = f.read()

        textArea.delete("1.0", END)
        textArea.insert(END, contenido)

def enviarTexto(textAreaInicial):
    texto = textAreaInicial.get("1.0", "end")
    html_contenido = "<html><head><title>HTML Traducido</title></head><body><p>Este es el contenido traducido</p></body></html>"
    return html_contenido

def generarHTML(textAreaInicial):
    texto = textAreaInicial.get("1.0", "end")
    caracteres_invalidos = analizadorLexico(texto)
    for char in caracteres_invalidos:
        texto = texto.replace(char, '')
    return texto

def abrirHTMLGenerado(textAreaInicial, textAreaFinal):
    texto = textAreaInicial.get("1.0", "end")
    html_contenido = "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n<meta charset=\"UTF-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n<title>Ejemplo título</title>\n</head>\n<body>\n<div>\n"

    instrucciones = texto.split('\n')

    for instruccion in instrucciones:
        if instruccion.strip() == 'Inicio:{' or instruccion.strip() == 'Cuerpo:[' or instruccion.strip() == '}':
            continue

        if instruccion.strip() == 'Encabezado:{' or instruccion.strip() == 'Texto:{':
            html_contenido += "\t<div>\n"
        elif instruccion.strip() == 'Parrafo:{':
            html_contenido += "\t<p>\n"
        elif instruccion.strip() == 'Titulo:{':
            html_contenido += "\t<h2>\n"
        elif instruccion.strip() == '},':
            html_contenido += "\t</div>\n"
        elif instruccion.strip() == '},':
            html_contenido += "\t</p>\n"
        elif instruccion.strip() == '},':
            html_contenido += "\t</h2>\n"
        elif ":" in instruccion:
            propiedad, valor = instruccion.split(":")
            propiedad = propiedad.strip()
            valor = valor.strip()

            if propiedad == 'Texto' and valor.startswith('{'):
                estilo = ''
                color = ''
                fuente = ''
                tamaño = ''
                texto = ''
                for v in valor[1:-1].split(';'):
                    key, val = v.split(':')
                    if key.strip() == 'texto':
                        texto = val.strip('"')
                    elif key.strip() == 'estilo':
                        estilo = val.strip('"')
                    elif key.strip() == 'color':
                        color = val.strip('"')
                    elif key.strip() == 'fuente':
                        fuente = val.strip('"')
                    elif key.strip() == 'tamaño':
                        tamaño = val.strip('"')
                
                estilo_html = ''
                if estilo == 'cursiva':
                    estilo_html = 'font-style: italic;'
                elif estilo == 'negrita':
                    estilo_html = 'font-weight: bold;'
                elif estilo == 'normal':
                    estilo_html = ''
                
                color_html = f'color: {color};'
                fuente_html = f'font-family: {fuente};'
                tamaño_html = f'font-size: {tamaño}px;'

                html_contenido += f"\t\t<div style=\"{fuente_html} {color_html} {tamaño_html} {estilo_html}\">\n\t\t\t{texto}\n\t\t</div>\n"

            elif propiedad == 'Parrafo' and valor.startswith('{'):
                posicion = ''
                color = ''
                tamaño = ''
                texto = ''
                for v in valor[1:-1].split(';'):
                    key, val = v.split(':')
                    if key.strip() == 'texto':
                        texto = val.strip('"')
                    elif key.strip() == 'posicion':
                        posicion = val.strip('"')
                    elif key.strip() == 'color':
                        color = val.strip('"')
                    elif key.strip() == 'tamaño':
                        tamaño = val.strip('"')
                
                posición_html = ''
                if posicion == 'centro':
                    posición_html = 'text-align: center;'
                elif posicion == 'izquierda':
                    posición_html = 'text-align: left;'
                elif posicion == 'derecha':
                    posición_html = 'text-align: right;'
                
                color_html = f'color: {color};'
                tamaño_html = f'font-size: {tamaño}px;'

                html_contenido += f"\t\t<p style=\"{posición_html} {color_html} {tamaño_html}\">\n\t\t\t{texto}\n\t\t</p>\n"

            elif propiedad == 'Titulo' and valor.startswith('{'):
                posicion = ''
                tamaño = ''
                color = ''
                texto = ''
                for v in valor[1:-1].split(';'):
                    key, val = v.split(':')
                    if key.strip() == 'texto':
                        texto = val.strip('"')
                    elif key.strip() == 'posicion':
                        posicion = val.strip('"')
                    elif key.strip() == 'tamaño':
                        tamaño = val.strip('"')
                    elif key.strip() == 'color':
                        color = val.strip('"')
                
                posición_html = ''
                if posicion == 'centro':
                    posición_html = 'text-align: center;'
                elif posicion == 'izquierda':
                    posición_html = 'text-align: left;'
                elif posicion == 'derecha':
                    posición_html = 'text-align: right;'
                
                tamaño_html = f'font-size: {tamaño}px;'
                color_html = f'color: {color};'

                html_contenido += f"\t\t<h2 style=\"{posición_html} {tamaño_html} {color_html}\">\n\t\t\t{texto}\n\t\t</h2>\n"

    html_contenido += "</div>\n</body>\n</html>"

    with open("html_generado.html", "w") as f:
        f.write(html_contenido)

    return "html_generado.html"


def corregirHTMLGenerado(texto):
    # Separar el texto en bloques de elementos
    bloques = texto.split('},')

    html = "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n\t<meta charset=\"UTF-8\">\n\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t<title>Ejemplo título</title>\n</head>\n<body>\n\t<div>\n\t\t<h1>Ejemplo título</h1>\n"

    for bloque in bloques:
        elementos = bloque.split(',')

        for elemento in elementos:
            partes = elemento.split(':')
            etiqueta = partes[0].strip()
            propiedades = partes[1:]

            if etiqueta == "Texto":
                fuente = ""
                color = ""
                tamaño = ""
                estilo = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'fuente':
                        fuente = val.strip().strip('"')
                    elif key.strip() == 'color':
                        color = val.strip().strip('"')
                    elif key.strip() == 'tamaño':
                        tamaño = val.strip().strip('"')
                    elif key.strip() == 'estilo':
                        estilo = val.strip().strip('"')

                html += f"\t\t<div style=\"font-family: {fuente}; color: {color}; font-size: {tamaño}px; font-style: {estilo};\">{propiedades[-1].strip().strip('"}')}</div>\n"

            elif etiqueta == "Cursiva":
                texto = ""
                color = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'texto':
                        texto = val.strip().strip('"')
                    elif key.strip() == 'color':
                        color = val.strip().strip('"')

                html += f"\t\t<div style=\"font-style: italic; color: {color};\">{texto}</div>\n"

            elif etiqueta == "Fondo":
                color = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'color':
                        color = val.strip().strip('"')

                html += f"\t\t<div style=\"background-color: {color};\"></div>\n"

            elif etiqueta == "Tachado":
                texto = ""
                color = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'texto':
                        texto = val.strip().strip('"')
                    elif key.strip() == 'color':
                        color = val.strip().strip('"')

                html += f"\t\t<del style=\"color: {color};\">{texto}</del>\n"

            elif etiqueta == "Subrayado":
                texto = ""
                color = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'texto':
                        texto = val.strip().strip('"')
                    elif key.strip() == 'color':
                        color = val.strip().strip('"')

                html += f"\t\t<div style=\"text-decoration: underline; color: {color};\">{texto}</div>\n"

            elif etiqueta == "Negrita":
                texto = ""
                color = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'texto':
                        texto = val.strip().strip('"')
                    elif key.strip() == 'color':
                        color = val.strip().strip('"')

                html += f"\t\t<div style=\"font-weight: bold; color: {color};\">{texto}</div>\n"

            elif etiqueta == "Codigo":
                texto = ""
                posicion = ""
                color = ""
                tamaño = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'texto':
                        texto = val.strip().strip('"')
                    elif key.strip() == 'posicion':
                        posicion = val.strip().strip('"')
                    elif key.strip() == 'color':
                        color = val.strip().strip('"')
                    elif key.strip() == 'tamaño':
                        tamaño = val.strip().strip('"')

                html += f"\t\t<pre style=\"font-family: monospace; text-align: {posicion}; color: {color}; font-size: {tamaño}px;\">{texto}</pre>\n"

            elif etiqueta == "Parrafo":
                texto = ""
                posicion = ""
                color = ""
                tamaño = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'texto':
                        texto = val.strip().strip('"')
                    elif key.strip() == 'posicion':
                        posicion = val.strip().strip('"')
                    elif key.strip() == 'color':
                        color = val.strip().strip('"')
                    elif key.strip() == 'tamaño':
                        tamaño = val.strip().strip('"')

                html += f"\t\t<p style=\"font-family: Arial; color: {color}; font-size: {tamaño}px; font-style: normal; text-align: {posicion};\">{texto}</p>\n"

            elif etiqueta == "Titulo":
                texto = ""
                posicion = ""
                tamaño = ""
                color = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'texto':
                        texto = val.strip().strip('"')
                    elif key.strip() == 'posicion':
                        posicion = val.strip().strip('"')
                    elif key.strip() == 'tamaño':
                        tamaño = val.strip().strip('"')
                    elif key.strip() == 'color':
                        color = val.strip().strip('"')

                html += f"\t\t<h2 style=\"text-align: {posicion}; font-size: {tamaño}px; color: {color};\">{texto}</h2>\n"

    html += "\t</div>\n</body>\n</html>"
    
    return html



def imprimirLexemasYErrores(lexemas, errores, textAreaFinal):
    textAreaFinal.delete("1.0", END)
    textAreaFinal.insert(END, "-----------------------------------\n")
    textAreaFinal.insert(END, "Lexemas:\n")
    for lexema in lexemas:
        textAreaFinal.insert(END, f"{lexema.tipo}: {lexema.valor}\n")

    textAreaFinal.insert(END, "-----------------------------------\n")
    textAreaFinal.insert(END, "Errores:\n")
    for error in errores:
        textAreaFinal.insert(END, f"{error.mensaje}\n")


def Traductor():
    root = Tk()
    root.title("Traductor")
    root.geometry("800x600")
    frm = ttk.Frame(root)
    frm.pack(fill=BOTH, expand=True)

    labelInput = ttk.Label(frm, text="Texto de entrada")
    labelInput.grid(row=0, column=0, padx=10, pady=5)

    textAreaInicial = Text(frm, width=50, height=25)
    textAreaInicial.grid(row=1, column=0, padx=10, pady=10)

    labelOutput = ttk.Label(frm, text="Traducción")
    labelOutput.grid(row=0, column=1, padx=10, pady=5)

    textAreaFinal = Text(frm, width=50, height=25)
    textAreaFinal.grid(row=1, column=1, padx=10, pady=10)

    reportArea = Text(frm, width=50, height=5)
    reportArea.grid(row=3, column=0, columnspan=2, padx=2, pady=1)

    buttonFrame = ttk.Frame(frm)
    buttonFrame.grid(row=4, column=0, columnspan=2, pady=10)

    ttk.Button(buttonFrame, text="Abrir Archivo", command=lambda: cargarArchivo(textAreaInicial)).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(buttonFrame, text="Traducir", command=lambda: analizadorLexico(textAreaInicial, textAreaFinal, reportArea)).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(buttonFrame, text="Abrir HTML Generado", command=lambda: abrirHTMLGenerado(textAreaInicial, textAreaFinal)).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(buttonFrame, text="Regresar", command=root.destroy).grid(row=0, column=3, padx=5, pady=5)

    root.mainloop()

def main():
    root = Tk()
    root.title("Menú Principal")
    root.geometry("300x300")
    frm = ttk.Frame(root)
    frm.pack(fill=BOTH, expand=True)
    ttk.Label(frm, text="Nombre: Keitlyn Valentina Tunchez Castañeda").pack(pady=5)
    ttk.Label(frm, text="Carnet: 202201139").pack(pady=5)
    ttk.Label(frm, text="Curso: Lenguajes Formales y de Programación").pack(pady=5)

    buttonFrame = ttk.Frame(frm)
    buttonFrame.pack(pady=90)

    ttk.Button(buttonFrame, text="Abrir Traductor HTML", command=Traductor).pack(side=LEFT, padx=5)
    ttk.Button(buttonFrame, text="Salir", command=root.destroy).pack(side=LEFT, padx=5)

    root.mainloop()

main()
