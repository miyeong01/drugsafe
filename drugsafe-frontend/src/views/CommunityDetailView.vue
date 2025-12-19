<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowLeft,
  ThumbsUp,
  Share2,
  MoreVertical,
  User,
  Star
} from 'lucide-vue-next'

const router = useRouter()

// 댓글 입력 데이터
const newComment = ref('')

// 목록으로 돌아가기
const goList = () => {
  router.push('/community')
}

// 상세 페이지 이동 (관련 리뷰 클릭 시)
const goDetail = (id) => {
  // 실제로는 router.push(`/community/${id}`) 처럼 이동
  console.log(id + '번 글로 이동')
  window.scrollTo(0, 0) // 화면 맨 위로
}

// --- 더미 데이터 (보내주신 내용 그대로) ---
const review = ref({
  id: '1',
  author: '김**',
  authorAvatar: '👤',
  rating: 5,
  date: '2025.01.15',
  title: '타이레놀정 500mg 사용 후기',
  drugName: '타이레놀정 500mg',
  content: `두통에 정말 효과가 좋았어요. 평소 편두통이 심한 편인데, 이 약을 먹고 30분 정도 지나니 통증이 많이 가라앉았습니다.

특히 속이 편한 것도 장점인 것 같아요. 다른 진통제는 속이 쓰린 경우가 있었는데, 타이레놀은 공복에 먹어도 괜찮더라고요.

집에 항상 구비해두고 있습니다. 두통뿐만 아니라 생리통이나 치통에도 효과가 있어서 만능으로 쓰고 있어요.

다만 효과가 너무 좋아서 자주 먹게 되는데, 간에 무리가 갈 수 있다고 해서 용량과 횟수를 잘 지키려고 노력하고 있습니다.`,
  helpful: 24,
  views: 342,
})

const comments = ref([
  {
    id: '1',
    author: '이**',
    date: '2025.01.16',
    content: '저도 타이레놀 애용자예요! 정말 효과 좋죠. 공감합니다.',
    likes: 5,
  },
  {
    id: '2',
    author: '박**',
    date: '2025.01.16',
    content: '간 건강이 걱정되시면 밀크시슬 같은 영양제를 함께 드시는 것도 좋을 것 같아요.',
    likes: 3,
  },
  {
    id: '3',
    author: '최**',
    date: '2025.01.17',
    content: '좋은 후기 감사합니다. 저도 한번 사용해봐야겠어요!',
    likes: 2,
  },
])

const relatedReviews = ref([
  {
    id: '2',
    title: '게보린정 효과 있나요?',
    author: '이**',
    rating: 4,
    date: '2025.01.14',
    preview: '두통에 효과는 있는데 졸음이 와서...',
  },
  {
    id: '3',
    title: '펜잘정 사용 후기',
    author: '박**',
    rating: 5,
    date: '2025.01.13',
    preview: '효과 빠르고 좋습니다',
  },
])

// 댓글 작성 핸들러
function handleSubmitComment() {
  if (!newComment.value.trim()) return
  
  // 댓글 목록에 추가 (프론트엔드에서만)
  comments.value.push({
    id: Date.now().toString(),
    author: '나(User)',
    date: new Date().toLocaleDateString(),
    content: newComment.value,
    likes: 0
  })
  
  alert('댓글이 등록되었습니다!')
  newComment.value = ''
}
</script>

