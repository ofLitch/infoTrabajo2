@echo off
echo Iniciando Controller...
start "Controller" powershell -Command "python Controller\Controller.py; Read-Host 'Presiona Enter para cerrar...'"

echo Creando Routers...
for /l %%x in (0, 1, 1) do (
    start "Router %%x" powershell -Command "python Router\main.py %%x; Read-Host 'Presiona Enter para cerrar...'"
    echo Router %%x creado
)

echo Creando Hosts...
:: Crear el primer Host y conectarlo al Router 1
set HOST1_ID=0
set ROUTER1_ID=1
set ROUTER1_IP=127.0.0.1
set ROUTER1_PORT=60001
start "Host %HOST1_ID%" powershell -Command "python Host\main.py %HOST1_ID% %ROUTER1_IP% %ROUTER1_PORT%; Read-Host 'Presiona Enter para cerrar...'"

:: Crear el segundo Host y conectarlo al Router 2
set HOST2_ID=1
set ROUTER2_IP=127.0.0.1
set ROUTER2_PORT=60002
start "Host %HOST2_ID%" powershell -Command "python Host\main.py %HOST2_ID% %ROUTER2_IP% %ROUTER2_PORT%; Read-Host 'Presiona Enter para cerrar...'"
