from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'agency/dashboard.html')


def subscription(request):
    return render(request, 'agency/subscription.html')


def add_tour_view(request):
    return render(request, 'agency/add_tour.html')
