import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AuthView from '@/views/AuthView.vue'
import CommunityDetail from '@/views/CommunityDetail.vue'
import FAQView from '@/views/FAQView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ProfileDetailView from '@/views/ProfileDetailView.vue'
import SearchResultView from '@/views/SearchResultView.vue'
import DrugDetailView from '@/views/DrugDetailView.vue'
import AIChatView from '@/views/AIChatView.vue'
import ReviewWrite from '@/views/ReviewWrite.vue'
import ReviewDetail from '@/views/ReviewDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/chatbot',
      name: 'chatbot',
      component: AIChatView,
    },
    {
      path: '/auth',
      name: 'auth',
      component: AuthView,
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityDetail,
    },
    {
      path: '/FAQ',
      name: 'FAQ',
      component: FAQView,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
    {
      path: '/profile/edit',
      name: 'profile-edit',
      component: ProfileDetailView,
    },
    {
      path: '/search',
      name: 'search',
      component: SearchResultView,
    },
    {
      path: '/drug/:drugId',
      name: 'drug-detail',
      component: DrugDetailView,
    },
    {
      path: '/drug/:drugId/review',
      name: 'ReviewWrite',
      component: ReviewWrite,
      props: true
    },
    {
      path: '/drug/:drugId/review/:reviewId',
      name: 'ReviewDetail',
      component: ReviewDetail,
    }
  ],

  // ✨ 페이지 이동 시 스크롤 위치 제어
  scrollBehavior(to, from, savedPosition) {
    // 1. 뒤로가기/앞으로가기 버튼을 눌렀을 때는 이전 스크롤 위치를 유지합니다.
    if (savedPosition) {
      return savedPosition
    } else {
      // 2. 그 외에 일반적인 페이지 이동은 항상 맨 위(0, 0)로 보냅니다.
      return { top: 0 }
    }
  },
})

export default router
