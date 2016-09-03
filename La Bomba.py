# #!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""BackUp automático con calendario."""

from os.path import expanduser
import os
import schedule
import shutil
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from backup import Ui_MainWindow

# import datetime
# from datetime import datetime as dt
# from datetime import timedelta
# import re

class MainWindow(QMainWindow, Ui_MainWindow):
    """Clase para la ventana principal de la aplicacion."""

    def __init__(self, parent=None):
        """Inicializacion ventana principal y conexiones de funciones."""
        super(MainWindow, self).__init__(parent)
        QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.pushCopiar.clicked.connect(self.BackUp)
        self.ui.pushProgramar.clicked.connect(self.Calendario)
        self.ui.radioCada.clicked.connect(self.programarTiempo)
        self.ui.radioDiario.clicked.connect(self.programarTiempo)
        self.ui.toolDestino.clicked.connect(self.AbrirDestino)
        self.ui.toolOrigen.clicked.connect(self.AbrirOrigen)

        
        self.statusBar().showMessage("Listo")
        
    def AbrirDestino(self):
        """Abre el menu de dialogo para seleccionar la carpeta de destino."""
        dirDestino = QFileDialog.getExistingDirectory(self, 'Directorio destino',
                                                      expanduser("~"), QFileDialog.ShowDirsOnly)
        if os.path.isdir(dirDestino):
            self.ui.lineDestino.setText(dirDestino)
    
    def AbrirOrigen(self):
        """Abre el menu de dialogo para seleccionar la carpeta de origen."""
        dirOrigen = QFileDialog.getExistingDirectory(self, 'Directorio origen',
                                                     expanduser("~"), QFileDialog.ShowDirsOnly)
        if os.path.isdir(dirOrigen):
            self.ui.lineOrigen.setText(dirOrigen)

    def BackUp(self):
        """Copia los archivos/directorio elegido como origen en el directorio elegido como destino."""
        copiados = 0
        total = 0
        archivosOrigen = os.listdir(self.ui.lineOrigen.text())
        # total = len(archivosOrigen)
        # for archivo in archivosOrigen:
        #     rutaCompletaArchivo = os.path.join(self.ui.lineOrigen.text(), archivo)
        #     if (os.path.isfile(rutaCompletaArchivo)):
        #         shutil.copy2(rutaCompletaArchivo, self.ui.lineDestino.text())
        #         copiados += 1
        shutil.copytree(self.ui.lineOrigen.text(), self.ui.lineDestino.text())
        if total == copiados:
            estado = 'Se copiaron con éxito ' + str(copiados) + ' archivos'
        else:
            estado = 'De un total de ' + str(total) + ' archivos, solo se copiaron ' + str(copiados)
        self.statusBar().showMessage(estado)
    
    def ThreadBackground(self):
        schedule.run_pending()
        time.sleep(1)

    def Calendario(self):
        horario = str(self.ui.timeDiario.time().hour()) + ':' + str(self.ui.timeDiario.time().minute())
        schedule.every().day.at(horario).do(self.BackUp)
        schedule.run_pending()

    def programarTiempo(self):
        pass


def run():
    """Ejecucion de la parte grafica del programa."""
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

try:
    run()

except Exception as e:
    print("Error: " + str(e))
