from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from .ai.gms_client import parse_user_input, explain
import asyncio, re

from .models import Drug, Review, Comment, Favorite
from .serializers import DrugListSerializer, CommentSerializer, ReviewSerializer, ReviewDetailSerializer, ReviewListSerializer
from django.db.models import Avg, Count, Max
from django.db.models.functions import Coalesce
from .pagination import ReviewPagination
from rest_framework.pagination import PageNumberPagination

# Create your views here.
@api_view(['GET'])
def drug_list(request):
    # 1. 기본 쿼리셋
    drugs = Drug.objects.annotate(
        avg_rating=Coalesce(Avg('drugs__score'), 0.0),
        review_cnt=Coalesce(Count('drugs'), 0)
    )
    
    # 2. 검색 필터
    symptom_id = request.GET.get('symptom')
    search_query = request.GET.get('search')
    
    if symptom_id:
        drugs = drugs.filter(symptom_id=symptom_id)
    elif search_query:
        drugs = drugs.filter(name__icontains=search_query)
    
    # 3. 제형 필터 (여러 개 선택 가능)
    form_filter = request.GET.get('form')  # 예: "1,2,3"
    if form_filter:
        form_ids = [int(f) for f in form_filter.split(',') if f.isdigit()]
        if form_ids:
            drugs = drugs.filter(form_id__in=form_ids)
    
    # 4. 정렬
    sort_by = request.GET.get('sort', 'relevance')
    if sort_by == 'rating':
        drugs = drugs.order_by('-avg_rating', '-review_cnt')
    elif sort_by == 'reviews':
        drugs = drugs.order_by('-review_cnt', '-avg_rating')
    # relevance는 기본 정렬 유지
    
    # 5. 페이지네이션 (필터링/정렬 후에!)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    page = paginator.paginate_queryset(drugs, request)

    serializer = DrugListSerializer(
        page,
        many=True,
        context={'request': request}
    )

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def drug_detail(request, drug_pk):
    drug = (
        Drug.objects.filter(pk=drug_pk)
        .annotate(
            avg_rating=Coalesce(Avg('drugs__score'), 0.0),
            review_cnt=Coalesce(Count('drugs'), 0)
        )
        .first()
    )
    if not drug:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = DrugListSerializer(drug, context={'request': request})
    return Response(serializer.data)

# @api_view(['GET','POST'])
# def review_list(request, drug_pk):
#     drug = get_object_or_404(Drug, pk=drug_pk)
#     if request.method == 'GET':
#         serializer = ReviewSerializer(drug)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(drug=drug)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
from django.db.models import Q

