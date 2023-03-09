from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from web.form import NoteForm, RegistrationForm
from web.models import Note, Tag, User


def main_view(request):
    return redirect('notes_list')


def notes_view(request):
    with_alerts = 'with_alerts' in request.GET
    search = request.GET.get('search', None)
    notes = Note.objects.all()

    try:
        tag_id = int(request.GET.get('tag_id', None))
    except (TypeError, ValueError):
        tag_id = None

    if with_alerts:
        notes = notes.filter(alert_send_at__isnull=False)

    if search:
        notes = notes.filter(
            Q(title__icontains=search) |
            Q(text__icontains=search)
        )

    if tag_id:
        tag = Tag.objects.get(id=tag_id)
        notes = notes.filter(tags__in=[tag])

    return render(request, 'web/main.html', {
        'count': Note.objects.count(),
        'notes': notes,
        'with_alerts': with_alerts,
        'query_params': request.GET,
        'search': request.GET.get('search'),
        'tags': Tag.objects.all(),
        'tag_id': tag_id,
    })


def note_view(request, id):
    note = get_object_or_404(Note, id=id)
    return render(request, 'web/note.html', {
        'note': note
    })


def note_edit_view(request, id=None):
    user = User.objects.first()
    form = NoteForm()

    if id is not None:
        note = get_object_or_404(Note, id=id)
        form = NoteForm(instance=note)

    if request.method == 'POST':
        form = NoteForm(request.POST, initial={'user': user})
        if form.is_valid():
            note = form.save()
            return redirect('note', note.id)

    return render(request, 'web/note_form.html', {
        'id': id,
        'form': form,
    })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User(email=email, username=email.split('@')[0])
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, 'web/registration.html', {
        'form': form,
        'is_success': is_success,
    })
