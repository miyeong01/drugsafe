<script setup>
import { ref, computed } from 'vue'
import { Search } from 'lucide-vue-next'

const searchQuery = ref('')

// 데이터 정의 (내용은 그대로 유지)
const faqCategories = [
  {
    category: '서비스 이용',
    items: [
      {
        id: 'service-1',
        question: 'DrugSafe는 어떤 서비스인가요?',
        answer: 'DrugSafe는 안전하고 정확한 의약품 정보를 제공하는 서비스입니다. 증상에 맞는 의약품을 검색하고, 다른 사용자들의 리뷰를 확인하며, 자주 복용하는 약을 관리할 수 있습니다.',
      },
      {
        id: 'service-2',
        question: '회원가입은 어떻게 하나요?',
        answer: '상단 메뉴의 "회원가입" 버튼을 클릭한 후, 필요한 정보를 입력하시면 바로 서비스를 이용하실 수 있습니다.',
      },
      {
        id: 'service-3',
        question: '서비스 이용 요금이 있나요?',
        answer: 'DrugSafe의 모든 기본 서비스는 무료로 제공됩니다. 의약품 검색, 리뷰 작성 및 확인, 즐겨찾기 등 모든 기능을 무료로 이용하실 수 있습니다.',
      },
    ],
  },
  {
    category: '의약품 검색',
    items: [
      {
        id: 'search-1',
        question: '의약품은 어떻게 검색하나요?',
        answer: '메인 페이지의 검색창에 증상이나 약품명을 입력하시거나, 증상 카테고리 아이콘을 클릭하여 관련 의약품을 찾으실 수 있습니다.',
      },
      {
        id: 'search-2',
        question: '검색 결과가 정확한가요?',
        answer: '모든 의약품 정보는 식품의약품안전처의 공식 데이터를 기반으로 제공되므로 신뢰할 수 있습니다.',
      },
      {
        id: 'search-3',
        question: '처방전 필요한 약도 검색할 수 있나요?',
        answer: '네, 처방전이 필요한 전문의약품도 검색이 가능합니다. 다만 의사의 처방이 필요합니다.',
      },
    ],
  },
  {
    category: '즐겨찾기',
    items: [
      {
        id: 'medication-1',
        question: '복용 중인 약은 어떻게 등록하나요?',
        answer: '의약품 상세 페이지에서 "즐겨찾기" 버튼을 클릭하여 설정하실 수 있습니다.',
      },
    ],
  },
]

// 검색 필터 로직 (그대로 유지)
const filteredFAQs = computed(() => {
  return faqCategories
    .map((cat) => ({
      ...cat,
      items: cat.items.filter(
        (item) =>
          item.question.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          item.answer.toLowerCase().includes(searchQuery.value.toLowerCase())
      ),
    }))
    .filter((cat) => cat.items.length > 0)
})
</script>

<template>
  <div class="min-vh-100 py-5 bg-light">
    <div class="container" style="max-width: 900px;">

      <div class="text-center mb-5">
        <h1 class="fw-bold display-6 mb-3">자주 묻는 질문</h1>
        <p class="text-secondary mb-5">
          DrugSafe 이용에 대한 궁금증을 해결해드립니다.
        </p>

        <div class="mx-auto position-relative" style="max-width: 600px;">
          <Search 
            class="position-absolute text-secondary" 
            :size="20"
            style="left: 1.25rem; top: 50%; transform: translateY(-50%); z-index: 5;"
          />
          <input
            type="text"
            class="form-control form-control-lg border-0 shadow-sm rounded-pill"
            style="padding-left: 3.5rem;"
            placeholder="궁금한 내용을 검색하세요..."
            v-model="searchQuery"
          />
        </div>
      </div>

      <div v-if="filteredFAQs.length > 0">
        <div v-for="category in filteredFAQs" :key="category.category" class="mb-5">
          
          <h2 class="h5 fw-bold mb-3 ms-1 text-primary">{{ category.category }}</h2>

          <div class="accordion shadow-sm rounded overflow-hidden" :id="'accordion-' + category.category.replace(/\s/g, '')">
            
            <div 
              class="accordion-item border-0 border-bottom" 
              v-for="item in category.items" 
              :key="item.id"
            >
              <h2 class="accordion-header" :id="'heading-' + item.id">
                <button 
                  class="accordion-button collapsed fw-medium py-3" 
                  type="button" 
                  data-bs-toggle="collapse" 
                  :data-bs-target="'#collapse-' + item.id" 
                  aria-expanded="false" 
                  :aria-controls="'collapse-' + item.id"
                >
                  {{ item.question }}
                </button>
              </h2>
              <div 
                :id="'collapse-' + item.id" 
                class="accordion-collapse collapse" 
                :aria-labelledby="'heading-' + item.id"
                :data-bs-parent="'#accordion-' + category.category.replace(/\s/g, '')"
              >
                <div class="accordion-body text-secondary bg-light bg-opacity-50 lh-base">
                  {{ item.answer }}
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>

      <div v-else class="card border-0 shadow-sm p-5 text-center mb-5">
        <p class="text-secondary mb-0 fs-5">
          검색 결과가 없습니다. 다른 키워드로 검색해보세요.
        </p>
      </div>

      <div class="card border border-primary border-opacity-25 bg-white shadow-sm mt-5 overflow-hidden">
        <div class="card-body p-5 text-center bg-gradient" style="background: linear-gradient(135deg, #f8f9fa 0%, #e7f1ff 100%);">
          <h3 class="h4 fw-bold mb-2">문제가 해결되지 않으셨나요?</h3>
          <p class="text-secondary mb-4">
            고객센터로 문의해주시면 친절하게 도와드리겠습니다.
          </p>

          <div class="d-flex flex-column flex-sm-row gap-4 justify-content-center">
            <div class="d-flex align-items-center justify-content-center gap-2 text-secondary">
              <span>📧</span>
              <span class="fw-medium">support@drugsafe.com</span>
            </div>
            <div class="d-flex align-items-center justify-content-center gap-2 text-secondary">
              <span>📞</span>
              <span class="fw-medium">1588-0000</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* 아코디언 버튼 클릭 시(열렸을 때) 배경색과 글자색 커스텀 */
.accordion-button:not(.collapsed) {
  color: #0d6efd;
  background-color: #f0f7ff;
  box-shadow: none; /* 파란 테두리 제거 */
}

/* 아코디언 버튼 포커스 시 테두리 제거 */
.accordion-button:focus {
  box-shadow: none;
  border-color: rgba(0,0,0,.125);
}

.accordion-item:last-child {
  border-bottom: 0 !important;
}
</style>