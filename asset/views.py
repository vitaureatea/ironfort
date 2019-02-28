from django.shortcuts import render
from django.shortcuts import get_object_or_404

from . import models

def hostlist(request):
    assets = models.Asset.objects.all()
    return render(request,'assets.html', {'assets': assets})

def detail(request,asset_id):
    asset = get_object_or_404(models.Asset, id=asset_id)
    return render(request, 'detail.html', locals())

