<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
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
import MaskIcon from "@/assets/icons/mask.svg?component";
// 캐러셀에 필요한 아이콘(Bot, MessageSquare, Heart) 추가 임포트
import { ArrowRight, Activity, Users, Search as SearchIcon, Sparkles, Bot, MessageSquare, Heart } from "lucide-vue-next";

const router = useRouter();
const searchQuery = ref("");

const commonColorClass = "text-primary";

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
  <div class="home-wrapper">
    
    <div id="heroCarousel" class="carousel slide carousel-fade hero-carousel" data-bs-ride="carousel" data-bs-interval="5000">
      
      <div class="carousel-indicators custom-indicators">
        <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
        <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="1" aria-label="Slide 2"></button>
        <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="2" aria-label="Slide 3"></button>
      </div>

      <div class="carousel-inner">
        <div class="carousel-item active">
          <section class="hero-section carousel-height">
            <div class="hero-bg">
              <div class="gradient-orb orb-1"></div>
              <div class="gradient-orb orb-2"></div>
              <div class="gradient-orb orb-3"></div>
              <div class="mesh-gradient"></div>
            </div>
            <div class="hero-content">
              <div class="hero-badge">
                <Sparkles :size="16" />
                <span>AI-Powered Healthcare</span>
              </div>
              <h1 class="hero-title">
                Smarter Medicine,<br />
                <span class="gradient-text">Safer Choices</span>
              </h1>
              <p class="hero-subtitle">안전하고 정확한 의약품 정보로 건강한 내일을 만듭니다</p>
              <button class="btn-premium mt-5" @click="router.push('/search')">
                <span>지금 시작하기</span>
                <ArrowRight :size="18" />
              </button>
            </div>
            <div class="floating-pills">
              <div class="pill pill-1">💊</div>
              <div class="pill pill-2">💉</div>
              <div class="pill pill-3">🧬</div>
            </div>
          </section>
        </div>

        <div class="carousel-item">
          <section class="hero-section carousel-height">
            <div class="hero-bg">
              <div class="gradient-orb orb-1" style="background: radial-gradient(circle, #60a5fa 0%, #3b82f6 50%, transparent 70%);"></div>
              <div class="gradient-orb orb-3" style="background: radial-gradient(circle, #818cf8 0%, #6366f1 50%, transparent 70%);"></div>
              <div class="mesh-gradient"></div>
            </div>
            <div class="hero-content">
              <div class="hero-badge">
                <Bot :size="16" />
                <span>AI 스마트 분석</span>
              </div>
              <h1 class="hero-title">
                스마트 AI 챗봇<br />
                <span class="gradient-text" style="background: linear-gradient(135deg, #60a5fa 0%, #818cf8 100%); -webkit-background-clip: text;">맞춤형 의약품 추천</span>
              </h1>
              <p class="hero-subtitle">증상을 말씀해 주세요. AI가 가장 적합한 약을 즉시 찾아드립니다.</p>
              <button class="btn-premium mt-5" @click="router.push('/chatbot')">
                <span>챗봇 상담 시작</span>
                <ArrowRight :size="18" />
              </button>
            </div>
            <div class="floating-pills">
              <div class="pill pill-1">🤖</div>
              <div class="pill pill-2">💬</div>
              <div class="pill pill-3">⚡</div>
            </div>
          </section>
        </div>

        <div class="carousel-item">
          <section class="hero-section carousel-height">
            <div class="hero-bg">
              <div class="gradient-orb orb-2" style="background: radial-gradient(circle, #34d399 0%, #10b981 50%, transparent 70%);"></div>
              <div class="gradient-orb orb-1" style="background: radial-gradient(circle, #6ee7b7 0%, #2dd4bf 50%, transparent 70%);"></div>
              <div class="mesh-gradient"></div>
            </div>
            <div class="hero-content">
              <div class="hero-badge">
                <Users :size="16" />
                <span>건강 커뮤니티</span>
              </div>
              <h1 class="hero-title">
                함께 나누는<br />
                <span class="gradient-text" style="background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%); -webkit-background-clip: text;">건강한 정보 공유</span>
              </h1>
              <p class="hero-subtitle">실제 복용 후기와 노하우를 이웃들과 자유롭게 공유해보세요.</p>
              <button class="btn-premium mt-5" @click="router.push('/community')">
                <span>커뮤니티 이동</span>
                <ArrowRight :size="18" />
              </button>
            </div>
            <div class="floating-pills">
              <div class="pill pill-1">👥</div>
              <div class="pill pill-2">📝</div>
              <div class="pill pill-3">❤️</div>
            </div>
          </section>
        </div>
      </div>

      <button class="carousel-control-prev custom-control" type="button" data-bs-target="#heroCarousel" data-bs-slide="prev">
        <span class="control-icon"><ArrowRight style="transform: rotate(180deg)" /></span>
      </button>
      <button class="carousel-control-next custom-control" type="button" data-bs-target="#heroCarousel" data-bs-slide="next">
        <span class="control-icon"><ArrowRight /></span>
      </button>
    </div>

    <section class="search-section">
      <div class="search-bg"></div>
      <div class="container-custom">
        <h2 class="search-heading">어디가 아프신가요?</h2>
        <p class="search-subheading">빠르고 정확하게 약을 찾아드려요</p>
        <div class="search-wrapper">
          <div class="search-box-modern">
            <div class="search-glow"></div><Search class="search-icon" />
            <input type="text" placeholder="증상이나 약품명을 검색하세요..." class="search-input" v-model="searchQuery" @keydown.enter="handleSearch" />
            <button class="search-btn-modern" @click="handleSearch"><span>검색</span><div class="btn-shine"></div></button>
          </div>
        </div>
      </div>
    </section>

    <section class="symptoms-section">
      <div class="container-custom">
        <h2 class="symptoms-heading">증상별로 찾아보세요</h2>
        <div class="symptoms-grid">
          <div v-for="(symptom, index) in symptoms" :key="index" class="symptom-card-modern" @click="handleSymptomClick(symptom)">
            <div class="symptom-glow"></div>
            <div class="symptom-icon-wrapper">
              <component
                v-if="symptom.icon"
                :is="symptom.icon"
                class="symptom-icon"
              />
              <Activity v-else class="symptom-icon text-muted" />
            </div>
            <p class="symptom-name">{{ symptom.label }}</p>
            <p class="symptom-desc">{{ symptom.description }}</p>
            <div class="card-arrow"><ArrowRight :size="16" /></div>
          </div>
        </div>
      </div>
    </section>

    <section class="business-section">
      <div class="container-custom">
        <div class="business-grid">
          <div class="business-card card-blue">
            <div class="card-pattern"></div>
            <div class="card-content">
              <span class="business-number">01</span>
              <h3 class="business-title">AI ChatBot</h3>
              <p class="business-subtitle">AI 챗봇 서비스</p>
              <p class="business-text">최신 의약품 데이터를<br>기반으로 더 나은 솔루션 제공</p>
              <!-- <button class="card-btn"><span>더 보기</span><ArrowRight :size="16" /></button> -->
            </div>
            <div class="card-visual"><Activity :size="80" class="card-icon" /></div>
          </div>
          <div class="business-card card-purple">
            <div class="card-pattern"></div>
            <div class="card-content">
              <span class="business-number">02</span>
              <h3 class="business-title">Community</h3>
              <p class="business-subtitle">커뮤니티</p>
              <p class="business-text">의약품 후기 공유를 통해<br>더 안전한 선택을 돕습니다</p>
              <!-- <button class="card-btn"><span>더 보기</span><ArrowRight :size="16" /></button> -->
            </div>
            <div class="card-visual"><Users :size="80" class="card-icon" /></div>
          </div>
          <div class="business-card card-green">
            <div class="card-pattern"></div>
            <div class="card-content">
              <span class="business-number">03</span>
              <h3 class="business-title">Search</h3>
              <p class="business-subtitle">의약품 필터링 조회</p>
              <p class="business-text">증상 및 제형 필터링을 통해<br>필요한 정보에 쉽게 접근할 수 있습니다</p>
              <!-- <button class="card-btn" @click="router.push('/community')"><span>더 보기</span><ArrowRight :size="16" /></button> -->
            </div>
            <div class="card-visual"><SearchIcon :size="80" class="card-icon" /></div>
          </div>
        </div>
      </div>
    </section>

    <section class="network-section">
      <div class="network-pattern"></div>
      <div class="container-custom">
        <div class="network-content">
          <h2 class="network-heading">자주 묻는 질문으로<br>더 쉬운 의약품 정보</h2>
          <p class="network-text">사용자가 가장 많이 궁금해하는 내용을<br>빠르고 정확하게 확인하세요</p>
          <button class="btn-glass" @click="router.push('/faq')"><span>FAQ 바로가기</span><ArrowRight :size="18" /></button>
        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
