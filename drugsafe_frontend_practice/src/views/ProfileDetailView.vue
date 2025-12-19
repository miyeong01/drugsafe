<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Trash2, Edit } from 'lucide-vue-next'

const router = useRouter()

// 현재 활성화된 탭
const activeTab = ref('password')

// 비밀번호 데이터
const passwordData = reactive({
  current: '',
  new: '',
  confirm: '',
})

// 더미 데이터들
const favorites = ref([
  { id: '1', name: '타이레놀정 500mg', manufacturer: '한국얀센' },
  { id: '2', name: '게보린정', manufacturer: '삼진제약' },
  { id: '3', name: '어린이부루펜시럽', manufacturer: '삼일제약' },
])

const medications = ref([
  { id: '1', name: '타이레놀정 500mg', period: '2025.01.01 ~ 2025.01.14' },
  { id: '2', name: '비타민 D', period: '2025.01.01 ~ 2025.03.31' },
])

const reviews = ref([
  { id: '1', drugName: '타이레놀정 500mg', date: '2025.01.15', rating: 5 },
  { id: '2', drugName: '게보린정', date: '2025.01.10', rating: 4 },
])

// --- 핸들러 함수 ---

// 뒤로가기
const goBack = () => {
  router.back()
}

// 비밀번호 변경
const handlePasswordChange = () => {
  if (passwordData.new !== passwordData.confirm) {
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }
  alert('비밀번호가 성공적으로 변경되었습니다.')
  // 입력창 초기화
  passwordData.current = ''
  passwordData.new = ''
  passwordData.confirm = ''
}

// 삭제 핸들러 (브라우저 기본 confirm 사용)
const handleDeleteItem = (type, id) => {
  if (confirm(`정말 해당 ${type}을(를) 삭제하시겠습니까?`)) {
    // 실제로는 여기서 API로 삭제 요청을 보냄
    
    // 화면에서 지우는 시늉 (리스트 필터링)
    if (type === '즐겨찾기') {
      favorites.value = favorites.value.filter(item => item.id !== id)
    } else if (type === '복용기록') {
      medications.value = medications.value.filter(item => item.id !== id)
    } else if (type === '리뷰') {
      reviews.value = reviews.value.filter(item => item.id !== id)
    }
    
    alert('삭제되었습니다.')
  }
}

// 수정 핸들러 (예시)
const handleEdit = (type) => {
  alert(`${type} 수정 화면으로 이동합니다.`)
}
</script>

