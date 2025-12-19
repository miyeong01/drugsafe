<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  Heart,
  Pill,
  FileText,
  Settings,
  CheckCircle2,
  Circle,
  Star
} from 'lucide-vue-next'

const router = useRouter()

// 현재 활성화된 탭 ('medications', 'favorites', 'reviews')
const activeTab = ref('medications')

const times = ['아침', '점심', '저녁']

// 더미 데이터 (보내주신 내용 그대로)
const currentMedications = ref([
  {
    id: '1',
    name: '타이레놀정 500mg',
    dosage: '1일 3회',
    startDate: '2025.01.01',
    endDate: '2025.01.14',
    progress: 60,
    checklist: [true, true, false],
  },
  {
    id: '2',
    name: '비타민 D',
    dosage: '1일 1회',
    startDate: '2025.01.01',
    endDate: '2025.03.31',
    progress: 10,
    checklist: [true],
  },
  {
    id: '3',
    name: '종합비타민',
    dosage: '1일 2회',
    startDate: '2025.01.01',
    endDate: '2025.02.28',
    progress: 15,
    checklist: [true, false],
  },
])

const favorites = ref([
  {
    id: '1',
    name: '타이레놀정 500mg',
    manufacturer: '한국얀센',
    type: '해열진통제',
  },
  {
    id: '2',
    name: '게보린정',
    manufacturer: '삼진제약',
    type: '해열진통제',
  },
  {
    id: '3',
    name: '어린이부루펜시럽',
    manufacturer: '삼일제약',
    type: '해열진통제',
  },
])

const myReviews = ref([
  {
    id: '1',
    drugName: '타이레놀정 500mg',
    rating: 5,
    content: '두통에 정말 효과가 좋았어요.',
    date: '2025.01.15',
    likes: 24,
  },
  {
    id: '2',
    drugName: '게보린정',
    rating: 4,
    content: '효과는 좋은데 식후 복용 추천',
    date: '2025.01.10',
    likes: 18,
  },
])

// 페이지 이동 함수
const goProfileEdit = () => {
  router.push({ name: 'profile-edit' })
}

const goCommunity = () => {
  router.push('/community')
}
</script>