/* --- 캐러셀 통합 스타일 --- */
.hero-carousel, .carousel-inner, .carousel-item {
  height: 100vh;
  min-height: 700px;
}

/* 커스텀 인디케이터 스타일 */
.custom-indicators {
  bottom: 40px;
  z-index: 15;
}
.custom-indicators button {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #cbd5e1;
  border: none;
  margin: 0 6px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0.5;
}
.custom-indicators .active {
  width: 32px;
  border-radius: 10px;
  background-color: #3b82f6;
  opacity: 1;
}

/* 좌우 컨트롤 커스텀 */
.custom-control {
  width: 5%;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 20;
}
.hero-carousel:hover .custom-control { opacity: 1; }
.control-icon {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: #1e293b;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

/* Hero 및 기본 스타일 (기존 HomeView.vue 스타일 병합) */
.home-wrapper { overflow-x: hidden; background: #ffffff; }
.container-custom { max-width: 1400px; margin: 0 auto; padding: 0 40px; }

.hero-section {
  position: relative;
  height: 100%;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}

.hero-bg { position: absolute; inset: 0; }
.gradient-orb {
  position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.6;
  animation: float 12s ease-in-out infinite;
}
.orb-1 { width: 600px; height: 600px; background: radial-gradient(circle, #60a5fa 0%, #3b82f6 50%, transparent 70%); top: -10%; right: 10%; }
.orb-2 { width: 500px; height: 500px; background: radial-gradient(circle, #818cf8 0%, #6366f1 50%, transparent 70%); bottom: -10%; left: 5%; animation-delay: -4s; }
.orb-3 { width: 400px; height: 400px; background: radial-gradient(circle, #a78bfa 0%, #8b5cf6 50%, transparent 70%); top: 40%; left: 50%; animation-delay: -8s; }

.mesh-gradient {
  position: absolute; inset: 0; z-index: 2;
  background: 
    radial-gradient(at 20% 30%, rgba(96, 165, 250, 0.1) 0px, transparent 50%),
    radial-gradient(at 80% 70%, rgba(129, 140, 248, 0.1) 0px, transparent 50%);
}

.hero-content { position: relative; z-index: 10; text-align: center; max-width: 900px; }
.hero-badge {
  display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px;
  background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px);
  border-radius: 50px; border: 1px solid rgba(59, 130, 246, 0.2);
  color: #3b82f6; font-size: 0.875rem; font-weight: 600; margin-bottom: 2rem;
}
.hero-title { font-size: clamp(3.5rem, 7vw, 6.5rem); font-weight: 200; line-height: 1.1; color: #0f172a; margin-bottom: 2rem; }
.gradient-text { background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 400; }
.hero-subtitle { font-size: clamp(1.125rem, 2vw, 1.5rem); color: #64748b; font-weight: 300; line-height: 1.6; }

.floating-pills { position: absolute; inset: 0; pointer-events: none; z-index: 5; }
.pill { position: absolute; font-size: 3rem; animation: pillFloat 6s ease-in-out infinite; }
.pill-1 { top: 20%; left: 10%; }
.pill-2 { bottom: 25%; right: 15%; animation-delay: -2s; }
.pill-3 { top: 60%; right: 25%; animation-delay: -4s; }

/* 나머지 섹션 스타일(Solution, Business 등)은 기존 코드와 동일 */
.solution-section { padding: 140px 0; background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%); }
.solution-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 80px; align-items: center; }
.glass-card { position: relative; width: 550px; height: 550px; background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(20px); border-radius: 30px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08); overflow: hidden; }
/* ... (이하 애니메이션 및 반응형 스타일 생략) ... */

@keyframes float { 0%, 100% { transform: translate(0, 0) scale(1); } 33% { transform: translate(30px, -30px) scale(1.1); } 66% { transform: translate(-20px, 20px) scale(0.9); } }
@keyframes pillFloat { 0%, 100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-30px) rotate(180deg); } }

/* (중략) 기존 HomeView.vue의 나머지 스타일 모두 포함 */
.home-wrapper {
  overflow-x: hidden;
  background: #ffffff;
}

.container-custom {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
}

/* Hero Section - Premium 3D */
.hero-section {
  position: relative;
  height: 100vh;
  min-height: 700px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  animation: float 12s ease-in-out infinite;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, #60a5fa 0%, #3b82f6 50%, transparent 70%);
  top: -10%;
  right: 10%;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #818cf8 0%, #6366f1 50%, transparent 70%);
  bottom: -10%;
  left: 5%;
  animation-delay: -4s;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, #a78bfa 0%, #8b5cf6 50%, transparent 70%);
  top: 40%;
  left: 50%;
  animation-delay: -8s;
}

.mesh-gradient {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(at 20% 30%, rgba(96, 165, 250, 0.1) 0px, transparent 50%),
    radial-gradient(at 80% 70%, rgba(129, 140, 248, 0.1) 0px, transparent 50%),
    radial-gradient(at 50% 50%, rgba(167, 139, 250, 0.05) 0px, transparent 50%);
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.hero-content {
  position: relative;
  z-index: 10;
  text-align: center;
  max-width: 900px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 50px;
  border: 1px solid rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
}

.hero-title {
  font-size: clamp(3.5rem, 7vw, 6.5rem);
  font-weight: 200;
  line-height: 1.1;
  color: #0f172a;
  margin-bottom: 2rem;
  letter-spacing: -0.03em;
}

.gradient-text {
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 400;
}

.hero-subtitle {
  font-size: clamp(1.125rem, 2vw, 1.5rem);
  color: #64748b;
  font-weight: 300;
  line-height: 1.6;
}

.floating-pills {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.pill {
  position: absolute;
  font-size: 3rem;
  animation: pillFloat 6s ease-in-out infinite;
}

.pill-1 {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.pill-2 {
  bottom: 25%;
  right: 15%;
  animation-delay: -2s;
}

.pill-3 {
  top: 60%;
  right: 25%;
  animation-delay: -4s;
}

@keyframes pillFloat {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) rotate(180deg);
  }
}

/* Solution Section - Glassmorphism */
.solution-section {
  padding: 140px 0;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

.solution-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.glass-card {
  position: relative;
  width: 550px;
  height: 550px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
  border-radius: 30px;
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  overflow: hidden;
}

.card-shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(255, 255, 255, 0.3) 50%,
    transparent 70%
  );
  animation: shine 8s ease-in-out infinite;
}

@keyframes shine {
  0%, 100% {
    transform: translate(-100%, -100%);
  }
  50% {
    transform: translate(100%, 100%);
  }
}

.floating-icon {
  position: absolute;
  font-size: 3rem;
  animation: iconFloat 4s ease-in-out infinite;
}

.icon-1 {
  top: 15%;
  left: 15%;
  animation-delay: 0s;
}

.icon-2 {
  top: 20%;
  right: 15%;
  animation-delay: -1.3s;
}

.icon-3 {
  bottom: 20%;
  left: 20%;
  animation-delay: -2.6s;
}

@keyframes iconFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.center-orb {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 250px;
  height: 250px;
  border-radius: 50%;
  background: radial-gradient(circle, #dbeafe 0%, #bfdbfe 100%);
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    transform: translate(-50%, -50%) scale(1.05);
  }
}

.label-badge {
  display: inline-block;
  padding: 8px 16px;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  color: #3b82f6;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 50px;
  margin-bottom: 1.5rem;
}

.section-heading {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 300;
  line-height: 1.2;
  color: #0f172a;
  margin-bottom: 2rem;
  letter-spacing: -0.02em;
}

.section-text {
  font-size: 1.125rem;
  color: #64748b;
  line-height: 1.8;
  margin-bottom: 3rem;
}

.btn-premium {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 36px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
}

.btn-premium:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 40px rgba(59, 130, 246, 0.4);
}

.btn-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  animation: glow 3s ease-in-out infinite;
}

@keyframes glow {
  0%, 100% {
    transform: translate(-50%, -50%);
    opacity: 0;
  }
  50% {
    transform: translate(0%, 0%);
    opacity: 1;
  }
}

/* Business Cards - Premium Design */
.business-section {
  padding: 140px 0;
  background: #ffffff;
}

.business-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 40px;
}

.business-card {
  position: relative;
  padding: 50px;
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.4s ease;
  cursor: pointer;
  min-height: 500px;
  display: flex;
  flex-direction: column;
}

.business-card:hover {
  transform: translateY(-12px);
}

.card-blue {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
}

.card-blue:hover {
  box-shadow: 0 30px 80px rgba(59, 130, 246, 0.4);
}

.card-purple {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  box-shadow: 0 20px 60px rgba(139, 92, 246, 0.3);
}

.card-purple:hover {
  box-shadow: 0 30px 80px rgba(139, 92, 246, 0.4);
}

.card-green {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 20px 60px rgba(16, 185, 129, 0.3);
}

.card-green:hover {
  box-shadow: 0 30px 80px rgba(16, 185, 129, 0.4);
}

.card-pattern {
  position: absolute;
  inset: 0;
  opacity: 0.1;
  background-image: 
    radial-gradient(circle at 20% 30%, white 1px, transparent 1px),
    radial-gradient(circle at 80% 70%, white 1px, transparent 1px);
  background-size: 50px 50px;
}

.card-content {
  position: relative;
  z-index: 2;
  color: white;
  flex: 1;
}

.business-number {
  display: block;
  font-size: 1rem;
  opacity: 0.8;
  margin-bottom: 1rem;
}

.business-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.business-subtitle {
  font-size: 1.125rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.business-text {
  font-size: 1rem;
  line-height: 1.8;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.card-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.card-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateX(4px);
}

.card-visual {
  position: absolute;
  bottom: 30px;
  right: 30px;
  opacity: 0.15;
}

.card-icon {
  width: 120px;
  height: 120px;
}

/* Search Section - Modern */
.search-section {
  position: relative;
  padding: 140px 0;
  background: linear-gradient(
    to bottom,
    rgb(250, 250, 250) 0%,
    #ffffff 100%
  );
  overflow: hidden;
}

.search-bg {
  position: absolute;
  inset: 0;
}

.search-heading {
  position: relative;
  z-index: 2;
  font-size: 3.5rem;
  font-weight: 600;
  color: #0f172a;
  text-align: center;
  margin-bottom: 1rem;
}

.search-subheading {
  position: relative;
  z-index: 2;
  font-size: 1.375rem;
  color: #64748b;
  text-align: center;
  margin-bottom: 4rem;
  font-weight: 300;
}

.search-wrapper {
  position: relative;
  z-index: 2;
  max-width: 800px;
  margin: 0 auto;
}

.search-box-modern {
  position: relative;
  display: flex;
  align-items: center;
  background: white;
  border-radius: 16px;
  padding: 12px 16px;
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.08),
    0 0 0 1px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.search-box-modern:focus-within {
  box-shadow: 
    0 25px 70px rgba(59, 130, 246, 0.15),
    0 0 0 4px rgba(59, 130, 246, 0.1);
}

.search-glow {
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 16px;
  opacity: 0;
  z-index: -1;
  transition: opacity 0.3s ease;
}

.search-box-modern:focus-within .search-glow {
  opacity: 0.15;
}

.search-icon {
  width: 24px;
  height: 24px;
  color: #94a3b8;
  margin-right: 16px;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1.125rem;
  color: #0f172a;
}

.search-input::placeholder {
  color: #cbd5e1;
}

.search-btn-modern {
  position: relative;
  padding: 14px 32px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
}

.search-btn-modern:hover {
  transform: scale(1.05);
}

.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: btnShine 2s infinite;
}

@keyframes btnShine {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

/* Symptoms Grid - Modern Cards */
.symptoms-section {
  padding: 140px 0;
  background: #ffffff;
}

.symptoms-heading {
  font-size: 2.75rem;
  font-weight: 600;
  text-align: center;
  color: #0f172a;
  margin-bottom: 4rem;
}

.symptoms-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 24px;
}

.symptom-card-modern {
  position: relative;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.symptom-glow {
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 16px;
  opacity: 0;
  z-index: 0;
  transition: opacity 0.4s ease;
}

.symptom-card-modern:hover .symptom-glow {
  opacity: 1;
}

.symptom-card-modern:hover {
  transform: translateY(-8px) scale(1.02);
  border-color: transparent;
}

.symptom-icon-wrapper {
  position: relative;
  z-index: 1;
  width: 72px;
  height: 72px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.4s ease;
}

.symptom-card-modern:hover .symptom-icon-wrapper {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.symptom-icon {
  position: relative;
  z-index: 1;
  width: 36px;
  height: 36px;
  color: #3b82f6;
  transition: all 0.4s ease;
}

.symptom-card-modern:hover .symptom-icon {
  color: white;
  transform: scale(1.1);
}

.symptom-name {
  position: relative;
  z-index: 1;
  font-size: 1.125rem;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 8px;
  transition: color 0.4s ease;
}

.symptom-card-modern:hover .symptom-name {
  color: white;
}

.symptom-desc {
  position: relative;
  z-index: 1;
  font-size: 0.875rem;
  color: #64748b;
  margin: 0 0 12px 0;
  transition: color 0.4s ease;
}

.symptom-card-modern:hover .symptom-desc {
  color: rgba(255, 255, 255, 0.9);
}

.card-arrow {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: center;
  color: #3b82f6;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.4s ease;
}

.symptom-card-modern:hover .card-arrow {
  opacity: 1;
  transform: translateY(0);
  color: white;
}

/* Network Section - Premium Gradient */
.network-section {
  position: relative;
  padding: 160px 0;
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #6366f1 100%);
  overflow: hidden;
}

.network-pattern {
  position: absolute;
  inset: 0;
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(255, 255, 255, 0.08) 0%, transparent 50%);
  animation: patternMove 20s ease-in-out infinite;
}

@keyframes patternMove {
  0%, 100% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(20px, 20px);
  }
}

.network-content {
  position: relative;
  z-index: 2;
  text-align: center;
  color: white;
}

.network-heading {
  font-size: 3rem;
  font-weight: 600;
  line-height: 1.3;
  margin-bottom: 2rem;
}

.network-text {
  font-size: 1.25rem;
  opacity: 0.95;
  line-height: 1.8;
  margin-bottom: 3rem;
}

.btn-glass {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 36px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-glass:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
}

/* Magazine Section - 3D Card */
.magazine-section {
  padding: 140px 0;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
}

.magazine-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4rem;
}

