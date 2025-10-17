from django.urls import path


from pointing import views


app_name = 'pointing'


urlpatterns = [
    path('add-presence/', views.add_presence, name='add_presence'),
]