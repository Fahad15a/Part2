from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import models
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

def index (request):
    return render(request , "Part2/Part2.html")

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class ItemListView(ListView):
    queryset = Item.objects.all()
    template_name = 'Part2/items.html'


class ItemDetailView(DetailView):
    queryset = Item.objects.all()
    template_name = 'item_detail.html'


class ItemCreateView(CreateView):
    model = Item
    fields = ['name', 'description']
    template_name = 'item_create.html'


class ItemUpdateView(UpdateView):
    model = Item
    fields = ['name', 'description']
    template_name = 'item_update.html'


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'item_delete.html'





def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('items')
        else:
            return render(request, 'Part2/login.html', {'error_message': 'Invalid username or password.'})
    else:
        return render(request, 'Part2/login.html')


def logout(request):
    logout(request)
    return redirect('items')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                login(request, user)
                return redirect('items')
            except IntegrityError:
                return render(request, 'Part2/register.html', {'error_message': 'The username or email is already taken.'})
        else:
            return render(request, 'Part2/register.html', {'error_message': 'The passwords do not match.'})
    else:
        return render(request, 'Part2/register.html')