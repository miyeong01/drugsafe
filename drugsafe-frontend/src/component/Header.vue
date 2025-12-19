<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
// Vue용 Lucide 아이콘 임포트 (설치 필요: npm install lucide-vue-next)
import { Search, Heart, User, Menu, Pill } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()

// 현재 경로(route.name)를 확인해서 활성화된 메뉴인지 판단하는 함수
const isActive = (pageName) => {
  return route.name === pageName
}

// 로고 클릭 시 홈으로 이동
const goHome = () => {
  router.push('/')
}

// 로그인/회원가입 페이지 이동
const goAuth = () => {
  router.push('/auth')
}
</script>

<template>
  <header class="bg-white border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        
        <div 
          class="flex items-center gap-2 cursor-pointer"
          @click="goHome"
        >
          <div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
            <Pill class="w-6 h-6 text-white" />
          </div>
          <span class="text-blue-600 font-bold text-lg">DrugSafe</span>
        </div>

        <nav class="hidden md:flex items-center gap-6">
          <RouterLink 
            to="/" 
            class="transition-colors font-medium"
            :class="isActive('home') ? 'text-blue-600' : 'text-gray-700 hover:text-blue-600'"
          >
            홈
          </RouterLink>
          
          <RouterLink 
            to="/community" 
            class="transition-colors font-medium"
            :class="isActive('community') ? 'text-blue-600' : 'text-gray-700 hover:text-blue-600'"
          >
            커뮤니티
          </RouterLink>
          
          <RouterLink 
            to="/faq" 
            class="transition-colors font-medium"
            :class="isActive('faq') ? 'text-blue-600' : 'text-gray-700 hover:text-blue-600'"
          >
            FAQ
          </RouterLink>
        </nav>

        <div class="flex items-center gap-3">
          <button class="hidden md:flex p-2 hover:bg-gray-100 rounded-md transition-colors">
            <Heart class="w-5 h-5 text-gray-700" />
          </button>

          <button 
            class="p-2 hover:bg-gray-100 rounded-md transition-colors"
            @click="router.push('/profile')"
          >
            <User class="w-5 h-5 text-gray-700" />
          </button>

          <button 
            @click="goAuth"
            class="hidden sm:flex px-4 py-2 border border-gray-300 rounded-md text-sm font-medium hover:bg-gray-50 transition-colors"
          >
            회원가입
          </button>

          <button 
            @click="goAuth"
            class="hidden sm:flex px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
          >
            로그인
          </button>

          <button class="md:hidden p-2 hover:bg-gray-100 rounded-md transition-colors">
            <Menu class="w-5 h-5 text-gray-700" />
          </button>
        </div>

      </div>
    </div>
  </header>
</template>

<style scoped>
</style>