from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import (LoginRequiredMixin)
from .mixins import (CachePageVaryOnCookieMixin)

from django.views import generic
from django.views.generic import (ListView, DetailView, )
from django.views.generic.edit import CreateView

from .models import Stones, Typ, Mentions, Authors, Comment
from movie.models import Movie
from .forms import StonesForm, MentionsForm, AuthorsForm, CommentForm, \
    StonesImageForm, EmailPostForm


def index(request):
    stst = Stones.objects.all
    typs = Typ.objects.all()
    context = {'stst': stst, 'typs': typs}
    return render(request, 'volumbf/index.html', context)


def by_typ(request, typ_id):
    stst = Stones.objects.filter(typ=typ_id)
    typs = Typ.objects.all()
    current_typ = Typ.objects.get(pk=typ_id)
    context = {'stst': stst, 'typs': typs, 'current_typ': current_typ}
    return render(request, 'volumbf/by_typ.html', context)


class StonesCreateView(CreateView):
    template_name = 'volumbf/create.html'
    form_class = StonesForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['typs'] = Typ.objects.all()
        return context


class MentionsCreateView(CreateView):
    template_name = 'volumbf/createMentions.html'
    form_class = MentionsForm
    success_url = reverse_lazy('index')


class AuthorsCreateView(CreateView):
    template_name = 'volumbf/createAuthors.html'
    form_class = AuthorsForm
    success_url = reverse_lazy('index')


"""
def stone_detail(request, pk):
    stones = get_object_or_404(Stones, pk=pk)
    typs = Typ.objects.all() #мадэль Typ звязана са Stones праз ForeignKey
    works = Mentions.objects.filter(sacral_objects__in=[stones]) #мадэль Mentions звязана са Stones праз ManyToMany
    return render(request, 'volumbf/stone_detail.html', {'stones': stones, 'typs': typs, 'works': works})
"""


class StonesDetail(generic.DetailView):
    queryset = Stones.objects.all_with_prefetch_mentions()
    template_name = 'volumbf/stone_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = self.stones_image_form()
        return context

    def stones_image_form(self):
        if self.request.user.is_authenticated:
            return StonesImageForm()
        return None


class StonesImageUpload(LoginRequiredMixin, CreateView):
    form_class = StonesImageForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['stones'] = self.kwargs['stones_id']
        return initial

    def render_to_response(self, context, **response_kwargs):
        stones_id = self.kwargs['stones_id']
        stones_detail_url = reverse('stone_detail', kwargs={'pk': stones_id})
        return redirect(to=stones_detail_url)

    def get_success_url(self):
        stones_id = self.kwargs['stones_id']
        stones_detail_url = reverse('stone_detail', kwargs={'pk': stones_id})
        return stones_detail_url


def bibliography(request):
    works = Mentions.objects.all()
    for work in works:
        work.writers = Authors.objects.filter(publications__in=[work])
    return render(request, 'volumbf/bibliography.html', {'works': works, 'work.writers': work.writers})


def work_detail(request, pk):
    works = get_object_or_404(Mentions, pk=pk)
    authors = Authors.objects.filter(publications__in=[works])
    return render(request, 'volumbf/work_detail.html', {'works': works, 'authors': authors})


"""
def author_detail(request, pk):
    authors = get_object_or_404(Authors, pk=pk)
    works = Mentions.objects.filter(authors__in=[authors])  # Choices are: authors, id, sacral_objects, work
    movies = Movie.objects.filter(director__in=[authors], creators__in=[authors])
    context = {'works': works, 'authors': authors, 'movies': movies}
    return render(request, 'volumbf/authors_detail.html', context)

    """


class AuthorDetail(DetailView):
    queryset = Authors.objects.all_with_prefetch_movies_and_mentions()


def add_comment_to_stone(request, pk):
    stones = get_object_or_404(Stones, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.stones = stones
            comment.save()
            return render(request, 'volumbf/stone_detail_redirect.html', {'stones': stones})
    else:
        form = CommentForm()
    return render(request, 'volumbf/add_comment_to_stone.html', {'form': form})


def post_share(request, pk):
    post = get_object_or_404(Stones, pk=pk)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading " {}'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
            return render(request, 'post_share.html', {'post': post, 'form': form, 'sent': sent})
    return render(request, 'post_share.html', {'post': post, 'sent': sent})
