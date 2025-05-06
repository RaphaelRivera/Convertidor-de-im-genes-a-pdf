import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas 
from PIL import Image 
import os 

# Clase principal del convertidor

class ConvertidorImagenPdf:
    def __init__(self,ventana):
        self.ventana=ventana
        self.ruta_imagenes=[]
        self.nombreDelpdf=tk.StringVar()
        self.lista_imagenes=tk.Listbox(ventana,selectmode=tk.MULTIPLE)

        self.crear_interfaz()

# Crea los elementos de la ventana 
    def crear_interfaz(self):
        titulo=tk.Label(self.ventana,text="Convertidor de Imágenes a PDF",font=("Helvetica",16,"bold"))
        titulo.pack(pady=10)

        boton_seleccionar=tk.Button(self.ventana,text="Seleccionar Imágenes", command=self.seleccionar_imagenes)
        boton_seleccionar.pack(pady=(0,10))

        self.lista_imagenes.pack(pady=(0,10),fill=tk.BOTH,expand=True)

        etiqueta_nombre=tk.Label(self.ventana,text="Escribe el nombre del archivo PDF:")
        etiqueta_nombre.pack()
        entrada_nombre=tk.Entry(self.ventana,textvariable=self.nombreDelpdf, width=40, justify="center")
        entrada_nombre.pack()

        boton_convertir=tk.Button(self.ventana,text="Convertir",command=self.convertir_a_pdf)
        boton_convertir.pack(pady=(20,40))

        guardado=tk.Label(self.ventana,text="Su archivo se guardará en su carpeta de descargas",font=("Helvetica",10,"italic"))
        guardado.pack(pady=5)


        
#Selecciona las imágenes del equipo
    def seleccionar_imagenes(self):
        self.ruta_imagenes=filedialog.askopenfilenames(title="Seleccionar Imágenes", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        self.actualizar_lista_imagenes()

#Muestra la lista de imágenes seleccionadas
    def actualizar_lista_imagenes(self):
        self.lista_imagenes.delete(0, tk.END)
        for ruta in self.ruta_imagenes:
            _, nombre=os.path.split(ruta)
            self.lista_imagenes.insert(tk.END,nombre)

#Convierte las imágenes a pdf
    def convertir_a_pdf(self):
        
        if not self.ruta_imagenes:
            return
        
        # Obtener la carpeta "Descargas" del usuario
        carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")  # Obtener la ruta de la carpeta Descargas
        if not os.path.exists(carpeta_descargas):
            os.makedirs(carpeta_descargas)  # Crear la carpeta si no existe
            
        nombre_salida=self.nombreDelpdf.get()+".pdf" if self.nombreDelpdf.get() else "salida.pdf"
        ruta_salida = os.path.join(carpeta_descargas, nombre_salida)
        pdf=canvas.Canvas(ruta_salida,pagesize=(612,792))

        for ruta in self.ruta_imagenes:
            imagen=Image.open(ruta)
            ancho_disponible=540
            alto_disponible=720
            escala=min(ancho_disponible/imagen.width, alto_disponible/imagen.height)
            ancho_nuevo=imagen.width*escala
            alto_nuevo=imagen.height*escala
            x_centro=(612-ancho_nuevo)/2
            y_centro=(792-alto_nuevo)/2
            pdf.setFillColorRGB(255,255,255)
            pdf.rect(0,0,612,792,fill=True)
            pdf.drawInlineImage(imagen,x_centro,y_centro,ancho_nuevo,alto_nuevo)
            pdf.showPage()
        pdf.save()
 

# Función principal
def iniciar_app():
    ventana=tk.Tk()
    ventana.title("Convertidor")
    app=ConvertidorImagenPdf(ventana)
    ventana.geometry("400x600")
    ventana.mainloop()


# Ejectuar el programa
if __name__=="__main__":
    iniciar_app()