@api_view(['GET'])
@permission_classes([AllowAny])
def all_review_list(request):
    # 1. 기본 쿼리셋
    qs = (
         Review.objects
        .select_related("user", "drug")
    )
    
    # 2. 검색 필터 (페이지네이션 전에!)
    search_query = request.GET.get('search', '').strip()
    if search_query:
        # title, content, drug_name 모두 검색
        qs = qs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(drug__name__icontains=search_query)
        )
    
    # 3. 정렬 (페이지네이션 전에!)
    sort_by = request.GET.get('sort', 'latest')
    if sort_by == 'helpful':
        qs = qs.annotate(
            helpful_count=Count('helpful_users')
        ).order_by('-helpful_count', '-created_at')
    elif sort_by == 'comments':
        qs = qs.annotate(
            comment_count=Count('comments')
        ).order_by('-comment_count', '-created_at')
    else:  # latest
        qs = qs.order_by('-created_at')
    
    # 4. 필터링/정렬된 결과에 페이지네이션
    paginator = ReviewPagination()
    page = paginator.paginate_queryset(qs, request)

    serializer = ReviewSerializer(
        page,
        many=True,
        context={'request': request}
    )
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def review_list(request, drug_pk):
    drug = get_object_or_404(Drug, pk=drug_pk)

    if request.method == 'GET':
        qs = (
            Review.objects
            .filter(drug=drug)
            .select_related("user", "drug")
            .order_by("-created_at")
        )

        paginator = ReviewPagination()
        page = paginator.paginate_queryset(qs, request)

        serializer = ReviewListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(drug=drug, user=request.user, form=drug.form)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def review_detail(request, drug_pk, review_pk):
    review = get_object_or_404(
        Review,
        pk=review_pk,
        drug_id=drug_pk
    )
    if request.method == 'GET':
        serializer = ReviewDetailSerializer(review, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        if review.user != request.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        if review.user != request.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        comments = Comment.objects.filter(review=review)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                review=review,
                user=request.user,
                form=review.form
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_detail(request, review_pk, comment_pk):
    comment = get_object_or_404(
        Comment,
        pk=comment_pk,
        review_id=review_pk
    )
    if request.method == 'PUT':
        if comment.user != request.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        if comment.user != request.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reviews(request):
    # 최신순 정렬
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    
    # ✅ 페이지네이션 추가
    paginator = ReviewPagination()
    page = paginator.paginate_queryset(reviews, request)
    
    serializer = ReviewSerializer(page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_comments(request):
    # 최신순 정렬
    comments = Comment.objects.filter(user=request.user).order_by('-created_at')
    
    # ✅ 페이지네이션 추가
    paginator = PageNumberPagination()
    paginator.page_size = 10
    page = paginator.paginate_queryset(comments, request)
    
    serializer = CommentSerializer(page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_favorites(request):
    # 1. 내가 찜한 약의 ID 목록을 먼저 가져옵니다.
    favorite_ids = Favorite.objects.filter(user=request.user).values_list('drug_id', flat=True)
    
    # 2. 해당 약들을 가져오면서 별점과 리뷰 수를 계산(annotate)합니다.
    drugs = (
        Drug.objects.filter(id__in=favorite_ids)
        .annotate(
            avg_rating=Coalesce(Avg('drugs__score'), 0.0),
            review_cnt=Coalesce(Count('drugs'), 0)
        )
        .order_by('-id')  # 최신 즐겨찾기 순
    )
    
    # 3. ✅ 페이지네이션 추가
    paginator = PageNumberPagination()
    paginator.page_size = 10
    page = paginator.paginate_queryset(drugs, request)
    
    # 4. context에 request를 담아 즐겨찾기 여부 로직이 에러 나지 않게 합니다.
    serializer = DrugListSerializer(page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)

# 약 상세 페이지에서 즐겨찾기를 누를 때 호출할 함수
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, drug_pk):
    drug = get_object_or_404(Drug, pk=drug_pk)
    user = request.user
    
    favorite = Favorite.objects.filter(user=user, drug=drug)
    
    if favorite.exists():
        favorite.delete()
        return Response({'message': '즐겨찾기에서 제거되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
    else:
        Favorite.objects.create(user=user, drug=drug)
        return Response({'message': '즐겨찾기에 추가되었습니다.'}, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_helpful(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    user = request.user

    if review.helpful_users.filter(pk=user.pk).exists():
        # 이미 눌렀다면 취소
        review.helpful_users.remove(user)
        is_helpful = False
    else:
        # 처음 누르는 것이라면 추가
        review.helpful_users.add(user)
        is_helpful = True

    return Response({
        'is_helpful': is_helpful,
        'helpful_count': review.helpful_users.count()
    })
    
def recommend_drug(parsed, user_message):
    symptom = parsed.get('symptom')
    form = parsed.get('form')
    sort = parsed.get('sort', 'relevance')

    qs = Drug.objects.annotate(
        avg_rating = Coalesce(Avg('drugs__score'), 0.0),
        review_cnt = Coalesce(Count('drugs'), 0)
    )

    if symptom:
        qs = qs.filter(symptom__name__icontains=symptom)
    if form:
        qs = qs.filter(form__name__icontains=form)

    if sort == 'rating':
        qs = qs.order_by('-avg_rating', '-review_cnt')
    elif sort == 'review':
        qs = qs.order_by('-review_cnt', '-avg_rating')

    qs = qs[:3]

    if not qs.exists():
        return Response({
            'answer': '해당 조건에 맞는 의약품 정보가 없습니다.'
        })
    context = ''
    for d in qs:
        context += f"""
- 약명: {d.name}
- 평균 별점: {d.avg_rating or 0:.1f}
- 리뷰 수: {d.review_cnt}
- 효능: {d.efficacy}
"""
    answer = asyncio.run(
        explain(context, user_message)
    )

    return Response({'answer': answer})

# def check_interaction(parsed, user_message):
#     drugs = parsed.get("drugs")

#     if not drugs or len(drugs) < 2:
#         return Response({
#             "answer": "비교할 약품 이름을 두 개 이상 입력해주세요."
#         })

#     qs = Drug.objects.filter(name__in=drugs)[:2]

#     if qs.count() < 2:
#         return Response({
#             "answer": "입력한 약 중 일부의 정보가 없습니다."
#         })

#     context = ""
#     for d in qs:
#         context += f"""
# - 약명: {d.name}
# - 성분/효능: {d.efficacy}
# - 주의사항: {d.caution}
# """

#     answer = asyncio.run(
#         explain(context, user_message)
#     )

#     return Response({"answer": answer})

def find_drug_candidates(keyword: str):
    return (
        Drug.objects
        .filter(name__icontains=keyword)
        .values('name')
        .annotate(
            drug_id = Max('id'),
            avg_rating = Coalesce(Avg('drugs__score'), 0.0),
            review_cnt = Coalesce(Count('drugs'), 0)
        )
        .order_by('-review_cnt', '-avg_rating')
    )

def explain_drug_by_name(keyword: str):
    exact = Drug.objects.filter(name=keyword).annotate(
        avg_rating = Coalesce(Avg('drugs__score'), 0.0),
        review_cnt = Coalesce(Count('drugs'),0)
    ).first()

    if exact:
        return Response({
            'type': 'single',
            'drug_id': exact.id,
            'answer': format_drug_info(exact)
        })

    qs = find_drug_candidates(keyword)
    cnt = qs.count()

    if cnt == 0:
        return Response({
            "type": "not_found",
            "answer": "해당 이름의 의약품을 찾을 수 없습니다."
        })

    # 1개면 바로 설명
    if cnt == 1:
        drug = qs.first()
        return Response({
            "type": "single",
            "drug_id": drug.id,
            "answer": format_drug_info(drug)
        })

    # 여러 개면 선택지
    candidates = qs[:3]

    return Response({
        "type": "multiple",
        "candidates": [
            {
                "id": d["drug_id"],
                "name": d["name"]
            }
            for d in candidates
        ],
        "answer": "다음 중 어떤 의약품을 말씀하시는 건가요?"
    })

def format_drug_info(drug: Drug) -> str:
    return f"""💊 약품명: {drug.name}

🏭 제조사: {drug.company}

🩺 효능: {drug.efficacy}

⚠️ 주의사항: {drug.caution}

⭐ 평균 별점: {drug.avg_rating:.1f}

📝 리뷰 수: {drug.review_cnt}개
"""

def normalize_kwd(raw):
    if not raw:
        return ""

    if isinstance(raw, list):
        raw = raw[0]

    if not isinstance(raw, str):
        return ""

    raw = raw.strip()
    raw = re.sub(r'(무슨|어떤)\s*약.*$', '', raw)
    raw = re.sub(r'(은|는|이|가|을|를)\s*$', '', raw)

    return raw

SMALL_TALK_PATTERNS = [
    r'안녕',
    r'하이',
    r'hello',
    r'뭐해',
    r'고마워',
    r'감사',
    r'잘 지내',
    r'반가워',
    r'ㅎ+',
    r'ㅋㅋ+',
    r'^^'
]

def is_small_talk(text: str) -> bool:
    return any(re.search(p, text) for p in SMALL_TALK_PATTERNS)

SMALL_TALK_RESPONSES = [
    "안녕하세요 😊 어떤 증상이나 궁금한 약이 있으신가요?",
    "반가워요! 증상이나 약 이름을 알려주시면 도와드릴게요.",
    "네 😊 어떤 의약품이 궁금하신가요?",
    "괜찮아요! 필요하실 때 언제든 질문해주세요."
]

import random

def get_small_talk_response(_):
    return random.choice(SMALL_TALK_RESPONSES)


@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot_view(request):
    user_message = request.data.get('message', '').strip()
    selected_drug_id = request.data.get('selected_drug_id')

    # 1. 카드 클릭으로 들어온 경우 (최우선)
    if selected_drug_id:
        drug = (
            Drug.objects
            .filter(id=selected_drug_id)
            .annotate(
                avg_rating=Coalesce(Avg('drugs__score'), 0.0),
                review_cnt=Coalesce(Count('drugs'), 0)
            )
            .first()
        )
        if drug:
            return Response({
                "type": "single",
                "drug_id": drug.id,
                "answer": format_drug_info(drug)
            })
        

    # 2. 일반 자연어 처리
    parsed = asyncio.run(parse_user_input(user_message))
    intent = parsed.get('intent')

    if intent == 'recommend':
        return recommend_drug(parsed, user_message)
    
    if intent == 'drug_info':
        keyword = normalize_kwd(parsed.get('drug_name') or user_message)

        if keyword:
            return explain_drug_by_name(keyword)
        
        return Response({
            'type': 'fallback',
            'answer': '궁금한 약 이름을 조금 더 정확히 입력해 주세요 😊'
        })

    if is_small_talk(user_message):
        return Response({
            'type': 'smalltalk',
            'answer': get_small_talk_response(user_message)
        })


    return Response({
        'type': 'fallback',
        'answer': '증상이나 궁금한 약 이름을 말씀해주시면 도와드릴게요 😊'
    })
