from django.shortcuts import render


def main(request):

    ''' first page '''

    return render(request, "users/main.html")


def signup(request):

    ''' signup page '''

    return render(request, "users/signup.html")
