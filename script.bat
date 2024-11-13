@echo off
echo Ejecutando Controller
start "Controller" powershell -Command "python Controller\Controller.py; Read-Host 'Presiona Enter para cerrar...'"

echo Creando Routers

:: Crear routers con enlaces
for /l %%x in (0, 1, 4) do (
    start "Router %%x" powershell -Command "python Router\main.py %%x; Read-Host 'Presiona Enter para cerrar...'"
    echo Router %%x creado
)