<template>
  <div class="min-vh-100 py-5 bg-light">
    <div class="container" style="max-width: 900px;">

      <div class="card shadow-sm border-0 mb-4">
        <div class="card-body p-4">
          <div class="d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center gap-4">
              <div class="bg-primary bg-opacity-10 rounded-circle d-flex align-items-center justify-content-center" style="width: 80px; height: 80px;">
                <span style="font-size: 2.5rem;">👤</span>
              </div>
              <div>
                <h2 class="h4 fw-bold mb-1 text-dark">홍길동님</h2>
                <p class="text-secondary mb-0">hong@email.com</p>
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
              <Pill class="mx-auto mb-2 text-primary" :size="32" />
              <div class="fw-medium text-dark mb-1">복용 중인 약</div>
              <p class="text-secondary mb-0">{{ currentMedications.length }}개</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm border-0 h-100 text-center py-4">
            <div class="card-body">
              <Heart class="mx-auto mb-2 text-primary" :size="32" />
              <div class="fw-medium text-dark mb-1">즐겨찾기</div>
              <p class="text-secondary mb-0">{{ favorites.length }}개</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm border-0 h-100 text-center py-4">
            <div class="card-body">
              <FileText class="mx-auto mb-2 text-primary" :size="32" />
              <div class="fw-medium text-dark mb-1">작성한 리뷰</div>
              <p class="text-secondary mb-0">{{ myReviews.length }}개</p>
            </div>
          </div>
        </div>
      </div>

      <ul class="nav nav-pills nav-fill mb-4 bg-white p-1 rounded shadow-sm">
        <li class="nav-item">
          <button 
            class="nav-link fw-bold" 
            :class="{ active: activeTab === 'medications' }"
            @click="activeTab = 'medications'"
          >
            복용 중인 약
          </button>
        </li>
        <li class="nav-item">
          <button 
            class="nav-link fw-bold" 
            :class="{ active: activeTab === 'favorites' }"
            @click="activeTab = 'favorites'"
          >
            즐겨찾기
          </button>
        </li>
        <li class="nav-item">
          <button 
            class="nav-link fw-bold" 
            :class="{ active: activeTab === 'reviews' }"
            @click="activeTab = 'reviews'"
          >
            내 리뷰
          </button>
        </li>
      </ul>

      <div v-if="activeTab === 'medications'">
        <div class="d-flex flex-column gap-3">
          <div v-for="med in currentMedications" :key="med.id" class="card shadow-sm border-0">
            <div class="card-body p-4">
              
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h3 class="h5 fw-bold mb-1">{{ med.name }}</h3>
                  <p class="text-secondary small mb-0">
                    {{ med.dosage }} · {{ med.startDate }} ~ {{ med.endDate }}
                  </p>
                </div>
                <button class="btn btn-outline-secondary btn-sm">상세보기</button>
              </div>

              <div class="mb-4">
                <div class="d-flex justify-content-between mb-1">
                  <span class="small fw-medium">복용 진행률</span>
                  <span class="small fw-bold text-primary">{{ med.progress }}%</span>
                </div>
                <div class="progress" style="height: 8px;">
                  <div 
                    class="progress-bar bg-primary" 
                    role="progressbar" 
                    :style="{ width: med.progress + '%' }" 
                    :aria-valuenow="med.progress" 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                  ></div>
                </div>
              </div>

              <div>
                <p class="small text-secondary mb-2">오늘의 복용</p>
                <div class="d-flex gap-2">
                  <button 
                    v-for="(checked, index) in med.checklist" 
                    :key="index"
                    class="btn btn-sm d-flex align-items-center gap-2 border"
                    :class="checked ? 'btn-light text-primary border-primary bg-primary bg-opacity-10' : 'btn-light text-secondary'"
                  >
                    <CheckCircle2 v-if="checked" :size="16" />
                    <Circle v-else :size="16" />
                    <span class="small">{{ times[index] }}</span>
                  </button>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'favorites'">
        <div class="row g-3">
          <div class="col-md-6" v-for="fav in favorites" :key="fav.id">
            <div class="card shadow-sm border-0 h-100 hover-shadow cursor-pointer">
              <div class="card-body p-3 d-flex gap-3 align-items-center">
                
                <div class="bg-light rounded d-flex align-items-center justify-content-center flex-shrink-0" style="width: 60px; height: 60px;">
                  <span class="fs-4">💊</span>
                </div>

                <div class="flex-grow-1">
                  <h4 class="h6 fw-bold mb-1">{{ fav.name }}</h4>
                  <p class="text-secondary small mb-1">{{ fav.manufacturer }}</p>
                  <span class="badge bg-secondary bg-opacity-10 text-secondary fw-normal">{{ fav.type }}</span>
                </div>

                <button class="btn btn-link p-0 text-danger">
                  <Heart :size="20" fill="currentColor" />
                </button>

              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'reviews'">
        <div class="d-flex flex-column gap-3">
          <div v-for="review in myReviews" :key="review.id" class="card shadow-sm border-0">
            <div class="card-body p-4">
              
              <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                  <h4 class="h6 fw-bold mb-1">{{ review.drugName }}</h4>
                  <div class="d-flex align-items-center gap-2">
                    <div class="d-flex text-warning">
                      <Star 
                        v-for="i in 5" 
                        :key="i" 
                        :size="14" 
                        :fill="i <= review.rating ? 'currentColor' : 'none'"
                        :class="i <= review.rating ? 'text-warning' : 'text-secondary opacity-25'"
                      />
                    </div>
                    <span class="text-secondary small">{{ review.date }}</span>
                  </div>
                </div>
                <button class="btn btn-outline-secondary btn-sm" @click="goCommunity">수정</button>
              </div>

              <p class="text-dark mb-2">{{ review.content }}</p>
              <p class="text-secondary small mb-0">도움이 돼요 {{ review.likes }}</p>

            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* 탭 활성화 스타일 (부트스트랩 오버라이드) */
.nav-pills .nav-link.active {
  background-color: #f8f9fa; /* bg-light */
  color: #0d6efd; /* Primary Color */
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  font-weight: bold;
}
.nav-pills .nav-link {
  color: #6c757d; /* Secondary Color */
}

/* 호버 시 그림자 효과 */
.hover-shadow:hover {
  transform: translateY(-2px);
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15)!important;
  transition: all 0.2s ease;
}
.cursor-pointer {
  cursor: pointer;
}
</style>