<template>
  <div class="min-vh-100 bg-light py-5">
    <div class="container" style="max-width: 800px;">

      <div class="d-flex align-items-center gap-3 mb-4">
        <button class="btn btn-white border rounded-circle p-2 shadow-sm" @click="goBack">
          <ArrowLeft :size="20" class="text-dark" />
        </button>
        <h2 class="h4 fw-bold mb-0">설정 및 관리</h2>
      </div>

      <div class="mb-4 overflow-auto">
        <ul class="nav nav-pills flex-nowrap bg-white p-1 rounded shadow-sm" style="min-width: 500px;">
          <li class="nav-item flex-fill">
            <button class="nav-link fw-bold text-center w-100" :class="{ active: activeTab === 'password' }" @click="activeTab = 'password'">비밀번호</button>
          </li>
          <li class="nav-item flex-fill">
            <button class="nav-link fw-bold text-center w-100" :class="{ active: activeTab === 'favorites' }" @click="activeTab = 'favorites'">즐겨찾기</button>
          </li>
          <li class="nav-item flex-fill">
            <button class="nav-link fw-bold text-center w-100" :class="{ active: activeTab === 'medications' }" @click="activeTab = 'medications'">복용기록</button>
          </li>
          <li class="nav-item flex-fill">
            <button class="nav-link fw-bold text-center w-100" :class="{ active: activeTab === 'reviews' }" @click="activeTab = 'reviews'">리뷰관리</button>
          </li>
        </ul>
      </div>

      <div v-if="activeTab === 'password'">
        <div class="card shadow-sm border-0">
          <div class="card-body p-4">
            <h3 class="h5 fw-bold mb-4">비밀번호 변경</h3>
            <form @submit.prevent="handlePasswordChange" style="max-width: 400px;">
              <div class="mb-3">
                <label class="form-label fw-medium">현재 비밀번호</label>
                <input type="password" class="form-control" v-model="passwordData.current" required>
              </div>
              <div class="mb-3">
                <label class="form-label fw-medium">새 비밀번호</label>
                <input type="password" class="form-control" v-model="passwordData.new" required>
                <div class="form-text">8자 이상, 영문/숫자/특수문자 조합</div>
              </div>
              <div class="mb-4">
                <label class="form-label fw-medium">새 비밀번호 확인</label>
                <input type="password" class="form-control" v-model="passwordData.confirm" required>
              </div>
              <button type="submit" class="btn btn-primary w-100 py-2 fw-bold">비밀번호 변경</button>
            </form>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'favorites'">
        <div class="card shadow-sm border-0">
          <div class="card-body p-4">
            <h3 class="h5 fw-bold mb-4">즐겨찾기 관리</h3>
            <div class="d-flex flex-column gap-3">
              <div v-for="item in favorites" :key="item.id" class="border rounded p-3 d-flex justify-content-between align-items-center bg-white hover-bg">
                <div>
                  <h4 class="h6 fw-bold mb-1">{{ item.name }}</h4>
                  <p class="text-secondary small mb-0">{{ item.manufacturer }}</p>
                </div>
                <button class="btn btn-light text-danger btn-sm" @click="handleDeleteItem('즐겨찾기', item.id)">
                  <Trash2 :size="18" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'medications'">
        <div class="card shadow-sm border-0">
          <div class="card-body p-4">
            <h3 class="h5 fw-bold mb-4">복용기록 관리</h3>
            <div class="d-flex flex-column gap-3">
              <div v-for="item in medications" :key="item.id" class="border rounded p-3 d-flex justify-content-between align-items-center bg-white hover-bg">
                <div>
                  <h4 class="h6 fw-bold mb-1">{{ item.name }}</h4>
                  <p class="text-secondary small mb-0">{{ item.period }}</p>
                </div>
                <div class="d-flex gap-2">
                  <button class="btn btn-light text-secondary btn-sm" @click="handleEdit('복용기록')">
                    <Edit :size="18" />
                  </button>
                  <button class="btn btn-light text-danger btn-sm" @click="handleDeleteItem('복용기록', item.id)">
                    <Trash2 :size="18" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'reviews'">
        <div class="card shadow-sm border-0">
          <div class="card-body p-4">
            <h3 class="h5 fw-bold mb-4">리뷰 관리</h3>
            <div class="d-flex flex-column gap-3">
              <div v-for="item in reviews" :key="item.id" class="border rounded p-3 d-flex justify-content-between align-items-center bg-white hover-bg">
                <div class="flex-grow-1">
                  <h4 class="h6 fw-bold mb-1">{{ item.drugName }}</h4>
                  <div class="text-warning small mb-1">
                    <span v-for="i in 5" :key="i">{{ i <= item.rating ? '★' : '☆' }}</span>
                    <span class="text-secondary ms-2">{{ item.date }}</span>
                  </div>
                </div>
                <div class="d-flex gap-2">
                  <button class="btn btn-light text-secondary btn-sm" @click="handleEdit('리뷰')">
                    <Edit :size="18" />
                  </button>
                  <button class="btn btn-light text-danger btn-sm" @click="handleDeleteItem('리뷰', item.id)">
                    <Trash2 :size="18" />
                  </button>
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

/* 리스트 항목 호버 효과 */
.hover-bg:hover {
  background-color: #f8f9fa;
  transition: background-color 0.2s;
}

/* 버튼 흰색 배경 */
.btn-white {
  background-color: white;
}
.btn-white:hover {
  background-color: #f8f9fa;
}
</style>