<template>
  <div class="min-h-screen py-8 px-4">
    <div class="max-w-7xl mx-auto">

      <!-- Search Header -->
      <div class="mb-6">
        <div class="flex gap-2 mb-4">
          <div class="flex-1 relative">
            <Search
              class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground"
            />
            <Input
              type="text"
              placeholder="증상이나 약품명을 검색하세요..."
              class="pl-10"
              v-model="keyword"
            />
          </div>
          <Button>검색</Button>
        </div>

        <p class="text-muted-foreground">
          <span class="text-primary">
            '{{ keyword || "두통" }}'
          </span>
          에 대한 검색 결과 {{ mockDrugs.length }}건
        </p>
      </div>

      <div class="flex gap-6">

        <!-- Sidebar Filters -->
        <aside class="w-64 shrink-0 hidden lg:block">
          <Card class="p-6 sticky top-24">
            <div class="flex items-center gap-2 mb-4">
              <SlidersHorizontal class="w-5 h-5" />
              <h3>필터</h3>
            </div>

            <div class="space-y-6">
              <div>
                <h4 class="mb-3">제형</h4>

                <div class="space-y-2">
                  <label
                    v-for="(value, key) in filters"
                    :key="key"
                    class="flex items-center gap-2 cursor-pointer"
                  >
                    <Checkbox
                      :checked="value"
                      @update:checked="filters[key] = $event"
                    />
                    <span>{{ formLabels[key] }}</span>
                  </label>
                </div>
              </div>

              <Button
                variant="outline"
                class="w-full"
                @click="resetFilters"
              >
                필터 초기화
              </Button>
            </div>
          </Card>
        </aside>

        <!-- Results -->
        <div class="flex-1">

          <!-- Sort -->
          <div class="flex items-center justify-between mb-4">
            <p class="text-sm text-muted-foreground">
              총 {{ mockDrugs.length }}개의 의약품
            </p>

            <Select v-model="sortBy">
              <SelectTrigger class="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="relevance">관련도순</SelectItem>
                <SelectItem value="rating">평점 높은순</SelectItem>
                <SelectItem value="reviews">리뷰 많은순</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <!-- Drug List -->
          <div class="space-y-4">
            <Card
              v-for="drug in mockDrugs"
              :key="drug.id"
              class="p-4 hover:shadow-md transition-shadow cursor-pointer"
              @click="goDetail(drug.id)"
            >
              <div class="flex gap-4">

                <div class="w-24 h-24 bg-muted rounded-lg flex items-center justify-center shrink-0">
                  <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
                    <span class="text-primary">💊</span>
                  </div>
                </div>

                <div class="flex-1">
                  <h3 class="mb-1">{{ drug.name }}</h3>
                  <p class="text-sm text-muted-foreground mb-2">
                    {{ drug.manufacturer }} · {{ drug.type }}
                  </p>

                  <div class="flex items-center gap-2 mb-2">
                    <div class="flex items-center gap-1">
                      <Star class="w-4 h-4 fill-yellow-400 text-yellow-400" />
                      <span>{{ drug.rating }}</span>
                    </div>
                    <span class="text-sm text-muted-foreground">
                      리뷰 {{ drug.reviewCount.toLocaleString() }}
                    </span>
                    <span class="px-2 py-0.5 bg-secondary text-secondary-foreground rounded text-sm">
                      {{ drug.form }}
                    </span>
                  </div>
                </div>

                <div class="flex flex-col justify-between items-end">
                  <Button
                    variant="outline"
                    size="sm"
                    @click.stop
                  >
                    즐겨찾기
                  </Button>
                </div>

              </div>
            </Card>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Search, SlidersHorizontal, Star } from 'lucide-vue-next'

import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

const props = defineProps({
  onNavigate: {
    type: Function,
    required: true,
  },
  searchQuery: {
    type: String,
    default: '',
  },
})

const keyword = ref(props.searchQuery)

const sortBy = ref('relevance')

const filters = reactive({
  powder: false,
  lotion: false,
  cream: false,
  tablet: false,
  syrup: false,
  liquid: false,
  spray: false,
  patch: false,
  ointment: false,
  film: false,
})

const formLabels = {
  powder: '가루',
  lotion: '로션',
  cream: '크림',
  tablet: '알약',
  syrup: '시럽',
  liquid: '액상',
  spray: '스프레이',
  patch: '부착형',
  ointment: '연고',
  film: '필름',
}

const mockDrugs = [
  {
    id: '1',
    name: '타이레놀정 500mg',
    manufacturer: '한국얀센',
    type: '해열진통제',
    form: '정제',
    rating: 4.5,
    reviewCount: 1234,
  },
  {
    id: '2',
    name: '게보린정',
    manufacturer: '삼진제약',
    type: '해열진통제',
    form: '정제',
    rating: 4.3,
    reviewCount: 892,
  },
  {
    id: '3',
    name: '어린이부루펜시럽',
    manufacturer: '삼일제약',
    type: '해열진통제',
    form: '시럽',
    rating: 4.7,
    reviewCount: 567,
  },
]

function resetFilters() {
  Object.keys(filters).forEach(key => {
    filters[key] = false
  })
}

function goDetail(id) {
  props.onNavigate('detail', id)
}
</script>
