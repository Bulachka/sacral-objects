from django.shortcuts import render, get_object_or_404, redirect


from .models import Stones, Typ, Mentions, Authors

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

from django.views.generic.edit import CreateView

from .forms import StonesForm, MentionsForm, AuthorsForm
from django.urls import reverse_lazy

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

def stone_detail(request, pk):
    stones = get_object_or_404(Stones, pk=pk)
    typs = Typ.objects.all()
    works = Mentions.objects.filter(sacral_objects__in=[stones])
    return render(request, 'volumbf/stone_detail.html', {'stones': stones, 'typs': typs, 'works': works})


def bibliography(request): 
    works = Mentions.objects.all()
    for work in works:
        work.writers = Authors.objects.filter(publications__in=[work])
    return render(request, 'volumbf/bibliography.html', {'works': works, 'work.writers': work.writers})

def work_detail(request, pk):
    works = get_object_or_404(Mentions, pk=pk)
    authors = Authors.objects.filter(publications__in=[works])
    return render(request, 'volumbf/work_detail.html', {'works': works, 'authors': authors})

def author_detail(request, pk): 
    authors = get_object_or_404(Authors, pk=pk)
    works = Mentions.objects.filter(authors__in=[authors]) #Choices are: authors, id, sacral_objects, work
    return render(request, 'volumbf/author_detail.html', {'works': works, 'authors': authors})  

