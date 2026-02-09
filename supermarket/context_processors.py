from .models import Footer, Principal


def return_infos(request):
    return {
        "footer": Footer.objects.first(),
        "principal": Principal.objects.first(),
    }