<template>
  <div class="min-vh-100 bg-light py-5">
    <div class="container" style="max-width: 900px;">

      <button 
        class="btn btn-light hover-shadow mb-4 d-flex align-items-center gap-2 text-secondary fw-medium"
        @click="goList"
      >
        <ArrowLeft :size="18" />
        목록으로
      </button>

      <div class="card shadow-sm border-0 mb-4">
        <div class="card-body p-4 p-md-5">
          
          <div class="d-flex align-items-start justify-content-between mb-4">
            <div class="d-flex align-items-center gap-3">
              <div class="bg-primary bg-opacity-10 rounded-circle d-flex align-items-center justify-content-center text-primary fs-4" 
                   style="width: 50px; height: 50px;">
                {{ review.authorAvatar }}
              </div>

              <div>
                <div class="d-flex align-items-center gap-2 mb-1">
                  <span class="fw-bold text-dark">{{ review.author }}</span>
                  <span class="text-secondary small">·</span>
                  <span class="text-secondary small">{{ review.date }}</span>
                </div>

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
                  <span class="text-secondary small">조회 {{ review.views }}</span>
                </div>
              </div>
            </div>

            <button class="btn btn-light btn-sm rounded-circle p-2 text-secondary">
              <MoreVertical :size="18" />
            </button>
          </div>

          <div class="d-inline-flex align-items-center gap-2 px-3 py-1 bg-light rounded-pill mb-4 border">
            <span class="small text-secondary fw-medium">약품명:</span>
            <button class="btn btn-link p-0 text-decoration-none small fw-bold" @click="goDetail(review.id)">
              {{ review.drugName }}
            </button>
          </div>

          <h1 class="h3 fw-bold mb-4">{{ review.title }}</h1>

          <div class="mb-5">
            <p class="text-dark lh-lg" style="white-space: pre-wrap;">{{ review.content }}</p>
          </div>

          <div class="d-flex gap-2 border-top pt-4">
            <button class="btn btn-outline-secondary d-flex align-items-center gap-2 rounded-pill px-3">
              <ThumbsUp :size="16" />
              도움이 돼요 {{ review.helpful }}
            </button>
            <button class="btn btn-outline-secondary d-flex align-items-center gap-2 rounded-pill px-3">
              <Share2 :size="16" />
              공유하기
            </button>
          </div>

        </div>
      </div>

      <div class="card shadow-sm border-0 mb-4">
        <div class="card-body p-4">
          <h4 class="fw-bold mb-4">
            댓글 <span class="text-primary">{{ comments.length }}</span>
          </h4>

          <div class="mb-5">
            <textarea 
              class="form-control bg-light border-0 mb-2" 
              rows="3" 
              placeholder="댓글을 입력하세요..." 
              v-model="newComment"
              style="resize: none;"
            ></textarea>
            <div class="d-flex justify-content-end">
              <button class="btn btn-primary px-4 fw-medium" @click="handleSubmitComment">댓글 작성</button>
            </div>
          </div>

          <div class="d-flex flex-column gap-3">
            <div v-for="comment in comments" :key="comment.id" class="d-flex gap-3 p-3 bg-light rounded-3">
              <div class="bg-white rounded-circle d-flex align-items-center justify-content-center shadow-sm flex-shrink-0" 
                   style="width: 40px; height: 40px;">
                <User :size="20" class="text-secondary" />
              </div>

              <div class="flex-grow-1">
                <div class="d-flex align-items-center gap-2 mb-1">
                  <span class="fw-bold small">{{ comment.author }}</span>
                  <span class="text-secondary small">{{ comment.date }}</span>
                </div>
                
                <p class="mb-2 small text-dark">{{ comment.content }}</p>

                <button class="btn btn-link text-decoration-none p-0 text-secondary small d-flex align-items-center gap-1">
                  <ThumbsUp :size="12" /> {{ comment.likes }}
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>

      <div class="card shadow-sm border-0">
        <div class="card-body p-4">
          <h5 class="fw-bold mb-3">관련 리뷰</h5>
          
          <div class="list-group list-group-flush">
            <button 
              v-for="item in relatedReviews" 
              :key="item.id"
              class="list-group-item list-group-item-action border-0 rounded p-3 mb-1 bg-light-hover"
              @click="goDetail(item.id)"
            >
              <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="fw-bold text-dark">{{ item.title }}</span>
                <div class="d-flex text-warning">
                  <Star 
                    v-for="i in 5" 
                    :key="i" 
                    :size="12" 
                    :fill="i <= item.rating ? 'currentColor' : 'none'"
                    :class="i <= item.rating ? 'text-warning' : 'text-secondary opacity-25'"
                  />
                </div>
              </div>
              <p class="text-secondary small text-truncate mb-1">{{ item.preview }}</p>
              <div class="text-secondary x-small">
                {{ item.author }} · {{ item.date }}
              </div>
            </button>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* 커스텀 폰트 사이즈 */
.x-small {
  font-size: 0.75rem;
}

/* 호버 시 배경색 변경 (리스트 아이템) */
.bg-light-hover:hover {
  background-color: #e9ecef !important;
}

/* 버튼 그림자 효과 */
.hover-shadow:hover {
  box-shadow: 0 .125rem .25rem rgba(0,0,0,.075);
}
</style>