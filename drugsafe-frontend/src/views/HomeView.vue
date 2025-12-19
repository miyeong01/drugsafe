<script setup>
import { ref, h } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Search, Thermometer, Brain, Heart, Bone, Activity, 
  Zap, Droplet, Wind, Smile, Pill, Stethoscope, AlertCircle 
} from 'lucide-vue-next'

const router = useRouter()
const searchQuery = ref('')

// --- 커스텀 아이콘 정의 (Vue 함수형 컴포넌트) ---
const ToothIcon = (props) => h('svg', {
  class: props.class,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: '2',
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('path', { d: 'M8 2C6 2 5 4 5 6v10c0 2 0 4 2 6h2c1-2 1-4 1-6V6c0-2-1-4-2-4z' }),
  h('path', { d: 'M16 2c-1 0-2 2-2 4v10c0 2 0 4 1 6h2c2-2 2-4 2-6V6c0-2-1-4-3-4z' })
])

const StomachIcon = (props) => h('svg', {
  class: props.class,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: '2',
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('ellipse', { cx: '12', cy: '13', rx: '8', ry: '9' }),
  h('path', { d: 'M8 6c0-2 1-4 4-4s4 2 4 4' })
])

const DigestiveIcon = (props) => h('svg', {
  class: props.class,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: '2',
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('path', { d: 'M8 3c-1 0-2 1-2 3v3c0 2-1 3-2 4 1 1 2 2 2 4v3c0 2 1 3 2 3' }),
  h('path', { d: 'M16 3c1 0 2 1 2 3v3c0 2 1 3 2 4-1 1-2 2-2 4v3c0 2-1 3-2 3' })
])

const NoseIcon = (props) => h('svg', {
  class: props.class,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: '2',
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('path', { d: 'M12 2v8' }),
  h('ellipse', { cx: '10', cy: '14', rx: '2', ry: '3' }),
  h('ellipse', { cx: '14', cy: '14', rx: '2', ry: '3' }),
  h('path', { d: 'M12 10c-3 0-4 2-4 4' }),
  h('path', { d: 'M12 10c3 0 4 2 4 4' })
])

const MuscleIcon = (props) => h('svg', {
  class: props.class,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: '2',
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('path', { d: 'M6 8c0-2 2-4 4-4h4c2 0 4 2 4 4' }),
  h('path', { d: 'M6 8v4c0 3 1 6 6 8 5-2 6-5 6-8V8' }),
  h('path', { d: 'M10 10v6' }),
  h('path', { d: 'M14 10v6' })
])

// --- 데이터 정의 ---
const symptoms = [
  { icon: Brain, label: '두통', description: '머리가 아플 때', color: 'bg-blue-100 text-blue-600' },
  { icon: ToothIcon, label: '치통', description: '이가 아플 때', color: 'bg-blue-100 text-blue-600' },
  { icon: Thermometer, label: '발열', description: '열이 날 때', color: 'bg-blue-100 text-blue-600' },
  { icon: StomachIcon, label: '복통', description: '배가 아플 때', color: 'bg-blue-100 text-blue-600' },
  { icon: Heart, label: '생리통', description: '생리 시 통증', color: 'bg-blue-100 text-blue-600' },
  { icon: DigestiveIcon, label: '위장약', description: '위장이 불편할 때', color: 'bg-blue-100 text-blue-600' },
  { icon: Activity, label: '종합감기', description: '감기 증상 전반', color: 'bg-blue-100 text-blue-600' },
  { icon: NoseIcon, label: '코감기', description: '콧물·코막힘', color: 'bg-blue-100 text-blue-600' },
  { icon: Wind, label: '기침', description: '기침이 날 때', color: 'bg-blue-100 text-blue-600' },
  { icon: Droplet, label: '재채기', description: '재채기가 날 때', color: 'bg-blue-100 text-blue-600' },
  { icon: Pill, label: '소화불량', description: '소화가 안 될 때', color: 'bg-blue-100 text-blue-600' },
  { icon: Droplet, label: '알레르기', description: '알레르기 반응', color: 'bg-blue-100 text-blue-600' },
  { icon: Zap, label: '육체피로', description: '피로·권태감', color: 'bg-blue-100 text-blue-600' },
  { icon: Bone, label: '관절통', description: '관절이 아플 때', color: 'bg-blue-100 text-blue-600' },
  { icon: MuscleIcon, label: '근육통', description: '근육이 아플 때', color: 'bg-blue-100 text-blue-600' },
]

