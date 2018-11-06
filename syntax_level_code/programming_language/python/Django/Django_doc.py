#install django
$sudo apt-get install python-django
$django-admin --version

#Create a project
vulcantech@vulcantech-MS-7529:~$ django-admin startproject django_p #last one is project name
vulcantech@vulcantech-MS-7529:~$ cd django_p
vulcantech@vulcantech-MS-7529:~/django_p$ python manage.py migrate
Output:-
	Operations to perform:
	  Apply all migrations: admin, contenttypes, auth, sessions
	Running migrations:
	  Applying contenttypes.0001_initial... OK
	  Applying auth.0001_initial... OK
	  Applying admin.0001_initial... OK
	  Applying sessions.0001_initial... OK
	vulcantech@vulcantech-MS-7529:~/django_p$ python manage.py createsuperuser
	Username (leave blank to use 'vulcantech'): kendavar
	Email address: www.kendacool@gmail.com
	Password: 
	Password (again): 
	Superuser created successfully.

#Run the server
vulcantech@vulcantech-MS-7529:~/django_p$ python manage.py runserver 0.0.0.0:8000
Output:-
	Performing system checks...

	System check identified no issues (0 silenced).
	October 19, 2015 - 15:06:11
	Django version 1.7.6, using settings 'django_p.settings'
	Starting development server at http://0.0.0.0:8000/
	Quit the server with CONTROL-C.
	[19/Oct/2015 15:08:01] "GET / HTTP/1.1" 200 1759
	[19/Oct/2015 15:08:01] "GET /favicon.ico HTTP/1.1" 404 1929
	[19/Oct/2015 15:08:01] "GET /favicon.ico HTTP/1.1" 404 1929
	(In The browser enter link "127.0.0.1:8000" a message of it woks comes.!!!)
	(server_ip_address:8000/admin to get the admin page)


#create a various section of the website.
kendavar@uecb1d74a93b158e48e11:~/kendavar/Django/website$ python manage.py startapp music

#to include the urls from app section
#create urls.py in music or app
#include main url.py
    url(r'^music/',include('music.urls'))

#import the url module and views,  
#r'^$'- Any thing starts with http://127.0.0.1:8000/music/ give views.index function
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,name='index'),
]


#Take the request and send a response
#view.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1> This the music app home page<h1/>")

#Each function in models are a table.
#Each table has a primary key by default
#foreign key connects the upper table funtion
#on delete for contriction
from django.db import models

from django.db import models

class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.CharField(max_length=1000)

class Song(models.Model):
    album = models.ForeignKey(Album,on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)

#define it in the main settings
INSTALLED_APPS = [
    'music.apps.MusicConfig',<---------
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

#we connect the database using the below command with the model we developed.
kendavar@uecb1d74a93b158e48e11:~/kendavar/Django/website$ python manage.py makemigrations music
output:-
	Migrations for 'music':
	  music/migrations/0001_initial.py:
	    - Create model Album
	    - Create model Song

#The database scheme created by the model
kendavar@uecb1d74a93b158e48e11:~/kendavar/Django/website$ python manage.py  sqlmigrate music 0001
BEGIN;
--
-- Create model Album
--
CREATE TABLE "music_album" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "artist" varchar(250) NOT NULL, "album_title" varchar(500) NOT NULL, "genre" varchar(100) NOT NULL, "album_logo" varchar(1000) NOT NULL);
--
-- Create model Song
--
CREATE TABLE "music_song" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "file_type" varchar(10) NOT NULL, "song_title" varchar(250) NOT NULL, "album_id" integer NOT NULL REFERENCES "music_album" ("id"));
CREATE INDEX "music_song_95c3b9df" ON "music_song" ("album_id");
COMMIT;

#save the changes
kendavar@uecb1d74a93b158e48e11:~/kendavar/Django/website$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, music, sessions
Running migrations:
  Rendering model states... DONE
  Applying music.0001_initial... OK

#operation on the python manage.py shell.insert/update db.
$python manage.py shell
from music.models import Album, Song

Album.objects.all()
a = Album(artist="Taylor Swift", album_title="Red",genre="country",album_logo="asdfsdsfa")
a.save()
a.artist
a.id
a.pk #a.id or a.pk -primary key
#second way to input values to db
b=Album()
b.artist= "Myth"
b.album_title="High school"
b.album_logo="/home/local/ANT/kendavar/kendavar/"
b.save()
Album.objects.all()

#dunter/string representaion of the object.It gives a name to the object
class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.CharField(max_length=1000)

    def __str__(self):                                     #This will give the name to the object when we call Album.objects.all()
        return self.album_title + "_" + self.artist

