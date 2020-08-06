from django.shortcuts import render


def main(request):

    ''' the main page '''

    return render(request, "musics/main.html")
