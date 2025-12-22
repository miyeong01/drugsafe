<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useDrugStore } from "@/stores/drug";
import {
  Star,
  Heart,
  Share2,
  MessageSquare,
  Pill,
  ArrowLeft,
} from "lucide-vue-next";

const router = useRouter();
const route = useRoute();
const drugStore = useDrugStore();

// 스토어에서 selectedDrug 상태를 반응형으로 가져옴.
const { selectedDrug } = storeToRefs(drugStore);

// 현재 탭 상태
const activeTab = ref("info");

// 뒤로가기
const goBack = () => {
  router.back();
};

// 컴포넌트가 마운트될 때 API 호출
onMounted(() => {
  const drugId = route.params.id;
  drugStore.getDrugDetail(drugId);
});

const mockReviews = ref([
  {
    id: "1",
    author: "김**",
    rating: 5,
    date: "2025.01.15",
    content: "두통에 정말 효과가 좋았어요. 속쓰림도 없고 깔끔합니다.",
    helpful: 24,
  },
  {
    id: "2",
    author: "이**",
    rating: 4,
    date: "2025.01.10",
    content:
      "효과는 좋은데 식후 복용 추천합니다. 빈속에는 조금 부담될 수 있어요.",
    helpful: 18,
  },
]);

// 리뷰 작성하러 커뮤니티로 이동
const goCommunityWrite = () => {
  router.push("/community"); // 나중에 글쓰기 페이지로 연결
};
</script>

