#!/bin/bash
# Script de démarrage pour Linux/macOS

echo "========================================"
echo "  Scanner QR Code - JOISSE WIFI"
echo "========================================"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python n'est pas installé ou n'est pas dans le PATH"
    echo "Veuillez installer Python 3.8+ depuis https://www.python.org/"
    read -p "Appuyez sur Entrée pour quitter..."
    exit 1
fi

echo "[OK] Python detecte: $(python3 --version)"

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo ""
    echo "[INFO] Creation de l'environnement virtuel..."
    python3 -m venv venv
    echo "[OK] Environnement virtuel cree"
fi

# Activer l'environnement virtuel
echo ""
echo "[INFO] Activation de l'environnement virtuel..."
source venv/bin/activate

# Vérifier si les dépendances sont installées
echo ""
echo "[INFO] Verification des dependances..."
if ! python3 -c "import flet" 2>/dev/null; then
    echo "[INFO] Installation des dependances (cela peut prendre quelques minutes)..."
    pip install -r requirements.txt
    echo "[OK] Dependances installees"
else
    echo "[OK] Dependances deja installees"
fi

# Lancer l'application
echo ""
echo "========================================"
echo "  Demarrage de l'application..."
echo "========================================"
echo ""

python3 main.py

# Désactiver l'environnement virtuel
deactivate