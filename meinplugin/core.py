"""A short description of the project"""

# Standard Django imports for Views and URLs
from django.http import HttpResponse
from django.urls import path

# InvenTree plugin imports
from plugin import InvenTreePlugin
from plugin.mixins import (NavigationMixin, ScheduleMixin, SettingsMixin,
                           UrlsMixin, UserInterfaceMixin)

from . import PLUGIN_VERSION  # Stellt sicher, dass die Version aus __init__.py geladen wird

# Die Hauptklasse für dein Plugin
class meinplugin(ScheduleMixin, SettingsMixin, UserInterfaceMixin, NavigationMixin, UrlsMixin, InvenTreePlugin):
    """meinplugin - custom InvenTree plugin."""

    # Plugin metadata
    TITLE = "Mein Cooles Plugin"  # Angepasster Titel
    NAME = "meinplugin"
    SLUG = "meinplugin"  # Wichtig für URL-Referenzen!
    DESCRIPTION = "Ein Beispiel-Plugin mit Navigationselement"
    VERSION = PLUGIN_VERSION

    # Additional project information
    AUTHOR = "Jan Schüler"
    LICENSE = "MIT"

    # Optional: Gruppiere die Links unter einem eigenen Tab in der Navigation
    NAVIGATION_TAB_NAME = "Mein Plugin Tab"
    NAVIGATION_TAB_ICON = 'fas fa-cogs'  # Beispiel FontAwesome 4 Icon

    # Navigationselemente (von NavigationMixin)
    # Ref: https://docs.inventree.org/en/latest/extend/plugins/integration/navigation/
    NAVIGATION = [
        {
            'name': 'Beispiel Seite',  # Angezeigter Text des Links
            'link': 'plugin:meinplugin:hello',  # URL-Name: plugin:<SLUG>:<url_name>
            'icon': 'fas fa-info-circle',  # Beispiel FontAwesome 4 Icon
        },
        # Hier könnten weitere Links für dieses Plugin hinzugefügt werden
    ]

    # --- Bestehende Mixin-Konfigurationen ---

    # Scheduled tasks (from ScheduleMixin)
    # Ref: https://docs.inventree.org/en/stable/extend/plugins/schedule/
    SCHEDULED_TASKS = {
        # Define your scheduled tasks here...
    }

    # Plugin settings (from SettingsMixin)
    # Ref: https://docs.inventree.org/en/stable/extend/plugins/settings/
    SETTINGS = {
        'CUSTOM_VALUE': {
            'name': 'Custom Value',
            'description': 'A custom value',
            'validator': int,
            'default': 42,
        }
        # Hier könnten weitere Einstellungen definiert werden
    }

    # User interface elements (from UserInterfaceMixin)
    # Ref: https://docs.inventree.org/en/stable/extend/plugins/ui/
    # Diese sind für Dashboard-Elemente, Panels etc. relevant,
    # nicht direkt für die einfache Navigation, die wir hier erstellen.
    # Die bereitgestellten JavaScript-Beispiele würden hier konfiguriert werden,
    # wenn du z.B. ein benutzerdefiniertes Panel hinzufügen wolltest.

    def setup_urls(self):
        """Definiert URL-Muster für dieses Plugin."""
        return [
            # URL für die Beispielseite "Hallo Welt"
            path('hello/', self.hello_world_view, name='hello'),
            # URL für die Ausleihfunktion
            path('ausleihen/', self.loan_view, name='ausleihen'),
        ]

    def hello_world_view(self, request, *args, **kwargs):
        """Eine Beispiel-Ansicht, die von der URL aufgerufen wird."""
        html = "<h1>Hallo Welt!</h1><p>Dies ist eine einfache Seite vom 'meinplugin'.</p>"
        return HttpResponse(html)

    def loan_view(self, request, *args, **kwargs):
        """Ausleihfunktion in InvenTree.
        
        Zeigt ein Formular an, über das ein Artikel ausgeliehen werden kann.
        Bei POST wird die Anfrage verarbeitet und eine Bestätigung angezeigt.
        """
        if request.method == 'POST':
            # Formular-Daten aus dem POST-Request auslesen
            artikel_id = request.POST.get('artikel')
            benutzer = request.POST.get('benutzer')
            
            # Hier die Logik zur Ausleihe implementieren:
            # z. B. Status des Artikels aktualisieren, einen Ausleih-Datensatz anlegen, etc.
            html = f"<h1>Ausleihe bestätigt!</h1><p>Artikel {artikel_id} wurde an {benutzer} ausgeliehen.</p>"
            return HttpResponse(html)
        else:
            # GET-Request: Zeige das Ausleihformular an
            html = """
                <h1>Artikel ausleihen</h1>
                <form method="post">
                    <label for="artikel">Artikel-ID:</label>
                    <input type="text" id="artikel" name="artikel"><br><br>
                    <label for="benutzer">Benutzername:</label>
                    <input type="text" id="benutzer" name="benutzer"><br><br>
                    <input type="submit" value="Ausleihen">
                </form>
            """
            return HttpResponse(html)
