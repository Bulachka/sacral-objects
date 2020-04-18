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

from .forms import StonesForm
from django.urls import reverse_lazy

class StonesCreateView(CreateView):
    template_name = 'volumbf/create.html'
    form_class = StonesForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['typs'] = Typ.objects.all()
        return context


def stone_detail(request, pk):
    stones = get_object_or_404(Stones, pk=pk)
    typs = Typ.objects.all()
    works = Mentions.objects.all()
    return render(request, 'volumbf/stone_detail.html', {'stones': stones, 'typs': typs, 'works': works})


def bibliography(request):
    works = Mentions.objects.all()
    authors = Authors.objects.all()
    return render(request, 'volumbf/bibliography.html', {'works': works, 'authors': authors})

def work_detail(request, pk): #я акурат чытала, што поле айдзішнікаў не трэба яўна аб'яўляць, яно ствараецца аўтаматычна
    work = get_object_or_404(Mentions, pk=pk)
    authors = Authors.objects.all()
    return render(request, 'volumbf/work_detail.html', {'work': work, 'authors': authors})

def author_detail(request, pk): 
    author = get_object_or_404(Authors, pk=pk)
    works = Mentions.objects.all()
    return render(request, 'volumbf/author_detail.html', {'works': works, 'author': author})  

