from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.QuestionCreateView.as_view(), name="question_create"),
    path('<int:pk>/delete', views.QuestionDeleteView.as_view(), name="question_delete"),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name="question_detail"),
    path('', views.QuestionListView.as_view(), name="question_list"),
    path('api/<int:pk>', views.AdviceListView.as_view()),
    path('api/<int:pk>/create', views.AdviceCreateView.as_view()),

]