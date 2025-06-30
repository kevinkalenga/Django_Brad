from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.views.decorators.http import require_POST


@require_POST  # Facultatif : assure que seule la méthode POST est autorisée
def contact(request):
    listing_id = request.POST.get('listing_id')
    listing = request.POST.get('listing')
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    message = request.POST.get('message')
    user_id = request.POST.get('user_id')
    realtor_email = request.POST.get('realtor_email')

    # Créer une instance de Contact
    contact_obj = Contact(
        listing=listing,
        listing_id=listing_id,
        name=name,
        email=email,
        phone=phone,
        message=message,
        user_id=user_id
    )

    contact_obj.save()

    messages.success(
        request, 'Your request has been submitted, a realtor will get back to you soon.'
    )
    return redirect('/listings/' + str(listing_id))

