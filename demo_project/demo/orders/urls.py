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
  path('<projectID>/accept-invite-landing/',
       views.AcceptInviteLanding,
       name='AcceptInviteLanding'),
  path('projects',
       views.AllProjects.as_view(),
       name="AllProjects"),
  path('createProject/',
       views.createProject,
       name='createProject'),
  path('<projectID>/main/createPbi',
      views.addPbi,
      name='Cre-Pbi'),
  path('<projectID>/main/pbi/<target>/',
      views.OnePbi.as_view(),
      name='User-Pbi'),
  path('<projectID>/main/pbi/<target>/mod',
      views.modifyPbi,
      name='Mod-Pbi'),
  path('<projectID>/main/pbi/<pk>/mod/delete',
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
  path('<projectID>/main/createSprintLanding',
       views.CreateSprintLanding,
       name='CreateSprintLanding'),
  path('<projectID>/main/createSprint',
       views.CreateSprint,
       name='CreateSprint'),
  path('<projectID>/main/currentpbi/<target>/createTask',
       views.CreateTask,
       name='CreateTask'),
  path('<projectID>/main/<pbi>/task/<target>/',
        views.OneTask.as_view(),
        name='OneTask'),
  path('<projectID>/main/<pbi>/task/<target>/mod/',
        views.modifyTask,
        name='modifyTask'),
  path('<projectID>/main/pbi/<target>/bringPbi',
        views.BringPbiToSprint,
        name='bringPbi'),
    path('<projectID>/main/currentpbi/<target>/',
        views.CurrentPbi.as_view(),
        name='currentPbi'),
    path('<projectID>/main/currentpbi/<target>/remove',
        views.RemoveCurrentPbi,
        name='removeCurrentPbi'),
  path('<projectID>/main/<pbi>/task/<target>/mod/deleteTask',
        views.deleteTask,
        name='deleteTask'),
  path('<projectID>/main/AllSprint',
          views.allSprint.as_view(),
          name='allsprint'),
  path('<projectID>/main/create-invite',
       views.SendInvite,
       name='sendInvite'),
  path('logout',
       views.logout_view),
    path('<projectID>/main/<pbi>/task/<target>/takeownership',
        views.TakeOwnership,
        name='TakeOwnership'),
    path('<projectID>/main/<pbi>/task/<target>/giveupownership',
        views.GiveUpOwnership,
        name='GiveUpOwnership'),
  path('<projectID>/main/changeteam',
        views.ChangeTeam,
        name='ChangeTeam'),
  path('<projectID>/main/changeview',
        views.ChangeView,
        name='ChangeView'),
  path('<projectID>/main/end-sprint-landing',
       views.EndSprintLanding,
       ),
  path('<projectID>/main/start-sprint-landing',
       views.StartSprintLanding,
       ),
]
