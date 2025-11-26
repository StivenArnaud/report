from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'frontend/core/index.html')

def error400(request, exception):
    context = {
        'title': '400',
        'content': 'Requête invalide'
    }
    return render(request, 'frontend/core/error.html', context=context, status=400)


def error403(request, exception):
    context = {
        'title': '403',
        'content': 'accès refusé'
    }
    return render(request, 'frontend/core/error.html', context=context, status=403)


def error404(request, exception):
    context = {
        'title': '404',
        'content': 'ressource non trouvée'
    }
    return render(request, 'frontend/core/error.html', context=context, status=404)


def error500(request, *args, **argv):
    context = {
        'title': '500',
        'content': 'Erreur interne'
    }
    return render(request, 'frontend/core/error.html', context=context, status=500)

def error503(request, exception):
    context = {
        'title': '503',
        'content': 'Service indisponible'
    }
    return render(request, 'frontend/core/error.html', context=context, status=503)