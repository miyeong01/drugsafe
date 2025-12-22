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
      path: '/drug/:id',
      name: 'drug-detail',
      component: DrugDetailView,
    }
  ],

  scrollBehavior(to, from, savedPosition) {
    // 사용자가 '뒤로 가기'를 했을 때 (savedPosition이 있을 때)
    if (savedPosition) {
      return savedPosition
    } else {
      // 새로운 페이지로 이동했을 때는 무조건 맨 위로!
      return { top: 0 }
    }
  },
})

export default router
