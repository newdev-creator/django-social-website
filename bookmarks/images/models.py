from typing import Any  # Pour typage générique
from django.conf import settings  # Accès aux paramètres du projet (ex. AUTH_USER_MODEL)
from django.utils.text import slugify  # Fonction pour générer des slugs à partir de chaînes de caractères
from django.db import models  # Base pour tous les modèles Django
from django.urls import reverse  # Permet d'accéder aux URLs


class Image(models.Model):
    """
    Modèle représentant une image partagée par un utilisateur, avec des métadonnées associées.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Utilisateur lié à l'image
        related_name='images_created',  # Nom de la relation inverse (pour accéder aux images d'un utilisateur)
        on_delete=models.CASCADE  # Suppression des images si l'utilisateur est supprimé
    )
    title = models.CharField(max_length=200)  # Titre de l'image
    slug = models.SlugField(max_length=200, blank=True)  # Champ slug (généré automatiquement si vide)
    url = models.URLField(max_length=2000)  # URL de l'image d'origine
    image = models.ImageField(upload_to='images/%Y/%m/%d')  # Fichier image stocké sur le serveur
    description = models.TextField(blank=True)  # Description optionnelle de l'image
    created = models.DateTimeField(auto_now_add=True)  # Date de création automatique
    user_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # Utilisateurs ayant "liké" cette image
        related_name='images_liked',  # Nom de la relation inverse
        blank=True  # Champ optionnel
    )

    class Meta:
        """
        Métadonnées pour le modèle.
        """
        indexes: list[models.Index] = [
            models.Index(fields=['-created'])  # Index pour optimiser les requêtes par date de création
        ]
        ordering: list[str] = ['-created']  # Trie par défaut : images les plus récentes en premier

    def __str__(self) -> str:
        """
        Retourne une représentation sous forme de chaîne de caractères pour l'objet.
        """
        return self.title

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Surcharge de la méthode `save` pour générer un slug automatiquement si nécessaire.
        """
        if not self.slug:  # Si aucun slug n'est défini
            self.slug = slugify(self.title)  # Génère un slug à partir du titre
        super().save(*args, **kwargs)  # Appelle la méthode save() de la classe parente

    def get_absolute_url(self) -> str:
        """
        Retourne l'URL absolue pour cette image.
        """
        return reverse('images:detail', args=[self.id, self.slug])  # Retourne l'URL absolue pour cette image

"""
### Changements et annotations ajoutées :

1. **Ajout des types pour chaque champ** :
   - Par exemple, `title: models.CharField`, `created: models.DateTimeField`, etc.
   - Cela aide à rendre le modèle plus lisible et bien documenté.

2. **Typage des méthodes** :
   - La méthode `__str__` retourne un `str` : `def __str__(self) -> str`.
   - La méthode `save` utilise des paramètres variadiques avec des types génériques : `*args: Any, **kwargs: Any -> None`.

3. **Docstrings** :
   - Des docstrings ont été ajoutées à la classe et aux méthodes pour documenter leur fonction.

4. **Classe Meta** :
   - Ajout des types pour `indexes` (`list[models.Index]`) et `ordering` (`list[str]`).

### Pourquoi ces annotations et commentaires ?
- **Documentation intégrée** : Facilite la compréhension du code pour les autres développeurs ou pour vous-même à l'avenir.
- **Détection des erreurs** : Les outils comme `mypy` peuvent vérifier la compatibilité des types et aider à identifier les erreurs avant l'exécution.
- **Auto-complétion** : Améliore l'auto-complétion dans les IDE modernes comme PyCharm ou VS Code.

Avec ces ajouts, votre modèle est bien typé, lisible, et prêt pour une utilisation dans un projet Django robuste. ✔️
"""