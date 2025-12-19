<template>
  <div className="min-h-screen py-8 px-4">
    <div className="max-w-4xl mx-auto">

      <!-- Back Button -->
      <Button
        variant="ghost"
        className="mb-6"
        @click="onNavigate('community')"
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        목록으로
      </Button>

      <!-- Review Card -->
      <Card className="p-8 mb-6">
        <!-- Header -->
        <div className="flex items-start justify-between mb-6">
          <div className="flex items-start gap-4 flex-1">
            <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center shrink-0">
              <span className="text-xl">{{ review.authorAvatar }}</span>
            </div>

            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span>{{ review.author }}</span>
                <span className="text-muted-foreground">·</span>
                <span className="text-muted-foreground text-sm">{{ review.date }}</span>
              </div>

              <div className="flex items-center gap-2">
                <div className="flex">
                  <span
                    v-for="i in 5"
                    :key="i"
                    :class="i <= review.rating ? 'text-yellow-400' : 'text-gray-300'"
                  >
                    ★
                  </span>
                </div>
                <span className="text-sm text-muted-foreground">
                  조회 {{ review.views }}
                </span>
              </div>
            </div>
          </div>

          <Button variant="ghost" size="icon">
            <MoreVertical className="w-4 h-4" />
          </Button>
        </div>

        <!-- Drug Info -->
        <div className="inline-flex items-center gap-2 px-3 py-1 bg-secondary rounded-lg mb-4">
          <span className="text-sm">약품명:</span>
          <button
            className="text-sm text-primary hover:underline"
            @click="onNavigate('detail')"
          >
            {{ review.drugName }}
          </button>
        </div>

        <!-- Title -->
        <h1 className="mb-4">{{ review.title }}</h1>

        <!-- Content -->
        <div className="prose max-w-none mb-6">
          <p className="whitespace-pre-wrap text-foreground">
            {{ review.content }}
          </p>
        </div>

        <!-- Actions -->
        <div className="flex items-center gap-3 pt-6 border-t border-border">
          <Button variant="outline" className="gap-2">
            <ThumbsUp className="w-4 h-4" />
            도움이 돼요 {{ review.helpful }}
          </Button>
          <Button variant="outline" className="gap-2">
            <Share2 className="w-4 h-4" />
            공유하기
          </Button>
        </div>
      </Card>

      <!-- Comments -->
      <Card className="p-6 mb-6">
        <h3 className="mb-4">
          댓글 <span className="text-primary">{{ comments.length }}</span>
        </h3>

        <!-- Comment Input -->
        <div className="mb-6">
          <Textarea
            v-model="newComment"
            placeholder="댓글을 입력하세요..."
            rows="3"
            className="mb-2"
          />
          <div className="flex justify-end">
            <Button @click="handleSubmitComment">
              댓글 작성
            </Button>
          </div>
        </div>

        <!-- Comment List -->
        <div className="space-y-4">
          <div
            v-for="comment in comments"
            :key="comment.id"
            className="flex gap-3 p-4 bg-muted rounded-lg"
          >
            <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center shrink-0">
              <span>👤</span>
            </div>

            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <span>{{ comment.author }}</span>
                <span className="text-sm text-muted-foreground">
                  {{ comment.date }}
                </span>
              </div>

              <p className="mb-2">{{ comment.content }}</p>

              <Button variant="ghost" size="sm" className="gap-1">
                <ThumbsUp className="w-3 h-3" />
                {{ comment.likes }}
              </Button>
            </div>
          </div>
        </div>
      </Card>

      <!-- Related Reviews -->
      <Card className="p-6">
        <h3 className="mb-4">관련 리뷰</h3>

        <div className="space-y-3">
          <button
            v-for="item in relatedReviews"
            :key="item.id"
            className="w-full text-left p-4 rounded-lg hover:bg-muted transition-colors"
            @click="onNavigate('community')"
          >
            <div className="flex items-start justify-between mb-2">
              <h4>{{ item.title }}</h4>
              <div className="flex">
                <span
                  v-for="i in 5"
                  :key="i"
                  :class="i <= item.rating ? 'text-yellow-400' : 'text-gray-300'"
                  className="text-sm"
                >
                  ★
                </span>
              </div>
            </div>

            <p className="text-sm text-muted-foreground mb-1">
              {{ item.preview }}
            </p>

            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span>{{ item.author }}</span>
              <span>·</span>
              <span>{{ item.date }}</span>
            </div>
          </button>
        </div>
      </Card>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {
  ArrowLeft,
  ThumbsUp,
  Share2,
  MoreVertical,
} from 'lucide-vue-next'

import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'

defineProps({
  onNavigate: {
    type: Function,
    required: true,
  },
})

const newComment = ref('')

const review = {
  id: '1',
  author: '김**',
  authorAvatar: '👤',
  rating: 5,
  date: '2025.01.15',
  title: '타이레놀정 500mg 사용 후기',
  drugName: '타이레놀정 500mg',
  content: `두통에 정말 효과가 좋았어요. 평소 편두통이 심한 편인데, 이 약을 먹고 30분 정도 지나니 통증이 많이 가라앉았습니다.

특히 속이 편한 것도 장점인 것 같아요. 다른 진통제는 속이 쓰린 경우가 있었는데, 타이레놀은 공복에 먹어도 괜찮더라고요.

집에 항상 구비해두고 있습니다. 두통뿐만 아니라 생리통이나 치통에도 효과가 있어서 만능으로 쓰고 있어요.

다만 효과가 너무 좋아서 자주 먹게 되는데, 간에 무리가 갈 수 있다고 해서 용량과 횟수를 잘 지키려고 노력하고 있습니다.`,
  helpful: 24,
  views: 342,
}

const comments = [
  {
    id: '1',
    author: '이**',
    date: '2025.01.16',
    content: '저도 타이레놀 애용자예요! 정말 효과 좋죠. 공감합니다.',
    likes: 5,
  },
  {
    id: '2',
    author: '박**',
    date: '2025.01.16',
    content: '간 건강이 걱정되시면 밀크시슬 같은 영양제를 함께 드시는 것도 좋을 것 같아요.',
    likes: 3,
  },
  {
    id: '3',
    author: '최**',
    date: '2025.01.17',
    content: '좋은 후기 감사합니다. 저도 한번 사용해봐야겠어요!',
    likes: 2,
  },
]

const relatedReviews = [
  {
    id: '2',
    title: '게보린정 효과 있나요?',
    author: '이**',
    rating: 4,
    date: '2025.01.14',
    preview: '두통에 효과는 있는데 졸음이 와서...',
  },
  {
    id: '3',
    title: '펜잘정 사용 후기',
    author: '박**',
    rating: 5,
    date: '2025.01.13',
    preview: '효과 빠르고 좋습니다',
  },
]

function handleSubmitComment() {
  if (!newComment.value.trim()) return
  alert('댓글이 등록되었습니다!')
  newComment.value = ''
}
</script>
