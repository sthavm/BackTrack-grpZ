from django.urls import include,path
from orders import views
from orders.views import *
from django.conf.urls import url
from django.contrib.auth.views import LoginView
urlpatterns=[
  path('',
       views.HomePage.as_view(),
       name='homepage'),
  path('redir/',
       views.redir,
       name="Redirect"),
  path('noproject/',
       views.NoProjectView.as_view(),
       name="NoProject"),
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
  path('login/', LoginView.as_view(template_name='registration/login.html'), name="login"),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
  path('accounts/signup/manager/', views.ManagerSignUpView.as_view(), name='manager_signup'),
  path('accounts/signup/dev/', views.DevSignUpView.as_view(), name='dev_signup'),
  path('<projectID>/main/',
      views.mainPage.as_view(),
      name='mainPage'),
]
