"""
Application Scanner QR Code - JOISSE WIFI
Version corrigée avec gestion de la caméra et détection de QR codes
"""

import base64

import flet as ft
import cv2
import numpy as np
from PIL import Image
import requests
import json
import threading
import time
import os

class QRCodeApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Scanner QR | JOISSE WIFI"
        self.page.window_width = 400
        self.page.window_height = 800
        self.page.padding = 0
        self.page.bgcolor = ft.Colors.BLACK_87
        self.detector = cv2.QRCodeDetector()

        # Configuration API
        self.api_url = "http://10.0.0.1/api/qrcode/"
        self.portal_url = "http://10.0.0.1/portal"

        # État de l'application
        self.camera_active = False
        self.is_scanning = False
        self.cap = None

        # Éléments UI
        self.camera_feed = ft.Image(
            src="",
            width=300,
            height=300,
            fit=ft.BoxFit.COVER,
            border_radius=12,
            visible=False
        )
        self.status_text = ft.Text(
            "En attente de la caméra...",
            color=ft.Colors.WHITE_70,
            size=14
        )
        self.status_dot = ft.Container(
            width=10,
            height=10,
            bgcolor=ft.Colors.RED,
            border_radius=5
        )
        self.loading_overlay = ft.Container(
            width=self.page.window_width,
            height=self.page.window_height,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
            visible=False,
            content=ft.Column(
                [
                    ft.ProgressBar(width=200),
                    ft.Text("Connexion en cours...", color=ft.Colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.error_toast = ft.SnackBar(
            content=ft.Text("Erreur: Impossible d'accéder à la caméra.", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED,
            open=False
        )

        # Initialiser l'UI
        self._init_ui()

        # Démarrer la caméra
        self._start_camera()

    def _init_ui(self):
        """Initialise l'interface utilisateur"""
        header = ft.Column(
            [
                ft.Image(
                    src="icons/icon-512.png",
                    width=60,
                    height=60
                ),
                ft.Text("Scanner QR Code", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("JOISSE WIFI — Connexion rapide", size=14, color=ft.Colors.WHITE_70),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        )

        scanner_card = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.CAMERA_ALT, color=ft.Colors.WHITE),
                                ft.Text("Pointez votre QR code ici", color=ft.Colors.WHITE, weight=ft.FontWeight.W_600)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10
                        ),
                        bgcolor=ft.Colors.GREEN_500,
                        padding=15,
                        border_radius=ft.BorderRadius.only(top_left=20, top_right=20)
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                self.camera_feed,
                                ft.Text("Initialisation de la caméra...", color=ft.Colors.GREY_600, size=12)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        bgcolor=ft.Colors.WHITE,
                        padding=20,
                        border_radius=ft.BorderRadius.only(bottom_left=20, bottom_right=20)
                    )
                ],
                spacing=0
            ),
            width=350,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=ft.Colors.BLACK_54,
                offset=ft.Offset(0, 10)
            )
        )

        status_bar = ft.Container(
            content=ft.Row(
                [
                    self.status_dot,
                    self.status_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            padding=15,
            border_radius=20
        )

        info_section = ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.AMBER, size=30),
                            ft.Text("Comment ça marche ?", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Text(
                                "Autorisez l'accès à la caméra, puis placez votre QR code dans le cadre.",
                                size=12,
                                color=ft.Colors.WHITE_70,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=5
                    ),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    padding=15,
                    border_radius=15
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.LOCK, color=ft.Colors.GREEN_400, size=30),
                            ft.Text("Sécurisé", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Text(
                                "Vos identifiants ne sont jamais stockés. Le scan se fait localement.",
                                size=12,
                                color=ft.Colors.WHITE_70,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=5
                    ),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    padding=15,
                    border_radius=15
                )
            ],
            spacing=15
        )

        footer = ft.Text(
            "Propulsé par JOISSE WIFI • Scan sécurisé",
            color=ft.Colors.WHITE_70,
            size=12,
            text_align=ft.TextAlign.CENTER
        )

        self.page.add(
            ft.Column(
                [
                    header,
                    scanner_card,
                    status_bar,
                    info_section,
                    footer
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            ),
            self.loading_overlay,
            self.error_toast
        )

    def _start_camera(self):
        """Démarre la caméra dans un thread séparé"""
        def camera_loop():
            try:
                self.cap = cv2.VideoCapture(0, cv2.CAP_ANY)  # Utilise DirectShow pour Windows
                if not self.cap.isOpened():
                    self.cap = cv2.VideoCapture(0, cv2.CAP_MSMF)  # Essayer MSMF si DSHOW échoue
                    if not self.cap.isOpened():
                        self.cap = cv2.VideoCapture(0)  # Essayer par défaut
                
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

                if not self.cap.isOpened():
                    self.page.update()
                    self.error_toast.content = ft.Text("Erreur: Impossible d'ouvrir la caméra.", color=ft.Colors.WHITE)
                    self.error_toast.open = True
                    self.page.update()
                    return

                self.camera_active = True
                self.camera_feed.visible = True
                self._update_status(True, "Caméra active — Prêt à scanner")
                self.page.update()

                while self.camera_active:

                    ret, frame = self.cap.read()

                    if not ret:
                        continue

                    frame = cv2.flip(frame, 1)

                    qr = self._detect_qr_code(frame)
                    print(f"QR détecté: {qr}")  # Debug: Affiche le QR détecté dans la console  

                    if qr and not self.is_scanning:
                        self._on_qr_detected(qr)
                        print(f"QR détecté Scan: {qr}")

                    self._update_camera_feed(frame)

                    time.sleep(1 / 25)

            except Exception as e:
                self._show_error(f"Erreur caméra: {str(e)}")
            finally:
                if self.cap:
                    self.cap.release()

        camera_thread = threading.Thread(target=camera_loop, daemon=True)
        camera_thread.start()
    
    def _detect_qr_code(self, frame):
        try:
            data, points, _ = self.detector.detectAndDecode(frame)

            if points is not None:
                pts = points.astype(int)

                for i in range(4):
                    pt1 = tuple(pts[0][i])
                    pt2 = tuple(pts[0][(i + 1) % 4])

                    cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

            if data:
                return data

        except Exception as e:
            print(e)

        return None

    def _update_camera_feed(self, frame):
        try:

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            _, buffer = cv2.imencode(
                ".jpg",
                frame,
                [int(cv2.IMWRITE_JPEG_QUALITY), 80]
            )

            self.camera_feed.src = base64.b64encode(buffer).decode("utf-8")

            self.camera_feed.visible = True

            self.page.update()

        except Exception as e:
            print(e)

    def _on_qr_detected(self, qr_data: str):
        """Appelé quand un QR code est détecté"""
        self.is_scanning = True
        self._update_status(True, "QR code détecté ! Connexion...")
        self._show_loading()

        def process_qr():
            try:
                # Parser le QR code
                username, password, code = self._parse_qr_data(qr_data)

                # Construire l'URL
                url = self._build_api_url(username, password, code)

                # Faire la requête API
                response = requests.get(url)

                # Traiter la réponse
                self._handle_api_response(response.json())

            except json.JSONDecodeError:
                # Si ce n'est pas du JSON, utiliser comme code
                url = f"{self.api_url}?code={requests.utils.quote(qr_data)}"
                response = requests.get(url)
                self._handle_api_response(response.json())
            except Exception as e:
                self._show_error(f"Erreur: {str(e)}")
                self._hide_loading()
                self.is_scanning = False

        threading.Thread(target=process_qr, daemon=True).start()

    def _parse_qr_data(self, data: str):
        """Parse les données du QR code"""
        try:
            qr_json = json.loads(data)
            return (
                qr_json.get('username', ''),
                qr_json.get('password', ''),
                qr_json.get('code', '')
            )
        except json.JSONDecodeError:
            return '', '', data

    def _build_api_url(self, username: str, password: str, code: str) -> str:
        """Construit l'URL de l'API avec les paramètres"""
        url = self.api_url.rstrip('/')
        if username and password:
            url += f"?username={requests.utils.quote(username)}&password={requests.utils.quote(password)}"
        elif code:
            url += f"?code={requests.utils.quote(code)}"
        else:
            url += f"?code={requests.utils.quote('unknown')}"
        return url

    def _handle_api_response(self, response: dict):
        """Traite la réponse de l'API"""
        try:
            self._hide_loading()

            if response.get('status') == 'success':
                username = response.get('username', 'Utilisateur')
                time_remaining = response.get('time_remaining', 0)

                welcome_msg = f"Bienvenue, {username}!"
                if time_remaining:
                    minutes = time_remaining // 60
                    welcome_msg += f" Temps restant: {minutes} min"

                self._update_status(True, "✓ Connexion réussie!")

                # Redirection après 2 secondes
                def redirect():
                    time.sleep(2)
                    self.page.launch_url(response.get('redirect_url', self.portal_url))

                threading.Thread(target=redirect, daemon=True).start()

            else:
                error_msg = response.get('message') or response.get('detail') or 'Erreur lors de la connexion'
                self._update_status(False, "✗ Échec de la connexion")
                self._show_error(error_msg)

                # Redirection vers le portail avec l'erreur
                error_url = f"{self.portal_url}?error={requests.utils.quote(error_msg)}"
                def redirect_error():
                    time.sleep(3)
                    self.page.launch_url(error_url)

                threading.Thread(target=redirect_error, daemon=True).start()

        except Exception as e:
            self._show_error(f"Erreur traitement réponse: {str(e)}")
        finally:
            self.is_scanning = False

    def _update_status(self, active: bool, text: str):
        """Met à jour la barre de statut"""
        self.status_dot.bgcolor = ft.Colors.GREEN if active else ft.Colors.RED
        self.status_text.value = text
        self.page.update()

    def _show_loading(self):
        """Affiche l'overlay de chargement"""
        self.loading_overlay.visible = True
        self.page.update()

    def _hide_loading(self):
        """Cache l'overlay de chargement"""
        self.loading_overlay.visible = False
        self.page.update()

    def _show_error(self, message: str):
        """Affiche un toast d'erreur"""
        self.error_toast.content = ft.Text(f"❌ {message}", color=ft.Colors.WHITE)
        self.error_toast.open = True
        self.page.update()

        # Cacher après 4 secondes
        def hide_toast():
            time.sleep(4)
            self.error_toast.open = False
            self.page.update()

        threading.Thread(target=hide_toast, daemon=True).start()

    def on_close(self, e):
        """Nettoyage à la fermeture de l'application"""
        self.camera_active = False
        if self.cap:
            self.cap.release()

def main(page: ft.Page):
    app = QRCodeApp(page)
    page.on_close = app.on_close

if __name__ == "__main__":
    ft.app(target=main)