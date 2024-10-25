from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, RedirectView, FormView, CreateView, UpdateView, DeleteView

from web.form import NoteForm, AuthForm
from web.models import Note, Tag, User


class NotesListView(ListView):
    template_name = 'web/main.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Note.objects.none()
        queryset = Note.objects.filter(user=self.request.user)
        return self.filter_queryset(queryset)

    def filter_queryset(self, notes):
        self.with_alerts = 'with_alerts' in self.request.GET
        self.search = self.request.GET.get('search', None)

        try:
            self.tag_id = int(self.request.GET.get('tag_id', None))
        except (TypeError, ValueError):
            self.tag_id = None

        if self.with_alerts:
            notes = notes.filter(alert_send_at__isnull=False)

        if self.search:
            notes = notes.filter(
                Q(title__icontains=self.search) |
                Q(text__icontains=self.search)
            )

        if self.tag_id:
            tag = Tag.objects.get(id=self.tag_id)
            notes = notes.filter(tags__in=[tag])
        return notes

    def get_context_data(self, *, object_list=None, **kwargs):
        if not self.request.user.is_authenticated:
            return {}
        return {
            **super(NotesListView, self).get_context_data(),
            'count': Note.objects.filter(user=self.request.user).count(),
            'with_alerts': self.with_alerts,
            'query_params': self.request.GET,
            'search': self.request.GET.get('search'),
            'tags': Tag.objects.filter(user=self.request.user),
            'tag_id': self.tag_id,
        }


class NoteDetailView(DetailView):
    template_name = 'web/note.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteMixin:
    template_name = 'web/note_form.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_initial(self):
        return {'user': self.request.user}

    def get_success_url(self):
        return reverse('note', args=(self.object.id,))

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Note.objects.none()
        return Note.objects.filter(user=self.request.user)


class NoteCreateFormView(CreateView, NoteMixin):
    form_class = NoteForm


class NoteUpdateView(NoteMixin, UpdateView):
    form_class = NoteForm

    def get_context_data(self, **kwargs):
        return {
            **super(NoteUpdateView, self).get_context_data(),
            'id': self.kwargs[self.slug_url_kwarg],
        }


class NoteDeleteView(NoteMixin, DeleteView):
    template_name = 'web/note_delete.html'

    def get_success_url(self):
        return reverse('main')


class RegistrationView(View):
    def _render(self, request, form=AuthForm(), is_success=False):
        return render(request, 'web/registration.html', {
            'form': form,
            'is_success': is_success,
        })

    def get(self, request, *args, **kwargs):
        return self._render(request)

    def post(self, request, *args, **kwargs):
        is_success = False
        form = AuthForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            is_success = True
        return self._render(request, form, is_success)


def login_view(request):
    form = AuthForm()
    message = None
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is None:
                message = 'Электронная почта или пароль не правильный'
            else:
                login(request, user)
                next_url = 'main'
                if 'next' in request.GET:
                    next_url = request.GET.get('next')
                return redirect(next_url)
    return render(request, 'web/login.html', {
        'form': form,
        'message': message,
    })


def logout_view(request):
    logout(request)
    return redirect('main')
