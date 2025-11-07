from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from utils.decorators import clear_session_data

@method_decorator(clear_session_data(["discount_name", "discount_price"]), name="dispatch")
class InventoryView(LoginRequiredMixin, ListView):
    template_name = "inventory.html"
    context_object_name = "items"
    
    def get_queryset(self):
        user = self.request.user
        items = user.inventory.items.all()
        return items
    
        