<script setup>
import { useRouter, useRoute } from 'vue-router'
// Heart 아이콘 다시 추가
import { Heart, User, Menu, Pill } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()

// 현재 페이지인지 확인 (글자색 파랗게 만들기 위해)
const isActive = (pageName) => route.name === pageName

const goHome = () => router.push('/')
const goAuth = () => router.push('/auth')
</script>

<template>
  <header class="border-bottom bg-white sticky-top py-3">
    <div class="container-fluid px-4">
      <div class="d-flex align-items-center justify-content-between" style="height: 40px;">
        
        <div class="d-flex align-items-center gap-2" @click="goHome" style="cursor: pointer;">
          <div class="rounded-circle bg-primary d-flex align-items-center justify-content-center" 
               style="width: 36px; height: 36px;">
            <Pill class="text-white" :size="20" />
          </div>
          <span class="text-primary fw-bold fs-5">DrugSafe</span>
        </div>

        <nav class="d-none d-md-flex align-items-center gap-5">
          <RouterLink 
            to="/" 
            class="text-decoration-none fw-medium"
            :class="isActive('home') ? 'text-primary' : 'text-dark'"
          >
            홈
          </RouterLink>
          
          <RouterLink 
            to="/community" 
            class="text-decoration-none fw-medium"
            :class="isActive('community') ? 'text-primary' : 'text-dark'"
          >
            커뮤니티
          </RouterLink>
          
          <RouterLink 
            to="/faq" 
            class="text-decoration-none fw-medium"
            :class="isActive('faq') ? 'text-primary' : 'text-dark'"
          >
            FAQ
          </RouterLink>
        </nav>

        <div class="d-flex align-items-center gap-2">
          
          <button class="btn p-2 border-0 text-dark">
            <Heart :size="20" />
          </button>

          <button 
            class="btn p-2 border-0 text-dark"
            @click="router.push('/profile')"
          >
            <User :size="20" />
          </button>

          <button 
            @click="goAuth"
            class="btn btn-outline-secondary btn-sm fw-medium px-3 ms-2"
            style="border-color: #dee2e6; color: #495057;"
          >
            회원가입
          </button>

          <button 
            @click="goAuth"
            class="btn btn-primary btn-sm fw-medium px-3 text-white"
          >
            로그인
          </button>
          
          <button class="btn p-2 border-0 text-dark d-md-none">
            <Menu :size="20" />
          </button>
        </div>

      </div>
    </div>
  </header>
</template>

<style scoped>
/* 간격 조정 */
.gap-2 { gap: 0.5rem; }
.gap-5 { gap: 3rem; } /* 메뉴 사이 간격을 넓게 */
</style>