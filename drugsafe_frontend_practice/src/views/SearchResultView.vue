<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search, SlidersHorizontal, Star, Heart, Pill } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()

// URL의 쿼리(?q=...)를 가져와서 검색어 초기화
const keyword = ref(route.query.q || '')

// 검색어가 URL에서 바뀌면 같이 업데이트
watch(() => route.query.q, (newVal) => {
  keyword.value = newVal || ''
})

const sortBy = ref('relevance')

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
})

const formLabels = {
  powder: '가루',
  lotion: '로션',
  cream: '크림',
  tablet: '알약',
  syrup: '시럽',
  liquid: '액상',
  spray: '스프레이',
  patch: '부착형',
  ointment: '연고',
  film: '필름',
}

// 더미 데이터
const mockDrugs = ref([
  {
    id: '1',
    name: '타이레놀정 500mg',
    manufacturer: '한국얀센',
    type: '해열진통제',
    form: '정제',
    rating: 4.5,
    reviewCount: 1234,
  },
  {
    id: '2',
    name: '게보린정',
    manufacturer: '삼진제약',
    type: '해열진통제',
    form: '정제',
    rating: 4.3,
    reviewCount: 892,
  },
  {
    id: '3',
    name: '어린이부루펜시럽',
    manufacturer: '삼일제약',
    type: '해열진통제',
    form: '시럽',
    rating: 4.7,
    reviewCount: 567,
  },
])

// 필터 초기화
function resetFilters() {
  Object.keys(filters).forEach(key => {
    filters[key] = false
  })
}

// 상세 페이지 이동
function goDetail(id) {
  router.push({ name: 'drug-detail', params: { id: id } })
}

// 검색 실행
function handleSearch() {
  router.push({ query: { q: keyword.value } })
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
            >
            <button class="btn btn-primary px-4 fw-bold" @click="handleSearch">검색</button>
          </div>
        </div>

        <p class="text-secondary">
          <span class="text-primary fw-bold">'{{ keyword || "전체" }}'</span>
          에 대한 검색 결과 <span class="fw-bold text-dark">{{ mockDrugs.length }}</span>건
        </p>
      </div>

      <div class="row g-4">
        
        <aside class="col-lg-3 d-none d-lg-block">
          <div class="card shadow-sm border-0 sticky-top" style="top: 20px;">
            <div class="card-body p-4">
              <div class="d-flex align-items-center gap-2 mb-4">
                <SlidersHorizontal :size="20" />
                <h3 class="h6 fw-bold mb-0">상세 필터</h3>
              </div>

              <div class="mb-4">
                <h4 class="small fw-bold text-secondary mb-3">제형</h4>
                <div class="d-flex flex-column gap-2">
                  <div v-for="(label, key) in formLabels" :key="key" class="form-check">
                    <input 
                      class="form-check-input" 
                      type="checkbox" 
                      :id="key" 
                      v-model="filters[key]"
                    >
                    <label class="form-check-label small" :for="key" style="cursor: pointer;">
                      {{ label }}
                    </label>
                  </div>
                </div>
              </div>

              <button class="btn btn-outline-secondary w-100 btn-sm" @click="resetFilters">
                필터 초기화
              </button>
            </div>
          </div>
        </aside>

        <div class="col-lg-9">

          <div class="d-flex justify-content-between align-items-center mb-3">
            <span class="small text-secondary">총 {{ mockDrugs.length }}개의 의약품</span>
            
            <select class="form-select form-select-sm w-auto border-0 shadow-sm" v-model="sortBy">
              <option value="relevance">관련도순</option>
              <option value="rating">평점 높은순</option>
              <option value="reviews">리뷰 많은순</option>
            </select>
          </div>

          <div class="d-flex flex-column gap-3">
            <div 
              v-for="drug in mockDrugs" 
              :key="drug.id" 
              class="card border-0 shadow-sm hover-shadow cursor-pointer"
              @click="goDetail(drug.id)"
            >
              <div class="card-body p-4">
                <div class="d-flex gap-4 align-items-center">
                  
                  <div class="bg-light rounded d-flex align-items-center justify-content-center flex-shrink-0" style="width: 80px; height: 80px;">
                    <div class="bg-white rounded-circle p-2 shadow-sm">
                      <Pill class="text-primary" :size="24" />
                    </div>
                  </div>

                  <div class="flex-grow-1">
                    <div class="d-flex justify-content-between align-items-start mb-1">
                      <div>
                        <h3 class="h5 fw-bold mb-1">{{ drug.name }}</h3>
                        <p class="small text-secondary mb-2">{{ drug.manufacturer }} · {{ drug.type }}</p>
                      </div>
                      <button class="btn btn-outline-secondary btn-sm rounded-pill px-3 d-none d-sm-block" @click.stop>
                        <Heart :size="14" class="me-1" /> 즐겨찾기
                      </button>
                    </div>

                    <div class="d-flex align-items-center gap-3">
                      <div class="d-flex align-items-center gap-1 text-warning">
                        <Star :size="16" fill="currentColor" />
                        <span class="fw-bold text-dark">{{ drug.rating }}</span>
                      </div>
                      <span class="small text-secondary border-start ps-3">
                        리뷰 {{ drug.reviewCount.toLocaleString() }}
                      </span>
                      <span class="badge bg-secondary bg-opacity-10 text-secondary fw-normal">
                        {{ drug.form }}
                      </span>
                    </div>
                  </div>

                </div>
              </div>
            </div>
          </div>

        </div> </div> </div>
  </div>
</template>

<style scoped>
/* 카드 호버 효과 */
.hover-shadow:hover {
  transform: translateY(-3px);
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.1)!important;
  transition: all 0.2s ease;
}

.cursor-pointer {
  cursor: pointer;
}

/* 체크박스 커서 */
.form-check-input {
  cursor: pointer;
}
</style>