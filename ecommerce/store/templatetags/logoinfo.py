from django import template
from store.models import MyFavicon,MyLogo


register = template.Library()


@register.filter
def logo(request):
  
        logo = MyLogo.objects.filter(is_active=True).order_by('-id').first()
        if logo and logo.image:
             
          return logo.image.url
        else:
            return '/static/assets/images/logo.png' 

    

  


@register.filter
def favicon(request):
    favicon = MyFavicon.objects.filter(is_active=True).order_by('-id').first()
    if favicon and favicon.image:
        return favicon.image.url
    else:   
        return '/static/assets/images/favicon_defualt.png' 