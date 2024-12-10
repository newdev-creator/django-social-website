from django.contrib import admin  # Module pour l'administration Django
from .models import Image  # Importation du modèle Image


# Décorateur pour enregistrer le modèle Image avec une classe personnalisée d'administration
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Personnalisation de l'interface d'administration pour le modèle Image.
    """
    # Affiche les champs spécifiés dans la liste des objets du modèle
    list_display: list[str] = ['title', 'slug', 'image', 'created']
    # Permet la recherche sur certains champs
    search_fields: list[str] = ['created']
