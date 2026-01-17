from importlib import reload
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Listing,Location
from .forms import ListingForm,ProfileForm,LocationForm

from users.forms import LocationForm


# Create your views here.

def main_page(request):
    #return HttpResponse("<h1>hello</h1>")
    return render(request,"views/main.html",{"name":"AutoMax"})


@login_required
def home_view(request):
    listing=Listing.objects.all()
    context={'listing':listing}
    return render(request,"views/home.html",context)




@login_required
def list_view(request):
    if request.method=='POST':

        try:
            listing_form = ListingForm(request.POST,request.FILES)
            location_form=LocationForm(request.POST )
            if listing_form.is_valid() and location_form.is_valid():
                listing=listing_form.save(commit=False)
                listing_location=location_form.save()
                listing.seller=request.user.profile
                listing.location=listing_location
                listing.save()
                messages.info(request,f'listing done{listing.model}')
                return redirect('home')
            else:
                raise Exception()
            
        except Exception as error:
            print(error)
            messages.error(request,'error to listig data')

    elif request.method=='GET':
        listing_form = ListingForm()
        location_form=LocationForm()

        return render(request, 'views/list.html',{'listing_form': listing_form,'location_form':location_form})

@login_required
def listing_view(request,id):
    try:
        listings=Listing.objects.get(id=id)
        if listings is None:
            raise Exception
        return render(request,'views/listing.html',{'listing':listings})
    
    except Exception as e:
        messages.error(request,'Invalid product id ')
        return redirect('home')
        
        
        
        
        


@login_required
def edit_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form = ListingForm(
                request.POST, request.FILES, instance=listing)
            location_form = LocationForm(
                request.POST, instance=listing.location)
            if listing_form.is_valid and location_form.is_valid:
                listing_form.save()
                location_form.save()
                messages.info(request, f'Listing {id} updated successfully!')
                return redirect('home')
            else:
                messages.error(
                    request, f'An error occured while trying to edit the listing.')
                return reload()
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
        context = {
            'location_form': location_form,
            'listing_form': listing_form
        }
        return render(request, 'views/edit.html', context)
    except Exception as e:
        messages.error(
            request, f'An error occured while trying to access the edit page.')
        return redirect('home')









@login_required
def profile_update(request):
    profile = request.user.profile

    # IMPORTANT: location is linked via profile
    location = profile.location

    # If location does not exist, create it
    if location is None:
        location = Location.objects.create()
        profile.location = location
        profile.save()

    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=profile
        )
        location_form = LocationForm(
            request.POST, instance=location
        )

        if profile_form.is_valid() and location_form.is_valid():
            profile_form.save()
            location_form.save()
            return redirect('home')  # or profile page
    else:
        profile_form = ProfileForm(instance=profile)
        location_form = LocationForm(instance=location)

    return render(request, 'views/profile_update.html', {
        'profile_form': profile_form,
        'location_form': location_form,
    })
