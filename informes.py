from datetime import datetime

from PyQt6 import QtSql
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.pdfbase import pdfmetrics

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
import var
import os, shutil

class Informes:
    pageWidth = 595.27

    @staticmethod
    def reportPropiedades(muniSeleccionado,listaPropiedades):
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)

            fecha = datetime.today()
            fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
            nomepdfcli = fecha + "_listadoPropiedades_"+ muniSeleccionado +".pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)  # también esto
            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado Propiedades de "+ muniSeleccionado
            Informes.topInforme(titulo)
            Informes.footInforme(titulo)
            items = ['CÓDIGO', 'DIRECCIÓN', 'TIPO OPERACIÓN', 'PRECIO ALQUILER', 'PRECIO VENTA']
            var.report.setFont('Helvetica-Bold', size=10)

            anchoCodigo = pdfmetrics.stringWidth(items[0], 'Helvetica-Bold', 10)
            var.report.drawString(50, 650, str(items[0]))

            #var.report.drawString(55, 650, str(items[0]))
            var.report.drawString(100, 650, str(items[1]))
            var.report.drawString(190, 650, str(items[2]))
            var.report.drawString(280, 650, str(items[3]))
            var.report.drawString(360, 650, str(items[4]))
            var.report.line(50, 645, 525, 645)

            query = QtSql.QSqlQuery()
            query.prepare("SELECT dnicli, apecli, nomecli, movilcli, provcli, municli FROM clientes order by apecli")
            if query.exec():
                x = 55
                y = 630
                while query.next():
                    if y <= 90:
                        var.report.setFont("Helvetica-Oblique", size=7)

                        var.report.drawString(450, 80, "Pagina siguiente")
                        var.report.showPage()

                        Informes.footInforme(titulo)
                        Informes.topInforme(titulo)

                        items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 650, str(items[0]))
                        var.report.drawString(100, 650, str(items[1]))
                        var.report.drawString(190, 650, str(items[2]))
                        var.report.drawString(280, 650, str(items[3]))
                        var.report.drawString(360, 650, str(items[4]))
                        var.report.drawString(450, 650, str(items[5]))
                        var.report.line(50, 645, 525, 645)

                        var.report.setFont("Helvetica", size=7)
                        x = 55
                        y = 630

                    var.report.setFont("Helvetica", size=7)
                    dni = '***' + str(query.value(0)[4:7] + '***')
                    var.report.drawCentredString(x + 10, y, str(dni))
                    var.report.drawString(x + 45, y, str(query.value(1)))
                    var.report.drawString(x + 135, y, str(query.value(2)))
                    var.report.drawString(x + 225, y, str(query.value(3)))
                    var.report.drawString(x + 305, y, str(query.value(4)))
                    var.report.drawString(x + 395, y, str(query.value(5)))

                    y = y - 20

            var.report.save()
            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)
        except Exception as e:
            print("Error generando informe propiedades",e)

    @staticmethod
    def reportClientes(self):
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today()
            fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
            nomepdfcli = fecha + "_listadoclientes.pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)  # también esto
            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado Clientes"
            Informes.topInforme(titulo)
            Informes.footInforme(titulo)
            items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(55, 650, str(items[0]))
            var.report.drawString(100, 650, str(items[1]))
            var.report.drawString(190, 650, str(items[2]))
            var.report.drawString(280, 650, str(items[3]))
            var.report.drawString(360, 650, str(items[4]))
            var.report.drawString(450, 650, str(items[5]))
            var.report.line(50, 645, 525, 645)

            query = QtSql.QSqlQuery()
            query.prepare("SELECT dnicli, apecli, nomecli, movilcli, provcli, municli FROM clientes order by apecli")
            if query.exec():
                nRegistros = query.size()
                print("Nregistros",nRegistros)

                x=55
                y=630
                while query.next():
                    if y <= 90:
                        var.report.setFont("Helvetica-Oblique", size=7)

                        var.report.drawString(450,80, "Pagina siguiente")
                        var.report.showPage()

                        Informes.footInforme(titulo)
                        Informes.topInforme(titulo)

                        items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 650, str(items[0]))
                        var.report.drawString(100, 650, str(items[1]))
                        var.report.drawString(190, 650, str(items[2]))
                        var.report.drawString(280, 650, str(items[3]))
                        var.report.drawString(360, 650, str(items[4]))
                        var.report.drawString(450, 650, str(items[5]))
                        var.report.line(50, 645, 525, 645)

                        var.report.setFont("Helvetica", size=7)
                        x = 55
                        y = 630


                    var.report.setFont("Helvetica", size=7)
                    dni = '***' + str(query.value(0)[4:7] + '***')
                    var.report.drawCentredString(x+10 , y, str(dni))
                    var.report.drawString(x +45, y,str(query.value(1)))
                    var.report.drawString(x +135, y,str(query.value(2)))
                    var.report.drawString(x +225, y,str(query.value(3)))
                    var.report.drawString(x +305, y,str(query.value(4)))
                    var.report.drawString(x +395, y,str(query.value(5)))

                    y=y-20



            var.report.save()
            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)

        except Exception as error:
            print(error)

    def topInforme(titulo):
        try:
            ruta_logo = '.\\img\\house.svg'
            logo = svg2rlg(ruta_logo)

            test_drawing = Drawing(40, 40)

            test_drawing.add(Rect(0, 0, 40, 40, fillColor="red"))
            # Asegúrate de que el objeto 'logo' sea de tipo 'PngImageFile'
            if isinstance(logo, Drawing):
                logo.width=40
                logo.height=40

                var.report.line(50, 800, 525, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 782, 'Inmobiliaria Teis')

                widthTitulo = pdfmetrics.stringWidth(titulo,'Helvetica-Bold',14 )
                var.report.drawString((Informes.pageWidth - widthTitulo)/2, 675, titulo)

                var.report.line(50, 663, 525, 663)

                # Dibuja la imagen en el informe
                renderPDF.draw(logo, var.report, x=450, y=725)
                #renderPDF.draw(test_drawing, var.report, x=480, y=725)


                var.report.setFont('Helvetica', size=9)
                var.report.drawString(55, 767, 'CIF: A12345678')
                var.report.drawString(55, 752, 'Avda. Galicia - 101')
                var.report.drawString(55, 737, 'Vigo - 36216 - España')
                var.report.drawString(55, 722, 'Teléfono: 986 132 456')
                var.report.drawString(55, 707, 'e-mail: cartesteisr@mail.com')
            else:
                print(f'Error: No se pudo cargar la imagen en {ruta_logo}')
        except Exception as error:
            print('Error en cabecera informe:', error)

    def footInforme(titulo):
        try:
            total_pages = 0
            var.report.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s' % var.report.getPageNumber()))

        except Exception as error:
            print('Error en pie informe de cualquier tipo: ', error)
