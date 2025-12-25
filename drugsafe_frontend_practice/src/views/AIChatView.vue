<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { Send, Sparkles, Bot } from 'lucide-vue-next';
import axios from 'axios';


// Props 정의
const props = defineProps({
  onNavigate: {
    type: Function,
    required: true
  }
});

// 상태(State) 관리
const message = ref('');
const messages = ref([
  {
    role: 'ai',
    text: '안녕하세요! DrugSafe AI 도우미입니다.\n증상에 대해 말씀해주시면 적합한 의약품을 추천해드리겠습니다.'
  }
]);
const loading = ref(false);


const messageAreaRef = ref(null);

// 스크롤 하단 이동 함수
const scrollToBottom = async () => {
  await nextTick();
  if (messageAreaRef.value) {
    messageAreaRef.value.scrollTo({
      top: messageAreaRef.value.scrollHeight,
      behavior: 'smooth'
    });
  }
};

watch(messages, () => {
  scrollToBottom();
}, { deep: true });

onMounted(() => {
  scrollToBottom();
});

// 메시지 전송 로직
const handleSend = async (manualMessage = null) => {
  const userMessage = manualMessage || message.value;
  if (!userMessage.trim()) return;

  messages.value.push({ role: 'user', text: userMessage });
  message.value = '';
  loading.value = true;
  
  messages.value.push({
    role: 'ai',
    text: '',
    // type: res.data.type,
    // candidates: res.data.candidates || [], // 후보 리스트
    isStreaming: true,
    status: '입력 중입니다...'
  })
  const aiIndex = messages.value.length -1


  try {
    const res = await axios.post(
      'http://localhost:8000/api/medicines/chatbot/',
      { message: userMessage }
    );
    const answer = res.data.answer;
    messages.value[aiIndex].text = '';
    
    let i = 0;
    const interval = setInterval(() => {
      messages.value[aiIndex].text += answer[i];
      i++;

      if (i >= answer.length){
        clearInterval(interval);
        messages.value[aiIndex].isStreaming = false;
      }
    }, 20)
    messages.value[aiIndex].type = res.data.type;
    messages.value[aiIndex].candidates = res.data.candidates || [];
    messages.value[aiIndex].isStreaming = false;

  } catch (err) {
    messages.value[aiIndex].text = '⚠️ 현재 상담 서비스에 문제가 발생했습니다. 잠시 후 다시 시도해주세요.';
    messages.value[aiIndex].isStreaming = false
  } finally {
    loading.value = false
  }
}

const handleCandidateClick = (candidateName) => {
  handleSend(candidateName)
}

const handleKeyPress = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
};
</script>

