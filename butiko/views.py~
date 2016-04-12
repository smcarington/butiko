from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from .models import ItemList, Item, PermRequest
from .forms import ItemForm, ItemListForm, UserForm
    
def home_page(request):
    if request.user.is_authenticated():
        userItems = ItemList.objects.filter(owner=request.user).order_by('created_date')
        return render(request, 'butiko/home_page.html', {'userItems': userItems})
    else:
        return render(request, 'butiko/home_page.html', {})

def list_detail(request, pk):
    theList = get_object_or_404(ItemList, pk=pk)
    items   = theList.item_set.all()
    return render(request, 'butiko/list_detail.html', {'items': items, 'list': theList})

def change_item_count(request):
    if request.method == 'GET':
        item = get_object_or_404(Item, title__exact=request.GET['item']);
        if request.GET['action'] == "add":
            item.change_number(1);
        elif request.GET['action'] == "sub":
            item.change_number(-1);
        return HttpResponse(item.number)

def add_new_item(request, listpk):
    # listpk is the primary key of the list to which the item is
    # to be added.
    itemList = get_object_or_404(ItemList,pk=listpk)
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.itemList = itemList
            item.update   = timezone.now()
            item.save()
            # Update the modified property on list
            itemList.modified = timezone.now()
            itemList.save()
        return redirect('list_detail', pk=listpk)
    else:
        form = ItemForm()
        return render(request, 'butiko/add_new_item.html', {'form': form, 'list': itemList})


def delete_item(request, pk):
    item    = get_object_or_404(Item, pk = pk)
    theList = item.itemList
    if request.method == "POST":
        item.delete()
        return redirect('list_detail', pk=theList.pk)
    else:
        return render(request, 'butiko/delete_item.html', {'item': item})

def add_new_list(request):
    if request.method == "POST":
        form = ItemListForm(request.POST)
        if form.is_valid():
            itemList = form.save(commit=False)
            itemList.owner        = request.user
            itemList.created_date = timezone.now()
            itemList.modified     = timezone.now()
            itemList.save()
        return redirect('home_page')
    else:
        form = ItemListForm()
        return render(request, 'butiko/add_new_item.html', {'form': form})

def register_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return redirect('home_page')
        else:
            return render(request, 'butiko/register_user.html', {'form': form, 'error': form.errors})
    else:
        form = UserForm()
        return render(request, 'butiko/register_user.html', {'form': form})

# Helper function which queries the database by name 'starts_with'
# and returns an array of matches of size 'max_results"
def get_lists(max_results=0, starts_with=''):
    list_of_lists = []
    if starts_with:
        list_of_lists = ItemList.objects.filter(title__istartswith=starts_with)
    else:
        list_of_lists = ItemList.objects.all()

    if max_results >0:
        if len(list_of_lists) > max_results:
            list_of_lists=list_of_lists[:max_results]

    return list_of_lists


def suggest_list(request):
    MAX_RESULTS = 8
    list_of_lists = []
    starts_with = ''
    if request.method == "GET":
        starts_with = request.GET['suggestion']

    list_of_lists = get_lists(MAX_RESULTS, starts_with)

    # Pass the current list of requests for that user
    cur_requests = request.user.list_requests.all()

    return render(request, 'butiko/request_permission.html', {'list_of_lists': list_of_lists, 'requests': cur_requests})

def list_search(request):
    return render(request, 'butiko/list_search.html')

# Create your views here.
