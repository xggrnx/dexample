from django.shortcuts import render
from django.views.generic import FormView

from market.forms import ContactForm
from django.views.generic import ListView, DetailView

from market.models import Product
from orders.models import Cart, OrderProduct


def create_cart_by_cookie(request):
    if request.session.is_empty():
        request.session.create()
    if not Cart.objects.filter(cookie=request.session.session_key):
        cart = Cart.objects.create(
            cookie=request.session.session_key
        )
    else:
        cart = Cart.objects.filter(cookie=request.session.session_key).first()
    if request.session.session_key:
        OrderProduct.objects.filter(
            cart=cart, active=False).delete()


class IndexView(ListView):
    model = Product
    template_name = 'path/index.html'
    context_object_name = 'products'
    queryset = Product.objects.all()

    def get(self, *args, **kwargs):
        data = super(IndexView, self).get(*args, **kwargs)
        user = self.request.user
        if not user.is_anonymous:
            cart = Cart.objects.filter(user=user).first()
            if cart:
                if self.request.session.is_empty():
                    self.request.session.create()
                cart.cookie = self.request.session.session_key
                cart.save()
                pass
                OrderProduct.objects.filter(cart=cart, active=False).delete()
            else:
                create_cart_by_cookie(self.request)
        else:
            create_cart_by_cookie(self.request)
        return data


class ProductListView(ListView):
    model = Product
    template_name = 'path/products.html'
    context_object_name = 'products'
    queryset = Product.objects.all()


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'path/product.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = ContactForm
        return context

class ContactView(FormView):
    template_name = 'path/contact-us.html'
    form_class = ContactForm
    success_url = '/index/'  #TODO redirect to page success

    def form_valid(self, form):
        print(form.data)
        return super(ContactView, self).form_valid(form)