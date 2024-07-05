import unittest
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from pdf_creator import PDFCreator  # Certifique-se de que o nome do seu arquivo principal seja pdf_creator.py

class TestPDFCreator(unittest.TestCase):

    def setUp(self):
        # Cria um nome de arquivo temporário para o teste
        self.filename = "test_output.pdf"
        self.pdf = PDFCreator(self.filename)

    def test_add_title(self):
        # Testa se o título é adicionado corretamente
        self.pdf.add_title("Teste de Título")
        self.pdf.save()
        self.assertTrue(os.path.exists(self.filename))

    def test_add_paragraph(self):
        # Testa se o parágrafo é adicionado corretamente
        self.pdf.add_paragraph("Este é um parágrafo de exemplo. Você pode adicionar múltiplas linhas de texto.")
        self.pdf.save()
        self.assertTrue(os.path.exists(self.filename))

    def test_add_image(self):
        # Testa se a imagem é adicionada corretamente
        # Use uma imagem de exemplo que esteja no mesmo diretório ou forneça um caminho válido
        image_path = "example.jpg"  # Substitua pelo caminho da sua imagem
        if os.path.exists(image_path):
            self.pdf.add_image(image_path)
            self.pdf.save()
            self.assertTrue(os.path.exists(self.filename))

    def test_add_separator(self):
        # Testa se o separador é adicionado corretamente
        self.pdf.add_paragraph("Parágrafo com separador abaixo.").add_separator(thickness=2)
        self.pdf.save()
        self.assertTrue(os.path.exists(self.filename))

    def tearDown(self):
        # Remove o arquivo após o teste
        if os.path.exists(self.filename):
            os.remove(self.filename)

if __name__ == "__main__":
    unittest.main()
