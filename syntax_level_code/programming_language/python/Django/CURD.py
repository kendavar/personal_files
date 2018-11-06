#To create a new view of the model
#In views.py add 
from django.views.generic import (View,TemplateView,
                                  ListView,DetailView,
                                  CreateView,UpdateView,
                                  DeleteView)

#create a view
#example:-
class SchoolCreateView(CreateView):
    fields = ('name','principal','location')
    model=models.School


#in models.py
#create a function redirect the url
#when new data is added
from django.urls import reverse

#added within the model which is created
def get_absolute_url(self):
        return reverse("basic_app:detail",kwargs={"pk":self.pk})

#Added to Urls
url(r'^create/$',views.SchoolCreateView.as_view(),name='create')
**************************************************************************************