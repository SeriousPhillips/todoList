from django.urls import path,include

from . import views


app_name='todoLst'
urlpatterns = [
    path('', views.index),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in_process/', views.sign_in_process, name='sign_in_process'),
    path('sign_un_process/', views.sign_up_process, name='sign_up_process'),
    path('tasks/', views.tasks, name='tasks' ),
   # path('preauth/', views.preauth),
   # path('auth/', views.auth, name='auth' ),
    path('addtask/',views.addTask,name='addTask'),
    path('cnhgtasks/',views.chngTasks,name='chngTasks'),

    #path('tt/',views.tt,name='tt')]
]
    







	