#filter with id
Album.objects.filter(id=2)

#The row starts with 'Taylor'
Album.objects.filter(artist__startswith='Taylor')


#admin user access
kendavar@uecb1d74a93b158e48e11:~/kendavar/Django/website$ python manage.py createsuperuser
Username (leave blank to use 'kendavar'): admin
Email address: kendacool@gmail.com
Password: 12345678
Password (again): 

#setting the database on the admin site
#go to admin.py in music folder
from django.contrib import admin
from .models import Album

admin.site.register(Album)


#group the number like /music/712/ into a variable 
#music/urls.py
    #/music/71/
    url(r'^(?P<album_id>[0-9]+)$'),

#use the ID at view.py
def detail(request,album_id):
    return HttpResponse("<h2>Details for album ID:" + str(album_id) + "</h2>")

#http://127.0.0.1:8000/music/1/
ouput;-Details for album ID:1

#create a template folder in the app folder
#music/template/music/index.html

#How to connect the templete and pass the values.
#view.py
from django.http import HttpResponse
from django.template import loader       <----#load the module
from .models import Album


def index(request):
    all_albums =Album.objects.all()                      <-----#fetch the objects form db
    template = loader.get_template('music/index.html')   <-----#connect to the template
    context={                                            <-----#pass the objects as context dicts to the response
        'all_albums':all_albums,
    }
    return HttpResponse(template.render(context,request))    <--------------#pass the response


#Must config in setting.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['music/template'],                                  <--------------------#The folder for the template to be fetched
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#In the html file
#index.html
<ul>
    {% for album in all_albums %}                                          <-------------#python code is written in {% %},variable in {{ <value> }}
    <li><a href="/music/{{ album.id }}/">{{ album.album_title }}</a></li>        
    {% endfor %}
</ul>

#Http response is inbuilt in the following function
return render(request,'music/index.html',context)

#if page is not present
from django.http import Http404

def detail(request,album_id):
    try:
        ablum=Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        raise Http404("Album does not exits")
    return render(request, 'music/detail.html', {'ablum':ablum})

#put songs
album1=Album.objects.filter(pk=1).get()
album1.artist
song = Song()
from music.models import Album, Song
song = Song()
song.album=album1
song.file_type=="mp4"
song.file_type=="mp3"
song.song_title="I hate u"
song.save()

#This will create the new object
album1.song_set.create(song_title='I love bacon',file_type='mp3')
#count
album1.song_set.count()
#all the objects
album1.song_set.all()

#Hardcoding urls
#/music/urls.py
url(r'^(?P<album_id>[0-9]+)/$',views.detail,name='detail') #The name is the variable which stores the regex
#/music/index.html
<li><a href="{% url 'detail' album.id %}">{{ album.album_title }}</a></li>#start with {% and url to identify its a url,then variable which stored regex and next value

#Best way to implement 404 error
from django.shortcuts import render,get_object_or_404

def detail(request, album_id):
    album = get_object_or_404(Album,pk=album_id)
    return render(request, 'music/detail.html', {'album': album})

#To specify which detail I am using in index
#music/urls.py
app_name = 'music'

#index.html
<li><a href="{% url 'music:detail' album.id %}">{{ album.album_title }}</a></li>


#Create a env
conda create --name <env name> django
ex:-conda create --name myDjangoEnv django

#To know what all env are present in system
Conda info --envs

# To activate this environment, use:
# > source activate myDjangoEnv

# To deactivate an active environment, use:
# > source deactivate

#To create a django project
#type $django-admin startproject <project name>

#To create a django app
#python manage.py startapp <app name>

#Steps to create a django project
1)django-admin startproject <project name>
2) cd <project name>, python manage.py startapp <app name> or django-admin startapp <app name>
3) go to setting file in project folder and in INSTALLED_APPS list add the app name.
4) Then in view folder create view
5)connect the view in urls of project folder.

#create template folder in main project folder
<project folder>/templates/<app folder>/

#add the below to add settings,so template folder is connected to the main project.
TEMPLATE_DIR = os.path.join(BASE_DIR,"templates")

#Inside template dict in the setting. We had the path to dict
'DIRS': [TEMPLATE_DIR],

#project -> urls.py
from django.conf.urls import url,include


#And in pattern add  $To add the urls from the apps.
url(r'^AppTwo/',include('AppTwo.urls'))

#create urls.py file in the app folder.
from django.conf.urls import url
from first_app import views

urlpatterns = [
    url(r'^$',views.index,name='index')
]




#Dealing with images
#create static file in project folder -> /static/images/
#In setting.py 
    ->     STATIC_DIR = os.path.join(BASE_DIR,"static")
    ->     STATIC_URL = '/static/'
    ->     STATICFILES_DIRS = [ STATIC_DIR,]

