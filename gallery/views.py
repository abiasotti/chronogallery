from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from .models import Photo, Album
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect


def photo_gallery_view(request):
    if request.method == 'POST':
        album_id = request.POST.get('album')
        new_album_name = request.POST.get('new_album')
        image = request.FILES.get('image')
        album = None
        if album_id:
            try:
                album = Album.objects.get(id=album_id)
            except Album.DoesNotExist:
                album = None
        if new_album_name:
            album = Album.objects.create(title=new_album_name)
        if album and image:
            photo = Photo.objects.create(album=album, image=image)
            if not album.cover:
                album.cover = photo.image
                album.save()
            return redirect('gallery:photo_gallery')
    photos = Photo.objects.order_by('-uploaded_at')
    albums = Album.objects.all().order_by('title')
    return render(request, 'gallery/photo_gallery.html', {'photos': photos, 'albums': albums})


def album_overview_view(request):
    albums = Album.objects.all().order_by('-created_at')
    return render(request, 'gallery/album_overview.html', {'albums': albums})


def photo_detail_view(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    prev_photo = Photo.objects.filter(uploaded_at__lt=photo.uploaded_at).order_by('-uploaded_at').first()
    next_photo = Photo.objects.filter(uploaded_at__gt=photo.uploaded_at).order_by('uploaded_at').first()
    return render(request, 'gallery/photo_detail.html', {
        'photo': photo,
        'prev_photo': prev_photo,
        'next_photo': next_photo,
    })


def photo_detail_json_view(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    prev_photo = Photo.objects.filter(uploaded_at__lt=photo.uploaded_at).order_by('-uploaded_at').first()
    next_photo = Photo.objects.filter(uploaded_at__gt=photo.uploaded_at).order_by('uploaded_at').first()
    data = {
        'id': photo.id,
        'image_url': photo.image.url,
        'album': photo.album.title,
        'uploaded_at': photo.uploaded_at.strftime('%Y-%m-%d %H:%M'),
        'prev_id': prev_photo.id if prev_photo else None,
        'next_id': next_photo.id if next_photo else None,
    }
    return JsonResponse(data)


def album_detail_view(request, album_id):
    album = Album.objects.get(id=album_id)
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            photo = Photo.objects.create(album=album, image=image)
            if not album.cover:
                album.cover = photo.image
                album.save()
            return redirect('gallery:album_detail', album_id=album.id)
    photos = album.photos.order_by('-uploaded_at')
    return render(request, 'gallery/album_detail.html', {'album': album, 'photos': photos})


def delete_album_view(request, album_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    album = Album.objects.get(id=album_id)
    album.delete()
    from django.urls import reverse
    from django.shortcuts import redirect
    return redirect(reverse('gallery:album_overview'))


def edit_album_view(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    photos = album.photos.all()
    if request.method == 'POST':
        new_title = request.POST.get('title', '').strip()
        cover_id = request.POST.get('cover')
        if new_title:
            album.title = new_title
        if cover_id:
            try:
                cover_photo = photos.get(id=cover_id)
                album.cover = cover_photo.image
            except Photo.DoesNotExist:
                pass
        album.save()
        from django.urls import reverse
        return redirect(reverse('gallery:album_detail', args=[album.id]))
    return render(request, 'gallery/edit_album_modal.html', {'album': album, 'photos': photos})


def set_photo_as_cover_view(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    album = photo.album
    if request.method == 'POST':
        album.cover = photo.image
        album.save()
        from django.urls import reverse
        return redirect(reverse('gallery:photo_detail', args=[photo.id]))
    return HttpResponseNotAllowed(['POST'])

def delete_photo_view(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    album_id = photo.album.id
    if request.method == 'POST':
        photo.delete()
        from django.urls import reverse
        return redirect(reverse('gallery:album_detail', args=[album_id]))
    return HttpResponseNotAllowed(['POST'])

def create_album_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if title:
            album = Album.objects.create(title=title, description=description)
            from django.urls import reverse
            return redirect(reverse('gallery:album_overview'))
    return render(request, 'gallery/create_album_modal.html')

def bulk_delete_photos_view(request):
    if request.method == 'POST':
        photo_ids = request.POST.getlist('photo_ids')
        if photo_ids:
            Photo.objects.filter(id__in=photo_ids).delete()
        return redirect('gallery:photo_gallery')
    return HttpResponseNotAllowed(['POST'])


@require_POST
@csrf_protect
def ajax_photo_upload_view(request):
    album_id = request.POST.get('album')
    new_album_name = request.POST.get('new_album')
    files = request.FILES.getlist('images')  # Expecting multiple files
    album = None
    if album_id:
        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Album not found.'}, status=400)
    if new_album_name:
        album = Album.objects.create(title=new_album_name)
    if not album:
        return JsonResponse({'success': False, 'error': 'No album specified.'}, status=400)
    if not files:
        return JsonResponse({'success': False, 'error': 'No images uploaded.'}, status=400)
    photo_ids = []
    for image in files:
        photo = Photo.objects.create(album=album, image=image)
        photo_ids.append(photo.id)
        if not album.cover:
            album.cover = photo.image
            album.save()
    return JsonResponse({'success': True, 'photo_ids': photo_ids})
