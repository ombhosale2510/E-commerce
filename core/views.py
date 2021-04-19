from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Item, OrderItem, Order

# Create your views here.


# def item_list(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "home.html", context)


def checkout(request):
    return render(request, "checkout.html")


# def product(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "product.html", context)


class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = "home.html"


# def home(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "home.html", context)


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


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
        else:
            order.items.add(order_item)
            messages.info(
                request, "Item has been successfully added to your cart!")
            return redirect("core:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(
            request, "Item has been successfully added to your cart!")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


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
            messages.info(
                request, "Item has been successfully removed from your cart!")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "Item was never in your cart")
            return redirect("core:product", slug=slug)
    else:
        # Add a message saying the user doesn't have an order
        messages.info(request, "You do not have an active order!")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)