// --- 핸들러 ---
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    // 검색 페이지로 이동 (쿼리 파라미터 전달)
    router.push({ name: 'search', query: { q: searchQuery.value } })
  }
}

const handleSymptomClick = (label) => {
  router.push({ name: 'search', query: { q: label } })
}
</script>

<template>
  <div class="min-h-screen">
    
    <section class="bg-gradient-to-br from-blue-50 to-blue-100/30 py-24 px-4">
      <div class="max-w-5xl mx-auto text-center">
        <h1 class="mb-3 text-blue-600 text-5xl font-bold">어디가 아프신가요?</h1>
        <p class="mb-10 text-gray-500">
          빠르고 정확하게 약을 찾아드려요
        </p>

        <div class="max-w-2xl mx-auto">
          <div class="flex gap-2 bg-white rounded-full shadow-lg p-2">
            <div class="flex-1 relative">
              <Search class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="증상이나 약품명을 검색하세요..."
                class="w-full h-full pl-12 pr-4 border-0 focus:outline-none focus:ring-0 bg-transparent rounded-full text-base"
                v-model="searchQuery"
                @keydown.enter="handleSearch"
              />
            </div>
            <button 
              @click="handleSearch" 
              class="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-8 py-3 font-medium transition-colors"
            >
              검색
            </button>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16 px-4 max-w-6xl mx-auto">
      <h2 class="mb-10 text-center text-3xl font-bold text-gray-900">증상별로 찾아보세요</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6">
        <div
          v-for="(symptom, index) in symptoms"
          :key="index"
          @click="handleSymptomClick(symptom.label)"
          class="flex flex-col items-center gap-4 p-6 cursor-pointer hover:shadow-lg transition-shadow border border-gray-200 bg-white rounded-xl"
        >
          <div 
            class="w-12 h-12 rounded-full flex items-center justify-center"
            :class="symptom.color"
          >
            <component :is="symptom.icon" class="w-6 h-6" />
          </div>
          <div class="text-center">
            <p class="text-sm font-semibold mb-1 text-gray-900">{{ symptom.label }}</p>
            <p class="text-xs text-gray-500">{{ symptom.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16 px-4 bg-white">
      <div class="max-w-7xl mx-auto">
        <h2 class="mb-12 text-center text-3xl font-bold text-gray-900">DrugSafe의 특별한 기능</h2>
        <div class="grid md:grid-cols-3 gap-8">
          
          <div class="p-6 border border-gray-200 rounded-xl bg-white shadow-sm">
            <div class="w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center mb-4">
              <Search class="w-6 h-6 text-blue-600" />
            </div>
            <h3 class="mb-2 font-bold text-lg text-gray-900">정확한 검색</h3>
            <p class="text-gray-500">
              증상이나 약품명으로 정확한 의약품 정보를 빠르게 찾을 수 있습니다.
            </p>
          </div>

          <div class="p-6 border border-gray-200 rounded-xl bg-white shadow-sm">
            <div class="w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center mb-4">
              <Heart class="w-6 h-6 text-blue-600" />
            </div>
            <h3 class="mb-2 font-bold text-lg text-gray-900">복용 관리</h3>
            <p class="text-gray-500">
              복용 중인 약을 관리하고 일일 복용 여부를 체크할 수 있습니다.
            </p>
          </div>

          <div class="p-6 border border-gray-200 rounded-xl bg-white shadow-sm">
            <div class="w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center mb-4">
              <Pill class="w-6 h-6 text-blue-600" />
            </div>
            <h3 class="mb-2 font-bold text-lg text-gray-900">약물 상호작용 확인</h3>
            <p class="text-gray-500">
              복용 중인 약물 간의 상호작용을 확인하여 안전한 복용을 도와줍니다.
            </p>
          </div>

        </div>
      </div>
    </section>

    <section class="py-16 px-4 bg-gradient-to-br from-blue-600 to-blue-700 text-white">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="mb-4 text-3xl font-bold text-white">안전하고 정확한 의약품 정보</h2>
        <p class="mb-8 text-blue-100 text-lg">
          DrugSafe와 함께 건강을 지키세요.
        </p>
      </div>
    </section>
  </div>
</template>