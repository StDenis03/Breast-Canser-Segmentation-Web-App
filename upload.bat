@echo off
REM Скрипт для загрузки файлов на сервер сегментации (Windows)

setlocal enabledelayedexpansion

set API_URL=http://localhost:8081/api/v1

if "%~1"=="" (
    echo Использование: upload.bat ^<путь_к_файлу^>
    echo.
    echo Поддерживаемые форматы:
    echo   - .dcm (DICOM^)
    echo   - .nii (Nifti^)
    echo   - .nii.gz (Compressed Nifti^)
    echo.
    echo Пример:
    echo   upload.bat patient.nii.gz
    echo   upload.bat scan.dcm
    exit /b 1
)

set FILE=%~1

if not exist "%FILE%" (
    echo ERROR: файл '%FILE%' не найден
    exit /b 1
)

echo Загружаю %FILE%...

curl -X POST "%API_URL%/upload/" -F "file=@%FILE%"
