from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.contrib.auth.models import User
from postman.models import Message, STATUS_ACCEPTED
from shop.models.cart import Cart
from shop.models.order import Order, OrderProduct


class CheckoutView(TemplateView):
    model = Cart
    template_name = "shop/checkout_view.html"

    # form_class = CheckoutForm

    def get_object(self, *args, **kwargs):
        cart_id = self.request.session.get("cart_id")
        # print(cart_id)
        if not cart_id:
            return redirect("cart")
        cart = Cart.objects.get(id=cart_id)
        # print(cart.subtotal)
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)

        # context["form"] = self.get_form()
        # user_check_id = request.session.get("user_checkout_id")
        # context['']
        user_checkout = None
        if self.request.user.is_authenticated():
            # user_checkout, created = UserCheckout.objects.get_or_create(user=self.request.user)
            # user_checkout.user = self.request.user
            # user_checkout.save()
            # self.request.session['user_checkout_id'] = user_checkout.id
            context["cart"] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        # print(self.object)
        # form = self.get_form()
        # if form.is_valid():
        # email = form.cleaned_data.get('email')
        cart = self.get_object()
        order = Order(user=cart.user)
        op = list()
        user = self.request.user
        order.order_total = cart.subtotal
        order.save()

        body = 'Новый заказ от %s #%s.\r\n\r\nИнформация о заказе:\r\n' % (order.id, order.added)

        for idx, item in enumerate(cart.cartitem_set.all()):
            product = item.item
            price = product.get_price(user)
            qty = item.quantity
            body += '%s. %s, %s шт. x %s руб.., на общую сумму: %s руб.\r\n' % (idx+1, product, qty, price, qty*price)
            op = OrderProduct(order=order, item=product, qty=qty, price=price)
            # print(op)
            op.save()

        body += '\r\nИтого: %s руб.' % (order.order_total)

        subject = 'Сформирован новый заказ от %s № %s!' % (order.added, order.id)
        # body = 'Новый заказ'
        sender = User.objects.filter(username='admin').first()
        recipient = self.request.user
        status = STATUS_ACCEPTED
        message_user = Message(subject=subject, body=body, sender=sender, recipient=recipient, moderation_status=status)
        message_user.save()
        message_admin = Message(subject=subject, body=body, sender=recipient, recipient=sender, moderation_status=status)
        message_admin.save()

        send_mail(
            'Новый заказ',
            'Сформирован новый заказ',
            'no-reply@avtoresurs.net',
            ['o.artemov@gov39.ru'],
            fail_silently=False,
        )

        return HttpResponseRedirect('/checkout/')
        # order.save()

        # try:
        #     cart = self.get_object()
        #     order = Order(user=cart.user)
        #     op = list()
        #     user = self.request.user
        #     order.order_total = cart.subtotal
        #     order.save()
        #     for item in cart.cartitem_set.all():
        #         product = item.item
        #         product_price = get_price(product, user)
        #         qty = item.quantity
        #         order_product = OrderProduct(order=order, product=product, product_quantity=qty,
        #                                      product_price=product_price)
        #         op.append(order_product)
        # order.save()

        # user_checkout, created = UserCheckout.objects.get_or_create(user=self.request.user)
        # request.session['user_checkout_id'] = user_checkout.id
        # print(user_checkout)
        # print(created)
        # print(user_checkout)
        # return self.form_valid(form)
        # return HttpResponseRedirect('/checkout/')
        # except:
        #     pass

        # print(e)
        # return HttpResponse('not ok')
        # return self.form_invalid(form)


def get_success_url(self):
    return reverse("checkout")


def get(self, request, *args, **kwargs):
    get_data = super(CheckoutView, self).get(request, *args, **kwargs)
    # cart = self.get_object()
    # user_checkout_id = request.session.get("user_checkout_id")
    # if user_checkout_id:
    #     user_checkout = UserCheckout.objects.get(id=user_checkout_id)
    #     # billing_address_id = ?
    #     # shipping_address_id = ?
    #     try:
    #         new_order_id = request.session["order_id"]
    #         new_order = Order.objects.get(id=new_order_id)
    #     except:
    #         new_order = Order()
    #         request.session['order_id'] = new_order.id
    #     # new_order.cart = cart
    #     # new_order.user = user_checkout
    #     # new_order.save()
    return get_data
