# medicines/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from medicines.models import Drug, Review, Comment, Form
import random

User = get_user_model()

class Command(BaseCommand):
    help = '약별로 10개씩 테스트 리뷰와 댓글을 생성합니다.'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        drugs = Drug.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.ERROR('유저 데이터가 없습니다. 먼저 유저를 생성하세요.'))
            return
        
        # 리뷰에 쓸 샘플 텍스트들
        titles = ["효과가 좋네요", "그저 그래요", "부작용 조심하세요", "강력 추천!", "재구매 의사 있음"]
        contents = [
            "먹고 나서 증상이 바로 완화되었습니다.",
            "약간 졸음이 오긴 하는데 효과는 확실하네요.",
            "복용법을 잘 지켜야 할 것 같아요.",
            "생각보다 효과가 없어서 실망했습니다.",
            "가성비가 아주 좋습니다."
        ]

        for drug in drugs:
            self.stdout.write(f'{drug.name}에 대한 리뷰 생성 중...')
            
            # 각 약에 연결된 Form(제형)이 있다면 가져오기
            # 만약 Drug와 Form이 1:N 관계라면 drug.form을 사용, 
            # 여기서는 Review 모델 구조에 맞춰 임의의 Form 하나를 선택
            target_form = Form.objects.first() 

            for i in range(10):
                # 1. 리뷰 생성
                review = Review.objects.create(
                    user=random.choice(users),
                    drug=drug,
                    form=target_form,
                    score=random.randint(1, 5),
                    title=f"{random.choice(titles)} ({i+1}번째)",
                    content=random.choice(contents)
                )

                # 2. 각 리뷰당 댓글 1~3개 랜덤 생성
                for _ in range(random.randint(1, 3)):
                    Comment.objects.create(
                        review=review,
                        user=random.choice(users),
                        form=target_form,
                        content=f"좋은 리뷰 감사합니다! 정보에 큰 도움이 되었어요. ({random.randint(1, 100)})"
                    )

        self.stdout.write(self.style.SUCCESS('모든 테스트 데이터 생성 완료!'))