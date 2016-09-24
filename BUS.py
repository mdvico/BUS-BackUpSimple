# #!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""BackUpSimple, BackUp automático con calendario."""

from os.path import expanduser
import os
import schedule
import shutil
import sys
import threading
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from backup import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    """Clase para la ventana principal de la aplicacion."""

    def __init__(self, parent=None):
        """Inicializacion ventana principal y conexiones de funciones."""
        super(MainWindow, self).__init__(parent)
        QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.threadBackground = threadBackground()
        
        self.ui.pushCopiar.clicked.connect(self.BackUp)
        self.ui.pushProgramar.clicked.connect(self.Calendario)
        self.ui.radioCada.clicked.connect(self.programarTiempo)
        self.ui.radioDiario.clicked.connect(self.programarTiempo)
        self.ui.toolDestino.clicked.connect(self.AbrirDestino)
        self.ui.toolOrigen.clicked.connect(self.AbrirOrigen)

        self.ui.lineOrigen.setText(str(os.getcwd()))
        self.ui.lineDestino.setText(str(os.getcwd()))
        self.statusBar().showMessage("Listo")
        
    def AbrirDestino(self):
        """Abre el menu de dialogo para seleccionar la carpeta de destino."""
        dirDestino = QFileDialog.getExistingDirectory(self, 'Directorio destino',
                                                      expanduser(os.getcwd()), QFileDialog.ShowDirsOnly)
        if os.path.isdir(dirDestino):
            self.ui.lineDestino.setText(dirDestino)
    
    def AbrirOrigen(self):
        """Abre el menu de dialogo para seleccionar la carpeta de origen."""
        dirOrigen = QFileDialog.getExistingDirectory(self, 'Directorio origen',
                                                     expanduser(os.getcwd()), QFileDialog.ShowDirsOnly)
        if os.path.isdir(dirOrigen):
            self.ui.lineOrigen.setText(dirOrigen)

    def BackUp(self):
        """Copia los archivos/directorio elegido como origen en el directorio elegido como destino."""
        # copiados = 0
        # total = 0
        # archivosOrigen = os.listdir(self.ui.lineOrigen.text())
        # total = len(archivosOrigen)
        # for archivo in archivosOrigen:
        #     rutaCompletaArchivo = os.path.join(self.ui.lineOrigen.text(), archivo)
        #     if (os.path.isfile(rutaCompletaArchivo)):
        #         shutil.copy2(rutaCompletaArchivo, self.ui.lineDestino.text())
        #         copiados += 1
        # if total == copiados:
        #     estado = 'Se copiaron con éxito ' + str(copiados) + ' archivos'
        # else:
        #     estado = 'De un total de ' + str(total) + ' archivos, solo se copiaron ' + str(copiados)
        # self.statusBar().showMessage(estado)
        shutil.copytree(self.ui.lineOrigen.text(), self.ui.lineDestino.text())

    def Calendario(self):
        horario = str(self.ui.timeDiario.time().hour()) + ':' + str(self.ui.timeDiario.time().minute())
        # print(horario)
        schedule.every().day.at(horario).do(self.BackUp)
        # print("BackUp programado")
        self.threadBackground.start()
        self.statusBar().showMessage("BackUp diario programado")

    def programarTiempo(self):
        pass

class threadBackground(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while(True):
            # print("Esperando...")
            schedule.run_pending()
            # print("Esperandoooo")
            self.sleep(1)


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
