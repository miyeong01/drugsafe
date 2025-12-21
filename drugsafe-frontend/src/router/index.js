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
})

export default router
