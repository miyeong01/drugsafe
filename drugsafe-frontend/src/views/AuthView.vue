<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 탭 상태 ('login' 또는 'signup')
const activeTab = ref('login')

// 회원가입 폼 데이터
const signupData = ref({
  username: '',
  name: '',
  birthdate: '',
  phone: '',
  carrier: '',
  email: '',
  password: '',
  confirmPassword: '',
})

// 로그인 폼 데이터
const loginData = ref({
  username: '',
  password: '',
})

// 로그인 처리
const handleLogin = () => {
  // 실제 로그인 API 호출 로직이 들어갈 곳
  alert('로그인되었습니다!')
  router.push('/') // 홈으로 이동
}

// 회원가입 처리
const handleSignup = () => {
  // 실제 회원가입 API 호출 로직이 들어갈 곳
  alert('회원가입이 완료되었습니다!')
  router.push('/') // 홈으로 이동
}
</script>

<template>
  <div class="min-h-screen py-12 px-4 bg-gray-50 flex items-center justify-center">
    <div class="w-full max-w-md">
      
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold mb-2 text-gray-900">DrugSafe에 오신 것을 환영합니다</h1>
        <p class="text-gray-500">안전한 의약품 정보 서비스</p>
      </div>

      <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
        
        <div class="grid grid-cols-2 gap-1 mb-6 bg-gray-100 p-1 rounded-lg">
          <button 
            @click="activeTab = 'login'"
            class="py-2 text-sm font-medium rounded-md transition-all duration-200"
            :class="activeTab === 'login' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-500 hover:text-gray-900'"
          >
            로그인
          </button>
          <button 
            @click="activeTab = 'signup'"
            class="py-2 text-sm font-medium rounded-md transition-all duration-200"
            :class="activeTab === 'signup' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-500 hover:text-gray-900'"
          >
            회원가입
          </button>
        </div>

        <div v-if="activeTab === 'login'">
          <form @submit.prevent="handleLogin" class="space-y-4">
            <div class="space-y-2">
              <label for="login-username" class="text-sm font-medium text-gray-700">아이디</label>
              <input
                id="login-username"
                type="text"
                placeholder="아이디를 입력하세요"
                v-model="loginData.username"
                required
                class="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              />
            </div>

            <div class="space-y-2">
              <label for="login-password" class="text-sm font-medium text-gray-700">비밀번호</label>
              <input
                id="login-password"
                type="password"
                placeholder="비밀번호를 입력하세요"
                v-model="loginData.password"
                required
                class="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              />
            </div>

            <div class="flex items-center justify-between text-sm">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                <span class="text-gray-500">로그인 상태 유지</span>
              </label>
              <button type="button" class="text-blue-600 hover:underline">
                비밀번호 찾기
              </button>
            </div>

            <button 
              type="submit" 
              class="w-full inline-flex items-center justify-center rounded-md text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 h-10 px-4 py-2 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              로그인
            </button>
          </form>
        </div>

        <div v-if="activeTab === 'signup'">
          <form @submit.prevent="handleSignup" class="space-y-4">
            <div class="space-y-2">
              <label for="signup-username" class="text-sm font-medium text-gray-700">아이디</label>
              <input
                id="signup-username"
                type="text"
                placeholder="아이디를 입력하세요"
                v-model="signupData.username"
                required
                class="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div class="space-y-2">
              <label for="signup-name" class="text-sm font-medium text-gray-700">이름</label>
              <input
                id="signup-name"
                type="text"
                placeholder="이름을 입력하세요"
                v-model="signupData.name"
                required
                class="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div class="space-y-2">
              <label for="signup-birthdate" class="text-sm font-medium text-gray-700">생년월일</label>
              <input
                id="signup-birthdate"
                type="date"
                v-model="signupData.birthdate"
                required
                class="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div class="space-y-2">
              <label for="signup-phone" class="text-sm font-medium text-gray-700">휴대폰 번호</label>
              <input
                id="signup-phone"
                type="tel"
                placeholder="010-0000-0000"
                v-model="signupData.phone"
                required
                class="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div class="space-y-2">
              <label for="signup-carrier" class="text-sm font-medium text-gray-700">통신사</label>
              <select
                id="signup-carrier"
                v-model="signupData.carrier"
                class="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none"
              >
                <option value="" disabled selected>통신사를 선택하세요</option>
                <option value="skt">SKT</option>
                <option value="kt">KT</option>
                <option value="lgu">LG U+</option>
                <option value="mvno">알뜰폰</option>
              </select>
            </div>

            <div class="space-y-2">
              <label for="signup-email" class="text-sm font-medium text-gray-700">이메일</label>
              <input
                id="signup-email"
                type="email"
                placeholder="example@email.com"
                v-model="signupData.email"
                required
                class="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div class="space-y-2">
              <label for="signup-password" class="text-sm font-medium text-gray-700">비밀번호</label>
              <input
                id="signup-password"
                type="password"
                placeholder="비밀번호를 입력하세요"
                v-model="signupData.password"
                required
                class="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div class="space-y-2">
              <label for="signup-confirm-password" class="text-sm font-medium text-gray-700">비밀번호 확인</label>
              <input
                id="signup-confirm-password"
                type="password"
                placeholder="비밀번호를 다시 입력하세요"
                v-model="signupData.confirmPassword"
                required
                class="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div class="space-y-2">
              <label class="flex items-start gap-2 text-sm cursor-pointer">
                <input type="checkbox" class="mt-1 rounded border-gray-300 text-blue-600 focus:ring-blue-500" required />
                <span class="text-gray-500">
                  이용약관 및 개인정보처리방침에 동의합니다.
                </span>
              </label>
            </div>

            <button 
              type="submit" 
              class="w-full inline-flex items-center justify-center rounded-md text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 h-10 px-4 py-2 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              회원가입
            </button>
          </form>
        </div>

      </div>
    </div>
  </div>
</template>