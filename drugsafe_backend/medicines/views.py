from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Drug, Review, Score, Comment
from .serializers import DrugListSerializer, CommentSerializer, ReviewSerializer, ReviewDetailSerializer, ScoreSerializer

# Create your views here.
@api_view(['GET'])
def drug_list(request):
    drugs = Drug.objects.all()
    serializer = DrugListSerializer(drugs, many=True)
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
            serializer.save(drug=drug, user=request.user)
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
                user=request.user
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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def score_list(request, drug_pk):
    drug = get_object_or_404(Drug, pk=drug_pk)
    if request.method == 'GET':
        scores = Score.objects.filter(drug=drug)
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                drug=drug,
                user=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def score_detail(request, drug_pk, score_pk):
    score = get_object_or_404(
        Score,
        pk=score_pk,
        drug_id=drug_pk
    )
    if request.method == 'PUT':
        if score.user != request.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ScoreSerializer(score, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        if score.user != request.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        score.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)