<script setup>
import { ref, computed } from 'vue';
import { 
  Search, 
  Star, 
  MessageSquare, 
  ThumbsUp, 
  TrendingUp, 
  Clock, 
  Filter,
  Plus
} from 'lucide-vue-next';

// Props 정의
const props = defineProps({
  onNavigate: {
    type: Function,
    required: true
  }
});

// 상태 관리
const searchQuery = ref('');
const sortBy = ref('latest');
const activeTab = ref('all');

// 모든 리뷰 데이터
const allReviews = [
  {
    id: '1',
    title: '타이레놀정 500mg 사용 후기',
    drugName: '타이레놀정 500mg',
    author: '김**',
    authorAvatar: '👤',
    rating: 5,
    date: '2025.01.15',
    preview: '두통에 정말 효과가 좋았어요. 평소 편두통이 심한 편인데, 이 약을 먹고 30분 정도 지나니 통증이 많이 가라앉았습니다.',
    category: '두통',
    helpful: 24,
    comments: 8,
    views: 342,
  },
  {
    id: '2',
    title: '게보린정 효과 있나요?',
    drugName: '게보린정',
    author: '이**',
    authorAvatar: '👤',
    rating: 4,
    date: '2025.01.14',
    preview: '두통에 효과는 있는데 졸음이 와서 운전 전에는 먹지 않는 게 좋을 것 같아요.',
    category: '두통',
    helpful: 18,
    comments: 5,
    views: 256,
  },
  {
    id: '3',
    title: '펜잘정 사용 후기',
    drugName: '펜잘정',
    author: '박**',
    authorAvatar: '👤',
    rating: 5,
    date: '2025.01.13',
    preview: '효과 빠르고 좋습니다. 생리통이 심할 때 먹으면 금방 나아져요.',
    category: '생리통',
    helpful: 15,
    comments: 3,
    views: 189,
  },
  {
    id: '4',
    title: '판피린티정 감기에 효과 좋아요',
    drugName: '판피린티정',
    author: '최**',
    authorAvatar: '👤',
    rating: 5,
    date: '2025.01.12',
    preview: '종합감기약으로 정말 좋습니다. 콧물, 기침, 열 모두 잡아줘요.',
    category: '종합감기',
    helpful: 32,
    comments: 12,
    views: 487,
  },
  {
    id: '5',
    title: '베아제정 소화불량에 추천',
    drugName: '베아제정',
    author: '정**',
    authorAvatar: '👤',
    rating: 4,
    date: '2025.01.11',
    preview: '과식했을 때 먹으면 속이 편해집니다. 항상 가방에 넣고 다녀요.',
    category: '소화불량',
    helpful: 21,
    comments: 6,
    views: 298,
  }
];

// 계산된 속성: 필터링 및 정렬된 리뷰
const filteredReviews = computed(() => {
  let filtered = [...allReviews];

  // 검색 필터링
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(review => 
      review.title.toLowerCase().includes(query) ||
      review.drugName.toLowerCase().includes(query) ||
      review.category.toLowerCase().includes(query)
    );
  }

  // 탭 필터링 (인기 리뷰 탭일 경우 도움순으로 고정)
  if (activeTab.value === 'popular') {
    return filtered.sort((a, b) => b.helpful - a.helpful);
  }

  // 일반 정렬
  if (sortBy.value === 'helpful') {
    filtered.sort((a, b) => b.helpful - a.helpful);
  } else if (sortBy.value === 'comments') {
    filtered.sort((a, b) => b.comments - a.comments);
  } else if (sortBy.value === 'views') {
    filtered.sort((a, b) => b.views - a.views);
  } else {
    // 최신순 (기본 데이터 순서가 최신순이라고 가정)
    filtered.sort((a, b) => new Date(b.date) - new Date(a.date));
  }

  return filtered;
});

// 전체 통계 계산
const totalComments = computed(() => allReviews.reduce((sum, r) => sum + r.comments, 0));
</script>

