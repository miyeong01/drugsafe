<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  Star,
  Heart,
  Share2,
  MessageSquare,
  Pill,
  ArrowLeft
} from 'lucide-vue-next'

const router = useRouter()

// 현재 탭 상태
const activeTab = ref('info')

// 뒤로가기
const goBack = () => {
  router.back()
}

// 더미 데이터
const drug = ref({
  name: '타이레놀정 500mg',
  manufacturer: '한국얀센',
  category: '해열진통제',
  rating: 4.5,
  reviewCount: 1234
})

const mockReviews = ref([
  {
    id: '1',
    author: '김**',
    rating: 5,
    date: '2025.01.15',
    content: '두통에 정말 효과가 좋았어요. 속쓰림도 없고 깔끔합니다.',
    helpful: 24,
  },
  {
    id: '2',
    author: '이**',
    rating: 4,
    date: '2025.01.10',
    content: '효과는 좋은데 식후 복용 추천합니다. 빈속에는 조금 부담될 수 있어요.',
    helpful: 18,
  },
])

// 리뷰 작성하러 커뮤니티로 이동
const goCommunityWrite = () => {
  router.push('/community') // 나중에 글쓰기 페이지로 연결
  alert('리뷰 작성 페이지로 이동합니다.')
}
</script>

<template>
  <div class="min-vh-100 bg-light py-5">
    <div class="container" style="max-width: 900px;">
      
      <button class="btn btn-light shadow-sm rounded-circle p-2 mb-4" @click="goBack">
        <ArrowLeft :size="20" class="text-secondary" />
      </button>

      <div class="row g-4 mb-5">
        
        <div class="col-md-5">
          <div class="card border-0 shadow-sm h-100 d-flex align-items-center justify-content-center py-5">
            <div class="bg-light rounded-circle p-4 d-flex align-items-center justify-content-center" style="width: 150px; height: 150px;">
              <span style="font-size: 4rem;">💊</span>
            </div>
          </div>
        </div>

        <div class="col-md-7">
          <div class="h-100 d-flex flex-column justify-content-center">
            
            <div class="mb-2">
              <span class="badge bg-secondary bg-opacity-10 text-secondary rounded-pill fw-normal px-3 py-2">
                {{ drug.category }}
              </span>
            </div>

            <h1 class="fw-bold mb-1 display-6">{{ drug.name }}</h1>
            <p class="text-secondary mb-3 fs-5">{{ drug.manufacturer }}</p>

            <div class="d-flex align-items-center gap-3 mb-4">
              <div class="d-flex text-warning">
                <Star 
                  v-for="i in 5" 
                  :key="i" 
                  :size="20" 
                  :fill="i <= Math.round(drug.rating) ? 'currentColor' : 'none'"
                  :class="i <= Math.round(drug.rating) ? 'text-warning' : 'text-secondary opacity-25'"
                />
              </div>
              <span class="fw-bold fs-5">{{ drug.rating }}</span>
              <span class="text-secondary small">({{ drug.reviewCount.toLocaleString() }}개의 리뷰)</span>
            </div>

            <div class="d-flex gap-2 mb-4">
              <button class="btn btn-outline-danger d-flex align-items-center gap-2 px-3">
                <Heart :size="18" /> 찜하기
              </button>
              <button class="btn btn-outline-secondary d-flex align-items-center gap-2 px-3">
                <Share2 :size="18" /> 공유
              </button>
            </div>

            <div class="card bg-light border-0 p-3">
              <div class="row g-2 small">
                <div class="col-6"><span class="fw-bold text-secondary">제형:</span> 정제</div>
                <div class="col-6"><span class="fw-bold text-secondary">용량:</span> 500mg</div>
                <div class="col-6"><span class="fw-bold text-secondary">포장단위:</span> 20정</div>
                <div class="col-6"><span class="fw-bold text-secondary">보관방법:</span> 실온보관</div>
              </div>
            </div>

          </div>
        </div>
      </div>

      <ul class="nav nav-pills nav-fill mb-4 bg-white p-1 rounded shadow-sm">
        <li class="nav-item">
          <button class="nav-link fw-bold" :class="{ active: activeTab === 'info' }" @click="activeTab = 'info'">상세정보</button>
        </li>
        <li class="nav-item">
          <button class="nav-link fw-bold" :class="{ active: activeTab === 'usage' }" @click="activeTab = 'usage'">용법·용량</button>
        </li>
        <li class="nav-item">
          <button class="nav-link fw-bold" :class="{ active: activeTab === 'warnings' }" @click="activeTab = 'warnings'">주의사항</button>
        </li>
        <li class="nav-item">
          <button class="nav-link fw-bold" :class="{ active: activeTab === 'reviews' }" @click="activeTab = 'reviews'">리뷰</button>
        </li>
      </ul>

      <div class="card shadow-sm border-0 mb-5">
        <div class="card-body p-4 p-md-5">
          
          <div v-if="activeTab === 'info'">
            <h3 class="h5 fw-bold mb-3">효능 · 효과</h3>
            <p class="text-secondary lh-lg mb-0">
              1. 감기로 인한 발열 및 통증, 두통, 신경통, 근육통, 월경통, 염좌통(삔 통증)<br>
              2. 치통, 관절통, 류마티스성 통증
            </p>
          </div>

          <div v-if="activeTab === 'usage'">
            <h3 class="h5 fw-bold mb-3">용법 · 용량</h3>
            <div class="alert alert-primary bg-opacity-10 border-0 text-primary mb-3">
              <p class="mb-0 fw-bold">⚠️ 만 12세 이상 소아 및 성인</p>
            </div>
            <p class="text-secondary lh-lg mb-0">
              1회 1~2정씩 1일 3-4회 (4-6시간 마다) 필요시 복용합니다.<br>
              하루 최대 8정(4,000mg)을 초과하여 복용하지 마십시오.
            </p>
          </div>

          <div v-if="activeTab === 'warnings'">
            <h3 class="h5 fw-bold text-danger mb-3">사용상의 주의사항</h3>
            <ul class="text-secondary lh-lg ps-3 mb-0">
              <li>매일 세잔 이상 정기적으로 술을 마시는 사람이 이 약이나 다른 해열진통제를 복용해야 할 경우 반드시 의사 또는 약사와 상의하십시오. 간손상이 유발될 수 있습니다.</li>
              <li>이 약에 과민증 환자는 투여하지 마십시오.</li>
              <li>소화성궤양 환자는 투여하지 마십시오.</li>
            </ul>
          </div>

          <div v-if="activeTab === 'reviews'">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <h3 class="h5 fw-bold mb-0">사용자 리뷰</h3>
              <button class="btn btn-primary btn-sm d-flex align-items-center gap-2" @click="goCommunityWrite">
                <MessageSquare :size="16" /> 리뷰 작성
              </button>
            </div>

            <div class="d-flex flex-column gap-3">
              <div v-for="review in mockReviews" :key="review.id" class="border rounded p-3">
                <div class="d-flex justify-content-between mb-2">
                  <span class="fw-bold">{{ review.author }}</span>
                  <div class="text-warning small">
                    <Star 
                      v-for="i in 5" 
                      :key="i" 
                      :size="14" 
                      :fill="i <= review.rating ? 'currentColor' : 'none'"
                      :class="i <= review.rating ? 'text-warning' : 'text-secondary opacity-25'"
                      class="d-inline-block"
                    />
                  </div>
                </div>
                <p class="text-secondary small mb-2">{{ review.date }}</p>
                <p class="text-dark mb-3">{{ review.content }}</p>
                <div class="d-flex gap-2">
                  <button class="btn btn-light btn-sm text-secondary small">도움이 돼요 {{ review.helpful }}</button>
                  <button class="btn btn-light btn-sm text-secondary small">댓글</button>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* 탭 활성화 스타일 */
.nav-pills .nav-link.active {
  background-color: #f8f9fa;
  color: #0d6efd;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.nav-pills .nav-link {
  color: #6c757d;
}
</style>