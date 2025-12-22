<script setup>
import { ref, onMounted } from 'vue';
import { ArrowLeft, Star } from 'lucide-vue-next';
import { useRoute, useRouter } from 'vue-router';
import { useDrugStore } from "@/stores/drug"; 
import { storeToRefs } from "pinia"; 

const props = defineProps({
  onNavigate: { type: Function, required: true }
});

const route = useRoute();
const router = useRouter();
const drugStore = useDrugStore(); 

const { selectedDrug } = storeToRefs(drugStore);
const drugId = route.params.drugId;

// 상태(State) 정의
const score = ref(0);
const hoverScore = ref(0);
const title = ref('');
const content = ref('');
const hasSideEffect = ref(false);
const selectedEffects = ref([]);

onMounted(() => {
  if (drugId) {
    drugStore.getDrugDetail(drugId);
  }
});

const effectOptions = ['매우 효과적', '효과적', '보통', '효과 미미', '효과 없음'];

const toggleEffect = (effect) => {
  const index = selectedEffects.value.indexOf(effect);
  if (index > -1) {
    selectedEffects.value.splice(index, 1);
  } else {
    selectedEffects.value.push(effect);
  }
};

// ✨ 수정된 리뷰 등록 제출 함수
const handleSubmit = async () => {
  // 1. 유효성 검사
  if (score.value === 0) { alert('별점을 선택해주세요.'); return; }
  if (!title.value.trim()) { alert('제목을 입력해주세요.'); return; }
  if (!content.value.trim()) { alert('리뷰 내용을 입력해주세요.'); return; }
  if (selectedEffects.value.length === 0) { alert('효과를 선택해주세요.'); return; }

  // 2. 서버로 보낼 데이터 묶기
  const reviewData = {
    title: title.value,
    content: content.value,
    score: score.value,
    has_side_effect: hasSideEffect.value,
    effects: selectedEffects.value // Django의 JSONField로 저장됨
  };

  try {
    // 3. DrugStore의 리뷰 생성 액션 호출
    await drugStore.createReview(drugId, reviewData);
    
    alert('리뷰가 등록되었습니다!');
    
    // 4. 등록 후 약 상세 페이지로 이동
    // (라우터의 name 설정이 'DrugDetail'인지 확인해 보세요!)
    router.push({ name: 'drug-detail', params: { drugId: drugId } });
  } catch (error) {
    console.error('리뷰 등록 실패:', error);
    alert('리뷰를 등록하는 중 오류가 발생했습니다.');
  }
};

const getScoreText = (val) => {
  const texts = { 5: '매우 만족', 4: '만족', 3: '보통', 2: '불만족', 1: '매우 불만족' };
  return texts[val] || '';
};
</script>

<template>
  <div class="min-vh-100 bg-light py-5 px-3">
    <div class="container" style="max-width: 800px;">
      
      <div class="mb-4">
        <button 
          @click="router.back()" 
          class="btn btn-link text-decoration-none text-secondary p-0 mb-3 d-flex align-items-center"
        >
          <ArrowLeft :size="18" class="me-2" /> 뒤로가기
        </button>
        <h1 class="h3 fw-bold text-dark">리뷰 작성</h1>
        
        <p class="text-secondary mt-2" v-if="selectedDrug">
          <span class="text-primary fw-bold">{{ selectedDrug.name }}</span>에 대한 리뷰를 작성해주세요
        </p>
        <p class="text-secondary mt-2" v-else>
          약 정보를 불러오는 중입니다...
        </p>
      </div>

      <div class="card border-0 shadow-sm">
        <div class="card-body p-4 p-md-5">
          <div class="d-flex flex-column gap-4">
            
            <div>
              <label class="form-label fw-bold mb-3 d-block">별점 *</label>
              <div class="d-flex align-items-center gap-2">
                <button
                  v-for="star in 5" :key="star" type="button"
                  class="btn border-0 p-0 star-btn"
                  @click="score = star"
                  @mouseenter="hoverScore = star"
                  @mouseleave="hoverScore = 0"
                >
                  <Star
                    :size="40"
                    :fill="star <= (hoverScore || score) ? '#FFC107' : 'none'"
                    :class="star <= (hoverScore || score) ? 'text-warning' : 'text-light-gray'"
                  />
                </button>
                <span v-if="score > 0" class="ms-3 text-secondary fw-medium">
                  {{ getScoreText(score) }}
                </span>
              </div>
            </div>

            <div>
              <label for="title" class="form-label fw-bold mb-2">제목 *</label>
              <input id="title" v-model="title" type="text" class="form-control py-2" placeholder="리뷰 제목을 입력하세요" maxlength="50" />
            </div>

            <div>
              <label class="form-label fw-bold mb-2">효과 * (복수 선택 가능)</label>
              <div class="row row-cols-1 row-cols-md-2 g-2">
                <div v-for="effect in effectOptions" :key="effect" class="col">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" :id="effect" :checked="selectedEffects.includes(effect)" @change="toggleEffect(effect)" />
                    <label class="form-check-label cursor-pointer" :for="effect">{{ effect }}</label>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <label class="form-label fw-bold mb-2">부작용 경험</label>
              <div class="d-flex gap-4">
                <div class="form-check">
                  <input class="form-check-input" type="radio" name="sideEffect" id="no-side-effect" :value="false" v-model="hasSideEffect" />
                  <label class="form-check-label cursor-pointer" for="no-side-effect">없음</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="radio" name="sideEffect" id="yes-side-effect" :value="true" v-model="hasSideEffect" />
                  <label class="form-check-label cursor-pointer" for="yes-side-effect">있음</label>
                </div>
              </div>
            </div>

            <div>
              <label for="content" class="form-label fw-bold mb-2">리뷰 내용 *</label>
              <textarea id="content" v-model="content" class="form-control" rows="8" placeholder="경험을 자세히 공유해주세요."></textarea>
            </div>

            <div class="row g-3 pt-3">
              <div class="col-6">
                <button type="button" @click="router.back()" class="btn btn-outline-secondary w-100 py-2 fw-bold">취소</button>
              </div>
              <div class="col-6">
                <button type="button" @click="handleSubmit" class="btn btn-primary w-100 py-2 fw-bold text-white">리뷰 등록</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>