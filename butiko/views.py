from django.shortcuts import render, get_object_or_404
from .models import ItemList, Item, PermRequest
    
def home_page(request):
    if request.user.is_authenticated():
        userItems = ItemList.objects.filter(owner=request.user).order_by('created_date')
        return render(request, 'butiko/home_page.html', {'userItems': userItems})
    else:
        return render(request, 'butiko/home_page.html', {})

def list_detail(request, pk):
    theList = get_object_or_404(ItemList, pk=pk)
    items   = theList.item_set.all()
    return render(request, 'butiko/list_detail.html', {'items': items})

# Create your views here.
