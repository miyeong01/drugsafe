<template>
  <div class="min-h-screen py-8 px-4">
    <div class="max-w-4xl mx-auto">

      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-3">
          <Button
            variant="ghost"
            size="icon"
            @click="onNavigate('profile')"
          >
            <ArrowLeft class="w-4 h-4" />
          </Button>
          <h1>설정</h1>
        </div>
      </div>

      <!-- Tabs -->
      <Tabs default-value="password">
        <TabsList class="mb-6">
          <TabsTrigger value="password">비밀번호 변경</TabsTrigger>
          <TabsTrigger value="favorites">즐겨찾기 관리</TabsTrigger>
          <TabsTrigger value="medications">복용기록 관리</TabsTrigger>
          <TabsTrigger value="reviews">리뷰 관리</TabsTrigger>
        </TabsList>

        <!-- Password -->
        <TabsContent value="password">
          <Card class="p-6">
            <h3 class="mb-6">비밀번호 변경</h3>

            <form class="space-y-4 max-w-md" @submit.prevent="handlePasswordChange">
              <div class="space-y-2">
                <Label>현재 비밀번호</Label>
                <Input type="password" v-model="passwordData.current" required />
              </div>

              <div class="space-y-2">
                <Label>새 비밀번호</Label>
                <Input type="password" v-model="passwordData.new" required />
                <p class="text-sm text-muted-foreground">
                  8자 이상, 영문/숫자/특수문자 조합
                </p>
              </div>

              <div class="space-y-2">
                <Label>새 비밀번호 확인</Label>
                <Input type="password" v-model="passwordData.confirm" required />
              </div>

              <Button type="submit" class="w-full">
                비밀번호 변경
              </Button>
            </form>
          </Card>
        </TabsContent>

        <!-- Favorites -->
        <TabsContent value="favorites">
          <Card class="p-6">
            <h3 class="mb-6">즐겨찾기 관리</h3>

            <div class="space-y-3">
              <div
                v-for="item in favorites"
                :key="item.id"
                class="flex items-center justify-between p-4 rounded-lg border hover:bg-muted"
              >
                <div>
                  <h4>{{ item.name }}</h4>
                  <p class="text-sm text-muted-foreground">{{ item.manufacturer }}</p>
                </div>

                <AlertDialog>
                  <AlertDialogTrigger as-child>
                    <Button variant="ghost" size="icon">
                      <Trash2 class="w-4 h-4 text-destructive" />
                    </Button>
                  </AlertDialogTrigger>

                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>즐겨찾기 삭제</AlertDialogTitle>
                      <AlertDialogDescription>
                        {{ item.name }}을(를) 즐겨찾기에서 삭제하시겠습니까?
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>취소</AlertDialogCancel>
                      <AlertDialogAction
                        @click="handleDeleteItem('즐겨찾기', item.id)"
                      >
                        삭제
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            </div>
          </Card>
        </TabsContent>

        <!-- Medications -->
        <TabsContent value="medications">
          <Card class="p-6">
            <h3 class="mb-6">복용기록 관리</h3>

            <div class="space-y-3">
              <div
                v-for="item in medications"
                :key="item.id"
                class="flex items-center justify-between p-4 rounded-lg border hover:bg-muted"
              >
                <div>
                  <h4>{{ item.name }}</h4>
                  <p class="text-sm text-muted-foreground">{{ item.period }}</p>
                </div>

                <div class="flex gap-2">
                  <Button variant="ghost" size="icon">
                    <Edit class="w-4 h-4" />
                  </Button>

                  <AlertDialog>
                    <AlertDialogTrigger as-child>
                      <Button variant="ghost" size="icon">
                        <Trash2 class="w-4 h-4 text-destructive" />
                      </Button>
                    </AlertDialogTrigger>

                    <AlertDialogContent>
                      <AlertDialogHeader>
                        <AlertDialogTitle>복용기록 삭제</AlertDialogTitle>
                        <AlertDialogDescription>
                          {{ item.name }}의 복용기록을 삭제하시겠습니까?
                        </AlertDialogDescription>
                      </AlertDialogHeader>
                      <AlertDialogFooter>
                        <AlertDialogCancel>취소</AlertDialogCancel>
                        <AlertDialogAction
                          @click="handleDeleteItem('복용기록', item.id)"
                        >
                          삭제
                        </AlertDialogAction>
                      </AlertDialogFooter>
                    </AlertDialogContent>
                  </AlertDialog>
                </div>
              </div>
            </div>
          </Card>
        </TabsContent>

        <!-- Reviews -->
        <TabsContent value="reviews">
          <Card class="p-6">
            <h3 class="mb-6">리뷰 관리</h3>

            <div class="space-y-3">
              <div
                v-for="item in reviews"
                :key="item.id"
                class="flex items-center justify-between p-4 rounded-lg border hover:bg-muted"
              >
                <div class="flex-1">
                  <h4>{{ item.drugName }}</h4>

                  <div class="flex items-center gap-2">
                    <div class="flex">
                      <span
                        v-for="i in 5"
                        :key="i"
                        class="text-sm"
                        :class="i <= item.rating ? 'text-yellow-400' : 'text-gray-300'"
                      >
                        ★
                      </span>
                    </div>
                    <span class="text-sm text-muted-foreground">
                      {{ item.date }}
                    </span>
                  </div>
                </div>

                <div class="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    @click="onNavigate('community')"
                  >
                    <Edit class="w-4 h-4 mr-2" />
                    수정
                  </Button>

                  <AlertDialog>
                    <AlertDialogTrigger as-child>
                      <Button variant="ghost" size="icon">
                        <Trash2 class="w-4 h-4 text-destructive" />
                      </Button>
                    </AlertDialogTrigger>

                    <AlertDialogContent>
                      <AlertDialogHeader>
                        <AlertDialogTitle>리뷰 삭제</AlertDialogTitle>
                        <AlertDialogDescription>
                          작성하신 리뷰를 삭제하시겠습니까?
                        </AlertDialogDescription>
                      </AlertDialogHeader>
                      <AlertDialogFooter>
                        <AlertDialogCancel>취소</AlertDialogCancel>
                        <AlertDialogAction
                          @click="handleDeleteItem('리뷰', item.id)"
                        >
                          삭제
                        </AlertDialogAction>
                      </AlertDialogFooter>
                    </AlertDialogContent>
                  </AlertDialog>
                </div>
              </div>
            </div>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { ArrowLeft, Trash2, Edit } from 'lucide-vue-next'

import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'

defineProps({
  onNavigate: {
    type: Function,
    required: true,
  },
})

const passwordData = reactive({
  current: '',
  new: '',
  confirm: '',
})

const favorites = [
  { id: '1', name: '타이레놀정 500mg', manufacturer: '한국얀센' },
  { id: '2', name: '게보린정', manufacturer: '삼진제약' },
  { id: '3', name: '어린이부루펜시럽', manufacturer: '삼일제약' },
]

const medications = [
  { id: '1', name: '타이레놀정 500mg', period: '2025.01.01 ~ 2025.01.14' },
  { id: '2', name: '비타민 D', period: '2025.01.01 ~ 2025.03.31' },
]

const reviews = [
  { id: '1', drugName: '타이레놀정 500mg', date: '2025.01.15', rating: 5 },
  { id: '2', drugName: '게보린정', date: '2025.01.10', rating: 4 },
]

function handlePasswordChange() {
  if (passwordData.new !== passwordData.confirm) {
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }
  alert('비밀번호가 변경되었습니다.')
  passwordData.current = ''
  passwordData.new = ''
  passwordData.confirm = ''
}

function handleDeleteItem(type, id) {
  alert(`${type}이(가) 삭제되었습니다.`)
}
</script>
