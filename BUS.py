# #!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""BackUpSimple, BackUp automático con calendario."""

from os.path import expanduser
import os
import schedule
import shutil
import sys
from datetime import date

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

GUI = os.getcwd() + '/GUI'

from GUI.backup import Ui_MainWindow


global dirOrigen
global dirDestino
global fecha

fecha = date.today()
dirOrigen = expanduser(os.getcwd())
dirDestino = expanduser(os.getcwd()) + '/' + fecha.strftime("%d-%m-%y")


class MainWindow(QMainWindow, Ui_MainWindow):
    """Clase para la ventana principal de la aplicacion."""

    def __init__(self, parent=None):
        """Inicializacion ventana principal y conexiones de funciones."""
        super(MainWindow, self).__init__(parent)
        QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ThreadBackground = ThreadBackground()
        
        self.ui.pushCopiar.clicked.connect(self.BackUp)
        self.ui.pushProgramar.clicked.connect(self.Calendario)
        self.ui.radioCada.clicked.connect(self.programarTiempo)
        self.ui.radioDiario.clicked.connect(self.programarTiempo)
        self.ui.toolDestino.clicked.connect(self.AbrirDestino)
        self.ui.toolOrigen.clicked.connect(self.AbrirOrigen)

        self.ui.lineOrigen.setText(dirOrigen)
        self.ui.lineDestino.setText(dirDestino)
        self.statusBar().showMessage("Listo")
        self.Calendario()
        
    def AbrirDestino(self):
        """Abre el menu de dialogo para seleccionar la carpeta de destino."""
        dirDestino = QFileDialog.getExistingDirectory(self, 'Directorio destino',
                                                      expanduser(os.getcwd()), QFileDialog.ShowDirsOnly)
        if os.path.isdir(dirDestino):
            dirDestino = dirDestino + '/' + fecha.strftime("%d-%m-%y")
            self.ui.lineDestino.setText(dirDestino)
    
    def AbrirOrigen(self):
        """Abre el menu de dialogo para seleccionar la carpeta de origen."""
        dirOrigen = QFileDialog.getExistingDirectory(self, 'Directorio origen',
                                                     expanduser(os.getcwd()), QFileDialog.ShowDirsOnly)
        if os.path.isdir(dirOrigen):
            self.ui.lineOrigen.setText(dirOrigen)

    def BackUp(self):
        """Copia los archivos/directorio elegido como origen en el directorio elegido como destino."""
        try:
            self.statusBar().showMessage("Copiando...")
            shutil.copytree(self.ui.lineOrigen.text(), self.ui.lineDestino.text())
            self.statusBar().showMessage("Se copiaron con éxito todos los archivos")
        except Exception as e:
            self.statusBar().showMessage("Error intentando copiar. " + str(e))
            with open('error.txt', 'a') as registro:
                registro.write(str(e))

    def Calendario(self):
        """Genera el evento de BackUp diario, inicia el thread de control continuo."""
        horario = str(self.ui.timeDiario.time().hour()) + ':' + str(self.ui.timeDiario.time().minute())
        schedule.every().day.at(horario).do(self.BackUp)
        self.ThreadBackground.start()
        self.statusBar().showMessage("BackUp diario programado")

    def programarTiempo(self):
        pass


class ThreadBackground(QThread):
    """Thread de ejecución continua para la realización de tareas de BackUp pendientes."""
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while(True):
            schedule.run_pending()
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
    with open('error.txt', 'a') as registro:
        registro.write(str(e))
