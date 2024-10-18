from django import template
from store.models import MyFavicon,MyLogo


register = template.Library()


@register.filter
def logo(user):
    if user.is_authenticated:
        logo = MyLogo.objects.filter(user=user,is_active=True).order_by('-id').first()
        return logo.image.url
    else:
         logo = MyLogo.objects.filter(usis_active=True).order_by('-id').first()
         return logo.image.url




@register.filter
def favicon(user):
    if user.is_authenticated:
        favicon = MyFavicon.objects.filter(user=user,is_active=True).order_by('-id').first()
        return favicon.image.url
    else:
         favicon = MyFavicon.objects.filter(user=user,is_active=True).order_by('-id').first()
         return favicon.image.url