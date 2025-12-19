<template>
  <div class="min-h-screen py-8 px-4">
    <div class="max-w-7xl mx-auto">

      <!-- Product Header -->
      <div class="grid md:grid-cols-2 gap-8 mb-8">

        <!-- Image -->
        <div class="bg-white rounded-lg p-8 flex items-center justify-center">
          <div class="w-64 h-64 bg-muted rounded-lg flex items-center justify-center">
            <div class="w-48 h-48 bg-primary/10 rounded-full flex items-center justify-center text-6xl">
              💊
            </div>
          </div>
        </div>

        <!-- Info -->
        <div>
          <div class="mb-4">
            <span class="px-3 py-1 bg-secondary text-secondary-foreground rounded-full text-sm">
              해열진통제
            </span>
          </div>

          <h1 class="mb-2">타이레놀정 500mg</h1>
          <p class="text-muted-foreground mb-4">한국얀센</p>

          <!-- Rating -->
          <div class="flex items-center gap-3 mb-6">
            <div class="flex items-center gap-1">
              <Star
                v-for="i in 5"
                :key="i"
                class="w-5 h-5"
                :class="i <= 4 ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'"
              />
            </div>
            <span>4.5</span>
            <span class="text-muted-foreground">
              ({{ reviewCount.toLocaleString() }}개의 리뷰)
            </span>
          </div>

          <!-- Actions -->
          <div class="flex gap-3 mb-6">
            <Button variant="outline" size="icon">
              <Heart class="w-5 h-5" />
            </Button>
            <Button variant="outline" size="icon">
              <Share2 class="w-5 h-5" />
            </Button>
          </div>

          <!-- Quick Info -->
          <Card class="p-4 bg-muted">
            <div class="grid grid-cols-2 gap-4">
              <InfoItem label="제형" value="정제" />
              <InfoItem label="용량" value="500mg" />
              <InfoItem label="포장단위" value="20정" />
              <InfoItem label="보관방법" value="실온보관" />
            </div>
          </Card>
        </div>
      </div>

      <!-- Tabs -->
      <Tabs default-value="info" class="mb-8">
        <TabsList class="mb-6">
          <TabsTrigger value="info">상세정보</TabsTrigger>
          <TabsTrigger value="usage">용법·용량</TabsTrigger>
          <TabsTrigger value="warnings">주의사항</TabsTrigger>
          <TabsTrigger value="reviews">리뷰</TabsTrigger>
        </TabsList>

        <!-- Reviews -->
        <TabsContent value="reviews">
          <div class="space-y-4">
            <Card
              v-for="review in mockReviews"
              :key="review.id"
              class="p-6"
            >
              <div class="flex items-center gap-2 mb-1">
                <span>{{ review.author }}</span>
                <Star
                  v-for="i in 5"
                  :key="i"
                  class="w-4 h-4"
                  :class="i <= review.rating
                    ? 'fill-yellow-400 text-yellow-400'
                    : 'text-gray-300'"
                />
              </div>

              <p class="text-sm text-muted-foreground mb-3">
                {{ review.date }}
              </p>

              <p class="mb-4">{{ review.content }}</p>

              <div class="flex gap-4">
                <Button variant="ghost" size="sm">
                  도움이 돼요 {{ review.helpful }}
                </Button>
                <Button variant="ghost" size="sm">
                  댓글
                </Button>
              </div>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      <!-- Write Review -->
      <Card class="p-6">
        <h3 class="mb-4">리뷰 작성하기</h3>
        <Button @click="navigateToCommunity">
          <MessageSquare class="w-4 h-4 mr-2" />
          리뷰 작성
        </Button>
      </Card>

    </div>
  </div>
</template>

<script setup>
import {
  Star,
  Heart,
  Share2,
  MessageSquare,
} from 'lucide-vue-next'

import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'

const props = defineProps({
  onNavigate: {
    type: Function,
    required: true,
  },
})

const reviewCount = 1234

const mockReviews = [
  {
    id: '1',
    author: '김**',
    rating: 5,
    date: '2025.01.15',
    content: '두통에 정말 효과가 좋았어요.',
    helpful: 24,
  },
  {
    id: '2',
    author: '이**',
    rating: 4,
    date: '2025.01.10',
    content: '효과는 좋은데 식후 복용 추천',
    helpful: 18,
  },
]

function navigateToCommunity() {
  props.onNavigate('community')
}
</script>
