from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class InventoryView(LoginRequiredMixin, ListView):
    template_name = "inventory.html"
    context_object_name = "items"
    
    def get_queryset(self):
        user = self.request.user
        items = user.inventory.items.all()
        return items
    
        