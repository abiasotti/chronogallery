from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('health/', views.health_check_view, name='health_check'),
    path('', views.photo_gallery_view, name='photo_gallery'),
    path('albums/', views.album_overview_view, name='album_overview'),
    path('albums/<int:album_id>/', views.album_detail_view, name='album_detail'),
    path('albums/<int:album_id>/delete/', views.delete_album_view, name='album_delete'),
    path('albums/<int:album_id>/edit/', views.edit_album_view, name='album_edit'),
    path('albums/create/', views.create_album_view, name='album_create'),
    path('photo/<int:photo_id>/', views.photo_detail_view, name='photo_detail'),
    path('photo/<int:photo_id>/json/', views.photo_detail_json_view, name='photo_detail_json'),
    path('photo/<int:photo_id>/set_cover/', views.set_photo_as_cover_view, name='photo_set_cover'),
    path('photo/<int:photo_id>/delete/', views.delete_photo_view, name='photo_delete'),
    path('photos/bulk_delete/', views.bulk_delete_photos_view, name='bulk_delete_photos'),
    path('photos/ajax_upload/', views.ajax_photo_upload_view, name='ajax_photo_upload'),
] 