<template>
  <div class="chat-page-container">
    <div class="content-wrapper">

      <header class="chat-header">
        <div class="bot-icon-wrapper main-icon">
          <Bot class="bot-icon" />
        </div>
        <h1 class="title">DrugSafe AI 도우미</h1>
        <p class="subtitle">
          증상을 말씀해주시면 적합한 의약품을 추천해드립니다
        </p>
      </header>

      <main class="chat-main-card">

        <div class="message-area" ref="messageAreaRef">
          <div v-for="(msg, index) in messages" :key="index" class="message-row"
            :class="msg.role === 'user' ? 'message-end' : 'message-start'">
            <template v-if="msg.role === 'ai'">
              <div class="bot-avatar">
                <Bot class="small-bot-icon" />
              </div>

              <div class="ai-container">
                <div v-if="msg.isStreaming" class="ai-status">
                  <span class="spinner"></span>
                  {{ msg.status || '답변을 생성 중입니다...' }}
                </div>

                <div class="message-bubble ai-bubble">
                  <p>{{ msg.text }}</p>
                </div>

                <div v-if="msg.type === 'multiple'" class="candidate-wrapper">
                  <div v-for="drug in msg.candidates" :key="drug.id" class="candidate-card"
                    @click="handleCandidateClick(drug.name)">
                    <span class="drug-name">{{ drug.name }}</span>
                    <span class="click-hint">클릭하여 선택</span>
                  </div>
                </div>
              </div>
            </template>

            <template v-else>
              <div class="message-bubble user-bubble">
                <p>{{ msg.text }}</p>
              </div>
            </template>
          </div>
          <div ref="messagesEndRef"></div>
        </div>

        <!-- <div class="quick-questions-area">
          <p class="quick-questions-title">자주 묻는 질문:</p>
          <div class="quick-questions-buttons">
            <button
              v-for="(question, index) in quickQuestions"
              :key="index"
              @click="handleQuickQuestion(question)"
              class="question-btn"
            >
              {{ question }}
            </button>
          </div>
        </div> -->


        <div class="input-area">
          <div class="input-wrapper">
            <input type="text" v-model="message" @keydown="handleKeyPress" placeholder="증상이나 궁금하신 의약품 이름을 입력하세요..."
              class="chat-input" />
            <button @click="handleSend()" :disabled="!message.trim()" class="send-btn">
              <Send class="send-icon" />
            </button>
          </div>
        </div>
      </main>

      <footer class="info-cards">
        <div class="info-card">
          <div class="info-card-header">
            <Sparkles class="sparkle-icon" />
            <h4>정확한 추천</h4>
          </div>
          <p>증상을 자세히 설명하면 더 정확한 의약품을 추천받을 수 있습니다</p>
        </div>

        <div class="info-card">
          <div class="info-card-header">
            <Sparkles class="sparkle-icon" />
            <h4>24시간 이용</h4>
          </div>
          <p>언제든지 AI 도우미에게 의약품에 대해 질문하세요</p>
        </div>

        <div class="info-card">
          <div class="info-card-header">
            <Sparkles class="sparkle-icon" />
            <h4>안전한 정보</h4>
          </div>
          <p>검증된 의약품 정보를 기반으로 안전하게 추천합니다</p>
        </div>
      </footer>

    </div>
  </div>
</template>

<style scoped>
/* 색상 변수 정의 */
:root {
  --primary-blue: #4D9FFF;
  --hover-blue: #3A8FEF;
  --pastel-bg: #F0F7FF;
  --light-border: #E5F0FF;
  --text-dark: #1a202c;
  --text-gray: #718096;
}

