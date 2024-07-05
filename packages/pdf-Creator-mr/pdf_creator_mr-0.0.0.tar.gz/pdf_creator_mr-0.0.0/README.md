# -*- coding: utf-8 -*-
# PDF pdf-Creator-mr

Uma biblioteca simples para criação de PDFs em Python.
A simple library for creating PDFs in Python.
Una biblioteca simple para crear PDFs en Python.

## Instalação - Install

```sh
pip install reportlab



################################English################################
The PDFCreator class facilitates the creation of PDF documents using the ReportLab library in Python.

#Constructor
def __init__(self, filename, width=A4[0], height=A4[1]):
    """
    Initializes a PDFCreator object.

    :param filename: Name of the PDF file to create.
    :param width: Width of the PDF page (default is A4 width).
    :param height: Height of the PDF page (default is A4 height).
    """
Methods
    *add_title(title, fontsize=24, x=None, y=None)
        -Adds a title to the PDF.
    *add_paragraph(text, fontsize=12, spacing=0.5*inch, x=0, y=0)
        -Adds a paragraph of text to the PDF.
    *add_image(image_path, x=inch, y=None, width=2inch, height=2inch)
        -Adds an image to the PDF.
    *add_separator(thickness=1, start_x=inch, y_position=None, width=None)
        -Adds a horizontal separator line to the PDF.
    *add_vertical_line(start_y, end_y, x, thickness=1)
        -Adds a vertical line to the PDF.
    *add_square(width, height, x=inch, y=None)
        -Adds a square or rectangle shape to the PDF.
    *add_multiples_squares(squares, width=None, height=None, x=inch, y=inch)
        -Adds multiple squares or rectangles to the PDF.
    *save()
        -Saves the PDF document.

################################PORTUGUES################################
A classe PDFCreator facilita a criação de documentos PDF utilizando a biblioteca ReportLab em Python.
#Construtor

def __init__(self, filename, width=A4[0], height=A4[1]):
    """
    Inicializa um objeto PDFCreator.

    :param filename: Nome do arquivo PDF a ser criado.
    :param width: Largura da página do PDF (padrão é a largura do A4).
    :param height: Altura da página do PDF (padrão é a altura do A4).
    """
Métodos
    *add_title(title, fontsize=24, x=None, y=None)
        -Adiciona um título ao PDF.
    *add_paragraph(text, fontsize=12, spacing=0.5*inch, x=0, y=0)
        -Adiciona um parágrafo de texto ao PDF.
    *add_image(image_path, x=inch, y=None, width=2inch, height=2inch)    
        -Adiciona uma imagem ao PDF.
    *add_separator(thickness=1, start_x=inch, y_position=None, width=None)
        -Adiciona uma linha separadora horizontal ao PDF.
    *add_vertical_line(start_y, end_y, x, thickness=1)
        -Adiciona uma linha vertical ao PDF.    
    *add_square(width, height, x=inch, y=None)
        -Adiciona um quadrado ou retângulo ao PDF.
    *add_multiples_squares(squares, width=None, height=None, x=inch, y=inch)
        -Adiciona múltiplos quadrados ou retângulos ao PDF.
    *save()
        -Salva o documento PDF.

################################Español################################
La clase PDFCreator facilita la creación de documentos PDF utilizando la biblioteca ReportLab en Python.

#Constructor
def __init__(self, filename, width=A4[0], height=A4[1]):
    """
    Inicializa un objeto PDFCreator.

    :param filename: Nombre del archivo PDF a crear.
    :param width: Ancho de la página del PDF (por defecto es el ancho de A4).
    :param height: Altura de la página del PDF (por defecto es la altura de A4).
    """

Métodos
    *add_title(title, fontsize=24, x=None, y=None)
        -Añade un título al PDF.
    *add_paragraph(text, fontsize=12, spacing=0.5*inch, x=0, y=0)
        -Añade un párrafo de texto al PDF.
    *add_image(image_path, x=inch, y=None, width=2inch, height=2inch)
        -Añade una imagen al PDF.
    *add_separator(thickness=1, start_x=inch, y_position=None, width=None)
        -Añade una línea separadora horizontal al PDF.
    *add_vertical_line(start_y, end_y, x, thickness=1)
        -Añade una línea vertical al PDF.
    *add_square(width, height, x=inch, y=None)
        -Añade un cuadrado o rectángulo al PDF.
    *add_multiples_squares(squares, width=None, height=None, x=inch, y=inch)
        -Añade múltiples cuadrados o rectángulos al PDF.
    *save()
        -Guarda el documento PDF.