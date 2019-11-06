from django.urls import include,path
from orders import views
from orders.views import *
from django.conf.urls import url
urlpatterns=[
  path('pbi/',
      views.AllPbis.as_view(),
      name='AllPbis'),
  path('pbi/createPbi',
      views.addPbi,
      name='Cre-Pbi'),
  path('pbi/<target>/',
      views.OnePbi.as_view(),
      name='User-Pbi'),
  path('pbi/<target>/mod',
      views.modifyPbi,
      name='Mod-Pbi'),
  path('pbi/<pk>/mod/delete',
      views.deletePbi,
      name='deletePbi'),
]
