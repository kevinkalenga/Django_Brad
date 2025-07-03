from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
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

    #  Check if user has made inquiry already 
    if request.user.is_authenticated:
       user_id = request.user.id 
       has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id) 
       if has_contacted:
          messages.error(request, 'You have already made an inquiry for this listing')
          return redirect('/listings/'+listing_id)
   
   
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

    # Send email 
    send_mail(
        'Property Listing Inquiry',
        'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
        'kevinkalenga10@gmail.com',
        [realtor_email, 'nathanaelkalenga2@gmail.com'],
        fail_silently=False
    )

    messages.success(
        request, 'Your request has been submitted, a realtor will get back to you soon.'
    )
    return redirect('/listings/' + str(listing_id))

