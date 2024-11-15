@echo off
echo Iniciando Controller...
start "Controller" powershell -NoExit -Command "python Controller\Controller.py; Read-Host 'Presiona Enter para cerrar...'"

echo Creando Routers...
for /l %%x in (0, 1, 2) do (
    start "Router %%x" powershell -Command "python Router\main.py %%x; Read-Host 'Presiona Enter para cerrar...'"
    echo Router %%x creado
)

echo Creando Hosts...
@powershell -Command "Start-Sleep -s 4"  # Asegurarse de que los routers hayan terminado de asignar los puertos

set PORTS_FILE=router_ports.json

:: Leer los puertos asignados desde el archivo JSON para cada host
set HOST1_ID=0
for /F "tokens=1 delims=:," %%i in ('powershell -NoLogo -NoProfile -Command "[System.IO.File]::ReadAllText('%PORTS_FILE%') | ConvertFrom-Json | ForEach-Object { $_.'0' }"') do set ROUTER1_PORT=%%i

set HOST2_ID=1
for /F "tokens=1 delims=:," %%i in ('powershell -NoLogo -NoProfile -Command "[System.IO.File]::ReadAllText('%PORTS_FILE%') | ConvertFrom-Json | ForEach-Object { $_.'1' }"') do set ROUTER2_PORT=%%i

set ROUTER1_IP=127.0.0.1
start "Host %HOST1_ID%" powershell -NoExit -Command "python Host\main.py %HOST1_ID% %ROUTER1_IP% %ROUTER1_PORT%; Read-Host 'Presiona Enter para cerrar...'"

set ROUTER2_IP=127.0.0.1
start "Host %HOST2_ID%" powershell -NoExit -Command "python Host\main.py %HOST2_ID% %ROUTER2_IP% %ROUTER2_PORT%; Read-Host 'Presiona Enter para cerrar...'"
