from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from .models import Articles
from .forms import ArticlesForm
# Create your views here.
class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            context['articles'] = Articles.objects.filter(title__icontains=query)
        else:
            context['articles'] = Articles.objects.all()
        context['form'] = ArticlesForm()
        return context
    
    def post(self, request):
        form = ArticlesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        return self.render_to_response(self.get_context_data(form=form))

class ArticleUpdateView(UpdateView):
    model = Articles
    form_class = ArticlesForm
    template_name = 'main/create_form.html'
    success_url = reverse_lazy('index')