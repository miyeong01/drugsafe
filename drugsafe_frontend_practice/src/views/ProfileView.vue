<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useDrugStore } from '@/stores/drug'
import { storeToRefs } from 'pinia'
import {
  Heart,
  Pill,
  Droplet,
  SprayCan,
  Bandage,
  FileText,
  Settings,
  CheckCircle2,
  Circle,
  Star,
  MessageCircle,
  MessageSquare,
  MessageCircleCode,
  MessageCircleHeart,
  ChevronLeft,
  ChevronRight,
} from 'lucide-vue-next'

import film from "@/assets/icons/film.svg?component";
import lotion from "@/assets/icons/lotion.svg?component";
import cream from "@/assets/icons/cream.svg?component";
import ointment from "@/assets/icons/ointment.svg?component";
import powder from "@/assets/icons/powder.svg?component";

const getFormIcon = (form) => {
  const map = {
    1: Pill,
    2: powder,
    3: Droplet,
    4: Droplet,
    5: SprayCan,
    6: film,
    7: cream,
    8: ointment,
    9: Bandage,
    10: lotion,
  };
  return map[form] || Pill;
}

const router = useRouter()
const accountStore = useAccountStore()
const drugStore = useDrugStore()
const { 
  myReviews, 
  myReviewsPage,
  myReviewsTotal,
  myReviewsNext,
  myReviewsPrev,
  myComments,
  myCommentsPage,
  myCommentsTotal,
  myCommentsNext,
  myCommentsPrev,
  myFavorites,
  myFavoritesPage,
  myFavoritesTotal,
  myFavoritesNext,
  myFavoritesPrev,
} = storeToRefs(drugStore)

// 페이지네이션 계산
const reviewTotalPages = computed(() => Math.ceil(myReviewsTotal.value / 10) || 1)
const commentTotalPages = computed(() => Math.ceil(myCommentsTotal.value / 10) || 1)
const favoriteTotalPages = computed(() => Math.ceil(myFavoritesTotal.value / 10) || 1)

onMounted(async () => {
  // 토큰이 있을 때만 실행
  if (accountStore.token) {
    // 유저 정보가 없으면 먼저 가져오기
    if (!accountStore.userInfo) {
      await accountStore.getUserInfo()
    }
    await drugStore.getMyReviews(1)
    await drugStore.getMyComments(1)
    await drugStore.getFavorites(1)
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

// 리뷰 페이지 변경
const changeReviewPage = (direction) => {
  if (direction === 'prev' && myReviewsPrev.value && myReviewsPage.value > 1) {
    drugStore.getMyReviews(myReviewsPage.value - 1)
  } else if (direction === 'next' && myReviewsNext.value) {
    drugStore.getMyReviews(myReviewsPage.value + 1)
  }
}

// 댓글 페이지 변경
const changeCommentPage = (direction) => {
  if (direction === 'prev' && myCommentsPrev.value && myCommentsPage.value > 1) {
    drugStore.getMyComments(myCommentsPage.value - 1)
  } else if (direction === 'next' && myCommentsNext.value) {
    drugStore.getMyComments(myCommentsPage.value + 1)
  }
}

// 즐겨찾기 페이지 변경
const changeFavoritePage = (direction) => {
  if (direction === 'prev' && myFavoritesPrev.value && myFavoritesPage.value > 1) {
    drugStore.getFavorites(myFavoritesPage.value - 1)
  } else if (direction === 'next' && myFavoritesNext.value) {
    drugStore.getFavorites(myFavoritesPage.value + 1)
  }
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
              <p class="text-secondary mb-0">{{ myFavoritesTotal || 0 }}개</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm border-0 h-100 text-center py-4">
            <div class="card-body">
              <FileText class="mx-auto mb-2 text-primary" :size="32" />
              <div class="fw-medium text-dark mb-1">작성한 리뷰</div>
              <p class="text-secondary mb-0">{{ myReviewsTotal || 0 }}개</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm border-0 h-100 text-center py-4">
            <div class="card-body">
              <MessageCircle class="mx-auto mb-2 text-primary" :size="32" />
              <div class="fw-medium text-dark mb-1">작성한 댓글</div>
              <p class="text-secondary mb-0">{{ myCommentsTotal || 0 }}개</p>
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
                  <div v-else class="text-secondary opacity-50" :size="32">
                    <component :is="getFormIcon(drug.form)" class="text-primary drug-icon" />
                  </div>
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
        <!-- 즐겨찾기 페이지네이션 -->
        <nav v-if="myFavoritesNext || myFavoritesPrev" class="d-flex justify-content-center mt-4">
          <div class="minimal-pagination d-flex align-items-center gap-3">
            <button class="btn-arrow" :disabled="!myFavoritesPrev" @click="changeFavoritePage('prev')">
              <ChevronLeft :size="20" />
            </button>

            <div class="current-page-display shadow-sm">
              <span class="fw-bold text-primary">{{ myFavoritesPage }}</span>
              <span class="text-muted mx-1">/</span>
              <span class="text-secondary small">{{ favoriteTotalPages }}</span>
            </div>

            <button class="btn-arrow" :disabled="!myFavoritesNext" @click="changeFavoritePage('next')">
              <ChevronRight :size="20" />
            </button>
          </div>
        </nav>
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

        <!-- 리뷰 페이지네이션 -->
        <nav v-if="myReviewsNext || myReviewsPrev" class="d-flex justify-content-center mt-4">
          <div class="minimal-pagination d-flex align-items-center gap-3">
            <button class="btn-arrow" :disabled="!myReviewsPrev" @click="changeReviewPage('prev')">
              <ChevronLeft :size="20" />
            </button>

            <div class="current-page-display shadow-sm">
              <span class="fw-bold text-primary">{{ myReviewsPage }}</span>
              <span class="text-muted mx-1">/</span>
              <span class="text-secondary small">{{ reviewTotalPages }}</span>
            </div>

            <button class="btn-arrow" :disabled="!myReviewsNext" @click="changeReviewPage('next')">
              <ChevronRight :size="20" />
            </button>
          </div>
        </nav>
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

        <!-- 댓글 페이지네이션 -->
        <nav v-if="myCommentsNext || myCommentsPrev" class="d-flex justify-content-center mt-4">
          <div class="minimal-pagination d-flex align-items-center gap-3">
            <button class="btn-arrow" :disabled="!myCommentsPrev" @click="changeCommentPage('prev')">
              <ChevronLeft :size="20" />
            </button>

            <div class="current-page-display shadow-sm">
              <span class="fw-bold text-primary">{{ myCommentsPage }}</span>
              <span class="text-muted mx-1">/</span>
              <span class="text-secondary small">{{ commentTotalPages }}</span>
            </div>

            <button class="btn-arrow" :disabled="!myCommentsNext" @click="changeCommentPage('next')">
              <ChevronRight :size="20" />
            </button>
          </div>
        </nav>
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

/* 페이지네이션 스타일 */
.minimal-pagination {
  background-color: white;
  padding: 8px 16px;
  border-radius: 50px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5f0ff;
}

.btn-arrow {
  border: none;
  background: none;
  color: #4d9fff;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.btn-arrow:hover:not(:disabled) {
  background-color: #f0f7ff;
  transform: scale(1.1);
}

.btn-arrow:disabled {
  color: #dee2e6;
  cursor: not-allowed;
}

.current-page-display {
  background-color: #f8f9fa;
  padding: 6px 18px;
  border-radius: 20px;
  min-width: 80px;
  text-align: center;
  border: 1px solid #edf2f7;
}
.drug-icon {
  width: 25px;
  height: 25px;
}
</style>