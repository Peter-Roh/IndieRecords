from django.shortcuts import render


def main(request):

    ''' users page to choose how to sign up '''

    return render(request, "users/user.html")
