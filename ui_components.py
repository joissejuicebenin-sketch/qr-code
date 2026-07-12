"""
Module des composants UI
Définit tous les éléments d'interface utilisateur avec le style JOISSE WIFI
"""

import flet as ft
from typing import Dict


# Palette de couleurs JOISSE WIFI
COLORS = {
    # Couleurs principales
    'background_gradient': ft.LinearGradient(
        begin=ft.Alignment.TOP_CENTER,
        end=ft.Alignment.BOTTOM_CENTER,
        colors=['#0f3460', '#16213e', '#1a1a2e']
    ),
    'primary_red': '#e94560',
    'secondary_red': '#ff6b6b',
    
    # Couleurs de statut
    'success_green': '#28a745',
    'error_red': '#e94560',
    'warning_orange': '#ffc107',
    
    # Couleurs de texte
    'text_primary': '#ffffff',
    'text_secondary': 'rgba(255, 255, 255, 0.7)',
    'text_muted': 'rgba(255, 255, 255, 0.5)',
    
    # Autres
    'shadow': ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
    'white': '#ffffff',
    'light_gray': '#f0f7ff',
    'border_gray': '#e0e0e0'
}


def create_header() -> ft.Container:
    """
    Crée l'en-tête de l'application
    
    Returns:
        Container avec l'en-tête
    """
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "📷",
                    size=48,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Scanner QR Code",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS['text_primary'],
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "JOISSE WIFI — Connexion rapide",
                    size=14,
                    color=COLORS['text_secondary'],
                    text_align=ft.TextAlign.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8
        ),
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
        padding=ft.Padding(left=20, top=30, right=20, bottom=20),
        border=ft.Border.only(
            bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE))
        )
    )


def create_scanner_card() -> ft.Container:
    """
    Crée la carte du scanner
    
    Returns:
        Container avec la carte scanner
    """
    # En-tête du scanner
    scanner_header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("📷", size=24),
                ft.Text(
                    "Pointez votre QR code ici",
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.WHITE
                )
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[COLORS['primary_red'], COLORS['secondary_red']]
        ),
        padding=15,
        border_radius=ft.BorderRadius(top_left=20, top_right=20, bottom_left=0, bottom_right=0)
    )
    
    # Corps du scanner (zone de caméra)
    camera_placeholder = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(
                    ft.Icons.CAMERA_ALT,
                    size=64,
                    color=ft.Colors.GREY_400
                ),
                ft.Text(
                    "Initialisation de la caméra...",
                    size=12,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        width=300,
        height=300,
        bgcolor=ft.Colors.GREY_100,
        border_radius=12,
        alignment=ft.alignment.center
    )
    
    scanner_body = ft.Container(
        content=camera_placeholder,
        padding=20,
        bgcolor=ft.Colors.WHITE
    )
    
    return ft.Container(
        content=ft.Column(
            controls=[scanner_header, scanner_body],
            spacing=0
        ),
        width=400,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=20,
            color=COLORS['shadow'],
            offset=ft.Offset(0, 10)
        )
    )


