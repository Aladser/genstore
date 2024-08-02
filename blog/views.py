from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from pytils.translit import slugify

from blog.forms import BlogForm
from blog.models import Blog
from config.settings import EMAIL_HOST_USER


class BlogListView(ListView):
    """LIST"""

    model = Blog
    template_name = 'blog/list.html'
    title = "блоги"
    extra_context = {
        'section': 'Блоги',
        "title": title,
        'header': title
    }

    def get_queryset(self,*args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if 'type' in self.request.GET:
            if self.request.GET['type'] == 'publish':
                return queryset.filter(is_published=True)
            elif self.request.GET['type'] == 'non-publish':
                return queryset.filter(is_published=False)
        return queryset


class BlogDetailView(DetailView):
    """SHOW"""

    model = Blog
    template_name = 'blog/detail.html'
    extra_context = {
        'section': 'Блоги'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.is_published:
            # счетчик просмотров
            self.object.views_count += 1
            self.object.save()

        # отправка письма, если блог набрал 10 просмотров
        views_count = 10
        if self.object.views_count == views_count:
            content = f"Блог \"{self.object.name}\" набрал {views_count} просмотров"
            send_mail(
                content,
                content,
                EMAIL_HOST_USER,
                (EMAIL_HOST_USER,),
            )
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['header'] = f"{self.object.name}"

        return context


class BlogCreateView(CreateView):
    """CREATE"""

    model = Blog
    template_name = 'blog/form.html'
    form_class = BlogForm

    title = "добавить блог"
    extra_context = {
        'section': 'Блоги',
        "title": title,
        'header': title
    }

    def form_valid(self, form):
        if form.is_valid():
            # slug
            self.object = form.save()
            self.object.slug = slugify(self.object.name)
            self.object.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("blog:detail", kwargs={"pk": self.object.pk})


class BlogUpdateView(UpdateView):
    """UPDATE"""

    model = Blog
    template_name = 'blog/form.html'
    form_class = BlogForm
    extra_context = {
        'section': 'Блоги',
        "title": " изменить блог",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = f"изменить блог {self.object.name}"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("blog:detail", kwargs={"pk": self.kwargs["pk"]})


class BlogDeleteView(DeleteView):
    """DELETE"""

    model = Blog
    template_name = 'blog/confirm_delete.html'
    success_url = reverse_lazy('blog:list')
    extra_context = {
        'section': 'Блоги',
        'title': f"удаление блога"
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = f"удаление блога {self.object.name}"
        return context


def blog_publish(request):
    """публикация блога"""

    pk = request.POST['pk']
    publish_state = not request.POST['state'] == 'True'
    Blog.objects.filter(pk=pk).update(is_published=publish_state)

    return HttpResponseRedirect(reverse('blog:detail', kwargs={'pk': pk}))
