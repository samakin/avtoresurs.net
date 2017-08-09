from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from shop.models.cart import Cart, CartItem
from shop.models.product import Product



class ItemCountView(View):
    """ через json отдает счетчик количества итемов в корзине """

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")
            if not cart_id:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()
            request.session["item_count"] = count
            return JsonResponse({"count": count})
        else:
            raise Http404


class CartView(SingleObjectMixin, View):
    """ вьюха для корзины с json """
    model = Cart
    template_name = "shop/cart_view.html"

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(259200)
        # self.request.session["cart_id"] = None
        cart_id = self.request.session.get("cart_id")
        # print(cart_id)
        if not cart_id:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False)
        flash_message = ""
        item_added = False
        cart_item = None
        title = None
        if item_id:
            item_instance = get_object_or_404(Product, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                # pass
                raise Http404
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
            if created:
                flash_message = "Товар успешно добавлен в корзину"
                item_added = True
            if delete_item:
                flash_message = "Товар удален из корзины"
                cart_item.delete()
            else:
                if not created:
                    flash_message = "Количество товара в корзине изменено"
                cart_item.quantity = qty
                cart_item.save()
            if not request.is_ajax:
                return HttpResponseRedirect(reverse('cart'))
                # return cart_item.cart.get_absolute_url()
        if request.is_ajax():
            # print(request.GET.get('item'))
            try:
                total = cart_item.line_item_total
            except:
                total = None
            try:
                subtotal = cart_item.cart.subtotal
            except:
                subtotal = None
            try:
                total_items = cart_item.cart.items.count()
            except:
                total_items = 0
            data = {
                "deleted": delete_item,
                "item_added": item_added,
                "line_total": total,
                "subtotal": subtotal,
                "flash_message": flash_message,
                "total_items": total_items,
            }
            return JsonResponse(data)

        context = {
            "object": self.get_object(),
        }
        template = self.template_name

        user = self.request.user

        # print(cart.cartitem_set.all())
        cart_items = cart.cartitem_set.all()
        for item in cart_items:
            price = item.item.get_price(user)
            item.item.price = price

        if cart_items:
            context.update({
                "cart_items": cart_items
            })
        return render(request, template, context)


