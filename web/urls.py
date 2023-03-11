from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from web.views import NotesListView, NoteDetailView, NoteUpdateView, RegistrationView, login_view, logout_view, \
    NoteCreateFormView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='notes_list'), name='main'),
    path('notes/', NotesListView.as_view(), name='notes_list'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note'),
    path('note/add/', NoteCreateFormView.as_view(), name='notes_add'),
    path('note/<int:id>/edit', NoteUpdateView.as_view(), name='notes_edit'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]