<template>
  <div v-if="selectedDrug" class="min-vh-100 bg-light py-5">
    <div class="container" style="max-width: 900px">
      <button
        class="btn btn-light shadow-sm rounded-circle p-2 mb-4"
        @click="goBack"
      >
        <ArrowLeft :size="20" class="text-secondary" />
      </button>

      <div class="row g-4 mb-5">
        <div class="col-md-5">
          <div
            class="card border-0 shadow-sm h-100 d-flex align-items-center justify-content-center py-5"
          >
            <div
              class="bg-light rounded-circle p-4 d-flex align-items-center justify-content-center"
              style="width: 150px; height: 150px"
            >
              <span style="font-size: 4rem">💊</span>
            </div>
          </div>
        </div>

        <div class="col-md-7">
          <div class="h-100 d-flex flex-column justify-content-center">
            <div class="mb-2">
              <span
                class="badge bg-secondary bg-opacity-10 text-secondary rounded-pill fw-normal px-3 py-2"
              >
                {{ selectedDrug.form_name }}
              </span>
            </div>

            <h1 class="fw-bold mb-1 display-6">{{ selectedDrug.name }}</h1>
            <p class="text-secondary mb-3 fs-5">{{ selectedDrug.company }}</p>

            <!-- <div class="d-flex align-items-center gap-3 mb-4">
              <div class="d-flex text-warning">
                <Star 
                  v-for="i in 5" 
                  :key="i" 
                  :size="20" 
                  :fill="i <= Math.round(selectedDrug.rating) ? 'currentColor' : 'none'"
                  :class="i <= Math.round(selectedDrug.rating) ? 'text-warning' : 'text-secondary opacity-25'"
                />
              </div>
              <span class="fw-bold fs-5">{{ selectedDrug.rating || 0 }}</span>
              <span class="text-secondary small">({{ (selectedDrug.review_count || 0).toLocaleString() }}개의 리뷰)</span>
            </div> -->

            <div class="d-flex gap-2 mb-4">
              <button
                class="btn btn-outline-danger d-flex align-items-center gap-2 px-3"
              >
                <Heart :size="18" /> 즐겨찾기
              </button>
            </div>
          </div>
        </div>
      </div>

      <ul class="nav nav-pills nav-fill mb-4 bg-white p-1 rounded shadow-sm">
        <li class="nav-item">
          <button
            class="nav-link fw-bold"
            :class="{ active: activeTab === 'info' }"
            @click="activeTab = 'info'"
          >
            상세정보
          </button>
        </li>
        <li class="nav-item">
          <button
            class="nav-link fw-bold"
            :class="{ active: activeTab === 'usage' }"
            @click="activeTab = 'usage'"
          >
            용법·용량
          </button>
        </li>
        <li class="nav-item">
          <button
            class="nav-link fw-bold"
            :class="{ active: activeTab === 'warnings' }"
            @click="activeTab = 'warnings'"
          >
            주의사항
          </button>
        </li>
        <li class="nav-item">
          <button
            class="nav-link fw-bold"
            :class="{ active: activeTab === 'side_effect' }"
            @click="activeTab = 'side_effect'"
          >
            부작용
          </button>
        </li>
        <li class="nav-item">
          <button
            class="nav-link fw-bold"
            :class="{ active: activeTab === 'store' }"
            @click="activeTab = 'store'"
          >
            보관방법
          </button>
        </li>
        <li class="nav-item">
          <button
            class="nav-link fw-bold"
            :class="{ active: activeTab === 'reviews' }"
            @click="activeTab = 'reviews'"
          >
            리뷰
          </button>
        </li>
      </ul>

      <div class="card shadow-sm border-0 mb-5">
        <div class="card-body p-4 p-md-5">
          <div v-if="activeTab === 'info'">
            <div class="mb-5">
              <h3 class="h5 fw-bold mb-3 d-flex align-items-center">
                <span
                  class="badge bg-primary me-2"
                  style="width: 4px; height: 18px; padding: 0"
                ></span>
                효능 · 효과
              </h3>
              <p
                class="text-secondary lh-lg mb-0"
                style="white-space: pre-wrap"
              >
                {{ selectedDrug.efficacy || "정보가 없습니다." }}
              </p>
            </div>

            <div>
              <h3 class="h5 fw-bold mb-3 d-flex align-items-center">
                <span
                  class="badge bg-primary me-2"
                  style="width: 4px; height: 18px; padding: 0"
                ></span>
                주성분
              </h3>
              <p
                class="text-secondary lh-lg mb-0"
                style="white-space: pre-wrap"
              >
                {{ selectedDrug.basis || "정보가 없습니다." }}
              </p>
            </div>
          </div>

          <div v-if="activeTab === 'usage'">
            <h3 class="h5 fw-bold mb-3">용법 · 용량</h3>
            <p class="text-secondary lh-lg mb-0" style="white-space: pre-wrap">
              {{ selectedDrug.use || "정보가 없습니다." }}
            </p>
          </div>

          <div v-if="activeTab === 'warnings'">
            <div class="mb-4">
              <h3
                class="h5 fw-bold text-danger mb-3 d-flex align-items-center gap-2"
              >
                <AlertTriangle :size="20" /> 사용상의 주의사항
              </h3>
              <div
                class="p-3 bg-danger bg-opacity-10 rounded text-dark lh-lg"
                style="white-space: pre-wrap"
              >
                {{ selectedDrug.caution || "정보가 없습니다." }}
              </div>
            </div>

            <div>
              <h3
                class="h5 fw-bold text-primary mb-3 d-flex align-items-center gap-2"
              >
                <Info :size="20" /> 복용 시 주의사항
              </h3>
              <div
                class="p-3 bg-primary bg-opacity-10 rounded text-dark lh-lg"
                style="white-space: pre-wrap"
              >
                {{ selectedDrug.caution_intake || "정보가 없습니다." }}
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'side_effect'">
            <h3 class="h5 fw-bold mb-3">부작용</h3>
            <p class="text-secondary lh-lg mb-0" style="white-space: pre-wrap">
              {{ selectedDrug.side_effect || "정보가 없습니다." }}
            </p>
          </div>

          <div v-if="activeTab === 'store'">
            <h3 class="h5 fw-bold mb-3">보관방법</h3>
            <p class="text-secondary lh-lg mb-0" style="white-space: pre-wrap">
              {{ selectedDrug.store || "정보가 없습니다." }}
            </p>
          </div>

          <div v-if="activeTab === 'reviews'">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <h3 class="h5 fw-bold mb-0">리뷰</h3>
              <button
                class="btn btn-primary btn-sm d-flex align-items-center gap-2"
                @click="goCommunityWrite"
              >
                <MessageSquare :size="16" /> 리뷰 작성
              </button>
            </div>

            <div class="d-flex flex-column gap-3">
              <div
                v-for="review in mockReviews"
                :key="review.id"
                class="border rounded p-3"
              >
                <div class="d-flex justify-content-between mb-2">
                  <span class="fw-bold">{{ review.author }}</span>
                  <div class="text-warning small">
                    <Star
                      v-for="i in 5"
                      :key="i"
                      :size="14"
                      :fill="i <= review.rating ? 'currentColor' : 'none'"
                      :class="
                        i <= review.rating
                          ? 'text-warning'
                          : 'text-secondary opacity-25'
                      "
                      class="d-inline-block"
                    />
                  </div>
                </div>
                <p class="text-secondary small mb-2">{{ review.date }}</p>
                <p class="text-dark mb-3">{{ review.content }}</p>
                <div class="d-flex gap-2">
                  <button class="btn btn-light btn-sm text-secondary small">
                    도움이 돼요 {{ review.helpful }}
                  </button>
                  <button class="btn btn-light btn-sm text-secondary small">
                    댓글
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div
    v-else
    class="min-vh-100 d-flex flex-column justify-content-center align-items-center"
  >
    <div class="spinner-border text-primary mb-3" role="status"></div>
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
</style>
