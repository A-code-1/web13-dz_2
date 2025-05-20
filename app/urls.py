from app import views
from django.urls import path

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('hot', views.hot, name="hot"),
    path('question/<int:question_id>/', views.question, name='question'),
    path('new_question/', views.new_question, name='new_question'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
]