def create_status_bar() -> ft.Container:
    """
    Crée la barre de statut
    
    Returns:
        Container avec la barre de statut
    """
    # Point de statut
    status_dot = ft.Container(
        width=10,
        height=10,
        border_radius=5,
        bgcolor=COLORS['error_red']
    )
    
    # Texte de statut
    status_text = ft.Text(
        "En attente de la caméra...",
        size=13,
        color=COLORS['text_secondary'],
        text_align=ft.TextAlign.CENTER
    )
    
    return ft.Container(
        content=ft.Row(
            controls=[
                status_dot,
                status_text
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=ft.Padding(left=20, top=12, right=20, bottom=12),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        border_radius=50,
        width=350
    )


def create_info_cards() -> ft.Container:
    """
    Crée les cartes d'information
    
    Returns:
        Container avec les cartes d'information
    """
    # Carte 1: Comment ça marche
    card1 = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("💡", size=32, text_align=ft.TextAlign.CENTER),
                ft.Text(
                    "Comment ça marche ?",
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=COLORS['text_primary'],
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Autorisez l'accès à la caméra, puis placez votre QR code dans le cadre. "
                    "Vous serez automatiquement redirigé vers la page de connexion avec vos identifiants pré-remplis.",
                    size=13,
                    color=COLORS['text_secondary'],
                    text_align=ft.TextAlign.CENTER,
                    height=1.6
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
        ),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.15, ft.Colors.WHITE)),
        border_radius=16,
        padding=20,
        width=400
    )
    
    # Carte 2: Sécurité
    card2 = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("🔒", size=32, text_align=ft.TextAlign.CENTER),
                ft.Text(
                    "Sécurisé",
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=COLORS['text_primary'],
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Vos identifiants ne sont jamais stockés. Le scan se fait localement sur votre appareil.",
                    size=13,
                    color=COLORS['text_secondary'],
                    text_align=ft.TextAlign.CENTER,
                    height=1.6
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
        ),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.15, ft.Colors.WHITE)),
        border_radius=16,
        padding=20,
        width=400
    )
    
    return ft.Container(
        content=ft.Column(
            controls=[card1, card2],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=400
    )


def create_loading_overlay() -> ft.Container:
    """
    Crée l'overlay de chargement
    
    Returns:
        Container avec l'overlay de chargement
    """
    # Spinner
    spinner = ft.ProgressRing(
        width=50,
        height=50,
        stroke_width=4,
        color=COLORS['primary_red'],
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)
    )
    
    # Texte principal
    loading_text = ft.Text(
        "Connexion en cours...",
        size=18,
        weight=ft.FontWeight.W_600,
        color=COLORS['text_primary'],
        text_align=ft.TextAlign.CENTER
    )
    
    # Sous-texte
    loading_subtext = ft.Text(
        "Redirection automatique",
        size=14,
        color=COLORS['text_secondary'],
        text_align=ft.TextAlign.CENTER
    )
    
    return ft.Container(
        content=ft.Column(
            controls=[
                spinner,
                loading_text,
                loading_subtext
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.BLUE_GREY_900),
        padding=40,
        border_radius=20,
        alignment=ft.Alignment.CENTER,
        visible=False  # Caché par défaut
    )


def create_error_toast() -> ft.Container:
    """
    Crée le toast d'erreur
    
    Returns:
        Container avec le toast d'erreur
    """
    # Icône et message
    error_icon = ft.Text("❌", size=24)
    error_message = ft.Text(
        "Erreur",
        size=14,
        weight=ft.FontWeight.W_500,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER
    )
    
    return ft.Container(
        content=ft.Row(
            controls=[
                error_icon,
                error_message
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor=ft.LinearGradient(
            begin=ft.Alignment.TOP_CENTER,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[COLORS['primary_red'], COLORS['secondary_red']]
        ),
        padding=ft.Padding(left=20, top=15, right=20, bottom=15),
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=30,
            color=ft.Colors.with_opacity(0.4, COLORS['primary_red']),
            offset=ft.Offset(0, 10)
        ),
        alignment=ft.Alignment.BOTTOM_CENTER,
        visible=False  # Caché par défaut
    )


def create_footer() -> ft.Container:
    """
    Crée le pied de page
    
    Returns:
        Container avec le pied de page
    """
    return ft.Container(
        content=ft.Text(
            "Propulsé par JOISSE WIFI • Scan sécurisé",
            size=12,
            color=COLORS['text_muted'],
            text_align=ft.TextAlign.CENTER
        ),
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
        padding=15
    )


def create_success_dialog(username: str, time_remaining: int = 0) -> ft.AlertDialog:
    """
    Crée une boîte de dialogue de succès
    
    Args:
        username: Nom d'utilisateur
        time_remaining: Temps restant en secondes
        
    Returns:
        AlertDialog de succès
    """
    message = f"Bienvenue, {username} !"
    if time_remaining > 0:
        minutes = time_remaining // 60
        message += f"\nTemps restant: {minutes} min"
    
    return ft.AlertDialog(
        modal=True,
        title=ft.Text("✓ Connexion réussie", color=COLORS['success_green']),
        content=ft.Text(message, size=16, text_align=ft.TextAlign.CENTER),
        actions=[
            ft.TextButton("OK", on_click=lambda e: None)
        ]
    )


def create_error_dialog(title: str, message: str) -> ft.AlertDialog:
    """
    Crée une boîte de dialogue d'erreur
    
    Args:
        title: Titre de l'erreur
        message: Message d'erreur
        
    Returns:
        AlertDialog d'erreur
    """
    return ft.AlertDialog(
        modal=True,
        title=ft.Text(f"✗ {title}", color=COLORS['error_red']),
        content=ft.Text(message, size=14),
        actions=[
            ft.TextButton("Fermer", on_click=lambda e: None)
        ]
    )


def create_permission_dialog() -> ft.AlertDialog:
    """
    Crée une boîte de dialogue pour demander la permission caméra
    
    Returns:
        AlertDialog de permission
    """
    return ft.AlertDialog(
        modal=True,
        title=ft.Text("📷 Accès à la caméra", weight=ft.FontWeight.BOLD),
        content=ft.Text(
            "Cette application nécessite l'accès à votre caméra pour scanner les QR codes. "
            "Veuillez autoriser l'accès lorsque demandé.",
            size=14,
            height=1.6
        ),
        actions=[
            ft.ElevatedButton(
                "Compris",
                bgcolor=COLORS['primary_red'],
                color=ft.Colors.WHITE,
                on_click=lambda e: None
            )
        ]
    )


class ResponsiveContainer:
    """
    Container responsive qui s'adapte à la taille de l'écran
    """
    
    def __init__(self, 
                 content: ft.Control,
                 max_width: int = 400,
                 padding: int = 20):
        """
        Initialise le container responsive
        
        Args:
            content: Contenu à afficher
            max_width: Largeur maximale
            padding: Padding interne
        """
        self.content = content
        self.max_width = max_width
        self.padding = padding
    
    def build(self, page_width: int) -> ft.Container:
        """
        Construit le container adapté à la largeur donnée
        
        Args:
            page_width: Largeur de la page
            
        Returns:
            Container adapté
        """
        width = min(page_width - 40, self.max_width)  # 40 = marges
        
        return ft.Container(
            content=self.content,
            width=width,
            padding=self.padding
        )


def apply_responsive_style(control: ft.Control, page: ft.Page):
    """
    Applique un style responsive à un contrôle
    
    Args:
        control: Contrôle Flet
        page: Page Flet
    """
    # Adapter la taille de la police selon la largeur
    if page.width < 360:
        # Très petit écran
        scale = 0.9
    elif page.width < 480:
        # Petit écran
        scale = 1.0
    else:
        # Écran normal ou plus grand
        scale = 1.0
    
    # Note: Flet gère automatiquement le responsive dans la plupart des cas
    # Cette fonction peut être étendue pour des ajustements spécifiques
    pass