from .models import Footer, Principal, Banners


def return_infos(request):
    return {
        "footer": Footer.objects.first(),
        "principal": Principal.objects.first(),
    }