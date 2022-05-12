# LIBRARII DJANGO
from django.shortcuts import redirect, render
from django.conf import ENVIRONMENT_VARIABLE, settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import random
from django.core.mail import send_mail
from flask import request_tearing_down
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
import mechanize
from .models import UserInformation

# VARIABILE GLOBALE
globalCode = ""
parole = None

# INITIALIZARE FERNET
fernet = Fernet(settings.KEY)

# INSTANTA A BROWSERULUI
browser = Browser()
# PENTRU A IGNORA WEBSITEURILE CARE NU NE LASA SA LE UTILIZAM INFORMATIILE
browser.set_handle_robots(False)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
 

def home(request):

    # PRELUAM DATELE DIN FORMULARUL DE INREGISTRARE(SIGN-UP FORM) SI EFECTUAM ANUMITE VERIFICARI
    if request.method == "POST":
        if "signup-form" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")

            # PAROLELE NU SUNT LA FEL
            if password != password2:
                msg = "Your passwords don't match! Make sure you use the same password!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)

            # USERNAME DEJA EXISTENT
            elif User.objects.filter(username=username).exists():
                msg = f"Username '{username}' is already being used!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)

             # EMAIL DEJA EXSITENT
            elif User.objects.filter(email=email).exists():
                msg = f"The email '{email}' is already being used!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)

            # DACA TOATE VERIFICARILE SUNT CORECTE, CREĂM UN NOU USER
            else:
                User.objects.create_user(username, email, password)
                user = authenticate(
                    request, username=username, password=password2)
                if user is not None:
                    login(request, user)
                    msg = f"Hello, {username}! You have successfully signed up!"
                    messages.success(request, msg)
                    return HttpResponseRedirect(request.path)

        # DELOGARE
        elif "logout" in request.POST:
            logout(request)
            msg = "You have successfully logged out!"
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)

        # PRELUAM DATELE DIN FORMULARUL DE LOGARE SI EFECTAAM CONECTAREA
        elif 'login-form' in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            loginUser = authenticate(
                request, username=username, password=password)
            # USERNAME-UL SI PAROLA NU COINCID
            if loginUser is None:
                msg = "Login failed! Use the the right credentials!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                # GENERAM CODUL DE VERIFICARE CARE VA FI TRIMIS PRIN MAIL LA ADRESA SPECIFICATA
                code = str(random.randint(100000, 999999))
                global globalCode
                globalCode = code
                send_mail(
                    "MYKEY - Password Manager : Verification Code",
                    f"Your verification code for is: {code}",
                    settings.EMAIL_HOST_USER,
                    [loginUser.email],
                    fail_silently=False,
                )
                return render(request, "index.html", {
                    "code": code,
                    "user": loginUser})

        elif "confirm-button" in request.POST:
            userCode = request.POST.get("email-code")
            loggedUser = request.POST.get("user")
            if userCode != globalCode:
                msg = "The code does not match with the one from the email!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                login(request, User.objects.get(username=loggedUser))
                msg = f"Hello, {loggedUser}. You logged in successfully!"
                messages.success(request, msg)
                return HttpResponseRedirect(request.path)
        elif "add-password" in request.POST:
            url = request.POST.get("url")
            accountEmail = request.POST.get("email")
            accountPassword = request.POST.get("password")

            # ENCRIPTAREA DATELOR UTILIZATORULUI
            encryptedEmail = fernet.encrypt(accountEmail.encode())
            encryptedPassword = fernet.encrypt(accountPassword.encode())

            # PRELUAREA TITLULUI SI A ICONITEI WEBSITEULUI
            try:
                browser.open(url)
                pageTitle = browser.title()
                
            except(mechanize.HTTPError, mechanize.URLError):
                msg = "The URL you have entered is not valid!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            try:
                icon = favicon.get(url)[0].url
            except:
                icon = "Icon"
            
            db_password = UserInformation.objects.create(
                user=request.user,
                name=pageTitle,
                logo=icon,
                email=encryptedEmail.decode(),
                password=encryptedPassword.decode()
            )
            msg = "Your password was saved! Click on 'Account' to see your passwords!"
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)

    return render(request, "index.html", {})


def passwords(request):
    if request.method == "POST":
        if "logout" in request.POST:
            logout(request)
            msg = "You have successfully logged out!"
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)

        elif "add-password" in request.POST:
            url = request.POST.get("url")
            accountEmail = request.POST.get("email")
            accountPassword = request.POST.get("password")

            # ENCRIPTAREA DATELOR UTILIZATORULUI
            encryptedEmail = fernet.encrypt(accountEmail.encode())
            encryptedPassword = fernet.encrypt(accountPassword.encode())

            # PRELUAREA TITLULUI SI A ICONITEI WEBSITEULUI
            browser.open(url)
            pageTitle = browser.title()

            icons = favicon.get(url)
            icon = icons[0].url

            # SALVAREA DATELOR IN BAZA DE DATE
            db_password = UserInformation.objects.create(
                user=request.user,
                name=pageTitle,
                logo=icon,
                email=encryptedEmail.decode(),
                password=encryptedPassword.decode()
            )
            msg = "Your password was saved!Click on 'View' to see your passwords!"
            messages.success(request, msg)
            return redirect(request.path)

        
    # TRIMITEREA DATELOR CATRE PAGINA 'VIEW', IMPLICIT CREAREA CARDURILOR CU INFORMATII
    userPasswords = UserInformation.objects.all().filter(user=request.user)
    for passwd in userPasswords:
        passwd.email = fernet.decrypt(passwd.email.encode()).decode()
        passwd.password = fernet.decrypt(passwd.password.encode()).decode()
    
    return render(request, "password.html", {
        "passwords": userPasswords
    })

# USERUL DECIDE SA STEARGA INFORMATILLE
def deleteItem(request, id):
    item = UserInformation.objects.get(pk=id)
    item.delete()
    return redirect('passwords')
