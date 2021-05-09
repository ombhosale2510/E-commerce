from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .models import Item, OrderItem, Order
from .forms import CheckoutForm

# Create your views here.


# def item_list(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "home.html", context)


class ChecoutView(View):
    def get(self, *args, **kwargs):
        # form
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            print("Form is valid")
            return redirect('core:checkout')


# def product(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "product.html", context)


class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order!")
            return redirect("/")


# def home(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "home.html", context)


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # Check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            # if yes, then it exists in cart hence add 1
            order_item.quantity += 1
            order_item.save()
            messages.info(
                request, "Item quantity has been successfully updated to your cart!")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(
                request, "Item has been successfully added to your cart!")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(
            request, "Item has been successfully added to your cart!")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # Check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            # order.delete()
            messages.info(
                request, "Item has been successfully removed from your cart!")
            return redirect("core:order-summary")
        else:
            messages.info(request, "Item was never in your cart")
            return redirect("core:order-summary")
    else:
        # Add a message saying the user doesn't have an order
        messages.info(
            request, "Item is not in your cart | You do not have an active order")
        return redirect("core:order-summary")


def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # Check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(
                request, "Item has been removed from your cart!")
            return redirect("core:order-summary")
        else:
            messages.info(request, "Item was never in your cart")
            return redirect("core:product", slug=slug)
    else:
        # Add a message saying the user doesn't have an order
        messages.info(request, "You do not have an active order!")
        return redirect("core:product", slug=slug)
