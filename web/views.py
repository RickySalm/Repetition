from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from web.models import Note, Tag


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
    note = Note.objects.get(id=id)
    return render(request, 'web/note.html',{
        'note': note
    })
