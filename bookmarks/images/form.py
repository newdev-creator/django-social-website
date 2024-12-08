from django import forms
from .models import Image  # Importation du modèle Image depuis vos modèles
import requests  # Module pour effectuer des requêtes HTTP (utile pour télécharger une image à partir d'une URL)
from django.core.files.base import ContentFile  # Utilisé pour traiter le contenu binaire des fichiers
from django.utils.text import slugify  # Convertit les chaînes de caractères en un format "slugifié" (URL-friendly)

# Définition d'un formulaire pour créer une instance du modèle Image
class ImageCreateForm(forms.ModelForm):
    class Meta:
        # Spécifie que ce formulaire est lié au modèle Image
        model = Image
        # Définition des champs à inclure dans le formulaire
        fields = ['title', 'url', 'description']
        # Configuration des widgets (pour personnaliser l'affichage des champs)
        widgets = {
            'url': forms.HiddenInput(),  # Le champ URL sera caché dans le formulaire
        }

    # Méthode pour valider le champ 'url' avant de sauvegarder les données
    def clean_url(self):
        # Récupère la valeur du champ 'url' nettoyé (cleaned_data contient les données valides)
        url = self.cleaned_data['url']
        # Liste des extensions valides pour les images
        valid_extensions = ['.jpg', '.jpeg', '.png']
        # Récupère l'extension du fichier en divisant l'URL à partir du dernier point
        extension = url.rsplit('.', 1)[1].lower()
        # Vérifie si l'extension est valide
        if extension not in valid_extensions:
            # Si non, lève une exception ValidationError
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url  # Retourne l'URL validée

    # Méthode pour sauvegarder l'instance du formulaire (et effectuer des actions supplémentaires)
    def save(self, force_insert=False, force_update=False, commit=True):
        # Appelle la méthode save() parente mais sans sauvegarder immédiatement dans la base de données
        image = super().save(commit=False)
        # Récupère l'URL de l'image depuis les données validées
        image_url = self.cleaned_data['url']
        # Génère un nom de fichier unique basé sur le titre de l'image
        name = slugify(image.title)  # Convertit le titre en un slug (e.g., "Mon Image" -> "mon-image")
        # Récupère l'extension du fichier depuis l'URL
        extension = image_url.rsplit('.', 1)[1].lower()
        # Combine le slug et l'extension pour créer un nom de fichier
        image_name = f'{name}.{extension}'
        
        # Télécharge l'image depuis l'URL spécifiée
        response = requests.get(image_url)
        # Sauvegarde l'image dans le champ `image` du modèle en utilisant son contenu binaire
        image.image.save(
            image_name,  # Nom du fichier de l'image
            ContentFile(response.content),  # Contenu binaire de l'image téléchargée
            save=True  # Enregistre immédiatement le fichier
        )
        # Si `commit` est True, enregistre l'objet dans la base de données
        if commit:
            image.save()
        # Retourne l'instance de l'image sauvegardée
        return image


"""
### Résumé des étapes importantes :
1. **Validation de l'URL** :
   - Vérifie que l'URL pointe vers un fichier d'image ayant une extension valide (`.jpg`, `.jpeg`, `.png`).

2. **Téléchargement et sauvegarde de l'image** :
   - Télécharge l'image depuis l'URL fournie via une requête HTTP (`requests.get()`).
   - Génère un nom de fichier basé sur le titre de l'image en format slugifié.
   - Sauvegarde l'image dans le champ fichier de l'objet Image avec le contenu téléchargé.

3. **Personnalisation de la sauvegarde** :
   - Le formulaire utilise la méthode `save()` pour gérer les actions supplémentaires avant d'enregistrer l'objet dans la base de données, notamment l'attribution de l'image téléchargée.

Ce processus garantit que seules des images valides sont acceptées, et que l'image est correctement téléchargée et associée au modèle. 🖼️✔️
"""