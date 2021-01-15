from django.shortcuts import render
from .models import Cat, CatToy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

######## USER ########
@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', { 'username': username, 'cats': cats })

def login_view(request):
  # if post, then authenticate (the user will be submitting a username and password)
  if request.method == 'POST':
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
      u = form.cleaned_data['username']
      p = form.cleaned_data.get('password')
      user = authenticate(username=u, password=p)
      if user is not None:
        if user.is_active:
          login(request, user)
          return HttpResponseRedirect('/user/' + u)
        else:
          print(f"The account for {u} has been disabled.")
      else:
        print('The username and/or password is incorrect.')
    else:
      form = AuthenticationForm()
      return render(request, 'login.html', {'form': form})
  else: # get request that sent up empty form
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/cats')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/cats')
        else: 
            form = UserCreationForm()
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

######## CATS ########
def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})

def cats_show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'cats/show.html', { 'cat': cat })

@method_decorator(login_required, name="dispatch")
class CatCreate(CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age', 'cattoys']
    success_url = '/cats'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/cats/' + str(self.object.pk))

@method_decorator(login_required, name="dispatch")
class CatUpdate(UpdateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age', 'cattoys']
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/cats')

@method_decorator(login_required, name="dispatch")
class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats'

######## CatToy ########
def cattoys_index(request):
    cattoys = CatToy.objects.all()
    return render(request, 'cattoys/index.html', { 'cattoys': cattoys })

def cattoys_show(request, cattoy_id):
    cattoy = CatToy.objects.get(id=cattoy_id)
    return render(request, 'cattoys/show.html', { 'cattoy': cattoy })

@method_decorator(login_required, name="dispatch")
class CatToyCreate(CreateView):
    model = CatToy
    fields = '__all__'
    success_url = '/cattoys'

@method_decorator(login_required, name="dispatch")
class CatToyUpdate(UpdateView):
    model = CatToy
    fields = ['name', 'color']
    success_url = '/cattoys'

@method_decorator(login_required, name="dispatch")
class CatToyDelete(DeleteView):
    model = CatToy
    success_url = '/cattoys'
