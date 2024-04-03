from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import webbrowser
import os
from Html import *

lexemas = []
errores = []

# funciones
def obtener_titulo(lexemas):
    texto = None
    posicion = None
    tamanio = None
    color = None
    
    i = 0
    while i < len(lexemas):
        lexema = lexemas[i]
        if lexema.tipo == 'PALABRA':
            if lexema.valor == 'Titulo':
                for siguiente_lexema in lexemas[i+1:]:
                    if siguiente_lexema.tipo == 'CADENA':
                        texto = siguiente_lexema.valor
                        lexemas.pop(lexemas.index(siguiente_lexema))  # Elimina el lexema encontrado
                        break
                if texto:
                    break
            elif lexema.valor == 'texto':
                for siguiente_lexema in lexemas[i+1:]:
                    if siguiente_lexema.tipo == 'CADENA':
                        texto = siguiente_lexema.valor
                        lexemas.pop(lexemas.index(siguiente_lexema))  # Elimina el lexema encontrado
                        break
                if texto:
                    break
            elif lexema.valor == 'posicion':
                for siguiente_lexema in lexemas[i+1:]:
                    if siguiente_lexema.tipo == 'CADENA':
                        posicion = siguiente_lexema.valor
                        lexemas.pop(lexemas.index(siguiente_lexema))  # Elimina el lexema encontrado
                        break
                if posicion:
                    break
            elif lexema.valor == 'tamaño':
                for siguiente_lexema in lexemas[i+1:]:
                    if siguiente_lexema.tipo == 'CADENA':
                        tamanio = siguiente_lexema.valor
                        lexemas.pop(lexemas.index(siguiente_lexema))  # Elimina el lexema encontrado
                        break
                if tamanio:
                    break
            elif lexema.valor == 'color':
                for siguiente_lexema in lexemas[i+1:]:
                    if siguiente_lexema.tipo == 'CADENA':
                        color = siguiente_lexema.valor
                        lexemas.pop(lexemas.index(siguiente_lexema))  # Elimina el lexema encontrado
                        break
                if color:
                    break
        i += 1
                
    if texto is not None and posicion is not None and tamanio is not None and color is not None:
        print(f'Aquí debería ir el texto: {texto}')
        print(f'Aquí debería ir la posición: {posicion}')
        print(f'Aquí debería ir el tamaño: {tamanio}')
        print(f'Aquí debería ir el color: {color}')

        nuevo_titulo = Titulo(texto, posicion, tamanio, color)
        return nuevo_titulo
    else:
        return None
# final funciones
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

    ejemplo_titulo = obtener_titulo(lexemas)
    print(ejemplo_titulo)

    imprimirLexemasYErrores(lexemas, errores, textAreaFinal)
    reportArea.delete("1.0", END)
    reportArea.insert(END, caracteres_invalidos)


def cargarArchivo(textArea):

    archivo = filedialog.askopenfilename(filetypes=[("Archivo de texto", "*.txt, *.html")])

    if archivo:
        with open(archivo, 'r', encoding="utf-8") as f:
            contenido = f.read()

        textArea.delete("1.0", END)
        textArea.insert(END, contenido)


def Traductor():
    root = Tk()
    root.title("Traductor")
    root.geometry("800x700")
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
    root.geometry("400x400")
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


