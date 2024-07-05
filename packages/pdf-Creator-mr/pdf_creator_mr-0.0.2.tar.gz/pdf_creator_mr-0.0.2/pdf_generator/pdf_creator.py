from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas

class PDFCreator:
    def __init__(self, filename, width=A4[0], height=A4[1]):
        self.filename = filename
        self.canvas = canvas.Canvas(filename, pagesize=(width, height))
        self.width = width
        self.height = height
        self.cursor_y = height - inch  
        self.last_text_width = 0  

    def add_title(self, title, fontsize=24, x=None, y=None):
        x *= inch  
        y *= inch  
        self.canvas.setFont("Helvetica-Bold", fontsize)
        if y is not None:
            self.cursor_y = y
        if x is None:
            x = self.width / 2.0
        self.canvas.drawCentredString(x, self.cursor_y, title)
        self.cursor_y -= 1 * inch
        return self

    def add_paragraph(self, text, fontsize=12, spacing=0.5*inch, x=0, y=0):
        x *= inch  
        y *= inch  
        self.canvas.setFont("Helvetica", fontsize)
        if y is not None:
            self.cursor_y = y
        if x is None:
            x = inch
        text_object = self.canvas.beginText(x, self.cursor_y)
        text_object.setTextOrigin(x, self.cursor_y)
        text_object.textLines(text)
        self.canvas.drawText(text_object)
        self.cursor_y -= spacing 
        self.last_text_width = self.canvas.stringWidth(text, "Helvetica", fontsize)
        return self

    def add_image(self, image_path, x=inch, y=None, width=2*inch, height=2*inch):
        x *= inch  
        y *= inch  
        if y is None:
            y = self.cursor_y - height - inch
        self.canvas.drawImage(image_path, x, y, width, height)
        self.cursor_y = y
        return self

    def add_separator(self, thickness=1, start_x=inch, y_position=None, width=None):
        if y_position is None:
            y_position = self.cursor_y - 0.3 * inch
        if width is None:
            width = self.width - 2 * inch

        self.canvas.setLineWidth(thickness)
        self.canvas.line(start_x, y_position, start_x + width, y_position)
        self.cursor_y = y_position - 0.3 * inch  
        return self
    def add_vertical_line(self, start_y, end_y, x, thickness=1):
        x *= inch  
        start_y *= inch  
        end_y *= inch  
        
        self.canvas.setLineWidth(thickness)
        self.canvas.line(x, start_y, x, end_y)
        return self
    
    def add_square(self, width, height, x=inch, y=None):
        x *= inch 
        y *= inch  
        width=width*inch
        height=height*inch
        if y is None:
            y = self.cursor_y - height
        self.canvas.rect(x, y, width, height)
        self.cursor_y = y - 0.3 * inch  
        return self
    
    def add_multiples_squares(self, squares, width=None, height=None, x=inch, y=inch):
        x *= inch 
        y *= inch  
        
        if width is None:
            width = 1 * inch 
        if height is None:
            height = 1 * inch  
        
        for sq_x, sq_y, sq_width, sq_height in squares:
            self.canvas.rect(x + sq_x * inch, y - sq_y * inch, sq_width * inch, sq_height * inch)
            self.cursor_y -= sq_height * inch + 0.1 * inch  
        return self
    def save(self):
        self.canvas.save()
        return self