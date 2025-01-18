from django.urls import path
from django.conf.urls import handler404, handler500
from django.shortcuts import redirect
from . import views

urlpatterns = [
	#auth
	path('home', views.HomeListView.as_view(), name='statpoolshome'),
    path('view/<str:statpoolid>', views.ViewListView.as_view(), name='statpoolsview'),
    path('view/<str:statpoolid>?user=<str:statpooluserid>', views.ViewListView.as_view(), name='statpoolsview'),
    path('addstatpooluser', views.AddStatPoolUserFormView.as_view(), name='statpoolsadduser'),
    path('create', views.CreateFormView.as_view(), name='statpoolscreate'),
    path('create/addcategory', views.AddCategoryFormView.as_view(), name='statpoolsaddcategory'),
    path('create/addcategory/players/<str:gameid>', views.AddCategoryFormView.get_players, name='statpoolsaddcategoryplayers'),
	path('create/addcategory/stat/<str:pos>', views.AddCategoryFormView.get_stats, name='statpoolsaddcategorystats'),
    path('create/statpool', views.AddStatPoolFormView.as_view(), name='statpoolscreatestatpool'),
]