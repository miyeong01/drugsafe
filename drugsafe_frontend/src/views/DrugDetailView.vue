<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useDrugStore } from "@/stores/drug";
import { useAccountStore } from "@/stores/accounts";
import {
  Star,
  Heart,
  MessageSquare,
  ArrowLeft,
  AlertTriangle, // 주의사항 아이콘 누락 방지
  Info, // 주의사항 아이콘 누락 방지
} from "lucide-vue-next";

const router = useRouter();
const route = useRoute();
const drugStore = useDrugStore();
const accountStore = useAccountStore();

const { selectedDrug, reviews } = storeToRefs(drugStore);

const activeTab = ref("info");

const goBack = () => {
  router.back();
};

onMounted(() => {
  const drugId = route.params.drugId;
  drugStore.getDrugDetail(drugId);
  drugStore.getReviews(drugId);
});

const goReviewWrite = () => {
  if (!accountStore.isLogin) {
    if (
      confirm(
        "리뷰 작성을 위해 로그인이 필요합니다. 로그인 페이지로 이동하시겠습니까?"
      )
    ) {
      router.push({ path: "/auth", query: { mode: "login" } });
    }
    return;
  }

  router.push({
    name: "ReviewWrite",
    params: { drugId: selectedDrug.value.id },
  });
};

const formatDate = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

const goReviewDetail = (reviewId) => {
  router.push({
    name: "ReviewDetail", // router/index.js에 정의된 상세 페이지 route 이름
    params: {
      drugId: selectedDrug.value.id, // 약 ID
      reviewId: reviewId            // 리뷰 ID
    },
  });
};

// 즐겨찾기 버튼 클릭 핸들러
const handleToggleFavorite = () => {
  if (!accountStore.isLogin) {
    if (confirm("즐겨찾기 기능은 로그인이 필요합니다. 로그인하시겠습니까?")) {
      router.push({ path: "/auth", query: { mode: "login" } });
    }
    return;
  }
  // ✅ 스토어의 토글 함수 호출
  drugStore.toggleFavorite(selectedDrug.value.id);
};

const getFormEmoji = (form) => {
  const map = {
    1:"💊",
    2:"🍚",
    3:"🧉",
    4:"💧",
    5:"💨",
    6:"⿻",
    7:"🧴",
    8:"🧴",
    9:"🩹",
    10:"🧴",
  };
  return map[form];
}
</script>

