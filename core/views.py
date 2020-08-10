from django.shortcuts import render


def main(request):

    ''' first page '''

    return render(request, "core/main.html")
