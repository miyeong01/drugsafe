<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useDrugStore } from '@/stores/drug'
import { storeToRefs } from 'pinia'
import {
  Heart,
  Pill,
  FileText,
  Settings,
  CheckCircle2,
  Circle,
  Star,
  MessageCircle,
  MessageSquare,
  MessageCircleCode,
  MessageCircleHeart
} from 'lucide-vue-next'

const router = useRouter()
const accountStore = useAccountStore()
const drugStore = useDrugStore()
const { myReviews, myComments, myFavorites } = storeToRefs(drugStore)

onMounted(async () => {
  // 토큰이 있을 때만 실행
  if (accountStore.token) {
    // 유저 정보가 없으면 먼저 가져오기
    if (!accountStore.userInfo) {
      await accountStore.getUserInfo()
    }
    await drugStore.getMyReviews()
    await drugStore.getMyComments()
    await drugStore.getFavorites()
  }

  console.log('리뷰 로드 완료:', drugStore.myReviews)
})

// 날짜 형식을 예쁘게 바꿔주는 함수
const formatDate = (dateString) => {
  if (!dateString) return ""
  return new Date(dateString).toLocaleDateString()
}

// 현재 활성화된 탭 ('favorites', 'reviews', 'comments')
const activeTab = ref('favorites')

const times = ['아침', '점심', '저녁']

// 페이지 이동 함수
const goProfileEdit = () => {
  router.push({ name: 'profile-edit' })
}

const goCommunity = () => {
  router.push('/community')
}

const goReviewDetail = (drugId, reviewId, commentId = null) => {
  const target = {
    name: 'ReviewDetail',
    params: { drugId: drugId, reviewId: reviewId }
  };

  // ✅ 댓글 ID가 있으면 해시(#)를 추가합니다.
  if (commentId) {
    target.hash = `#comment-${commentId}`;
  }

  router.push(target);
}
</script>

