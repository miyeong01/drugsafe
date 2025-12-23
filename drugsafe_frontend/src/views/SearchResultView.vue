<script setup>
import { ref, reactive, onMounted, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Search, SlidersHorizontal, Star, Heart, Pill, Droplet, SprayCan, Bandage } from "lucide-vue-next";
import { useDrugStore } from "@/stores/drug";
import film from "@/assets/icons/film.svg?component";
import lotion from "@/assets/icons/lotion.svg?component";
import cream from "@/assets/icons/cream.svg?component";
import ointment from "@/assets/icons/ointment.svg?component";
import powder from "@/assets/icons/powder.svg?component";

const router = useRouter();
const route = useRoute();
const drugStore = useDrugStore();

// URL의 쿼리(?q=...)를 가져와서 검색어 초기화
const keyword = ref(route.query.q || "");

// 필터와 정렬이 적용된 가공된 데이터 리스트
const filteredDrugs = computed(() => {
  let list = [...drugStore.drugs]; // 원본 데이터 복사

  // 1. 제형 필터링 로직
  // 체크된 필터 키들만 추출 (예: ['tablet', 'syrup'])
  const activeFilterKeys = Object.keys(filters).filter((key) => filters[key]);

  if (activeFilterKeys.length > 0) {
    list = list.filter((drug) => {
      // 데이터의 form_name(예: '알약')이 선택된 필터의 한글 라벨과 일치하는지 확인
      return activeFilterKeys.some((key) => drug.form_name === formLabels[key]);
    });
  }

  // 2. 정렬 로직
  if (sortBy.value === "rating") {
    list.sort((a, b) => (b.rating || 0) - (a.rating || 0));
  } else if (sortBy.value === "reviews") {
    list.sort((a, b) => (b.review_count || 0) - (a.review_count || 0));
  }
  // 'relevance'(관련도순)는 기본 서버 응답 순서를 유지합니다.

  return list;
});

// 데이터 불러오기 함수
const fetchDrugs = () => {
  const queryKeyword = route.query.q || "";
  const querySymptomId = route.query.symptom || null; // URL에서 ID 꺼내기

  console.log(
    "데이터 요청 시도 - 검색어:",
    queryKeyword,
    "증상ID:",
    querySymptomId
  );

  if (querySymptomId) {
    drugStore.getDrugs("", querySymptomId);
  } else {
    drugStore.getDrugs(queryKeyword, null);
  }
};

watch(
  () => [route.query.q, route.query.symptom],
  () => {
    fetchDrugs();
  }
);

onMounted(() => {
  fetchDrugs(); // 초기 로드 시 실행
});

// [수정] 중복된 watch를 하나로 통합했습니다.
watch(
  () => route.query.q,
  (newVal) => {
    keyword.value = newVal || "";
    fetchDrugs();
  }
);

const sortBy = ref("relevance");

// 필터 상태
const filters = reactive({
  powder: false,
  lotion: false,
  cream: false,
  tablet: false,
  syrup: false,
  liquid: false,
  spray: false,
  patch: false,
  ointment: false,
  film: false,
});

const formLabels = {
  powder: "가루",
  lotion: "로션",
  cream: "크림",
  tablet: "알약",
  syrup: "시럽",
  liquid: "액상",
  spray: "스프레이",
  patch: "부착형",
  ointment: "연고",
  film: "필름",
};

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
}
</script>

<template>
  <div class="min-vh-100 bg-light py-5">
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
          <span class="fw-bold text-dark">{{ filteredDrugs.length }}</span
          >건
        </p>
      </div>

      <div class="row g-4">
        <aside class="col-lg-3 d-none d-lg-block">
          <div class="card shadow-sm border-0 sticky-top" style="top: 20px">
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
              >총 {{ filteredDrugs.length }}개의 의약품</span
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
                    <!-- 이미지 있을 때 -->
                    <div v-if="drug.image_url">
                      <img
                        :src="drug.image_url"
                        alt="의약품 이미지"
                        style="width: 100%; height: 100%; object-fit: contain"
                      />
                    </div>

                    <!-- 이미지 없을 때 -->
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
  </div>
</template>

<style scoped>
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

/* 즐겨찾기 버튼 (크기와 위치를 강력하게 고정) */
.fav-btn {
  width: 105px !important;
  /* 너비를 명확하게 고정 */
  height: 34px !important;
  /* 높이 고정 */
  flex-shrink: 0 !important;
  /* 중요: 제목이 길어져도 버튼이 절대 찌그러지지 않음 */
  display: flex;
  /* 내부 아이콘과 텍스트 정렬을 위해 추가 */
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  white-space: nowrap;
  /* 버튼 안의 글자는 줄바꿈 방지 */
  margin-top: 2px;
  /* 제목 첫 줄과 높이를 맞춤 */
}

/* 약 이름 전용 스타일 (줄바꿈 허용) */
.drug-name {
  white-space: normal !important;
  /* 줄바꿈 허용 */
  word-break: keep-all;
  /* 한글 단어가 어색하게 잘리지 않게 함 */
  line-height: 1.4;
  display: block;
  /* 영역을 확실히 차지하게 함 */
}

/* 제조사 이름 등을 위한 기존 말줄임표 스타일 */
.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.drug-icon {
  width: 24px;
  height: 24px;
}
</style>
