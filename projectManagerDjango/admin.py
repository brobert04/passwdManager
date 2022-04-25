from django.contrib import admin
from .models import UserInformation


# ADAUGAM MODELUL BAZEI DE DATE CU INFORMATIILE USERULUI PAGINII DE ADMIN
admin.site.register(UserInformation)