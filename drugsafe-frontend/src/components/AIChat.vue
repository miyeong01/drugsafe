<script setup>
import { ref, nextTick } from 'vue'
// 아이콘 라이브러리
import { X, Send, Bot, User } from 'lucide-vue-next'

const isOpen = ref(false)
const message = ref('')
const messages = ref([
  {
    role: 'ai',
    text: '안녕하세요! DrugSafe AI 도우미입니다. 증상에 대해 말씀해주시면 적합한 의약품을 추천해드리겠습니다.'
  }
])
const messagesContainer = ref(null)

// 스크롤을 맨 아래로 내리는 함수
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const handleSend = () => {
  if (message.value.trim()) {
    // 사용자 메시지 추가
    messages.value.push({ role: 'user', text: message.value })
    const userMsg = message.value
    message.value = ''
    scrollToBottom()
    
    // AI 응답 시뮬레이션
    setTimeout(() => {
      messages.value.push({ 
        role: 'ai', 
        text: '증상에 대해 더 자세히 알려주시면 적합한 의약품을 추천해드리겠습니다.' 
      })
      scrollToBottom()
    }, 1000)
  }
}
</script>

<template>
  <button
    v-if="!isOpen"
    @click="isOpen = true"
    class="btn btn-light rounded-circle shadow-lg position-fixed bottom-0 end-0 m-4 d-flex align-items-center justify-content-center p-0"
    style="width: 60px; height: 60px; z-index: 1050;"
    aria-label="AI 도우미 열기"
  >
    <Bot :size="32" class="text-primary" />
  </button>

  <div 
    v-if="isOpen" 
    class="card shadow-lg position-fixed bottom-0 end-0 m-4 d-flex flex-column"
    style="width: 380px; height: 600px; z-index: 1050; border-radius: 1rem; overflow: hidden;"
  >
    
    <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center py-3 border-0">
      <div class="d-flex align-items-center gap-2">
        <div class="bg-white rounded-circle d-flex align-items-center justify-content-center text-primary" style="width: 40px; height: 40px;">
          <Bot :size="24" />
        </div>
        <div>
          <h6 class="mb-0 fw-bold">DrugSafe AI</h6>
          <small class="text-white-50">의약품 추천 도우미</small>
        </div>
      </div>
      <button 
        @click="isOpen = false" 
        class="btn btn-link text-white p-0 text-decoration-none"
      >
        <X />
      </button>
    </div>

    <div 
      class="card-body bg-light overflow-auto p-3" 
      ref="messagesContainer"
      style="scroll-behavior: smooth;"
    >
      <div 
        v-for="(msg, index) in messages" 
        :key="index" 
        class="d-flex w-100 mb-3"
        :class="msg.role === 'user' ? 'justify-content-end' : 'justify-content-start'"
      >
        
        <div v-if="msg.role === 'ai'" class="d-flex gap-2" style="max-width: 85%;">
          <div class="flex-shrink-0 bg-white rounded-circle d-flex align-items-center justify-content-center shadow-sm" style="width: 32px; height: 32px;">
            <Bot :size="18" class="text-primary" />
          </div>
          <div class="bg-white p-3 rounded-3 shadow-sm border text-dark">
            {{ msg.text }}
          </div>
        </div>

        <div v-if="msg.role === 'user'" class="bg-primary text-white p-3 rounded-3 shadow-sm" style="max-width: 85%;">
          {{ msg.text }}
        </div>

      </div>
    </div>

    <div class="card-footer bg-white border-top p-3">
      <div class="input-group">
        <input 
          type="text" 
          class="form-control border-end-0 bg-light" 
          placeholder="증상이나 질문을 입력하세요..." 
          v-model="message"
          @keydown.enter.exact="handleSend"
          style="border-radius: 2rem 0 0 2rem;"
        >
        <button 
          class="btn btn-primary border-start-0 px-4" 
          @click="handleSend" 
          :disabled="!message.trim()"
          style="border-radius: 0 2rem 2rem 0;"
        >
          <Send :size="18" />
        </button>
      </div>
    </div>

  </div>
</template>

<style scoped>
/* 모바일 반응형 처리: 화면이 작으면 꽉 차게 */
@media (max-width: 576px) {
  .card.position-fixed {
    width: 100% !important;
    height: 100% !important;
    bottom: 0 !important;
    right: 0 !important;
    margin: 0 !important;
    border-radius: 0 !important;
  }
}
</style>