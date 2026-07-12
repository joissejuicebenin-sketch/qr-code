"""
Module de détection de QR Code
Utilise OpenCV pour la détection en temps réel
"""

import json

import cv2
import numpy as np
from typing import Dict, Optional, List, Tuple
import threading
import time


class QRScanner:
    """Classe pour la détection de QR codes avec OpenCV"""
    
    def __init__(self):
        """Initialise le détecteur QR code"""
        # Initialiser le détecteur QR code d'OpenCV
        self.qr_detector = cv2.QRCodeDetector()
        self.last_detection_time = 0
        self.detection_cooldown = 1.0  # secondes entre les détections
        
    def detect(self, frame: np.ndarray) -> Optional[str]:
        """
        Détecte et décode un QR code dans l'image
        
        Args:
            frame: Image OpenCV (format BGR)
            
        Returns:
            Texte décodé du QR code ou None si aucun QR code détecté
        """
        try:
            # Vérifier le cooldown
            current_time = time.time()
            if current_time - self.last_detection_time < self.detection_cooldown:
                return None
            
            # Détecter et décoder le QR code
            data, bbox, straight_qrcode = self.qr_detector.detectAndDecode(frame)
            
            if data and bbox is not None:
                self.last_detection_time = current_time
                
                # Dessiner le contour du QR code sur l'image (pour debug)
                self._draw_qr_contour(frame, bbox)
                
                return data
            
            return None
            
        except Exception as e:
            print(f"Erreur détection QR: {e}")
            return None
    
    def _draw_qr_contour(self, frame: np.ndarray, bbox: np.ndarray):
        """
        Dessine le contour du QR code détecté
        
        Args:
            frame: Image OpenCV
            bbox: Coordonnées du contour du QR code
        """
        try:
            # Convertir les coordonnées en entiers
            bbox = bbox.astype(int)
            
            # Dessiner les lignes du contour
            for i in range(len(bbox)):
                # Ligne de i à i+1 (avec retour au début)
                pt1 = tuple(bbox[i][0])
                pt2 = tuple(bbox[(i + 1) % len(bbox)][0])
                
                # Dessiner la ligne en vert épaisse
                cv2.line(frame, pt1, pt2, (0, 255, 0), 3)
            
            # Ajouter un rectangle autour
            x, y, w, h = cv2.boundingRect(bbox)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        except Exception as e:
            print(f"Erreur dessin contour: {e}")
    
    def detect_multi(self, frame: np.ndarray) -> List[str]:
        """
        Détecte plusieurs QR codes dans l'image
        
        Args:
            frame: Image OpenCV (format BGR)
            
        Returns:
            Liste des textes décodés
        """
        try:
            # OpenCV ne détecte qu'un QR code à la fois par défaut
            # Pour multiple détection, il faudrait utiliser une autre bibliothèque
            result = self.detect(frame)
            return [result] if result else []
            
        except Exception as e:
            print(f"Erreur détection multiple: {e}")
            return []
    
    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Prétraite l'image pour améliorer la détection
        
        Args:
            frame: Image OpenCV brute
            
        Returns:
            Image prétraitée
        """
        try:
            # Convertir en niveaux de gris
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Améliorer le contraste
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            
            # Réduire le bruit
            denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
            
            # Convertir retour vers BGR pour la compatibilité
            result = cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)
            
            return result
            
        except Exception as e:
            print(f"Erreur prétraitement: {e}")
            return frame
    
    def set_detection_cooldown(self, cooldown: float):
        """
        Définit le délai entre les détections
        
        Args:
            cooldown: Délai en secondes
        """
        self.detection_cooldown = max(0.1, cooldown)
    
    def stop(self):
        """Arrête le scanner (libère les ressources)"""
        # OpenCV n'a pas besoin de libération spéciale pour QRCodeDetector
        pass


class AsyncQRScanner:
    """
    Scanner QR asynchrone pour utilisation dans un thread séparé
    """
    
    def __init__(self, callback, cooldown: float = 2.0):
        """
        Initialise le scanner asynchrone
        
        Args:
            callback: Fonction à appeler quand un QR code est détecté
            cooldown: Délai entre les détections en secondes
        """
        self.scanner = QRScanner()
        self.scanner.set_detection_cooldown(cooldown)
        self.callback = callback
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.cap: Optional[cv2.VideoCapture] = None
    
    def start(self, camera_index: int = 0):
        """
        Démarre le scan dans un thread séparé
        
        Args:
            camera_index: Index de la caméra à utiliser
        """
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(
            target=self._scan_loop,
            args=(camera_index,),
            daemon=True
        )
        self.thread.start()
    
    def _scan_loop(self, camera_index: int):
        """
        Boucle de scan dans un thread séparé
        
        Args:
            camera_index: Index de la caméra
        """
        try:
            self.cap = cv2.VideoCapture(camera_index)
            
            if not self.cap.isOpened():
                print(f"Impossible d'ouvrir la caméra {camera_index}")
                self.running = False
                return
            
            while self.running:
                ret, frame = self.cap.read()
                
                if not ret:
                    continue
                
                # Détecter le QR code
                qr_data = self.scanner.detect(frame)
                
                if qr_data:
                    # Appeler le callback avec les données
                    self.callback(qr_data)
                
                # Petit délai
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Erreur dans le scan loop: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Arrête le scanner"""
        self.running = False
        
        if self.cap and self.cap.isOpened():
            self.cap.release()
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
    
    def is_running(self) -> bool:
        """Vérifie si le scanner est en cours d'exécution"""
        return self.running and self.thread and self.thread.is_alive()


class QRCodeValidator:
    """Validateur de format de QR code"""
    
    @staticmethod
    def is_valid_json(data: str) -> bool:
        """
        Vérifie si la chaîne est un JSON valide
        
        Args:
            data: Chaîne à vérifier
            
        Returns:
            True si c'est un JSON valide
        """
        try:
            json.loads(data)
            return True
        except (json.JSONDecodeError, TypeError):
            return False
    
    @staticmethod
    def validate_qr_format(data: str) -> Tuple[bool, str, Dict]:
        """
        Valide et parse le format du QR code
        
        Args:
            data: Données du QR code
            
        Returns:
            Tuple (is_valid, format_type, parsed_data)
        """
        import json
        
        # Essayer de parser comme JSON
        if QRCodeValidator.is_valid_json(data):
            try:
                parsed = json.loads(data)
                
                # Vérifier les champs requis
                if 'username' in parsed or 'password' in parsed or 'code' in parsed:
                    return True, 'json', parsed
                else:
                    return False, 'json_invalid', {}
                    
            except Exception:
                return False, 'json_error', {}
        
        # Sinon, traiter comme code simple
        if data and len(data) > 0:
            return True, 'simple', {'code': data}
        
        return False, 'empty', {}
    
    @staticmethod
    def extract_credentials(data: Dict) -> Tuple[str, str, str]:
        """
        Extrait les identifiants du QR code
        
        Args:
            data: Données parsées du QR code
            
        Returns:
            Tuple (username, password, code)
        """
        username = data.get('username', '')
        password = data.get('password', '')
        code = data.get('code', '')
        
        return username, password, code