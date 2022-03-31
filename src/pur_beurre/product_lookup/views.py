from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from .models import Products, Favorites


class ProductLookupView(TemplateView):

    template_name = 'product_lookup/product_lookup.html'

    def post(self, request, *args, **kwargs):
        """
        This method is called when the user submits the form.
        """
        product_name = request.POST['product_name']
        return HttpResponseRedirect(reverse(
            'product_lookup:product_lookup_results',
            args=[product_name])
            )


class ProductLookupResultsView(TemplateView):

    template_name = 'product_lookup/product_lookup_results.html'

    def get_context_data(self, **kwargs) -> dict:

        context = super().get_context_data(**kwargs)
        product_name = kwargs['product_name']

        # Get the first item that matches the query to look for
        # alternatives in databases
        searched_product = Products.objects.filter(
            product_name__icontains=product_name).first()
        context['searched_product'] = searched_product

        # Get the alternatives to the found product

        if searched_product:
            alternatives = Products.objects.filter(
                product_nutriscore__lte=searched_product.product_nutriscore,
                product_category=searched_product.product_category
                ).exclude(
                product_name=searched_product.product_name
                ).order_by('product_nutriscore')
            context['alternatives'] = alternatives
        else:
            context['alternatives'] = None

        # Get the list of products ids that the user has already
        # added to his favorites
        if self.request.user.is_authenticated:
            user_favorites = self.request.user.favorites_set.all()
            fav_id_list = [favorite.product.id for favorite in user_favorites]
            context['favorites_id_list'] = fav_id_list
        else:
            context['favorites_id_list'] = None

        return context


def favorite_click(request, *args, **kwargs):
    """
    This method is called when the user clicks on the favorite button.
    """
    product_id = request.POST.dict()['product_id']
    product = Products.objects.get(pk=product_id)
    user = request.user

    is_favorite = Favorites.objects.filter(
        user=user, product=product).exists()
    if is_favorite:
        # Remove the favorite
        Favorites.objects.filter(
            user=user, product=product).delete()
    else:
        # Add the favorite
        Favorites.objects.create(user=user, product=product)

    return HttpResponse(status=200)


class FavoritesView(LoginRequiredMixin, TemplateView):

    template_name = 'product_lookup/favorites.html'

    def get_context_data(self, **kwargs) -> dict:

        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get the list of products ids that the user has already
        # added to his favorites
        user_favorites = Favorites.objects.filter(user=user)
        context['favorites'] = user_favorites

        context['favorites_id_list'] = \
            [product.product.id for product in user_favorites]

        return context


class ProductDetails(DetailView):
    model = Products
    template_name = 'product_lookup/product_details.html'
