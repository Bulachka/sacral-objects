from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import (CachePageVaryOnCookieMixin)

from django.views import generic
from django.views.generic import (ListView, DetailView, )
from django.views.generic.edit import CreateView
from taggit.models import Tag

from .models import Stones, Typ, Mentions, Authors, Comment
from movie.models import Movie
from .forms import StonesForm, MentionsForm, AuthorsForm, CommentForm, \
    StonesImageForm, EmailPostForm

SUBJECT_POST_SHARE_TEMPLATE = '{name} рэкамендуе Вам пачытаць пра {title}'
MESSAGE_POST_SHARE_TEMPLATE = 'Даведайся болей пра "{title}" па спасылцы {address}\n\nМой каментар: {comments}'


def index(request, tag_slug=None):
    stones = Stones.objects.all()
    typs = Typ.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        stones = Stones.objects.filter(tags__in=[tag])
    context = {'stones': stones, 'typs': typs, 'tag': tag}
    return render(request, 'volumbf/index.html', context)


def by_typ(request, typ_id):
    stst = Stones.objects.filter(typ=typ_id)
    typs = Typ.objects.all()
    current_typ = Typ.objects.get(pk=typ_id)
    context = {'stst': stst, 'typs': typs, 'current_typ': current_typ}
    return render(request, 'volumbf/by_typ.html', context)


class StonesCreateView(LoginRequiredMixin, CreateView):
    template_name = 'volumbf/create.html'
    form_class = StonesForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['typs'] = Typ.objects.all()
        return context


class MentionsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'volumbf/createMentions.html'
    form_class = MentionsForm
    success_url = reverse_lazy('index')


class AuthorsCreateView(LoginRequiredMixin, CreateView):
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
            post_url = request.build_absolute_uri()
            subject = SUBJECT_POST_SHARE_TEMPLATE.format(name=cd['name'], title=post.title)
            message = MESSAGE_POST_SHARE_TEMPLATE.format(title=post.title, address=post_url, name=cd['name'],
                                                         comments=cd['comments'])
            send_mail(subject, message, 'sacral.object@gmail.com', [cd['to_email'], ])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'volumbf/post_share.html', {'post': post, 'form': form, 'sent': sent})
