from PIL import Image
from django.shortcuts import redirect
from images.models import Image
from django.http import Http404 

import settings
import os

# Django image router
def load(request, image_id, size):
    try:
        i = Image.objects.get(name=image_id)
    except:
        raise Http404
    if not size or size == 'full':
        return redirect(settings.MEDIA_URL+'images/full/'+image_id)
    if size not in settings.IMAGE_SIZES:
        raise Http404
    # get size dir/check if image exists
    sizedir=settings.MEDIA_URL+'images/'+size+'/'
    if os.path.isfile(sizedir+image_id):
        return redirect(settings.MEDIA_URL+'images/'+size+'/'+image_id)
    if not os.path.exists(sizedir):
        os.makedirs(sizedir)
    # open up the image
    img=Image.open(i.image.path)
    iw=i.image.width
    ih=i.image.height
    nw=settings.IMAGE_SIZES[size][0]
    nh=settings.IMAGE_SIZES[size][1]
    #auto=settings.IMAGE_SIZES[size][2]
    # resizing needed
    if (iw, ih) != (nw, nh):
        iratio=float(iw)/float(ih)
        nratio=float(nw)/float(nh)
        if img.mode not in ('L','RGB'):
            img=img.convert('RGB')
        if iratio > nratio:
            # image is too wide. aspectw is the width with proper ratio
            aspectw=int(round(nh*iratio))
            img=img.resize((aspectw, nh), Image.ANTIALIAS)
            # then we crop it to the correct size
            middle=int(round((aspectw-nw)/2.0))
            img=img.crop((middle,0,middle+nw,nh))
        elif iratio < nratio:
            # image is too tall
            aspecth=int(round(nw/iratio))
            img=img.resize((nw, aspecth), Image.ANTIALIAS)
            middle=int(round((aspecth-nh)/2.0))
            img=img.crop((0,middle,nw,middle+nh))
        else:
            # proper ratio
            img=img.resize((nw,nh), Image.ANTIALIAS)
    img.save(sizedir+image_id,'PNG')
    return redirect(settings.MEDIA_URL+'images/'+size+'/'+image_id)