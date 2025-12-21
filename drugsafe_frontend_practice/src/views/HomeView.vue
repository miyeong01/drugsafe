<script setup>
import { ref, h } from "vue";
import { useRouter } from "vue-router";
// 기존 사용자 아이콘 임포트 유지
import HeadacheIcon from "@/assets/icons/headache.svg?component";
import ToothIcon from "@/assets/icons/tooth.svg?component";
import FeverIcon from "@/assets/icons/fever.svg?component";
import StomachIcon from "@/assets/icons/stomach.svg?component";
import BellyIcon from "@/assets/icons/belly.svg?component";
import FluIcon from "@/assets/icons/virus.svg?component";
import NoseIcon from "@/assets/icons/nose.svg?component";
import CoughIcon from "@/assets/icons/cough.svg?component";
import DigestiveIcon from "@/assets/icons/stomach_1.svg?component";
import AllergyIcon from "@/assets/icons/allergy.svg?component";
import TiredIcon from "@/assets/icons/tired.svg?component";
import JointIcon from "@/assets/icons/joint.svg?component";
import MuscleIcon from "@/assets/icons/muscle.svg?component"
import Search from "@/assets/icons/search.svg?component"; 
import Heart from "@/assets/icons/heart.svg?component"; 
import Pill from "@/assets/icons/pill.svg?component";
import MaskIcon from "@/assets/icons/mask.svg?component";

// Carousel용 추가 아이콘 (lucide-vue-next 활용)
import { Bot, MessageSquare, Users, ArrowRight } from "lucide-vue-next";

const router = useRouter();
const searchQuery = ref("");

const commonColorClass = "bg-primary bg-opacity-10 text-primary";

// 15개 증상 리스트 유지
const symptoms = [
  { id: 1, icon: HeadacheIcon, label: "두통", description: "머리가 아플 때", color: commonColorClass },
  { id: 2, icon: ToothIcon, label: "치통", description: "이가 아플 때", color: commonColorClass },
  { id: 3, icon: FeverIcon, label: "발열", description: "열이 날 때", color: commonColorClass },
  { id: 4, icon: StomachIcon, label: "복통", description: "배가 아플 때", color: commonColorClass },
  { id: 5, icon: BellyIcon, label: "생리통", description: "생리 시 통증", color: commonColorClass },
  { id: 6, icon: DigestiveIcon, label: "위장약", description: "위장이 불편할 때", color: commonColorClass },
  { id: 7, icon: FluIcon, label: "종합감기", description: "감기 증상 전반", color: commonColorClass },
  { id: 8, icon: NoseIcon, label: "코감기", description: "콧물·코막힘", color: commonColorClass },
  { id: 9, icon: MaskIcon, label: "기침", description: "기침이 날 때", color: commonColorClass },
  { id: 10, icon: CoughIcon, label: "재채기", description: "재채기가 날 때", color: commonColorClass },
  { id: 11, icon: DigestiveIcon, label: "소화불량", description: "소화가 안 될 때", color: commonColorClass },
  { id: 12, icon: AllergyIcon, label: "알레르기", description: "알레르기 반응", color: commonColorClass },
  { id: 13, icon: TiredIcon, label: "육체피로", description: "피로·권태감", color: commonColorClass },
  { id: 14, icon: JointIcon, label: "관절통", description: "관절이 아플 때", color: commonColorClass },
  { id: 15, icon: MuscleIcon, label: "근육통", description: "근육이 아플 때", color: commonColorClass },
];

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ name: "search", query: { q: searchQuery.value } });
  }
};

const handleSymptomClick = (symptom) => {
  router.push({ 
    name: "search", 
    query: { 
      q: symptom.label, 
      symptom: symptom.id
    } 
  });
};
</script>

