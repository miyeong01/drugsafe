<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useDrugStore } from "@/stores/drug";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import {
  Search,
  Star,
  MessageCircle,
  ThumbsUp,
  TrendingUp,
  Filter,
  Plus,
  ClipboardList,
  ChevronLeft,
  ChevronRight,
} from "lucide-vue-next";

// Props 정의
const props = defineProps({
  onNavigate: {
    type: Function,
    required: true,
  },
});

const drugStore = useDrugStore();
const { reviews } = storeToRefs(drugStore);
const router = useRouter();

// 상태 관리
const searchQuery = ref("");
const sortBy = ref("latest");
const activeTab = ref("all");

// 페이지 로드 시 전체 리뷰 데이터를 가져옴.
onMounted(() => {
  // drugId 없이 호출하면 전체 리뷰를 가져오도록 스토어 액션 구성
  drugStore.getReviews();
});

// 계산된 속성: 필터링 및 정렬된 리뷰
const filteredReviews = computed(() => {
  // reviews가 null일 경우를 대비해 빈 배열로 시작합니다.
  let list = reviews.value ? [...reviews.value] : [];

  // 검색 필터링 (제목, 약품명 기준)
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    list = list.filter(
      (review) =>
        review.title?.toLowerCase().includes(query) ||
        review.drug_name?.toLowerCase().includes(query) ||
        review.content?.toLowerCase().includes(query)
    );
  }

  // 정렬 로직
  if (activeTab.value === "popular" || sortBy.value === "comments") {
    // 댓글 많은 순 정렬
    list.sort((a, b) => (b.comment_count || 0) - (a.comment_count || 0));
  } else if (sortBy.value === "latest") {
    // 최신순 정렬
    list.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }

  return list;
});

// 전체 통계 계산
const totalComments = computed(() => {
  return reviews.value
    ? reviews.value.reduce((sum, r) => sum + (r.comment_count || 0), 0)
    : 0;
});

// 리뷰 상세 페이지 이동 함수 추가
const goReviewDetail = (drugId, reviewId) => {
  router.push({
    name: "ReviewDetail", // 1. router/index.js에 설정한 이름을 확인하세요!
    params: {
      drugId: drugId,
      reviewId: reviewId,
    },
  });
};

// 페이지네이션 관련 상태 추가
const currentPage = ref(1);
const itemsPerPage = 10;

// 전체 페이지 수 계산 보완
const totalPages = computed(() => {
  const count = filteredReviews.value ? filteredReviews.value.length : 0;
  return Math.ceil(count / itemsPerPage) || 1; // 최소 1페이지 보장
});

// paginatedReviews 계산 로직 보완
const paginatedReviews = computed(() => {
  const list = filteredReviews.value || [];
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return list.slice(start, end);
});

// 검색어나 탭 변경 시 1페이지로 리셋
watch([searchQuery, sortBy, activeTab], () => {
  currentPage.value = 1;
});

// 페이지 변경 함수
const changePage = (page) => {
  currentPage.value = page;
  window.scrollTo(0, 0);
};
</script>

