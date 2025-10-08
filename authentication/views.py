import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
from authentication.models import User
from authentication.forms import RegisterForm, LoginForm, UpdateUserForm

def login_view(request):
    msg = _("")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                login(request, user)

                messages.success(request, _(f"Salut {user.get_full_name()} ! Nous sommes content de vous revoir"))
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        next_page = params['next']
                        return redirect(next_page)
                except:
                    return redirect('reporting:list_reports')
            else:
                msg = _("Adresse e-mail ou mot de passe incorrect!")
        else:
            msg = _("Veillez renseigner correctement tous les champs !!")

    else:
        form = LoginForm()

    context = {
        'form': form,
        'message': msg,
    }

    return render(request, 'frontend/authentication/login.html', context)



def user_register(request):
    message = _("")
    if request.method == 'POST':
        print(request.POST)
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['email'],
                password=form.cleaned_data['phone'],
                role=User.EMPLOYEE,
            )
            user.username = user.email
            user.set_password(form.cleaned_data['phone'])
            user.save()
            messages.success(request, _(f"Salut {user.get_full_name()} ! Votre compte a été créé avec succès."))

            return redirect('authentication:list_users')
            #return render(request, 'frontend/authentication/partials/add_user.html', {'single_user': user})
        else:
            messages.error(request, _("Veillez renseigner correctement tous les champs !!"))
            #print(form.errors)
            #return HttpResponse('')
            return redirect('authentication:list_users')
    else:
        form = RegisterForm()

        #return HttpResponse('')
        return redirect('authentication:list_users')




@login_required
def list_users(request):
    all_users = User.objects.select_related('responsible').all()
    responsible_users = User.objects.filter(role=User.RESPONSIBLE)
    paginator = Paginator(all_users, 10)
    page = request.GET.get('page')

    try:
        all_users = paginator.page(page)
    except PageNotAnInteger:
        all_users = paginator.page(1)
    except EmptyPage:
        all_users = paginator.page(paginator.num_pages)

    context = {
        'all_users': all_users,
        'employee_count': User.objects.filter(role=User.EMPLOYEE).count(),
        'rh_count': User.objects.filter(role=User.RH).count(),
        'responsible_count': User.objects.filter(role=User.RESPONSIBLE).count(),
        'responsible_users': responsible_users,
    }

    return render(request, 'frontend/authentication/list_users.html', context)



@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Mot de passe modifie avec succes !"))
            return redirect('authentication:list_users')
        else:
            messages.error(request, _("Veuillez remplir tous les champs !"))
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'frontend/authentication/change_password.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Vos informations ont ete modifie avec succes !"))
            return redirect('reporting:list_reports')
        else:
            messages.error(request, _("Veuillez remplir tous les champs !"))
    else:
        form = UpdateUserForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'frontend/authentication/profile.html', context)