<template>
  <div class="min-vh-100 py-5 bg-light">
    <div class="container" style="max-width: 900px;">

      <div class="card shadow-sm border-0 mb-4">
        <div class="card-body p-4">
          <div class="d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center gap-4">
              <div class="bg-primary bg-opacity-10 rounded-circle d-flex align-items-center justify-content-center"
                style="width: 80px; height: 80px;">
                <span style="font-size: 2.5rem;">👤</span>
              </div>
              <div>
                <h2 class="h4 fw-bold mb-1 text-dark">
                  {{ accountStore.userInfo?.name || accountStore.userInfo?.username }}님
                </h2>
                <p class="text-secondary mb-0">
                  {{ accountStore.userInfo?.email || '이메일 정보가 없습니다.' }}
                </p>
              </div>
            </div>

            <button class="btn btn-outline-secondary d-flex align-items-center gap-2" @click="goProfileEdit">
              <Settings :size="16" />
              설정
            </button>
          </div>
        </div>
      </div>

      <div class="row g-4 mb-4">
        <div class="col-md-4">
          <div class="card shadow-sm border-0 h-100 text-center py-4">
            <div class="card-body">
              <Heart class="mx-auto mb-2 text-primary" :size="32" />
              <div class="fw-medium text-dark mb-1">즐겨찾기</div>
              <p class="text-secondary mb-0">{{ myFavorites?.length || 0 }}개</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm border-0 h-100 text-center py-4">
            <div class="card-body">
              <FileText class="mx-auto mb-2 text-primary" :size="32" />
              <div class="fw-medium text-dark mb-1">작성한 리뷰</div>
              <p class="text-secondary mb-0">{{ myReviews?.length || 0 }}개</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm border-0 h-100 text-center py-4">
            <div class="card-body">
              <MessageCircle class="mx-auto mb-2 text-primary" :size="32" />
              <div class="fw-medium text-dark mb-1">작성한 댓글</div>
              <p class="text-secondary mb-0">{{ myComments?.length || 0 }}개</p>
            </div>
          </div>
        </div>
      </div>

      <ul class="nav nav-pills nav-fill mb-4 bg-white p-1 rounded shadow-sm">
        <li class="nav-item">
          <button class="nav-link fw-bold" :class="{ active: activeTab === 'favorites' }"
            @click="activeTab = 'favorites'">
            즐겨찾기
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link fw-bold" :class="{ active: activeTab === 'reviews' }" @click="activeTab = 'reviews'">
            내 리뷰
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link fw-bold" :class="{ active: activeTab === 'comments' }"
            @click="activeTab = 'comments'">
            내 댓글
          </button>
        </li>
      </ul>

      <div v-if="activeTab === 'favorites'">
        <div class="d-flex flex-column gap-3">
          <div v-for="drug in myFavorites" :key="drug.id" class="card shadow-sm border-0 hover-shadow">
            <div class="card-body p-4">

              <div class="d-flex align-items-center gap-4">
                <div class="flex-shrink-0 bg-light rounded d-flex align-items-center justify-content-center"
                  style="width: 80px; height: 80px; overflow: hidden;">
                  <img v-if="drug.image_url" :src="drug.image_url" alt="약 이미지" class="w-100 h-100 object-fit-contain" />
                  <Pill v-else class="text-secondary opacity-50" :size="32" />
                </div>

                <div class="flex-grow-1">
                  <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                      <h3 class="h5 fw-bold mb-1">{{ drug.name }}</h3>
                      <p class="text-secondary small mb-0">{{ drug.company }}</p>
                    </div>
                    <button class="btn btn-outline-primary btn-sm rounded-pill px-3"
                      @click="router.push({ name: 'drug-detail', params: { drugId: drug.id } })">
                      상세보기
                    </button>
                  </div>

                  <p class="text-dark small mb-0 text-truncate" style="max-width: 500px;">
                    {{ drug.use }}
                  </p>
                </div>
              </div>

            </div>
          </div>

          <div v-if="!myFavorites?.length" class="text-center py-5 text-secondary bg-white rounded shadow-sm">
            <Heart class="mx-auto mb-3 opacity-25" :size="48" />
            <p>즐겨찾기한 약이 없습니다.<br><small>자주 복용하시는 약을 등록해보세요!</small></p>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'reviews'">
        <div class="d-flex flex-column gap-3">
          <div v-for="review in myReviews" :key="review.id" class="card shadow-sm border-0">
            <div class="card-body p-4">

              <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                  <h4 class="h6 fw-bold mb-1">{{ review.drug_name || '의약품 리뷰' }}</h4>
                  <div class="d-flex align-items-center gap-2">
                    <div class="d-flex text-warning">
                      <Star v-for="i in 5" :key="i" :size="14" :fill="i <= review.score ? 'currentColor' : 'none'"
                        :class="i <= review.score ? 'text-warning' : 'text-secondary opacity-25'" />
                    </div>
                    <span class="text-secondary small">{{ formatDate(review.created_at) }}</span>
                  </div>
                </div>
                <button class="btn btn-outline-primary btn-sm rounded-pill px-3" @click="goReviewDetail(review.drug, review.id)">
                  상세보기
                </button>
              </div>

              <p class="text-dark mb-2">{{ review.content }}</p>
            </div>
          </div>

          <div v-if="!myReviews?.length" class="text-center py-5 text-secondary">
            <FileText class="mx-auto mb-3 opacity-25" :size="48" />
            <p>아직 작성한 리뷰가 없습니다.</p>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'comments'">
        <div class="d-flex flex-column gap-3">
          <div v-for="comment in myComments" :key="comment.id" class="card shadow-sm border-0">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                  <h4 class="h6 fw-bold mb-1">{{ comment.drug_name || '작성한 댓글' }}</h4>
                  <span class="text-secondary small">{{ formatDate(comment.created_at) }}</span>
                </div>
                <button class="btn btn-outline-primary btn-sm rounded-pill px-3"
                  @click="goReviewDetail(comment.drug_id, comment.review, comment.id)">
                  상세보기
                </button>
              </div>
              <p class="text-dark mb-0">{{ comment.content }}</p>
            </div>
          </div>

          <div v-if="!myComments?.length" class="text-center py-5 text-secondary">
            <MessageSquare class="mx-auto mb-3 opacity-25" :size="48" />
            <p>아직 작성한 댓글이 없습니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 탭 활성화 스타일 (부트스트랩 오버라이드) */
.nav-pills .nav-link.active {
  background-color: #f8f9fa;
  /* bg-light */
  color: #0d6efd;
  /* Primary Color */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  font-weight: bold;
}

.nav-pills .nav-link {
  color: #6c757d;
  /* Secondary Color */
}

/* 호버 시 그림자 효과 */
.hover-shadow:hover {
  transform: translateY(-2px);
  box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .15) !important;
  transition: all 0.2s ease;
}

.cursor-pointer {
  cursor: pointer;
}
</style>