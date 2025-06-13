from app import views
from django.urls import path
from .views import logout_view

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('hot', views.hot, name="hot"),
    path('question/<int:question_id>/', views.question, name='question'),
    path('new_question/', views.new_question, name='new_question'),
    path('login/', views.login_view, name='login1'),
    path('signup/', views.signup_view, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('tag/<str:tag_name>/', views.questions_by_tag, name='questions_by_tag'),
    path('logout/', logout_view, name='logout'),
]

