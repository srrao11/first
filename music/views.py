#generic views default name is modelname_form
from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth import authenticate,login
from django.core.urlresolvers import reverse_lazy
from .models import Album,Song
from .forms import UserForm
class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_album'
    ''' returns in object_list '''
    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'

class AlbumCreate(CreateView):
    model=Album
    fields = ['artist','album_title','genre','album_logo']

class AlbumUpdate(UpdateView):
    model=Album
    fields = ['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
    model=Album
    success_url = reverse_lazy('music:index')

class UserFormView(View):
    form_class=UserForm
    template_name='music/registration_form.html'

    # display blank form
    def get(self,request):
        form=self.form_class
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user=form.save(commit=False) #locally saves the user

            #clean the data
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']

            user.set_password(password)
            user.save() #saves the user to the database

            #return user object if credentials are correct
            user=authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                return redirect('music:index')
            return render(request, self.template_name, {'form': form})

#Before using generic views

'''from django.http import HttpResponse
from django.http import Http404
from .models import Album,Song
from django.shortcuts import render,get_object_or_404
#from django.template import loader
def index(request):
    all_album=Album.objects.all()
    #template=loader.get_template('music/index.html/')
    context={
        'all_album':all_album,
    }
    return render(request,'music/index.html',context)
    #return HttpResponse(template.render(context,request))
def detail(request,album_id):

    try:
        album=Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        raise Http404("Album does not exist.")
        ///
    album = get_object_or_404(Album,pk=album_id)

    return render(request,'music/detail.html',{'album':album,})

    #return HttpResponse("<h1> The album id is :"+str(album_id)+"</h1>")

    def favourite(request,album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song=album.song_set.get(pk=request.POST['song'])
    except(KeyError,Song.DoesNotExist):
        return render(request,'music/detail.html',{'album':album,'error_message':"You did not select any song",})
    else:
        selected_song.is_favourite=True
        selected_song.save()
    return render(request, 'music/detail.html', {'album': album, })///
    '''