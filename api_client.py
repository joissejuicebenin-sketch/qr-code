"""
Module client API
Gère les requêtes HTTP vers le serveur
"""

import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime
import time


class APIClient:
    """Client pour communiquer avec l'API du serveur"""
    
    def __init__(self, base_url: str = "http://10.0.0.1"):
        """
        Initialise le client API
        
        Args:
            base_url: URL de base du serveur
        """
        self.base_url = base_url
        self.api_url = f"{base_url}/api/qrcode/"
        self.portal_url = f"{base_url}/portal"
        self.timeout = 10  # timeout en secondes
        self.max_retries = 2
        
    def get(self, url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Effectue une requête GET
        
        Args:
            url: URL de la requête
            params: Paramètres GET optionnels
            
        Returns:
            Réponse JSON parsée
            
        Raises:
            Exception: Si la requête échoue
        """
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    url,
                    params=params,
                    timeout=self.timeout,
                    headers={
                        'Accept': 'application/json',
                        'User-Agent': 'QRCodeScanner/1.0'
                    }
                )
                
                # Vérifier le statut HTTP
                if response.status_code == 200:
                    try:
                        data = response.json()
                        return data
                    except json.JSONDecodeError:
                        return {
                            'status': 'error',
                            'message': 'Réponse serveur invalide (JSON attendu)',
                            'detail': response.text[:200]
                        }
                else:
                    # Erreur HTTP
                    error_msg = f"Erreur HTTP {response.status_code}"
                    try:
                        error_data = response.json()
                        error_msg = error_data.get('message') or error_data.get('detail') or error_msg
                    except:
                        pass
                    
                    return {
                        'status': 'error',
                        'message': error_msg,
                        'http_code': response.status_code
                    }
                    
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                return {
                    'status': 'error',
                    'message': 'Délai de connexion dépassé. Le serveur ne répond pas.'
                }
                
            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                return {
                    'status': 'error',
                    'message': 'Impossible de se connecter au serveur. Vérifiez votre connexion réseau.'
                }
                
            except requests.exceptions.RequestException as e:
                return {
                    'status': 'error',
                    'message': f'Erreur de requête: {str(e)}'
                }
        
        return {
            'status': 'error',
            'message': 'Nombre maximum de tentatives atteint'
        }
    
    def post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Effectue une requête POST
        
        Args:
            url: URL de la requête
            data: Données à envoyer
            
        Returns:
            Réponse JSON parsée
        """
        try:
            response = requests.post(
                url,
                json=data,
                timeout=self.timeout,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'User-Agent': 'QRCodeScanner/1.0'
                }
            )
            
            if response.status_code == 200:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {
                        'status': 'error',
                        'message': 'Réponse serveur invalide'
                    }
            else:
                error_msg = f"Erreur HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message') or error_data.get('detail') or error_msg
                except:
                    pass
                
                return {
                    'status': 'error',
                    'message': error_msg
                }
                
        except requests.exceptions.Timeout:
            return {
                'status': 'error',
                'message': 'Délai de connexion dépassé'
            }
        except requests.exceptions.ConnectionError:
            return {
                'status': 'error',
                'message': 'Impossible de se connecter au serveur'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erreur: {str(e)}'
            }
    
    def check_server_status(self) -> Dict[str, Any]:
        """
        Vérifie si le serveur est accessible
        
        Returns:
            Dict avec le statut du serveur
        """
        try:
            # Essayer d'accéder à l'URL de base
            response = requests.get(
                self.base_url,
                timeout=5,
                allow_redirects=True
            )
            
            return {
                'online': True,
                'status_code': response.status_code,
                'url': self.base_url
            }
            
        except requests.exceptions.Timeout:
            return {
                'online': False,
                'error': 'timeout',
                'message': 'Serveur hors ligne ou inaccessible'
            }
        except requests.exceptions.ConnectionError:
            return {
                'online': False,
                'error': 'connection',
                'message': 'Impossible de se connecter au serveur'
            }
        except Exception as e:
            return {
                'online': False,
                'error': 'unknown',
                'message': str(e)
            }
    
    def build_qr_url(self, 
                     username: str = "", 
                     password: str = "", 
                     code: str = "") -> str:
        """
        Construit l'URL de l'API avec les paramètres QR
        
        Args:
            username: Nom d'utilisateur
            password: Mot de passe
            code: Code simple
            
        Returns:
            URL complète avec paramètres
        """
        from urllib.parse import quote
        
        url = self.api_url.rstrip('/')
        
        if username and password:
            url += f"?username={quote(username)}&password={quote(password)}"
        elif code:
            url += f"?code={quote(code)}"
        else:
            url += "?code=unknown"
        
        return url
    
    def test_connection(self) -> bool:
        """
        Test rapide de connexion au serveur
        
        Returns:
            True si le serveur est accessible
        """
        try:
            response = requests.get(
                self.api_url,
                timeout=3,
                allow_redirects=False
            )
            return response.status_code < 500
        except:
            return False


class ConnectionMonitor:
    """Moniteur de connexion pour détecter les problèmes réseau"""
    
    def __init__(self, check_interval: int = 30):
        """
        Initialise le moniteur
        
        Args:
            check_interval: Intervalle de vérification en secondes
        """
        self.api_client = APIClient()
        self.check_interval = check_interval
        self.last_check: Optional[datetime] = None
        self.is_online = False
        self.consecutive_failures = 0
        self.max_consecutive_failures = 3
        
    def check(self) -> Dict[str, Any]:
        """
        Effectue une vérification de connexion
        
        Returns:
            Dict avec les informations de connexion
        """
        self.last_check = datetime.now()
        status = self.api_client.check_server_status()
        
        if status.get('online'):
            self.is_online = True
            self.consecutive_failures = 0
        else:
            self.consecutive_failures += 1
            if self.consecutive_failures >= self.max_consecutive_failures:
                self.is_online = False
        
        return {
            'is_online': self.is_online,
            'last_check': self.last_check.isoformat(),
            'consecutive_failures': self.consecutive_failures,
            'details': status
        }
    
    def get_status_message(self) -> str:
        """
        Retourne un message de statut utilisateur
        
        Returns:
            Message de statut
        """
        if self.is_online:
            return "✓ Serveur accessible"
        elif self.consecutive_failures > 0:
            return f"⚠ Serveur inaccessible ({self.consecutive_failures} tentatives)"
        else:
            return "○ Vérification en cours..."