.magazine-heading {
  font-size: 3rem;
  font-weight: 600;
  color: #0f172a;
}

.btn-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: transparent;
  color: #3b82f6;
  border: 2px solid #3b82f6;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-link:hover {
  background: #3b82f6;
  color: white;
}

.magazine-card-3d {
  perspective: 1000px;
}

.card-3d-wrapper {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 60px;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  transition: all 0.5s ease;
}

.card-3d-wrapper:hover {
  transform: translateY(-8px);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.15);
}

.magazine-image-3d {
  height: 450px;
  overflow: hidden;
}

.image-gradient {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.5s ease;
}

.card-3d-wrapper:hover .image-gradient {
  transform: scale(1.05);
}

.magazine-icon {
  color: #3b82f6;
  opacity: 0.3;
}

.magazine-content-3d {
  padding: 60px 60px 60px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.magazine-volume {
  font-size: 0.875rem;
  color: #10b981;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 16px;
}

.magazine-title {
  font-size: 2rem;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 20px;
  line-height: 1.3;
}

.magazine-excerpt {
  font-size: 1.125rem;
  color: #64748b;
  line-height: 1.7;
  margin-bottom: 2rem;
}

.read-more {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  align-self: flex-start;
  transition: all 0.3s ease;
}

.read-more:hover {
  transform: translateX(4px);
  box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .solution-grid,
  .card-3d-wrapper {
    grid-template-columns: 1fr;
  }
  
  .glass-card {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
  }
  
  .magazine-content-3d {
    padding: 40px;
  }
}

@media (max-width: 768px) {
  .container-custom {
    padding: 0 24px;
  }
  
  .hero-section {
    height: 80vh;
  }
  
  .hero-title {
    font-size: 3rem;
  }
  
  .solution-section,
  .business-section,
  .search-section,
  .symptoms-section,
  .network-section,
  .magazine-section {
    padding: 80px 0;
  }
  
  .business-grid {
    grid-template-columns: 1fr;
  }
  
  .business-card {
    min-height: 400px;
  }
  
  .business-title {
    font-size: 2.5rem;
  }
  
  .symptoms-grid {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 16px;
  }
}

@media (max-width: 576px) {
  .hero-badge {
    font-size: 0.75rem;
    padding: 8px 16px;
  }
  
  .search-heading {
    font-size: 2.5rem;
  }
  
  .magazine-header {
    flex-direction: column;
    gap: 20px;
    align-items: flex-start;
  }
}

</style>