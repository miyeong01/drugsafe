<template>
  <div class="min-h-screen py-8 px-4">
    <div class="max-w-4xl mx-auto">

      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="mb-4">자주 묻는 질문</h1>
        <p class="text-muted-foreground mb-8">
          DrugSafe 이용에 대한 궁금증을 해결해드립니다.
        </p>

        <!-- Search -->
        <div class="max-w-xl mx-auto relative">
          <Search
            class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground"
          />
          <Input
            type="text"
            placeholder="궁금한 내용을 검색하세요..."
            class="pl-10"
            v-model="searchQuery"
          />
        </div>
      </div>

      <!-- FAQ List -->
      <div v-if="filteredFAQs.length > 0" class="space-y-8">
        <div
          v-for="category in filteredFAQs"
          :key="category.category"
        >
          <h2 class="mb-4">{{ category.category }}</h2>

          <Card class="overflow-hidden">
            <Accordion type="single" collapsible>
              <AccordionItem
                v-for="item in category.items"
                :key="item.id"
                :value="item.id"
              >
                <AccordionTrigger
                  class="px-6 hover:no-underline hover:bg-muted"
                >
                  {{ item.question }}
                </AccordionTrigger>
                <AccordionContent class="px-6 pb-4 text-muted-foreground">
                  {{ item.answer }}
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </Card>
        </div>
      </div>

      <!-- Empty State -->
      <Card v-else class="p-12 text-center">
        <p class="text-muted-foreground">
          검색 결과가 없습니다. 다른 키워드로 검색해보세요.
        </p>
      </Card>

      <!-- Contact -->
      <Card
        class="p-8 mt-12 bg-gradient-to-br from-blue-50 to-white border-primary/20"
      >
        <div class="text-center">
          <h3 class="mb-2">문제가 해결되지 않으셨나요?</h3>
          <p class="text-muted-foreground mb-6">
            고객센터로 문의해주시면 친절하게 도와드리겠습니다.
          </p>

          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <div class="flex items-center gap-2 text-muted-foreground">
              <span>📧</span>
              <span>support@drugsafe.com</span>
            </div>
            <div class="flex items-center gap-2 text-muted-foreground">
              <span>📞</span>
              <span>1588-0000</span>
            </div>
          </div>
        </div>
      </Card>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Search } from 'lucide-vue-next'

import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'

const searchQuery = ref('')

const faqCategories = [
  {
    category: '서비스 이용',
    items: [
      {
        id: 'service-1',
        question: 'DrugSafe는 어떤 서비스인가요?',
        answer:
          'DrugSafe는 안전하고 정확한 의약품 정보를 제공하는 서비스입니다. 증상에 맞는 의약품을 검색하고, 다른 사용자들의 리뷰를 확인하며, 복용 중인 약을 관리할 수 있습니다.',
      },
      {
        id: 'service-2',
        question: '회원가입은 어떻게 하나요?',
        answer:
          '상단 메뉴의 "로그인" 버튼을 클릭한 후, "회원가입" 탭을 선택하여 필요한 정보를 입력하시면 됩니다. 이메일 인증을 완료하면 바로 서비스를 이용하실 수 있습니다.',
      },
      {
        id: 'service-3',
        question: '서비스 이용 요금이 있나요?',
        answer:
          'DrugSafe의 모든 기본 서비스는 무료로 제공됩니다. 의약품 검색, 리뷰 작성 및 확인, 복용 관리 등 모든 기능을 무료로 이용하실 수 있습니다.',
      },
    ],
  },
  {
    category: '의약품 검색',
    items: [
      {
        id: 'search-1',
        question: '의약품은 어떻게 검색하나요?',
        answer:
          '메인 페이지의 검색창에 증상이나 약품명을 입력하시거나, 증상 카테고리 아이콘을 클릭하여 관련 의약품을 찾으실 수 있습니다.',
      },
      {
        id: 'search-2',
        question: '검색 결과가 정확한가요?',
        answer:
          '모든 의약품 정보는 식품의약품안전처의 공식 데이터를 기반으로 제공되므로 신뢰할 수 있습니다.',
      },
      {
        id: 'search-3',
        question: '처방전 필요한 약도 검색할 수 있나요?',
        answer:
          '네, 처방전이 필요한 전문의약품도 검색이 가능합니다. 다만 의사의 처방이 필요합니다.',
      },
    ],
  },
  {
    category: '복용 관리',
    items: [
      {
        id: 'medication-1',
        question: '복용 중인 약은 어떻게 등록하나요?',
        answer:
          '의약품 상세 페이지에서 "복용 추가" 버튼을 클릭하여 복용 기간과 횟수를 설정하실 수 있습니다.',
      },
      {
        id: 'medication-2',
        question: '복용 알림 기능이 있나요?',
        answer:
          '현재는 웹에서 수동으로 복용 체크를 하는 기능만 제공되고 있습니다.',
      },
      {
        id: 'medication-3',
        question: '복용 기록은 얼마나 보관되나요?',
        answer:
          '복용 기록은 별도로 삭제하지 않는 한 계속 보관됩니다.',
      },
    ],
  },
]

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
