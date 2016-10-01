from subprocess import call
import os

print("Script de generación de todos los archivos ejecutables para las distintas plataformas haciendo uso de PyInstaller. Solo se puede generar el ejecutable para el SO desde el que se este realizando la ejecución del script.")

if os.name == 'nt':
    call(["pyinstaller", "--onefile", "--noconsole", "BUS.py", "./Ejecutables/Windows/"]) 
elif os.name == 'posix':
    call(["pyinstaller", "--onefile", "--noconsole", "BUS.py", "./Ejecutables/Linux/"])
else:
    print("No puede ser generado un ejecutable para este sistema.")

# print("Ejecutable generado exitosamente")