/* 전체 레이아웃 */
.chat-page-container {
  min-height: 100vh;
  background-color: var(--pastel-bg, #F0F7FF);
  /* 파스텔톤 하늘색 배경 */
  padding: 2.5rem 1rem;
  box-sizing: border-box;
}

.content-wrapper {
  max-width: 56rem;
  /* max-w-4xl */
  margin: 0 auto;
}

/* 헤더 */
.chat-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.bot-icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: var(--primary-blue, #4D9FFF);
  margin-bottom: 1rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.main-icon {
  width: 4rem;
  height: 4rem;
}

.bot-icon {
  width: 2.5rem;
  height: 2.5rem;
  color: white;
}

.title {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--text-dark, #1a202c);
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.125rem;
  color: var(--text-gray, #718096);
}

/* 메인 채팅 카드 */
.chat-main-card {
  background-color: white;
  border-radius: 30px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

/* 메시지 영역 */
.message-area {
  height: 500px;
  overflow-y: auto;
  padding: 2rem;
  background-color: white;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.message-row {
  display: flex;
  gap: 1rem;
  max-width: 85%;
}

.message-start {
  justify-content: flex-start;
}

.message-end {
  justify-content: flex-end;
  align-self: flex-end;
}

.bot-avatar {
  width: 3rem;
  height: 3rem;
  background-color: var(--primary-blue, #4D9FFF);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.small-bot-icon {
  width: 1.75rem;
  height: 1.75rem;
  color: white;
}

.message-bubble {
  padding: 1rem 1.5rem;
  border-radius: 1.5rem;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.message-bubble p {
  font-size: 1.125rem;
  line-height: 1.625;
  white-space: pre-wrap;
  margin: 0;
}

.ai-bubble {
  background-color: white;
  border: 2px solid var(--light-border, #E5F0FF);
  border-top-left-radius: 0;
  color: #2d3748;
}

.user-bubble {
  background-color: var(--primary-blue, #4D9FFF);
  color: white;
  border-top-right-radius: 0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* 자주 묻는 질문 영역 */
.quick-questions-area {
  padding: 0 2rem 1.5rem 2rem;
  background-color: white;
}

.quick-questions-title {
  font-size: 1rem;
  color: var(--text-gray, #718096);
  margin-bottom: 1rem;
  font-weight: 500;
}

.quick-questions-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.question-btn {
  padding: 0.75rem 1.25rem;
  background-color: white;
  border: 2px solid var(--primary-blue, #4D9FFF);
  color: var(--primary-blue, #4D9FFF);
  border-radius: 9999px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.question-btn:hover {
  background-color: var(--light-border, #E5F0FF);
}

/* 입력 영역 */
.input-area {
  padding: 2rem;
  border-top: 1px solid #f7fafc;
  background-color: white;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.chat-input {
  width: 100%;
  padding: 1.25rem 1.5rem;
  padding-right: 5rem;
  /* 버튼 공간 확보 */
  border: 2px solid var(--light-border, #E5F0FF);
  border-radius: 9999px;
  outline: none;
  background-color: #F8FBFF;
  font-size: 1.125rem;
  transition: all 0.2s;
}

.chat-input:focus {
  border-color: var(--primary-blue, #4D9FFF);
}

.chat-input::placeholder {
  color: #cbd5e0;
}

.send-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 3.5rem;
  height: 3.5rem;
  background-color: var(--primary-blue, #4D9FFF);
  color: white;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.send-btn:hover:not(:disabled) {
  background-color: var(--hover-blue, #3A8FEF);
}

.send-btn:disabled {
  background-color: #cbd5e0;
  cursor: not-allowed;
}

.send-icon {
  width: 1.75rem;
  height: 1.75rem;
}

/* 하단 정보 카드 */
.info-cards {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1.5rem;
  margin-top: 2.5rem;
}

@media (min-width: 768px) {
  .info-cards {
    grid-template-columns: repeat(3, 1fr);
  }
}

.info-card {
  padding: 1.5rem;
  background-color: var(--pastel-bg, #F0F7FF);
  /* 카드도 파스텔톤 배경 */
  border-radius: 1rem;
}

.info-card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.sparkle-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--primary-blue, #4D9FFF);
}

.info-card h4 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-dark, #1a202c);
  margin: 0;
}

.info-card p {
  font-size: 1rem;
  color: var(--text-gray, #718096);
  line-height: 1.625;
  margin: 0;
}

/* 💡 AI 컨테이너 (말풍선과 카드를 묶음) */
.ai-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 100%;
}

/* 💡 후보 카드 영역 */
.candidate-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding-left: 0.5rem;
}

.candidate-card {
  background-color: white;
  border: 2px solid var(--primary-blue);
  border-radius: 1rem;
  padding: 0.6rem 1.2rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
  box-shadow: 0 2px 4px rgba(77, 159, 255, 0.1);
}

.candidate-card:hover {
  background-color: var(--primary-blue, #4D9FFF);
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(77, 159, 255, 0.3);
}

.drug-name {
  font-weight: 700;
  color: var(--primary-blue);
  font-size: 0.95rem;
}

.candidate-card:hover .drug-name {
  color: white;
}

.click-hint {
  font-size: 0.75rem;
  color: var(--text-gray);
  margin-top: 2px;
}

.candidate-card:hover .click-hint {
  color: rgba(255, 255, 255, 0.8);
}

.ai-status {
  font-size: 0.8rem;
  color: #6c757d;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.spinner {
  width: 12px;
  height: 12px;
  border: 2px solid #ddd;
  border-top: 2px solid #5b9cff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

</style>