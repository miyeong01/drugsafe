<template>
  <div class="min-h-screen py-8 px-4">
    <div class="max-w-7xl mx-auto">

      <!-- Profile Header -->
      <Card class="p-6 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center">
              <span class="text-3xl">👤</span>
            </div>
            <div>
              <h2 class="mb-1">홍길동님</h2>
              <p class="text-muted-foreground">hong@email.com</p>
            </div>
          </div>

          <Button @click="goProfileEdit">
            <Settings class="w-4 h-4 mr-2" />
            설정
          </Button>
        </div>
      </Card>

      <!-- Stats -->
      <div class="grid md:grid-cols-3 gap-4 mb-6">
        <Card class="p-6 text-center">
          <Pill class="w-8 h-8 mx-auto mb-2 text-primary" />
          <div class="mb-1">복용 중인 약</div>
          <p class="text-muted-foreground">{{ currentMedications.length }}개</p>
        </Card>

        <Card class="p-6 text-center">
          <Heart class="w-8 h-8 mx-auto mb-2 text-primary" />
          <div class="mb-1">즐겨찾기</div>
          <p class="text-muted-foreground">{{ favorites.length }}개</p>
        </Card>

        <Card class="p-6 text-center">
          <FileText class="w-8 h-8 mx-auto mb-2 text-primary" />
          <div class="mb-1">작성한 리뷰</div>
          <p class="text-muted-foreground">{{ myReviews.length }}개</p>
        </Card>
      </div>

      <!-- Tabs -->
      <Tabs default-value="medications">
        <TabsList class="mb-6">
          <TabsTrigger value="medications">복용 중인 약</TabsTrigger>
          <TabsTrigger value="favorites">즐겨찾기</TabsTrigger>
          <TabsTrigger value="reviews">내 리뷰</TabsTrigger>
        </TabsList>

        <!-- Current Medications -->
        <TabsContent value="medications">
          <div class="space-y-4">
            <Card
              v-for="med in currentMedications"
              :key="med.id"
              class="p-6"
            >
              <div class="flex items-start justify-between mb-4">
                <div>
                  <h3 class="mb-1">{{ med.name }}</h3>
                  <p class="text-sm text-muted-foreground">
                    {{ med.dosage }} · {{ med.startDate }} ~ {{ med.endDate }}
                  </p>
                </div>
                <Button variant="outline" size="sm">
                  상세보기
                </Button>
              </div>

              <!-- Progress -->
              <div class="mb-4">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm">복용 진행률</span>
                  <span class="text-sm text-primary">{{ med.progress }}%</span>
                </div>
                <Progress :value="med.progress" />
              </div>

              <!-- Daily Checklist -->
              <div>
                <p class="text-sm mb-2">오늘의 복용</p>
                <div class="flex gap-3">
                  <button
                    v-for="(checked, index) in med.checklist"
                    :key="index"
                    class="flex items-center gap-2 px-4 py-2 rounded-lg border transition-colors"
                    :class="checked
                      ? 'bg-primary/10 border-primary text-primary'
                      : 'border-border hover:bg-muted'"
                  >
                    <CheckCircle2
                      v-if="checked"
                      class="w-4 h-4"
                    />
                    <Circle
                      v-else
                      class="w-4 h-4"
                    />
                    <span class="text-sm">{{ times[index] }}</span>
                  </button>
                </div>
              </div>
            </Card>
          </div>
        </TabsContent>

        <!-- Favorites -->
        <TabsContent value="favorites">
          <div class="grid md:grid-cols-2 gap-4">
            <Card
              v-for="fav in favorites"
              :key="fav.id"
              class="p-4 hover:shadow-md transition-shadow cursor-pointer"
            >
              <div class="flex gap-4">
                <div class="w-16 h-16 bg-muted rounded-lg flex items-center justify-center shrink-0">
                  <span class="text-2xl">💊</span>
                </div>

                <div class="flex-1">
                  <h4 class="mb-1">{{ fav.name }}</h4>
                  <p class="text-sm text-muted-foreground mb-2">
                    {{ fav.manufacturer }}
                  </p>
                  <span class="px-2 py-0.5 bg-secondary text-secondary-foreground rounded text-sm">
                    {{ fav.type }}
                  </span>
                </div>

                <Button variant="ghost" size="icon">
                  <Heart class="w-5 h-5 fill-primary text-primary" />
                </Button>
              </div>
            </Card>
          </div>
        </TabsContent>

        <!-- My Reviews -->
        <TabsContent value="reviews">
          <div class="space-y-4">
            <Card
              v-for="review in myReviews"
              :key="review.id"
              class="p-6"
            >
              <div class="flex items-start justify-between mb-3">
                <div>
                  <h4 class="mb-1">{{ review.drugName }}</h4>
                  <div class="flex items-center gap-2">
                    <div class="flex">
                      <span
                        v-for="i in 5"
                        :key="i"
                        :class="i <= review.rating
                          ? 'text-yellow-400'
                          : 'text-gray-300'"
                      >
                        ★
                      </span>
                    </div>
                    <span class="text-sm text-muted-foreground">
                      {{ review.date }}
                    </span>
                  </div>
                </div>

                <Button
                  variant="outline"
                  size="sm"
                  @click="goCommunity"
                >
                  수정
                </Button>
              </div>

              <p class="mb-3">{{ review.content }}</p>
              <p class="text-sm text-muted-foreground">
                도움이 돼요 {{ review.likes }}
              </p>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  </div>
</template>

<script setup>
import {
  Heart,
  Pill,
  FileText,
  Settings,
  CheckCircle2,
  Circle,
} from 'lucide-vue-next'

import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

const props = defineProps({
  onNavigate: {
    type: Function,
    required: true,
  },
})

const times = ['아침', '점심', '저녁']

const currentMedications = [
  {
    id: '1',
    name: '타이레놀정 500mg',
    dosage: '1일 3회',
    startDate: '2025.01.01',
    endDate: '2025.01.14',
    progress: 60,
    checklist: [true, true, false],
  },
  {
    id: '2',
    name: '비타민 D',
    dosage: '1일 1회',
    startDate: '2025.01.01',
    endDate: '2025.03.31',
    progress: 10,
    checklist: [true],
  },
  {
    id: '3',
    name: '종합비타민',
    dosage: '1일 2회',
    startDate: '2025.01.01',
    endDate: '2025.02.28',
    progress: 15,
    checklist: [true, false],
  },
]

const favorites = [
  {
    id: '1',
    name: '타이레놀정 500mg',
    manufacturer: '한국얀센',
    type: '해열진통제',
  },
  {
    id: '2',
    name: '게보린정',
    manufacturer: '삼진제약',
    type: '해열진통제',
  },
  {
    id: '3',
    name: '어린이부루펜시럽',
    manufacturer: '삼일제약',
    type: '해열진통제',
  },
]

const myReviews = [
  {
    id: '1',
    drugName: '타이레놀정 500mg',
    rating: 5,
    content: '두통에 정말 효과가 좋았어요.',
    date: '2025.01.15',
    likes: 24,
  },
  {
    id: '2',
    drugName: '게보린정',
    rating: 4,
    content: '효과는 좋은데 식후 복용 추천',
    date: '2025.01.10',
    likes: 18,
  },
]

function goProfileEdit() {
  props.onNavigate('profile-edit')
}

function goCommunity() {
  props.onNavigate('community')
}
</script>
