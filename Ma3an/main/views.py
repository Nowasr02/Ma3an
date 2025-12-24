from django.shortcuts import render, redirect
from django.http import HttpRequest
from agency.models import Tour
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def home_view(request: HttpRequest):
    tours = Tour.objects.all().order_by('-start_date')[:6]
    return render(request, "main/home.html", {"tours": tours})


def contact(request):
    if request.method != "POST":
        return redirect("main:home_view")

    full_name = request.POST.get("full_name", "").strip()
    email = request.POST.get("email", "").strip()
    message = request.POST.get("message", "").strip()

    subject = f"New Contact Message from {full_name}"

    ctx = {
        "full_name": full_name,
        "email": email,
        "message": message,
    }

    text_body = render_to_string("main/contact_email.txt", ctx)
    html_body = render_to_string("main/contact_email.html", ctx)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_RECEIVER_EMAIL],
        reply_to=[email] if email else None,
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)

    messages.success(request, "Your message has been sent. We’ll get back to you soon.")
    return redirect("/#contact")
