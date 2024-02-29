from django.shortcuts import render


def not_found(request):
    return render(request, "404.html")

def rejected(request):
    return render(request, "rejected.html")
def accepted(request):
    return render(request, "accepted.html")