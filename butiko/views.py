from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.utils import timezone
from .models import ItemList, Item, PermRequest
from .forms import ItemForm, ItemListForm, UserForm
import json
    
def home_page(request):
    if request.user.is_authenticated():
        user = request.user
        userItems = user.lists.order_by('created_date')
        #perm_requests = PermRequest.objects.filter(itemList__owner=user).values_list('itemList__title', 'user__username')
        perm_requests = PermRequest.objects.filter(itemList__owner=user)
        #userItems = ItemList.objects.filter(owner=request.user).order_by('created_date')
        return render(request, 'butiko/home_page.html', {'userItems': userItems, 'perm_requests': perm_requests})
    else:
        return render(request, 'butiko/home_page.html', {})

@login_required
def list_detail(request, pk):
    theList = get_object_or_404(ItemList, pk=pk)
    items   = theList.item_set.all()
    return render(request, 'butiko/list_detail.html', {'items': items, 'list': theList})

def change_item_count(request):
    if request.method == 'GET':
        item = get_object_or_404(Item, title__exact=request.GET['item']);
#        if request.GET['action'] == "add":
#            item.change_number(1);
#        elif request.GET['action'] == "sub":
#            item.change_number(-1);
        if 'num' in request.GET:
            item.change_number(int(request.GET['num']))

        return HttpResponse(item.number)

@login_required
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
@login_required
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

@login_required
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
        return redirect('list_detail', pk=itemList.pk)
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
            
            # Log user in and redirect to home page
            user = authenticate(username = form.cleaned_data['username'],
                                password = form.cleaned_data['password'])
            login(request, user)
            return redirect('home_page')
        else:
            return render(request, 'butiko/register_user.html', {'form': form, 'error': form.errors})
    else:
        form = UserForm()
        return render(request, 'butiko/register_user.html', {'form': form})

# Helper function which queries the database by name 'starts_with'
# and returns an array of matches of size 'max_results". user should
# be a User model.
def get_lists(user,max_results=0, starts_with=''):
    list_of_lists = []
    if starts_with:
#        list_of_lists = ItemList.objects.filter(title__istartswith=starts_with)
        list_of_lists = ItemList.objects.filter(title__istartswith=starts_with).exclude(users__username=user.username)
    else:
        list_of_lists = ItemList.objects.exclude(users__username=user.username)

    if max_results >0:
        if len(list_of_lists) > max_results:
            list_of_lists=list_of_lists[:max_results]

    return list_of_lists

# Ajax response that returns a list of lists, but filters according
# to whether the user already belongs or not
@login_required
def suggest_list(request):
    MAX_RESULTS = 8
    list_of_lists = []
    starts_with = ''
    if 'suggestion' in request.GET:
        starts_with = request.GET['suggestion']

    list_of_lists = get_lists(request.user, MAX_RESULTS, starts_with)

    # Get the titles of the lists that the user has already made requests upon
    cur_requests   = request.user.list_requests.values_list('itemList__title', flat=True)

    return render(request, 'butiko/request_permission.html', {'list_of_lists': list_of_lists, 'requests': cur_requests})

@login_required
def list_search(request):
    return render(request, 'butiko/list_search.html')

@login_required
def request_perm(request, listpk):
    itemList = get_object_or_404(ItemList, pk=listpk)
    list_request = PermRequest(itemList = itemList, user = request.user)
    list_request.save()

    return render(request, 'butiko/perm_request_success.html', {'list': itemList})

# AJAX request handler. Sends data whether the owner of a list permits an access
# request to his/her list.
# Request should have instances of 'action', 'list', 'user' (who makes the request)
@login_required
def grant_deny(request):
    try:
        action   = request.GET['action']
        listName = request.GET['list']
        ask_user = request.GET['user']
    except:
        raise Http404('One of the required variables does not exist')

    itemList = get_object_or_404(ItemList, title=listName)
    req_user = get_object_or_404(User, username=ask_user)

    try:
        theRequest = PermRequest.objects.filter(itemList=itemList, user=req_user);
    except:
        raise Http404('No such permission was requested.')
    
    if itemList.owner == request.user:
        # Check to see if the action is to grant or deny. In either case,
        # give the corresponding message then delete the permission
        if action == "grant":
            itemList.users.add(req_user)
            response_data = {'response': "<p>"+ req_user.username + " was <b>successfully</b> added to " + itemList.title+"</p>" }
            theRequest.delete()
        elif action == "deny": 
            response_data = {'response': "<p>" + req_user.username + " was <b>denied</b> access to " + itemList.title+"</p>" }
            theRequest.delete()
    else:
        raise HttpResponseForbidden()

    return HttpResponse(json.dumps(response_data))

# Create your views here.
