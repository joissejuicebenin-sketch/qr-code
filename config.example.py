"""
Fichier de configuration exemple
Copiez ce fichier vers config.py et modifiez les valeurs selon vos besoins
"""

# Configuration du serveur
SERVER_URL = "http://10.0.0.1"
API_ENDPOINT = "/api/qrcode/"
PORTAL_URL = "/portal"

# Configuration de la caméra
CAMERA_INDEX = 0  # 0 = caméra par défaut, 1 = deuxième caméra, etc.
SCAN_COOLDOWN = 3  # secondes entre les scans
CAMERA_FPS = 10

# Configuration de l'interface
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800
THEME = "dark"  # "dark" ou "light"

# Configuration réseau
REQUEST_TIMEOUT = 10  # secondes
MAX_RETRIES = 2

# Configuration du logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "qr_scanner.log"