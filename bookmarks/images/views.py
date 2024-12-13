from django.contrib import messages  # Permet d'afficher des messages temporaires à l'utilisateur
from django.contrib.auth.decorators import login_required  # Décorateur pour restreindre l'accès aux utilisateurs connectés
from django.http import HttpResponse, HttpRequest, JsonResponse  # Permet d'envoyer des réponses HTTP et JSON
from django.shortcuts import redirect, render  # Utilisé pour rediriger ou rendre des templates HTML
from django.shortcuts import get_object_or_404  # Permet d'accéder à une instance d'objet
from django.views.decorators.http import require_POST  # Décorateur pour vérifier si la requête est de type POST

from .forms import ImageCreateForm  # Formulaire pour créer une instance du modèle Image
from .models import Image  # Importe le modèle Image

# Vue pour permettre aux utilisateurs de créer une nouvelle image
@login_required  # Assure que seuls les utilisateurs connectés peuvent accéder à cette vue
def image_create(request):
    # Vérifie si la requête est de type POST (soumission de formulaire)
    if request.method == 'POST':
        # Instancie le formulaire avec les données POST envoyées par l'utilisateur
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():  # Vérifie si les données du formulaire sont valides
            # Récupère les données validées (cleaned_data contient les données nettoyées)
            cd = form.cleaned_data
            # Crée une nouvelle instance d'Image mais sans la sauvegarder immédiatement dans la base de données
            new_image = form.save(commit=False)
            # Associe l'utilisateur actuellement connecté à l'image
            new_image.user = request.user
            # Sauvegarde l'instance dans la base de données
            new_image.save()
            # Ajoute un message de succès à afficher à l'utilisateur
            messages.success(request, 'Image added successfully!')
            # Redirige l'utilisateur vers la vue détail de l'image nouvellement créée
            return redirect(new_image.get_absolute_url())
    else:
        # Si la requête n'est pas de type POST, construit le formulaire avec les données GET
        # (par exemple, des données transmises via un bookmarklet)
        form = ImageCreateForm(data=request.GET)
    
    # Rendu du template HTML pour afficher le formulaire
    return render(
        request,  # Objet de requête
        'images/image/create.html',  # Template utilisé pour afficher la page de création
        {'form': form}  # Contexte contenant le formulaire
    )

def image_detail(request,id: int, slug: str) -> HttpResponse:
    """
    Vue pour afficher les détails d'une image donnée.
    """
    image = get_object_or_404(Image, id=id, slug=slug)  # Recherche de l'image avec l'ID et le slug
    return render(
        request,  # Objet de requête
        'images/image/detail.html',  # Template utilisé pour afficher la page de détail
        {'section': 'images', 'image': image}  # Contexte contenant l'image
    )

@login_required
@require_POST
def image_like(request: HttpRequest) -> HttpResponse:
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


"""
### Résumé des étapes importantes :

1. **Restriction aux utilisateurs connectés** :
   - La vue est protégée par le décorateur `@login_required`, ce qui empêche les utilisateurs non connectés d'y accéder.

2. **Gestion des requêtes POST** :
   - Si l'utilisateur soumet un formulaire (`request.method == 'POST'`), les données sont utilisées pour initialiser le formulaire `ImageCreateForm`.
   - Une fois que le formulaire est validé (`form.is_valid()`), une nouvelle instance d'image est créée sans être immédiatement enregistrée dans la base de données (`commit=False`).
   - L'image est ensuite associée à l'utilisateur actuellement connecté (`new_image.user = request.user`) avant d'être sauvegardée.

3. **Gestion des requêtes GET** :
   - Si la requête est de type GET, le formulaire est initialisé avec les données envoyées en paramètre (par exemple, via un bookmarklet).

4. **Ajout de messages utilisateur** :
   - En cas de succès, un message temporaire est ajouté via `messages.success()` pour informer l'utilisateur que l'image a été ajoutée.

5. **Redirection après succès** :
   - Une fois l'image sauvegardée, l'utilisateur est redirigé vers une vue détail correspondant à l'image créée (grâce à `get_absolute_url()`).

6. **Rendu du formulaire dans le template** :
   - Si le formulaire n'est pas soumis ou s'il contient des erreurs, il est rendu dans le template `'images/image/create.html'`.

### Points importants :
- **Sécurité et validations** :
   - Le formulaire `ImageCreateForm` gère les validations de l'URL et des autres champs (comme vu dans votre code précédent).
   - L'utilisation de `@login_required` garantit que seuls les utilisateurs autorisés peuvent soumettre des images.

- **Expérience utilisateur** :
   - Les messages (via `django.contrib.messages`) améliorent la communication avec l'utilisateur en affichant des informations sur le statut de l'opération.

Ce code est bien structuré et conforme aux bonnes pratiques Django. 👍
"""