<script setup>
import { useRouter, useRoute } from 'vue-router'
// 아이콘은 그대로 사용합니다
import { Heart, User, Menu, Pill } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()

const isActive = (pageName) => route.name === pageName
const goHome = () => router.push('/')
const goAuth = () => router.push('/auth')
</script>

<template>
  <header class="border-bottom bg-white sticky-top py-2">
    <div class="container">
      <div class="d-flex align-items-center justify-content-between" style="height: 64px;">
        
        <div class="d-flex align-items-center gap-2 cursor-pointer" @click="goHome" style="cursor: pointer;">
          <div class="rounded-circle bg-primary d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
            <Pill class="text-white" :size="24" />
          </div>
          <span class="text-primary fw-bold fs-4">DrugSafe</span>
        </div>

        <nav class="d-none d-md-flex align-items-center gap-4">
          <RouterLink 
            to="/" 
            class="text-decoration-none fw-medium"
            :class="isActive('home') ? 'text-primary' : 'text-secondary'"
          >
            홈
          </RouterLink>
          
          <RouterLink 
            to="/community" 
            class="text-decoration-none fw-medium"
            :class="isActive('community') ? 'text-primary' : 'text-secondary'"
          >
            커뮤니티
          </RouterLink>
          
          <RouterLink 
            to="/faq" 
            class="text-decoration-none fw-medium"
            :class="isActive('faq') ? 'text-primary' : 'text-secondary'"
          >
            FAQ
          </RouterLink>
        </nav>

        <div class="d-flex align-items-center gap-2">
          <button class="btn btn-light d-none d-md-block p-2 border-0">
            <Heart class="text-secondary" :size="20" />
          </button>

          <button 
            class="btn btn-light p-2 border-0"
            @click="router.push('/profile')"
          >
            <User class="text-secondary" :size="20" />
          </button>

          <button 
            @click="goAuth"
            class="btn btn-outline-secondary d-none d-sm-block btn-sm fw-medium px-3"
          >
            회원가입
          </button>

          <button 
            @click="goAuth"
            class="btn btn-primary d-none d-sm-block btn-sm fw-medium px-3 text-white"
          >
            로그인
          </button>

          <button class="btn btn-light d-md-none p-2 border-0">
            <Menu class="text-secondary" :size="20" />
          </button>
        </div>

      </div>
    </div>
  </header>
</template>

<style scoped>
.gap-2 { gap: 0.5rem; }
.gap-4 { gap: 1.5rem; }
</style>