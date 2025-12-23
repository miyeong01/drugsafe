<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()

// 1. 초기 탭 설정 (주소창에 ?mode=signup 있으면 회원가입 탭 열기)
const activeTab = ref(route.query.mode === 'signup' ? 'signup' : 'login')

// 2. 주소(URL)가 바뀌면 탭도 자동으로 바뀜 (헤더 버튼 대응)
watch(() => route.query.mode, (newMode) => {
  activeTab.value = (newMode === 'signup') ? 'signup' : 'login'
})

// 3. 탭 버튼 클릭 시 주소 변경
const setTab = (mode) => {
  router.replace({ query: { mode: mode } })
}

// --- 데이터 정의 ---
const loginData = ref({
  username: '',
  password: '',
})

const signupData = ref({
  username: '',
  name: '',
  birthdate: '',
  phone: '',
  carrier: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false,
})

// --- 핸들러 ---
const handleLogin = async () => {
  // 1. 입력값 확인
  if (!loginData.value.username || !loginData.value.password) {
    alert('아이디와 비밀번호를 모두 입력해주세요.')
    return
  }
  // 2. 스토어의 로그인 액션 호출
  await accountStore.login(loginData.value)
}

const handleSignup = () => {
  if (signupData.value.password !== signupData.value.confirmPassword) {
    alert('비밀번호가 일치하지 않습니다.');
    return;
  }
  
  // 스토어 액션 호출
  accountStore.signup(signupData.value);
}
</script>

<template>
  <div class="min-vh-100 bg-light d-flex align-items-center justify-content-center py-5">
    <div class="container" style="max-width: 500px;">
      
      <div class="text-center mb-4">
        <h1 class="h3 fw-bold text-dark mb-2">DrugSafe에 오신 것을 환영합니다</h1>
        <p class="text-secondary">안전한 의약품 정보 서비스</p>
      </div>

      <div class="card shadow-sm border-0">
        <div class="card-body p-4 p-md-5">
          
          <ul class="nav nav-pills nav-fill mb-4 bg-light p-1 rounded" role="tablist">
            <li class="nav-item">
              <button 
                class="nav-link fw-bold" 
                :class="{ active: activeTab === 'login' }"
                @click="setTab('login')" 
                type="button"
              >
                로그인
              </button>
            </li>
            <li class="nav-item">
              <button 
                class="nav-link fw-bold" 
                :class="{ active: activeTab === 'signup' }"
                @click="setTab('signup')"
                type="button"
              >
                회원가입
              </button>
            </li>
          </ul>

          <div v-if="activeTab === 'login'">
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="login-username" class="form-label fw-medium">아이디</label>
                <input id="login-username" type="text" class="form-control" placeholder="아이디를 입력하세요" v-model="loginData.username" required />
              </div>
              <div class="mb-3">
                <label for="login-password" class="form-label fw-medium">비밀번호</label>
                <input id="login-password" type="password" class="form-control" placeholder="비밀번호를 입력하세요" v-model="loginData.password" required />
              </div>
              <div class="d-flex justify-content-between align-items-center mb-4">
                <div class="form-check">
                  <input type="checkbox" class="form-check-input" id="remember-me" />
                  <label class="form-check-label text-secondary small" for="remember-me">로그인 상태 유지</label>
                </div>
                <button type="button" class="btn btn-link text-decoration-none p-0 small">비밀번호 찾기</button>
              </div>
              <button type="submit" class="btn btn-primary w-100 py-2 fw-bold">로그인</button>
            </form>
          </div>

          <div v-if="activeTab === 'signup'">
            <form @submit.prevent="handleSignup">
              <div class="mb-3">
                <label for="signup-username" class="form-label fw-medium">아이디</label>
                <input id="signup-username" type="text" class="form-control" placeholder="아이디를 입력하세요" v-model="signupData.username" required />
              </div>
              
              <div class="mb-3">
                <label for="signup-password" class="form-label fw-medium">비밀번호</label>
                <input id="signup-password" type="password" class="form-control" placeholder="비밀번호를 입력하세요" v-model="signupData.password" required />
              </div>

              <div class="mb-3">
                <label for="signup-confirm-password" class="form-label fw-medium">비밀번호 확인</label>
                <input id="signup-confirm-password" type="password" class="form-control" placeholder="비밀번호를 다시 입력하세요" v-model="signupData.confirmPassword" required />
              </div>
              <div class="mb-3">
                <label for="signup-name" class="form-label fw-medium">이름</label>
                <input id="signup-name" type="text" class="form-control" placeholder="이름을 입력하세요" v-model="signupData.name" required />
              </div>

              <div class="mb-3">
                <label for="signup-birthdate" class="form-label fw-medium">생년월일</label>
                <input id="signup-birthdate" type="date" class="form-control" v-model="signupData.birthdate" required />
              </div>

              <div class="mb-3">
                <label for="signup-carrier" class="form-label fw-medium">통신사</label>
                <select id="signup-carrier" class="form-select" v-model="signupData.carrier" required>
                  <option value="" disabled selected>통신사를 선택하세요</option>
                  <option value="skt">SKT</option>
                  <option value="kt">KT</option>
                  <option value="lgu">LG U+</option>
                  <option value="mvno">알뜰폰</option>
                </select>
              </div>

              <div class="mb-3">
                <label for="signup-phone" class="form-label fw-medium">휴대폰 번호</label>
                <input id="signup-phone" type="tel" class="form-control" placeholder="010-0000-0000" v-model="signupData.phone" required />
              </div>

              <div class="mb-3">
                <label for="signup-email" class="form-label fw-medium">이메일</label>
                <input id="signup-email" type="email" class="form-control" placeholder="name@example.com" v-model="signupData.email" required />
              </div>


              <div class="mb-4 form-check">
                <input type="checkbox" class="form-check-input" id="terms" required v-model="signupData.agreeTerms" />
                <label class="form-check-label text-secondary small" for="terms">이용약관 및 개인정보처리방침에 동의합니다.</label>
              </div>

              <button type="submit" class="btn btn-primary w-100 py-2 fw-bold">회원가입</button>
            </form>
          </div>
          </div> </div> </div> </div> </template>

<style scoped>
.nav-pills .nav-link.active {
  background-color: white;
  color: #0d6efd;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.nav-pills .nav-link {
  color: #6c757d;
}
</style>