<template>
  <div v-if="selectedDrug" class="min-vh-100 bg-light py-5">
    <div class="container" style="max-width: 900px">
      <button class="btn btn-light shadow-sm rounded-circle p-2 mb-4" @click="goBack">
        <ArrowLeft :size="20" class="text-secondary" />
      </button>

      <div class="row g-4 mb-5">
        <div class="col-md-5">
          <div class="card border-0 shadow-sm h-100">
            <!-- 이미지 있을 때: 카드 전체를 이미지로 -->
            <div v-if="selectedDrug && selectedDrug.image_url" class="d-flex align-items-center justify-content-center"
              style="height: 100%;">
              <img :src="selectedDrug.image_url" alt="의약품 이미지" style="
        width: 100%;
        height: 100%;
        object-fit: contain;
      " />
            </div>

            <!-- 이미지 없을 때: 기존 원형 + 이모지 -->
            <div v-else class="d-flex align-items-center justify-content-center py-5">
              <div class="bg-light rounded-circle d-flex align-items-center justify-content-center"
                style="width: 150px; height: 150px">
                <span style="font-size: 4rem">{{ getFormEmoji(selectedDrug.form) }}</span>
              </div>
            </div>
          </div>


        </div>
        <div class="col-md-7">
          <div class="h-100 d-flex flex-column justify-content-center">
            <div class="mb-2">
              <span class="badge bg-secondary bg-opacity-10 text-secondary rounded-pill fw-normal px-3 py-2">
                {{ selectedDrug.form_name }}
              </span>
            </div>
            <h1 class="fw-bold mb-1 display-6">{{ selectedDrug.name }}</h1>
            <p class="text-secondary mb-3 fs-5">{{ selectedDrug.company }}</p>
            <div class="d-flex gap-2 mb-4">
              <button @click="handleToggleFavorite" class="btn d-flex align-items-center gap-2 px-3"
                :class="selectedDrug.is_favorite ? 'btn-danger' : 'btn-outline-danger'">
                <Heart :size="18" :fill="selectedDrug.is_favorite ? 'currentColor' : 'none'" />
                {{ selectedDrug.is_favorite ? '즐겨찾기 취소' : '즐겨찾기' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <ul class="nav nav-pills nav-fill mb-4 bg-white p-1 rounded shadow-sm">
        <li class="nav-item" v-for="tab in [
          'info',
          'usage',
          'warnings',
          'side_effect',
          'store',
          'reviews',
        ]" :key="tab">
          <button class="nav-link fw-bold" :class="{ active: activeTab === tab }" @click="activeTab = tab">
            {{
              tab === "info"
                ? "상세정보"
                : tab === "usage"
                  ? "용법·용량"
                  : tab === "warnings"
                    ? "주의사항"
                    : tab === "side_effect"
                      ? "부작용"
                      : tab === "store"
                        ? "보관방법"
                        : "리뷰"
            }}
          </button>
        </li>
      </ul>

      <div class="card shadow-sm border-0 mb-5">
        <div class="card-body p-4 p-md-5">
          <div v-if="activeTab === 'info'">
            <div class="mb-5">
              <h3 class="h5 fw-bold mb-3 d-flex align-items-center">
                <span class="badge bg-primary me-2" style="width: 4px; height: 18px; padding: 0"></span>
                효능 · 효과
              </h3>
              <p class="text-secondary lh-lg mb-0" style="white-space: pre-wrap">
                {{ selectedDrug.efficacy || "정보가 없습니다." }}
              </p>
            </div>
            <div>
              <h3 class="h5 fw-bold mb-3 d-flex align-items-center">
                <span class="badge bg-primary me-2" style="width: 4px; height: 18px; padding: 0"></span>
                주성분
              </h3>
              <p class="text-secondary lh-lg mb-0">
                {{ selectedDrug.basis || "정보가 없습니다." }}
              </p>
            </div>
          </div>

          <div v-else-if="activeTab === 'usage'">
            <h3 class="h5 fw-bold mb-3">용법 · 용량</h3>
            <p class="text-secondary lh-lg mb-0" style="white-space: pre-wrap">
              {{ selectedDrug.use || "정보가 없습니다." }}
            </p>
          </div>

          <div v-if="activeTab === 'warnings'">
            <div class="mb-4">
              <h3 class="h5 fw-bold text-danger mb-3 d-flex align-items-center gap-2">
                <AlertTriangle :size="20" /> 사용상의 주의사항
              </h3>
              <div class="p-3 bg-danger bg-opacity-10 rounded text-dark lh-lg" style="white-space: pre-wrap">
                {{ selectedDrug.caution || "정보가 없습니다." }}
              </div>
            </div>

            <div>
              <h3 class="h5 fw-bold text-primary mb-3 d-flex align-items-center gap-2">
                <Info :size="20" /> 복용 시 주의사항
              </h3>
              <div class="p-3 bg-primary bg-opacity-10 rounded text-dark lh-lg" style="white-space: pre-wrap">
                {{ selectedDrug.caution_intake || "정보가 없습니다." }}
              </div>
            </div>
          </div>

          <div v-else-if="activeTab === 'side_effect'">
            <h3 class="h5 fw-bold mb-3">부작용</h3>
            <p class="text-secondary lh-lg mb-0" style="white-space: pre-wrap">
              {{ selectedDrug.side_effect || "정보가 없습니다." }}
            </p>
          </div>

          <div v-else-if="activeTab === 'store'">
            <h3 class="h5 fw-bold mb-3">보관방법</h3>
            <p class="text-secondary lh-lg mb-0" style="white-space: pre-wrap">
              {{ selectedDrug.store || "정보가 없습니다." }}
            </p>
          </div>

          <div v-else-if="activeTab === 'reviews'">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <h3 class="h5 fw-bold mb-0">리뷰 ({{ reviews?.length || 0 }})</h3>
              <button class="btn btn-primary btn-sm text-white" @click="goReviewWrite">
                <MessageSquare :size="16" /> 리뷰 작성
              </button>
            </div>

            <div v-if="reviews?.length > 0" class="d-flex flex-column gap-3">
              <div v-for="review in reviews" :key="review.id" class="border rounded p-4 bg-white shadow-sm"
                @click="goReviewDetail(review.id)">
                <div class="d-flex justify-content-between mb-2">
                  <span class="fw-bold">{{ review.username }}님</span>
                  <div class="text-warning small">
                    <Star v-for="i in 5" :key="i" :size="16" :fill="i <= review.score ? '#FFC107' : 'none'" :class="i <= review.score
                      ? 'text-warning'
                      : 'text-secondary opacity-25'
                      " />
                  </div>
                </div>
                <p class="text-secondary small mb-2">
                  {{ formatDate(review.created_at) }}
                </p>
                <h5 class="h6 fw-bold mb-2">{{ review.title }}</h5>
                <p class="text-dark mb-3 lh-base" style="white-space: pre-wrap">
                  {{ review.content }}
                </p>
              </div>
            </div>
            <div v-else class="text-center py-5 text-secondary">
              아직 작성된 리뷰가 없습니다.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="min-vh-100 d-flex flex-column justify-content-center align-items-center">
    <div class="spinner-border text-primary mb-3"></div>
    <p class="text-secondary">약 정보를 불러오는 중입니다...</p>
  </div>
</template>

<style scoped>
/* 탭 활성화 스타일 */
.nav-pills .nav-link.active {
  background-color: #f8f9fa;
  color: #0d6efd;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.nav-pills .nav-link {
  color: #6c757d;
}

.review-card {
  cursor: pointer;
  /* 마우스 커서를 손가락 모양으로 변경 */
  transition: all 0.2s ease-in-out;
  /* 부드러운 애니메이션 효과 */
}

.review-card:hover {
  background-color: #fdfdfd !important;
  /* 배경색 아주 살짝 변경 */
  transform: translateY(-3px);
  /* 위로 살짝 떠오름 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
  /* 그림자 강조 */
  border-color: #0d6efd !important;
  /* 테두리 강조 */
}
</style>