<template>
  <div class="min-vh-100">
    <div id="heroCarousel" class="carousel slide carousel-fade" data-bs-ride="carousel">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="0" class="active"></button>
        <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="1"></button>
        <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="2"></button>
      </div>
      
      <div class="carousel-inner">
        <div class="carousel-item active" data-bs-interval="3000">
          <div class="promo-banner chatbot-bg d-flex align-items-center">
            <div class="container text-white">
              <div class="row align-items-center">
                <div class="col-lg-7 text-center text-lg-start">
                  <span class="badge bg-light text-primary mb-3">AI 스마트 분석</span>
                  <h2 class="display-5 fw-bold mb-3">스마트 AI 챗봇으로<br/>맞춤형 의약품 추천</h2>
                  <p class="lead mb-4 text-white-50">증상을 말씀해 주세요. AI가 가장 적합한 약을 즉시 찾아드립니다.</p>
                  <button class="btn btn-light btn-lg rounded-pill px-4 fw-bold text-primary">챗봇 상담 시작</button>
                </div>
                <div class="col-lg-5 d-none d-lg-block">
                  <div class="mockup-chat shadow-lg p-3 bg-white rounded-4 text-dark">
                    <div class="d-flex align-items-center mb-3 text-primary border-bottom pb-2">
                      <Bot class="me-2" /> <span class="fw-bold small">DrugSafe AI Assistant</span>
                    </div>
                    <div class="chat-bubble user mb-2 small p-2 bg-light rounded-3 ms-auto w-75">머리가 너무 지끈거려요.</div>
                    <div class="chat-bubble bot mb-2 small p-2 bg-primary text-white rounded-3 w-75">해열진통제를 추천해 드릴게요!</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="carousel-item" data-bs-interval="3000">
          <div class="promo-banner search-bg d-flex align-items-center text-white text-center">
            <div class="container">
              <div class="icon-circle mb-4 mx-auto bg-white text-primary shadow-sm">
                <Search style="width: 48px; height: 48px;" />
              </div>
              <h2 class="display-5 fw-bold mb-3">빠르고 정확한 스마트 검색</h2>
              <p class="lead text-white-50">성분부터 주의사항까지, 궁금한 약 정보를 한 번에 확인하세요.</p>
            </div>
          </div>
        </div>

        <div class="carousel-item" data-bs-interval="3000">
          <div class="promo-banner community-bg d-flex align-items-center">
            <div class="container text-center text-lg-start">
              <div class="row align-items-center">
                <div class="col-lg-6">
                  <h2 class="display-5 fw-bold text-dark mb-3">함께 나누는 <span class="text-primary">건강 커뮤니티</span></h2>
                  <p class="lead text-secondary mb-4">실제 복용 후기와 건강 관리 노하우를<br/>이웃들과 자유롭게 공유해보세요.</p>
                  <button class="btn btn-primary btn-lg rounded-pill px-4">커뮤니티 구경하기</button>
                </div>
                <div class="col-lg-6 d-none d-lg-flex justify-content-center">
                  <div class="community-visual">
                    <div class="comm-card p-3 shadow-sm bg-white rounded-3 mb-3 animate-up">
                      <div class="d-flex gap-2 align-items-center small"><b>💊 복용 꿀팁 공유해요!</b></div>
                    </div>
                    <div class="comm-card p-3 shadow-sm bg-white rounded-3 animate-down" style="margin-left: 50px; top: 70px;">
                      <div class="d-flex gap-2 align-items-center small"><b>💬 이 약 효과 정말 좋네요.</b></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <section
      class="py-5 bg-white">
      <div class="container py-5 text-center">
        <h1 class="mb-3 text-primary fw-bold display-4">어디가 아프신가요?</h1>
        <p class="mb-5 text-secondary lead">빠르고 정확하게 약을 찾아드려요</p>

        <div class="mx-auto" style="max-width: 42rem">
          <div
            class="d-flex bg-white rounded-pill shadow-lg p-2 position-relative"
          >
            <Search
              class="position-absolute text-secondary"
              style="
                left: 1.5rem;
                top: 50%;
                transform: translateY(-50%);
                width: 1.25rem;
              "
            />

            <input
              type="text"
              placeholder="증상이나 약품명을 검색하세요..."
              class="form-control border-0 shadow-none bg-transparent rounded-pill"
              style="padding-left: 3.5rem; height: 3.5rem; font-size: 1rem"
              v-model="searchQuery"
              @keydown.enter="handleSearch"
            />

            <button
              @click="handleSearch"
              class="btn btn-primary rounded-pill px-3 fw-medium flex-shrink-0 text-nowrap" style="height: 2.8rem; margin: auto 4px;"
            >
              검색
            </button>
          </div>
        </div>
      </div>
    </section>

    <section class="py-5 container">
      <div style="max-width: 72rem; margin: 0 auto">
        <h2 class="mb-5 text-center fw-bold text-dark">증상별로 찾아보세요</h2>

        <div class="row row-cols-2 row-cols-sm-3 row-cols-md-5 g-4">
          <div v-for="(symptom, index) in symptoms" :key="index" class="col">
            <div
              @click="handleSymptomClick(symptom)"
              class="card h-100 border-1 shadow-sm hover-effect cursor-pointer text-center py-4"
              style="border-color: #e5e7eb; border-radius: 1rem"
            >
              <div
                class="card-body d-flex flex-column align-items-center gap-3 p-0"
              >
                <div
                  class="rounded-circle d-flex align-items-center justify-content-center mb-2"
                  :class="symptom.color"
                  style="width: 3rem; height: 3rem"
                >
                  <component
                    :is="symptom.icon"
                    style="width: 1.5rem; height: 1.5rem"
                  />
                </div>

                <div>
                  <p class="mb-1 fw-bold text-dark small">
                    {{ symptom.label }}
                  </p>
                  <p class="mb-0 text-secondary x-small">
                    {{ symptom.description }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Carousel 관련 스타일 추가 */
.promo-banner { height: 400px; overflow: hidden; }
.chatbot-bg { background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%); }
.search-bg { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
.community-bg { background: #f8fafc; border-bottom: 1px solid #e2e8f0; }

.mockup-chat { width: 280px; transform: rotate(-3deg); border-left: 5px solid #60a5fa; }
.icon-circle { width: 90px; height: 90px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.community-visual { position: relative; width: 100%; height: 200px; }
.comm-card { width: 240px; border-left: 5px solid #3b82f6; position: absolute; }

.animate-up { animation: floatUp 4s infinite ease-in-out; }
.animate-down { animation: floatDown 4s infinite ease-in-out; }
@keyframes floatUp { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }
@keyframes floatDown { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(12px); } }

/* 기존 사용자 스타일 유지 */
.x-small {
  font-size: 0.75rem;
}
.hover-effect {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-effect:hover {
  transform: translateY(-5px);
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.1) !important;
}
.cursor-pointer {
  cursor: pointer;
}

/* Carousel 인디케이터 스타일 */
:deep(.carousel-indicators [data-bs-target]) {
  width: 10px; height: 10px; border-radius: 50%; background-color: rgba(255,255,255,0.4); border: none;
}
:deep(.carousel-indicators .active) { background-color: #ffffff; }
.community-bg :deep(.carousel-indicators [data-bs-target]) { background-color: rgba(0,0,0,0.1); }
.community-bg :deep(.carousel-indicators .active) { background-color: #3b82f6; }
</style>