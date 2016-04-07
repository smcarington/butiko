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

def change_item_count(request):
    if request.method == 'GET':
        item = get_object_or_404(Item, title__exact=request.GET['item']);
        if request.GET['action'] == "add":
            item.change_number(1);
        elif request.GET['action'] == "sub":
            item.change_number(-1);
        return HttpResponse(returnNumber)



# Create your views here.
