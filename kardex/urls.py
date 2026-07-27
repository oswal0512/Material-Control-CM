from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.kardex_list,
        name="kardex_list"
    ),

]