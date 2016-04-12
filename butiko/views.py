from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from .models import ItemList, Item, PermRequest
from .forms import ItemForm, ItemListForm, UserForm
    
def home_page(request):
    if request.user.is_authenticated():
        user = request.user
        userItems = user.lists.order_by('created_date')
        #userItems = ItemList.objects.filter(owner=request.user).order_by('created_date')
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


# Deletes either an item or a list, as given by the string object_type
# Checks to see if the user is allowed access
def delete_item(request, objectStr, pk):

    # Depending on which item is set, we return different pages
    if objectStr == "item":
        theObj      = get_object_or_404(Item, pk = pk)
        theList     = theObj.itemList
        return_View = redirect('list_detail', pk=theList.pk)
    elif objectStr == "list":
        theList     = get_object_or_404(ItemList, pk = pk)
        theObj      = theList
        return_View = redirect('home_page')
    else:
        return HttpResponse('<h1>Invalid Object Type</h1>')

    # Check to see if the user is allowed to edit the list
    if request.user.lists.filter(title=theList.title).exists():
        if request.method == "POST":
            theObj.delete()
            return return_View
        else:
            return render(request, 'butiko/delete_item.html', {'object': theObj, 'type' : objectStr})
    else:
        return render(request, 'butiko/access_denied.html', {'object': theObj})

def add_new_list(request):
    if request.method == "POST":
        form = ItemListForm(request.POST)
        if form.is_valid():
            itemList = form.save(commit=False)
            itemList.owner        = request.user
            itemList.created_date = timezone.now()
            itemList.modified     = timezone.now()
            itemList.save()
            itemList.users.add(request.user)
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
# Create your views here.
