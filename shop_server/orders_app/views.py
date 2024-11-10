from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from .models import Orders, Items
from .forms import OrderForm, OrderItemFormSet


def home_page(request):
    context = {
        "orders_count": Orders.objects.count(),
        "items_count": Items.objects.count(),
    }
    return render(request, "home.html", context)


# Orders Views
class OrderListView(ListView):
    model = Orders
    template_name = "orders/order_list.html"
    context_object_name = "orders"
    paginate_by = 10


class OrderDetailView(DetailView):
    model = Orders
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context["order_items"] = order.order_items.all()
        return context


class OrderCreateView(CreateView):
    model = Orders
    form_class = OrderForm
    template_name = "orders/order_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = OrderItemFormSet(self.request.POST)
        else:
            context["formset"] = OrderItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect("order-list")
        else:
            return self.form_invalid(form)


class OrderUpdateView(UpdateView):
    model = Orders
    form_class = OrderForm
    template_name = "orders/order_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = OrderItemFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["formset"] = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect("order-list")
        else:
            return self.form_invalid(form)


class OrderDeleteView(DeleteView):
    model = Orders
    template_name = "orders/order_confirm_delete.html"
    success_url = reverse_lazy("order-list")


# Items Views
class ItemListView(ListView):
    model = Items
    template_name = "items/item_list.html"
    context_object_name = "items"
    paginate_by = 10


class ItemDetailView(DetailView):
    model = Items
    template_name = "items/item_detail.html"
    context_object_name = "item"


class ItemCreateView(CreateView):
    model = Items
    fields = ["item_name", "price"]
    template_name = "items/item_form.html"
    success_url = reverse_lazy("item-list")


class ItemUpdateView(UpdateView):
    model = Items
    fields = ["item_name", "price"]
    template_name = "items/item_form.html"
    success_url = reverse_lazy("item-list")


class ItemDeleteView(DeleteView):
    model = Items
    template_name = "items/item_confirm_delete.html"
    success_url = reverse_lazy("item-list")
