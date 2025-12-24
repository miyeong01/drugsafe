<script setup>
import { ref, reactive, onMounted, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  Search,
  SlidersHorizontal,
  Star,
  Heart,
  Pill,
  Droplet,
  SprayCan,
  Bandage,
  ChevronLeft,
  ChevronRight,
} from "lucide-vue-next";
import { useDrugStore } from "@/stores/drug";
import film from "@/assets/icons/film.svg?component";
import lotion from "@/assets/icons/lotion.svg?component";
import cream from "@/assets/icons/cream.svg?component";
import ointment from "@/assets/icons/ointment.svg?component";
import powder from "@/assets/icons/powder.svg?component";

const router = useRouter();
const route = useRoute();
const drugStore = useDrugStore();
const currentPage = ref(1);

const keyword = ref(route.query.q || "");
const sortBy = ref("relevance");

// 필터 상태 (form_name → form_id로 매핑)
const filters = reactive({
  tablet: false,    // 1
  powder: false,    // 2
  liquid: false,    // 3
  syrup: false,     // 4
  spray: false,     // 5
  film: false,      // 6
  cream: false,     // 7
  ointment: false,  // 8
  patch: false,     // 9
  lotion: false,    // 10
});

const formLabels = {
  tablet: "알약",
  powder: "가루",
  liquid: "액상",
  syrup: "시럽",
  spray: "스프레이",
  film: "필름",
  cream: "크림",
  ointment: "연고",
  patch: "부착형",
  lotion: "로션",
};

// form_name → form_id 매핑
const formIdMap = {
  tablet: 1,
  powder: 2,
  liquid: 3,
  syrup: 4,
  spray: 5,
  film: 6,
  cream: 7,
  ointment: 8,
  patch: 9,
  lotion: 10,
};

// ✅ 백엔드에서 필터링/정렬된 데이터를 그대로 사용
const filteredDrugs = computed(() => drugStore.drugs || []);

const totalPages = computed(() => {
  return Math.ceil(drugStore.totalCount / 10) || 1;
});

// 선택된 제형 ID 배열 계산
const selectedFormIds = computed(() => {
  return Object.keys(filters)
    .filter(key => filters[key])
    .map(key => formIdMap[key]);
});

// 데이터 불러오기 함수
const fetchDrugs = (page = 1) => {
  currentPage.value = page;
  
  const filterParams = {
    sort: sortBy.value,
    forms: selectedFormIds.value
  };
  
  const queryKeyword = route.query.q || "";
  const querySymptomId = route.query.symptom || null;
  
  drugStore.getDrugs(queryKeyword, querySymptomId, page, filterParams);
};

onMounted(() => {
  fetchDrugs();
});

// URL 쿼리 변경 감지
watch(
  () => [route.query.q, route.query.symptom],
  () => {
    keyword.value = route.query.q || "";
    fetchDrugs(1);
  }
);

// 필터/정렬 변경 시 1페이지부터 다시 조회
watch(
  [filters, sortBy],
  () => {
    fetchDrugs(1);
  },
  { deep: true }
);

// 필터 초기화
function resetFilters() {
  Object.keys(filters).forEach((key) => {
    filters[key] = false;
  });
}

// 상세 페이지 이동
function goDetail(drugId) {
  router.push({ name: "drug-detail", params: { drugId: drugId } });
}

// 검색 실행
function handleSearch() {
  router.push({ query: { q: keyword.value } });
}

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
};

// 페이지 변경
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return;
  fetchDrugs(page);
  window.scrollTo(0, 0);
};
</script>

