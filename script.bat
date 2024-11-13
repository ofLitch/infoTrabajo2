@echo off
echo Ejecutando Controller
start "Controller" powershell -Command "python Controller\Controller.py; Read-Host 'Presiona Enter para cerrar...'"

echo Creando Routers

:: Definir enlaces para cada router
set "links[0]=1,2"
set "links[1]=0,3,6,9"
set "links[2]=0,3,4"
set "links[3]=1,2,5,6"
set "links[4]=2,7"
set "links[5]=3,8"
set "links[6]=1,3,8,9"
set "links[7]=4,11,8"
set "links[8]=5,6,7,12,11,18,20,17"
set "links[9]=1,6,10,12,13"
set "links[10]=9,13"
set "links[11]=7,8,20,14"
set "links[12]=9,8,21,13,19"
set "links[13]=9,10,12"
set "links[14]=11,15"
set "links[15]=14,16"
set "links[16]=15,17"
set "links[17]=8,16,18"
set "links[18]=8,17,21"
set "links[19]=12,23"
set "links[20]=8,11"
set "links[21]=12,18,22"
set "links[22]=21,23"
set "links[23]=19,22"

:: Crear routers con enlaces
for /l %%x in (0, 1, 1) do (
    set "current_links=!links[%%x]!"
    start "Router %%x" powershell -Command "python Router\main.py %%x '!current_links!'; Read-Host 'Presiona Enter para cerrar...'"
    echo Router %%x creado
)
