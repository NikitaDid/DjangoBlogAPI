from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index. And you are on the main page.")