<template>
  <div class="community-page bg-pastel py-5 min-vh-100">
    <div class="container" style="max-width: 1000px">
      <div class="mb-5">
        <h1 class="fw-bold text-dark mb-2">커뮤니티</h1>
        <p class="text-secondary fs-5">
          다양한 의약품 사용 후기를 확인하고 공유하세요
        </p>
      </div>

      <div class="card border-0 shadow-sm p-4 mb-4 rounded-4">
        <div class="row g-3">
          <div class="col-md-8">
            <div class="search-input-group">
              <Search class="search-icon" :size="20" />
              <input
                type="text"
                class="form-control ps-5 py-3 border-0 bg-light rounded-3"
                placeholder="리뷰 검색 (제목, 내용, 약품명)"
                v-model="searchQuery"
              />
            </div>
          </div>
          <div class="col-md-4">
            <div class="d-flex align-items-center gap-2 h-100">
              <Filter class="text-secondary" :size="20" />
              <select
                class="form-select border-0 bg-light py-3 rounded-3"
                v-model="sortBy"
              >
                <option value="latest">최신순</option>
                <option value="comments">댓글순</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <ul class="nav nav-pills mb-4 gap-2">
        <li class="nav-item">
          <button
            class="nav-link rounded-pill px-4 py-2"
            :class="{ active: activeTab === 'all' }"
            @click="activeTab = 'all'"
          >
            <ClipboardList class="me-2" :size="16" />전체 리뷰
          </button>
        </li>
        <li class="nav-item">
          <button
            class="nav-link rounded-pill px-4 py-2"
            :class="{ active: activeTab === 'popular' }"
            @click="activeTab = 'popular'"
          >
            <TrendingUp class="me-2" :size="16" />인기 리뷰
          </button>
        </li>
      </ul>

      <div class="review-list d-flex flex-column gap-4 mb-5">
        <template v-if="filteredReviews.length > 0">
          <div
            v-for="review in paginatedReviews"
            :key="review.id"
            class="card border-0 shadow-sm p-4 rounded-4 review-card mb-3"
            @click="goReviewDetail(review.drug, review.id)"
          >
            <div class="d-flex align-items-center gap-2 mb-2">
              <span class="small fw-bold text-dark">
                {{ review.drug_name }}
              </span>
            </div>

            <h5 class="h6 fw-bold text-dark mb-2">
              {{ review.title || "제목 없는 리뷰" }}
            </h5>

            <p
              class="text-secondary small mb-3 text-truncate-2"
              style="white-space: pre-wrap"
            >
              {{ review.content }}
            </p>

            <div
              class="d-flex align-items-center gap-4 pt-3 border-top text-muted small"
            >
              <span class="d-flex align-items-center gap-1">
                <MessageCircle :size="14" /> 댓글
                {{ review.comment_count || 0 }}
              </span>
              <span class="ms-auto">{{ review.username }}님</span>
              <span class="vr" style="height: 12px; margin-top: 2px"></span>
              <span>{{
                new Date(review.created_at).toLocaleDateString()
              }}</span>
            </div>
          </div>
        </template>

        <div v-else class="card border-0 shadow-sm p-5 text-center rounded-4">
          <p class="text-muted mb-0">검색 결과가 없습니다.</p>
        </div>
      </div>

      <button
        class="btn btn-primary fab-button shadow-lg d-flex align-items-center gap-2 px-4 py-3 rounded-pill"
        @click="onNavigate('write-review')"
      >
        <Plus :size="24" />
        <span class="fw-bold">리뷰 작성하기</span>
      </button>
    </div>

    <nav
      v-if="totalPages > 1"
      class="custom-position-nav d-flex justify-content-center"
    >
      <div class="minimal-pagination d-flex align-items-center gap-3">
        <button
          class="btn-arrow"
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
        >
          <ChevronLeft :size="20" />
        </button>

        <div class="current-page-display shadow-sm">
          <span class="fw-bold text-primary">{{ currentPage }}</span>
          <span class="text-muted mx-1">/</span>
          <span class="text-secondary small">{{ totalPages }}</span>
        </div>

        <button
          class="btn-arrow"
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
        >
          <ChevronRight :size="20" />
        </button>
      </div>
    </nav>
  </div>
</template>

<style scoped>
/* 파스텔 배경 및 폰트 */
.bg-pastel {
  background-color: #f0f7ff;
}

/* 검색창 아이콘 배치 */
.search-input-group {
  position: relative;
}
.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #adb5bd;
}

/* 통계 카드 */
.stat-card {
  background: white;
  transition: transform 0.2s;
}
.stat-card:hover {
  transform: translateY(-5px);
}

/* 탭 버튼 스타일 (DrugSafe 테마) */
.nav-pills .nav-link {
  color: #6c757d;
  background: white;
  border: 1px solid #dee2e6;
  font-weight: 500;
}
.nav-pills .nav-link.active {
  background-color: #4d9fff;
  border-color: #4d9fff;
  color: white;
}

/* 리뷰 카드 */
.review-card {
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #e5f0ff !important;
}
.review-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08) !important;
}

.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.text-light-gray {
  color: #dee2e6;
}

.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 플로팅 버튼 (FAB) */
.fab-button {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 1000;
  background-color: #4d9fff;
  border: none;
}
.fab-button:hover {
  background-color: #3a8fef;
}

/* 별점 fill 효과 */
.fill-warning {
  fill: #ffc107;
}

/* 페이지네이션 컨테이너 (위치 조정 포함) */
.custom-position-nav {
  position: relative;
  transform: translateY(-20px); /* 목록과 적절한 간격 유지 */
  margin-bottom: 2rem;
}

.minimal-pagination {
  background-color: white;
  padding: 8px 16px;
  border-radius: 50px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5f0ff;
}

/* 화살표 버튼 */
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

/* 중앙 번호 표시 */
.current-page-display {
  background-color: #f8f9fa;
  padding: 6px 18px;
  border-radius: 20px;
  min-width: 80px;
  text-align: center;
  border: 1px solid #edf2f7;
}
</style>
