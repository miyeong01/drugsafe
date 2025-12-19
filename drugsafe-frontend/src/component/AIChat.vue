<script setup>
import { ref } from 'vue'
// 아이콘 라이브러리 (설치 필요: npm install lucide-vue-next)
import { X, Send } from 'lucide-vue-next'

const isOpen = ref(false)
const message = ref('')
const messages = ref([
  {
    role: 'ai',
    text: '안녕하세요! DrugSafe AI 도우미입니다. 증상에 대해 말씀해주시면 적합한 의약품을 추천해드리겠습니다.'
  }
])

const handleSend = () => {
  if (message.value.trim()) {
    // 사용자 메시지 추가
    messages.value.push({ role: 'user', text: message.value })
    const userMsg = message.value // 임시 저장
    message.value = '' // 입력창 초기화
    
    // AI 응답 시뮬레이션
    setTimeout(() => {
      messages.value.push({ 
        role: 'ai', 
        text: '증상에 대해 더 자세히 알려주시면 적합한 의약품을 추천해드리겠습니다.' 
      })
    }, 1000)
  }
}

// Vue에서는 keyup 이벤트를 템플릿에서 바로 처리할 수 있어 별도 함수가 거의 필요 없지만,
// 로직이 복잡해질 경우를 대비해 script에 둘 수도 있습니다.
// 여기선 템플릿의 @keyup.enter.exact="handleSend"로 대체합니다.
</script>

<template>
  <button
    v-if="!isOpen"
    @click="isOpen = true"
    class="fixed bottom-6 right-6 w-14 h-14 bg-white rounded-full shadow-lg flex items-center justify-center hover:shadow-xl transition-shadow z-50"
    aria-label="AI 도우미 열기"
  >
    <img 
      src="@/assets/ai-avatar.png" 
      alt="AI 도우미"
      class="w-8 h-8"
      onerror="this.style.display='none'" 
    />
    </button>

  <div v-if="isOpen" class="fixed bottom-6 right-6 w-[400px] h-[600px] bg-white rounded-2xl shadow-2xl flex flex-col z-50">
    
    <div class="flex items-center justify-between px-5 py-4 bg-blue-500 rounded-t-2xl">
      <div class="flex items-center gap-3">
        <img 
          src="@/assets/ai-avatar.png"
          alt="AI 도우미"
          class="w-10 h-10 bg-white rounded-full"
        />
        <div>
          <h2 class="text-white font-bold">DrugSafe AI</h2>
          <p class="text-blue-100 text-sm">의약품 추천 도우미</p>
        </div>
      </div>
      <button
        @click="isOpen = false"
        class="text-white hover:text-blue-100 transition-colors"
        aria-label="닫기"
      >
        <X class="w-5 h-5" />
      </button>
    </div>

    <div class="flex-1 overflow-y-auto p-5 space-y-4 bg-gray-50">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="flex"
        :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div v-if="msg.role === 'ai'" class="flex gap-2 max-w-[85%]">
          <img 
            src="@/assets/ai-avatar.png"
            alt="AI"
            class="w-8 h-8 flex-shrink-0 bg-white rounded-full"
          />
          <div class="bg-white rounded-2xl rounded-tl-none px-4 py-3 shadow-sm border border-gray-100">
            <p class="text-gray-800 text-sm leading-relaxed">{{ msg.text }}</p>
          </div>
        </div>

        <div v-if="msg.role === 'user'" class="bg-blue-500 text-white rounded-2xl rounded-tr-none px-4 py-3 max-w-[85%] shadow-sm">
          <p class="text-sm leading-relaxed">{{ msg.text }}</p>
        </div>
      </div>
    </div>

    <div class="p-4 border-t border-gray-100 bg-white rounded-b-2xl">
      <div class="flex items-center gap-2">
        <input
          type="text"
          v-model="message"
          @keyup.enter.exact="handleSend"
          placeholder="증상이나 질문을 입력하세요..."
          class="flex-1 px-4 py-3 text-sm border border-gray-200 rounded-full outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all"
        />
        <button
          @click="handleSend"
          :disabled="!message.trim()"
          class="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white rounded-full p-3 transition-colors flex items-center justify-center"
          aria-label="전송"
        >
          <Send class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 스크롤바 커스텀 (선택사항) */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}
.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}
.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 3px;
}
</style>