<template>
  <div class="min-vh-100 py-5 bg-light">
    <div class="container">
      <div class="mb-5">
        <div class="d-flex gap-2 mb-3">
          <div class="input-group input-group-lg shadow-sm">
            <span class="input-group-text bg-white border-end-0 text-secondary">
              <Search :size="20" />
            </span>
            <input
              type="text"
              class="form-control border-start-0"
              placeholder="증상이나 약품명을 검색하세요..."
              v-model="keyword"
              @keydown.enter="handleSearch"
            />
            <button class="btn btn-primary px-4 fw-bold" @click="handleSearch">
              검색
            </button>
          </div>
        </div>

        <p class="text-secondary">
          <span class="text-primary fw-bold">'{{ keyword || "전체" }}'</span>
          에 대한 검색 결과
          <span class="fw-bold text-dark">{{ drugStore.totalCount }}</span>건
        </p>
      </div>

      <div class="row g-4">
        <aside class="col-lg-3 d-none d-lg-block">
          <div class="card shadow-sm border-0 sticky-top" style="top: 90px">
            <div class="card-body p-4">
              <div class="d-flex align-items-center gap-2 mb-4">
                <SlidersHorizontal :size="20" />
                <h3 class="h6 fw-bold mb-0">상세 필터</h3>
              </div>

              <div class="mb-4">
                <h4 class="small fw-bold text-secondary mb-3">제형</h4>
                <div class="d-flex flex-column gap-2">
                  <div
                    v-for="(label, key) in formLabels"
                    :key="key"
                    class="form-check"
                  >
                    <input
                      class="form-check-input"
                      type="checkbox"
                      :id="key"
                      v-model="filters[key]"
                    />
                    <label
                      class="form-check-label small"
                      :for="key"
                      style="cursor: pointer"
                    >
                      {{ label }}
                    </label>
                  </div>
                </div>
              </div>

              <button
                class="btn btn-outline-secondary w-100 btn-sm"
                @click="resetFilters"
              >
                필터 초기화
              </button>
            </div>
          </div>
        </aside>

        <div class="col-lg-9">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <span class="small text-secondary"
              >총 {{ drugStore.totalCount }}개의 의약품</span
            >

            <select
              class="form-select form-select-sm w-auto border-0 shadow-sm"
              v-model="sortBy"
            >
              <option value="relevance">관련도순</option>
              <option value="rating">평점 높은순</option>
              <option value="reviews">리뷰 많은순</option>
            </select>
          </div>

          <div class="d-flex flex-column gap-3">
            <div
              v-for="drug in filteredDrugs"
              :key="drug.id"
              class="card border-0 shadow-sm hover-shadow cursor-pointer"
              @click="goDetail(drug.id)"
            >
              <div class="card-body p-4">
                <div class="d-flex gap-4 align-items-center">
                  <div
                    class="bg-light rounded d-flex align-items-center justify-content-center flex-shrink-0 overflow-hidden"
                    style="width: 80px; height: 80px"
                  >
                    <div v-if="drug.image_url">
                      <img
                        :src="drug.image_url"
                        alt="의약품 이미지"
                        style="width: 100%; height: 100%; object-fit: contain"
                      />
                    </div>

                    <div v-else class="bg-white rounded-circle p-2 shadow-sm">
                      <component
                        :is="getFormIcon(drug.form)"
                        class="text-primary drug-icon"
                      />
                    </div>
                  </div>

                  <div class="flex-grow-1">
                    <div
                      class="d-flex justify-content-between align-items-start mb-1"
                    >
                      <div class="flex-grow-1 me-3">
                        <h3 class="h5 fw-bold mb-1 drug-name">
                          {{ drug.name }}
                        </h3>
                        <p class="small text-secondary mb-2">
                          {{ drug.company }}
                        </p>
                      </div>

                      <button
                        class="btn btn-sm rounded-pill d-none d-sm-flex align-items-center justify-content-center fav-btn"
                        :class="
                          drug.is_favorite
                            ? 'btn-danger text-white border-danger'
                            : 'btn-outline-secondary'
                        "
                        @click.stop="drugStore.toggleFavorite(drug.id)"
                      >
                        <Heart
                          :size="14"
                          class="me-1"
                          :fill="drug.is_favorite ? 'currentColor' : 'none'"
                        />
                        <span>즐겨찾기</span>
                      </button>
                    </div>

                    <div class="d-flex align-items-center gap-3">
                      <div class="d-flex align-items-center">
                        <div class="d-flex gap-1 text-warning me-2">
                          <Star
                            v-for="n in 5"
                            :key="n"
                            :size="16"
                            :fill="
                              n <= Math.round(drug.rating || 0)
                                ? 'currentColor'
                                : 'none'
                            "
                            :class="
                              n <= Math.round(drug.rating || 0)
                                ? 'text-warning'
                                : 'text-secondary opacity-25'
                            "
                          />
                        </div>
                        <span class="fw-bold text-dark small">
                          {{
                            drug.rating ? Number(drug.rating).toFixed(1) : "0.0"
                          }}
                        </span>
                      </div>

                      <span class="small text-secondary border-start ps-3">
                        리뷰 {{ (drug.review_count || 0).toLocaleString() }}
                      </span>
                      <span
                        class="badge bg-secondary bg-opacity-10 text-secondary fw-normal"
                      >
                        {{ drug.form_name }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div
              v-if="filteredDrugs.length === 0"
              class="text-center py-5 text-secondary"
            >
              검색 결과가 없습니다.
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <nav
      v-if="totalPages > 1"
      class="custom-position-nav mt-5 d-flex justify-content-center"
    >
      <div class="minimal-pagination d-flex align-items-center gap-3">
        <button
          class="btn-arrow"
          :disabled="!drugStore.prevPage"
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
          :disabled="!drugStore.nextPage"
          @click="changePage(currentPage + 1)"
        >
          <ChevronRight :size="20" />
        </button>
      </div>
    </nav>
  </div>
</template>

<style scoped>
/* 기존 스타일 유지 */
.hover-shadow:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
  transition: all 0.2s ease;
}

.cursor-pointer {
  cursor: pointer;
}

.form-check-input {
  cursor: pointer;
}

.fav-btn {
  width: 105px !important;
  height: 34px !important;
  flex-shrink: 0 !important;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  white-space: nowrap;
  margin-top: 2px;
}

.drug-name {
  white-space: normal !important;
  word-break: keep-all;
  line-height: 1.4;
  display: block;
}

.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.drug-icon {
  width: 24px;
  height: 24px;
}

.minimal-pagination {
  background-color: white;
  padding: 8px 16px;
  border-radius: 50px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
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

.current-page-display span {
  font-size: 1rem;
}

.custom-position-nav {
  position: relative;
  transform: translateY(-20px);
  z-index: 10;
  margin-bottom: -40px;
}
</style>