from django.contrib import admin
from django.urls import path

from web.views import notes_view, main_view, note_view

urlpatterns = [
    path('', main_view),
    path('notes/', notes_view, name='notes_list'),
    path('notes/<int:id>', note_view, name='note'),
]