#Images saved by the users
#create static file in project folder -> /static/media/
#In setting.py 
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'

#In html
    #we add load staticfiles after doctype html
    {% load staticfiles %}
    #we can link css and images as follows
    ->img tag, attribute src="{% static "images/django_im.jpeg" %}"
    -> link tag, attribute href="{% static "css/mystyle.css" %}"

#Models
           #Make user in INSTALLED_APPS app is added with comma
            -INSTALLED_APPS['first_app',]
           
           #In the models.py file add tables.
class Webpage(models.Model):   //Webpage is table name
    topic = models.ForeignKey(Topic)  //topic is foreign key
    name = models.CharField(max_length = 264, unique = True)
    url = models.URLField(unique=True)

    def __str__(self):
               return self.name
#After creating a model. We run migrate to mage changes
->In project folder>python manage.py migrate
->In project folder>python manage.py makemigrations <app name>
->In project folder>python manage.py migrate

#Register the models in admin page
from first_app.models import AccessRecord,Topic,Webpage
admin.site.register(AccessRecord)


#Create super user
python manage.py createsuperuser
Kendavar
kendavar@amazon.com
Lufy3kenda

#link url with anchor tag
#First make user urls.py has a pattern, then view is created, then add <a href="/AppTwo/user/">
https://stackoverflow.com/questions/35272890/how-to-link-html-files-together-using-django-1-9

#Forms
+Create a forms.py in app folder
+Add
From django import forms
+Create a class with form name and pass argument forms.Form. 
+Create form objects.
 Ex:-
class FormName(forms.Form):
name = forms.CharField()
email = forms.EmailField()
text = forms.CharField(widget=forms.Textarea) // widgets can be added to the fields.




+create views for form
def form_name_view(request):
    form = forms.FormName()  //create a form object
    if request.method == 'POST':    //if the form method is post
            form = forms.FormName(request.POST)

            if form.is_valid(): //check if the form fields are valid
                    print("validation success!")
                    print("NAME: "+form.cleaned_data['name']) //get the data and print
                    print("EMAIL: "+form.cleaned_data['email'])
                    print("TEXT: "+form.cleaned_data['text'])
    return render(request,'basicapp/form_page.html',{'form':form}) 
+add urls.py
url(r'^formpage/',views.form_name_view, name='form_name')

+add in html
<div class="container">
      <h1>Fill out the Form!</h1>
        <form method="post">
            {{ form.as_p }} //align the inputs in paragraph form
            {% csrf_token %}  //security certificate
            <input type="submit" class="btn btn-primary" name="" value="Submit">
        </form>
    </div>

#form validation
from django.core import validators
Bot catcher
botcatcher = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])


#How to recreate the db
python manage.py flush




#create a template tagging
#Template tagging in urls.py of app
app_name = 'basic_app' #this is to tell the template which app its from

urlpatterns = [
    url(r’relative/$',views.relative,name="relative"),
    url(r'other/$',views.other,name="other"),
]
#html 
<a href="{% url 'basic_app:other' %}">GO to other page</a>



#filter
pip install django-filter
INSTALLED_APPS - > 'django_filters',

#template inheritance

#Django filters
{{ text|upper }}
{{ number|add:”99” }}

#Create a custom filter
In the app dir create a folder > templatetags
Then create a >__init__.py file
Then create a file where you create a customised filters.
File contents like :
from django import template

register = template.Library()

@register.filter("cut",cut) #decorator to add new function to a already existing one
def cut(value,arg):
    return value.replace(arg,"")




#Decorator
Decorators provide a simple syntax for calling higher-order functions. By definition, a decorator is a function that takes another function and extends the behavior of the latter function without explicitly modifying it.

#security
Pip install bcrypt
Pip install django[argon2]

#At setting.py
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

 
#Add in images from form
<form  method="post" enctype="multipart/form-data">

#Class based views

Urls.py
url(r'^$',views.CBView.as_view())






Views
from django.shortcuts import render
from django.views.generic import View,TemplateView
from django.http import HttpResponse

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self,**kwargs):
            context = super().get_context_data(**kwargs)
            context['injectme'] = 'BASIC INJECTION!'
            return context

Template view allows to easy inject the view and values




          
Views:
from django.views.generic import View,TemplateView,ListView,DetailView

class SchoolListView(ListView):
    model =models.School
#returns context model lower case list ex:-school_list

class SchoolDetailView(DetailView):
    model models.School
    template_name = 'basic_app/school_detail.html'
#returns context model lower case list ex:-school_detail

#set time zone to india
TIME_ZONE =  'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False









