from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .ai.gms_client import parse_user_input, explain
import asyncio, re

from .models import Drug, Review, Comment
from .serializers import DrugListSerializer, CommentSerializer, ReviewSerializer, ReviewDetailSerializer
from django.db.models import Avg, Count, Max
from django.db.models.functions import Coalesce

# Create your views here.
@api_view(['GET'])
def drug_list(request):
    drugs = Drug.objects.all()
    symptom_id = request.GET.get('symptom')
    search_query = request.GET.get('search')

    print(f"--- 요청 들어옴 ---")
    print(f"받은 증상 ID: {symptom_id}")
    print(f"받은 검색어: {search_query}")

    if symptom_id:
        drugs = drugs.filter(symptom_id=symptom_id)
        print(f"증상 필터링 적용됨. 결과: {drugs.count()}건")
    
    elif search_query:
        drugs = drugs.filter(name__icontains=search_query)
        print(f"이름 검색 적용됨. 결과: {drugs.count()}건")
    serializer = DrugListSerializer(drugs, many=True)
    return Response(serializer.data)

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

    serializer = DrugListSerializer(drug)
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

@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def review_list(request, drug_pk):
    drug = get_object_or_404(Drug, pk=drug_pk)

    if request.method == 'GET':
        reviews = Review.objects.filter(drug=drug)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

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
        serializer = ReviewDetailSerializer(review)
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


@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot_view(request):
    user_message = request.data.get('message', '')
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

    keyword = normalize_kwd(parsed.get('drug_name') or user_message)

    if keyword:
        return explain_drug_by_name(keyword)

    return Response({
        'answer': '어떤 도움을 드릴까요? 증상이나 궁금한 약 이름을 말씀해주세요'
    })
