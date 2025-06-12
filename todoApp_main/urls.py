from django.urls import path
from . import views


urlpatterns = [
    path('login_page/',views.login_page,name='login'),
    path('register_page/',views.register_page,name='register'),
    path('logout/',views.logoutUser,name='logout'),
    path('',views.home,name="home"),
    path('task/<str:pk>/',views.task,name='task'),
    path('task_create/<str:pk>/',views.create_task,name='task_create' ),
    path('task_update/<str:pk>/',views.update_task,name='task_update' ),
    path('task_delete/<str:pk>/',views.delete_task,name='task_delete' ),
    path('project/<str:pk>/',views.project,name='project'),
    path('project_create/',views.project_create,name='project_create'),
    path('not_allowed/',views.not_allowed,name='not_allowed'),
]