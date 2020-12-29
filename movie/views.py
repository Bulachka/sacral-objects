from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import (ListView, DetailView,)

from .forms import MovieForm, EmailPostForm #VoteForm
from .models import Movie #Vote

SUBJECT_POST_SHARE_TEMPLATE = '{name} рэкамендуе Вам пачытаць пра {title}'
MESSAGE_POST_SHARE_TEMPLATE = 'Даведайся болей пра "{title}" па спасылцы {address}\n\nМой каментар: {comments}'


class MovieList(ListView):
    model = Movie


@login_required
def movie_new(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect('movie:MovieList')
    else:
        form = MovieForm()
    return render(request, 'movie/movie_new', {'form': form})


def movie_edit(request, pk):
    post = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = MovieForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect('movie:MovieList')
    else:
        form = MovieForm(instance=post)
    return render(request, 'movie/movie_new', {'form': form})


def movie_share(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri()
            subject = SUBJECT_POST_SHARE_TEMPLATE.format(name=cd['name'], title=movie.title)
            message = MESSAGE_POST_SHARE_TEMPLATE.format(title=movie.title, address=post_url, name=cd['name'],
                                                         comments=cd['comments'])
            send_mail(subject, message, 'sacral.object@gmail.com', [cd['to_email'], ])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'movie/movie_share.html', {'movie': movie, 'form': form, 'sent': sent})


class MovieDetail(DetailView):
    queryset = Movie.objects.all_with_prefetch_authors()
"""
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object,
                user=self.request.user
            )
            if vote.id:
                vote_form_url = reverse(
                    'movie:UpdateVote',
                    kwargs={
                        'movie_id': vote.movie.id,
                        'pk': vote.id})
            else:
                vote_form_url = (
                    reverse(
                        'movie:CreateVote',
                        kwargs={
                            'movie_id': self.object.id}
                    )
                )
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
        return ctx
"""