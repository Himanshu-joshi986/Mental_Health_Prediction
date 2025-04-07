from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze_text, name='analyze_text'),
    path('recommend/', views.recommend_page, name='recommend_page'),
    path('get_recommendations/', views.get_recommendations, name='get_recommendations'),
]
