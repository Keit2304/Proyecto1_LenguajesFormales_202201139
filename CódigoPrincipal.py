from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import webbrowser
import os

lexemas = []
errores = []
caracteres_invalidos = "!¡@#%$\\[\\]{ }^&*()_+:;¿?<>,"

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
    global lexemas
    global errores
    global caracteres_invalidos

    # Limpiamos las listas de lexemas y errores
    lexemas.clear()
    errores.clear()
   
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
    
    imprimirLexemasYErrores(lexemas, errores, textAreaFinal)
    generarTablaErrores(errores)
    generarTablaLexemas(lexemas)
    reportArea.delete("1.0", END)  # Limpiar el área de texto
    reportArea.insert(END, f"Caracteres no válidos: {caracteres_invalidos}")


def generarTablaErrores(errores):
    if errores:
        # Abre el archivo HTML en modo escritura
        with open("tabla_errores.html", "w", encoding="utf-8") as f:
            # Escribe el encabezado del archivo HTML
            f.write("<!DOCTYPE html>\n")
            f.write(f'<html lang="es">\n')
            f.write("<head>\n")
            f.write("<title>Tabla de Errores</title>\n")
            f.write("</head>\n")
            f.write("<body>\n")
            f.write("<h1>Tabla de Errores</h1>\n")
            
            # Escribe la tabla HTML
            f.write("<table border='1'>\n")
            f.write("<tr><th>Caracter</th><th>Fila</th><th>Columna</th></tr>\n")
            
            # Escribe cada fila de la tabla con la información de los errores
            for error in errores:
                f.write(f"<tr><td>{error.mensaje}</td><td>{error.fila}</td><td>{error.columna}</td></tr>\n")
            
            # Cierra la tabla y el archivo HTML
            f.write("</table>\n")
            f.write("</body>\n")
            f.write("</html>\n")

def generarTablaLexemas(lexemas):
    with open("tabla_lexemas.html", "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n")
        f.write(f'<html lang="es">\n')
        f.write("<head>\n")
        f.write("<title>Tabla de Lexemas</title>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write("<h1>Tabla de Lexemas</h1>\n")
        f.write("<table border='1'>\n")
        f.write("<tr><th>Token</th><th>Lexema</th><th>Fila</th><th>Columna</th></tr>\n")
        for lexema in lexemas:
            f.write(f"<tr><td>{lexema.tipo}</td><td>{lexema.valor}</td><td>{lexema.fila}</td><td>{lexema.columna}</td></tr>\n")
        f.write("</table>\n")
        f.write("</body>\n")
        f.write("</html>\n")

def cargarArchivo(textArea):
    archivo = filedialog.askopenfilename(filetypes=[("Archivo de texto", "*.txt, *.html")])

    if archivo:
        with open(archivo, 'r') as f:
            contenido = f.read()

        textArea.delete("1.0", END)
        textArea.insert(END, contenido)

def enviarTexto(textAreaInicial):
    texto = textAreaInicial.get("1.0", "end")
    # Aquí deberías enviar el texto al servidor y obtener el código HTML traducido
    # Supongamos que la variable html_contenido contiene el código HTML traducido
    html_contenido = "<html><head><title>HTML Traducido</title></head><body><p>Este es el contenido traducido</p></body></html>"
    return html_contenido

def generarHTML(textAreaInicial):
    texto = textAreaInicial.get("1.0", "end")
    caracteres_invalidos = analizadorLexico(texto)
    # Reemplazar los caracteres no válidos en el texto original
    for char in caracteres_invalidos:
        texto = texto.replace(char, '')
    return texto

def abrirHTMLGenerado(textAreaInicial, textAreaFinal):
    texto = textAreaInicial.get("1.0", "end")
    # Corregir el HTML generado
    html_corregido = corregirHTMLGenerado(texto)
    # Mostrar el HTML corregido en el textAreaFinal
    textAreaFinal.delete("1.0", END)
    textAreaFinal.insert(END, html_corregido)

def generar_estilo(propiedad, valor):
    if propiedad == "fuente":
        return f"font-family: {valor}; "
    elif propiedad == "color":
        return f"color: {valor}; "
    elif propiedad == "tamaño":
        return f"font-size: {valor}px; "
    elif propiedad == "estilo":
        if valor == "negrita":
            return "font-weight: bold; "
        elif valor == "cursiva":
            return "font-style: italic; "
    elif propiedad == "posicion":
        if valor == "centro":
            return "text-align: center; "
        elif valor == "izquierda":
            return "text-align: left; "
        elif valor == "derecha":
            return "text-align: right; "
    elif propiedad == "fondo":
        return f"background-color: {valor}; "
    elif propiedad == "del":
        return f"text-decoration: line-through; color: {valor}; "
    elif propiedad == "subrayado":
        return f"text-decoration: underline; color: {valor}; "
    return ""


def corregirHTMLGenerado(texto):
    # Separar el texto en bloques de elementos
    bloques = texto.split('},')

    html = "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n\t<meta charset=\"UTF-8\">\n\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t<title>Ejemplo título</title>\n</head>\n<body>\n\t<div>\n\t\t<h1>Ejemplo título</h1>\n"

    for bloque in bloques:
        elementos = bloque.split(',')

        etiqueta = elementos[0].split(':')[-1].strip().capitalize()

        html += f"\t\t<div>\n\t\t<{etiqueta} style=\""

        for elemento in elementos[1:]:
            partes = elemento.split(':')
            propiedad = partes[0].strip()
            valor = partes[1].strip().strip('"')

            if propiedad == "texto":
                html += f">{valor}</{etiqueta}>\n\t\t</div>\n\t\t<div>\n\t\t<{etiqueta} style=\""
            else:
                html += generar_estilo(propiedad, valor)

        html += "\t\t</div>\n"

    html += "</body>\n</html>"
    
    return html


texto = '''Inicio:{
    Encabezado:{
        TituloPagina:"Ejemplo titulo";
    },
    Cuerpo:[
        Texto:{
            fuente:"Arial";
            color:"azul";
            tamaño:"11";
            estilo:"normal";
        },
        Cursiva:{
            texto:"Este es un texto en cursiva.";
            color:"azul";
        },
        Fondo:{
            color:"#FFA07A";
        },
        Tachado:{
            texto:"Este es un texto tachado.";
            color:"rojo";
        }
    ]
}'''

html_corregido = corregirHTMLGenerado(texto)
print(html_corregido) 


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

    reportLabel = ttk.Label(frm, text="Caracteres no válidos:")
    reportLabel.grid(row=2, column=0, padx=10, pady=5)

    reportArea = Text(frm, width=50, height=5)
    reportArea.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
    reportArea.insert(END, f"Caracteres no válidos: {caracteres_invalidos}")

    buttonFrame = ttk.Frame(frm)
    buttonFrame.grid(row=4, column=0, columnspan=2, pady=10)

    ttk.Button(buttonFrame, text="Abrir Archivo", command=lambda: cargarArchivo(textAreaInicial)).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(buttonFrame, text="Traducir", command=lambda: analizadorLexico(textAreaInicial, textAreaFinal, reportArea)).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(buttonFrame, text="Abrir HTML Generado", command=lambda: abrirHTMLGenerado(textAreaInicial, textAreaFinal)).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(buttonFrame, text="Regresar", command=root.destroy).grid(row=0, column=3, padx=5, pady=5)
    root.mainloop()

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
