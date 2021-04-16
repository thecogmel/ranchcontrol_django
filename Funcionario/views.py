from django.http import HttpResponse


def index(request):
    return HttpResponse("Rota acessada: Funcionários, teste return to maine!")
