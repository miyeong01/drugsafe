from django.urls import path
from . import views


urlpatterns = [
    path('drugs/', views.drug_list),
    # 리뷰 CRUD
    path('drugs/<int:drug_pk>/reviews/', views.review_list),    # GET(전체), POST
    path('drugs/<int:drug_pk>/reviews/<int:review_pk>/', views.review_detail),  # GET(상세), PUT, DELETE
    # 댓글 CRUD
    path('reviews/<int:review_pk>/comments/', views.comment_list),  # GET, POST
    path('reviews/<int:review_pk>/comments/<int:comment_pk>/', views.comment_detail),   # PUT, DELETE
    # 별점 CRUD
    path('drugs/<int:drug_pk>/scores/', views.score_list),  # GET, POST
    path('drugs/<int:drug_pk>/scores/<int:score_pk>/', views.score_detail), # PUT, DELETE
]
