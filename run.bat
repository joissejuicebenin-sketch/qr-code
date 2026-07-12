@echo off
REM Script de démarrage pour Windows

echo ========================================
echo   Scanner QR Code - JOISSE WIFI
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python detecte

REM Vérifier si l'environnement virtuel existe
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo [INFO] Creation de l'environnement virtuel...
    python -m venv venv
    echo [OK] Environnement virtuel cree
)

REM Activer l'environnement virtuel
echo.
echo [INFO] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Vérifier si les dépendances sont installées
echo.
echo [INFO] Verification des dependances...
pip show flet >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation des dependances (cela peut prendre quelques minutes)...
    pip install -r requirements.txt
    echo [OK] Dependances installees
) else (
    echo [OK] Dependances deja installees
)

REM Lancer l'application
echo.
echo ========================================
echo   Demarrage de l'application...
echo ========================================
echo.

python main.py

REM Désactiver l'environnement virtuel
call venv\Scripts\deactivate.bat