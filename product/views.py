from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from config.settings import CACHED_TIME
from libs.custom_formatter import CustomFormatter
from libs.login_required_mixin import CustomLoginRequiredMixin
from product.forms import ProductForm, ProductVersionForm
from product.models import Product, ProductVersion


class ProductListView(ListView):
    """LIST"""

    paginate_by = 5
    model = Product
    template_name = 'product/list.html'

    title = 'товары'
    extra_context = {
        'section': title.title(),
        'header': title,
        'title': '',
        'css_list': ("publication.css",)
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if isinstance(self.request.user, AnonymousUser):
            # анонимы
            return queryset.filter(is_published=True).order_by('-updated_at')
        elif self.request.user.is_superuser:
            # админы
            return queryset.order_by('-updated_at')
        else:
            # остальные
            return queryset.filter(creator=self.request.user).union(queryset.filter(is_published=True)).order_by('-updated_at')


class ProductDetailView(DetailView):
    """SHOW"""

    model = Product
    template_name = 'product/detail.html'

    extra_context = {
        "section": "Товары",
        'css_list': ("publication.css",)
    }

    def get_object(self, queryset=None):
        # Кэширование товара для всех пользователей
        product_cache_key = f'product_detail_{self.kwargs["pk"]}'
        product = cache.get(product_cache_key)

        if product is None:
            product = super().get_object(queryset)
            cache.set(product_cache_key, product, CACHED_TIME)

        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['header'] = f"товар {self.object.name}"

        return context


class ProductCreateView(CustomLoginRequiredMixin, CreateView):
    """CREATE"""

    template_name = 'product/form.html'
    model = Product
    form_class = ProductForm

    extra_context = {
        "section": "Товары",
        'title': "добавить товар",
        'form_type': 'create'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_btn_name'] = 'Создать'
        context['back_url'] = reverse_lazy('product:list')
        context['required_fields'] = CustomFormatter.get_form_required_field_labels(context['form'])

        return context

    def form_valid(self, form):
        if form.is_valid():
            # указывает создателя товара
            self.object = form.save()
            self.object.creator = self.request.user
            self.object.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("product:detail", kwargs={"pk": self.object.pk})


class ProductUpdateView(CustomLoginRequiredMixin, UpdateView):
    """UPDATE"""

    template_name = 'product/form.html'
    model = Product
    form_class = ProductForm
    extra_context = {
        'section': 'Товары',
        'title': "изменить товар",
        'form_type': 'update'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # проверка доступа
        if self.request.user != context['object'].creator and not self.request.user.is_superuser:
            self.template_name = 'info.html'
            context['message'] = 'Ошибка 403: доступ запрещен'
            return context

        context['back_url'] = reverse_lazy("product:detail", kwargs={"pk": self.object.pk})
        context['form_btn_name'] = 'Сохранить'
        context['required_fields'] = CustomFormatter.get_form_required_field_labels(context['form'])

        # версия товара
        ProductVersionFormset = inlineformset_factory(Product, ProductVersion, form=ProductVersionForm, extra=1)
        if self.request.method == "POST":
            context['formset'] = ProductVersionFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = ProductVersionFormset(instance=self.object)

        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']

        # подсчет числа активных версий - проход REQUEST["POST"]
        current_version_count = 0
        for i in range(len(formset.forms)):
            key = f"product_version-{i}-is_current"
            if self.request.POST.get(key) == "on":
                current_version_count += 1
            if current_version_count > 1:
                form.add_error(None, 'У товара может быть только одна активная версия')
                return self.form_invalid(form)

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            form.add_error(None, formset.errors)
            return self.form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("product:detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(CustomLoginRequiredMixin, DeleteView):
    """DELETE"""

    model = Product
    template_name = 'product/confirm_delete.html'
    success_url = reverse_lazy('product:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'Товары'
        context['back'] = self.request.GET['type']

        # проверка доступа
        if self.request.user != context['object'].creator and not self.request.user.is_superuser:
            self.template_name = 'info.html'
            context['message'] = 'Ошибка 403: доступ запрещен'
            return context

        context['header'] = context['title'] = f"удаление товара {self.object.name}"

        return context
