# Guide de démarrage rapide

## Installation en 3 étapes

### 1. Installer les dépendances

**Windows:**
```bash
run.bat
```

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

### 2. Ou installation manuelle

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Lancer l'application

```bash
python main.py
```

## Structure des fichiers

```
qr-code/
├── main.py              # Application principale
├── requirements.txt     # Dépendances
├── qr_scanner.py       # Détection QR codes
├── api_client.py       # Client API
├── ui_components.py    # Interface utilisateur
├── config.example.py   # Configuration exemple
├── run.bat            # Script Windows
├── run.sh             # Script Linux/macOS
└── README.md          # Documentation complète
```

## Configuration

Copiez `config.example.py` vers `config.py` et modifiez les paramètres si nécessaire.

## Dépannage rapide

**Caméra ne fonctionne pas:**
- Vérifier les permissions système
- Fermer les autres apps utilisant la caméra

**Erreur de connexion API:**
- Vérifier que le serveur 10.0.0.1 est accessible
- Vérifier le câble réseau

**Performance lente:**
- Fermer les autres applications
- Réduire la résolution caméra dans main.py