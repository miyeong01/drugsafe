from django.urls import path
from . import views


urlpatterns = [
    # 의약품 R
    path('drugs/', views.drug_list),
    path('drugs/<int:drug_pk>/', views.drug_detail),
    # 리뷰 CRUD
    path('drugs/<int:drug_pk>/reviews/', views.review_list),    # GET(전체), POST
    path('drugs/<int:drug_pk>/reviews/<int:review_pk>/', views.review_detail),  # GET(상세), PUT, DELETE
    # 댓글 CRUD
    path('reviews/<int:review_pk>/comments/', views.comment_list),  # GET, POST
    path('reviews/<int:review_pk>/comments/<int:comment_pk>/', views.comment_detail),   # PUT, DELETE
]