<template>
  <div class="community-page bg-pastel py-5 min-vh-100">
    <div class="container" style="max-width: 1000px;">
      
      <div class="mb-5">
        <h1 class="fw-bold text-dark mb-2">커뮤니티</h1>
        <p class="text-secondary fs-5">다양한 의약품 사용 후기를 확인하고 공유하세요</p>
      </div>

      <div class="card border-0 shadow-sm p-4 mb-4 rounded-4">
        <div class="row g-3">
          <div class="col-md-8">
            <div class="search-input-group">
              <Search class="search-icon" :size="20" />
              <input 
                type="text" 
                class="form-control ps-5 py-3 border-0 bg-light rounded-3" 
                placeholder="리뷰 검색 (제목, 약품명, 카테고리)"
                v-model="searchQuery"
              >
            </div>
          </div>
          <div class="col-md-4">
            <div class="d-flex align-items-center gap-2 h-100">
              <Filter class="text-secondary" :size="20" />
              <select class="form-select border-0 bg-light py-3 rounded-3" v-model="sortBy">
                <option value="latest">최신순</option>
                <option value="helpful">도움순</option>
                <option value="comments">댓글순</option>
                <option value="views">조회순</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-4 mb-5">
        <div class="col-md-4">
          <div class="stat-card p-4 rounded-4 text-center border-0 shadow-sm">
            <TrendingUp class="mb-2 text-primary" :size="32" />
            <div class="fs-2 fw-bold text-dark">{{ allReviews.length }}</div>
            <div class="text-secondary small">전체 리뷰</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="stat-card p-4 rounded-4 text-center border-0 shadow-sm">
            <Star class="mb-2 text-warning fill-warning" :size="32" />
            <div class="fs-2 fw-bold text-dark">4.6</div>
            <div class="text-secondary small">평균 평점</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="stat-card p-4 rounded-4 text-center border-0 shadow-sm">
            <MessageSquare class="mb-2 text-info" :size="32" />
            <div class="fs-2 fw-bold text-dark">{{ totalComments }}</div>
            <div class="text-secondary small">전체 댓글</div>
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
            <Clock class="me-2" :size="16" />전체 리뷰
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
            v-for="review in filteredReviews" 
            :key="review.id" 
            class="card border-0 shadow-sm p-4 rounded-4 review-card"
            @click="onNavigate('review-detail')"
          >
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div class="d-flex align-items-center gap-3">
                <div class="avatar-circle bg-primary bg-opacity-10 d-flex align-items-center justify-content-center">
                  {{ review.authorAvatar }}
                </div>
                <div>
                  <div class="d-flex align-items-center gap-2 mb-1">
                    <span class="fw-bold text-dark">{{ review.author }}</span>
                    <span class="text-muted small">· {{ review.date }}</span>
                  </div>
                  <div class="star-rating">
                    <Star 
                      v-for="i in 5" 
                      :key="i" 
                      :size="14" 
                      :class="i <= review.rating ? 'fill-warning text-warning' : 'text-light-gray'" 
                    />
                  </div>
                </div>
              </div>
              <span class="badge rounded-pill bg-light text-secondary px-3 py-2">
                {{ review.category }}
              </span>
            </div>

            <h3 class="h5 fw-bold mb-2">{{ review.title }}</h3>
            <p class="text-secondary small mb-3 text-truncate-2">{{ review.preview }}</p>

            <div class="d-flex align-items-center gap-2 mb-3">
              <span class="small text-primary">약품명:</span>
              <button 
                class="btn btn-link p-0 small fw-bold text-decoration-none"
                @click.stop="onNavigate('detail')"
              >
                {{ review.drugName }}
              </button>
            </div>

            <div class="d-flex align-items-center gap-4 pt-3 border-top text-muted small">
              <span class="d-flex align-items-center gap-1">
                <ThumbsUp :size="14" /> 도움 {{ review.helpful }}
              </span>
              <span class="d-flex align-items-center gap-1">
                <MessageSquare :size="14" /> 댓글 {{ review.comments }}
              </span>
              <span>조회 {{ review.views }}</span>
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
  </div>
</template>

<style scoped>
/* 파스텔 배경 및 폰트 */
.bg-pastel {
  background-color: #F0F7FF;
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
  background-color: #4D9FFF;
  border-color: #4D9FFF;
  color: white;
}

/* 리뷰 카드 */
.review-card {
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #E5F0FF !important;
}
.review-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
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
  background-color: #4D9FFF;
  border: none;
}
.fab-button:hover {
  background-color: #3A8FEF;
}

/* 별점 fill 효과 */
.fill-warning {
  fill: #ffc107;
}
</style>