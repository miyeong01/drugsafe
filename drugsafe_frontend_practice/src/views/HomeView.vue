<script setup>
import { ref, h } from "vue";
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
import Heart from "@/assets/icons/heart.svg?component"; 
import Pill from "@/assets/icons/pill.svg?component";
import MaskIcon from "@/assets/icons/mask.svg?component";

const router = useRouter();
const searchQuery = ref("");

const commonColorClass = "bg-primary bg-opacity-10 text-primary";

const symptoms = [
  {
    icon: HeadacheIcon,
    label: "두통",
    description: "머리가 아플 때",
    color: commonColorClass,
  },
  {
    icon: ToothIcon,
    label: "치통",
    description: "이가 아플 때",
    color: commonColorClass,
  },
  {
    icon: FeverIcon,
    label: "발열",
    description: "열이 날 때",
    color: commonColorClass,
  },
  {
    icon: StomachIcon,
    label: "복통",
    description: "배가 아플 때",
    color: commonColorClass,
  },
  {
    icon: BellyIcon,
    label: "생리통",
    description: "생리 시 통증",
    color: commonColorClass,
  },
  {
    icon: DigestiveIcon,
    label: "위장약",
    description: "위장이 불편할 때",
    color: commonColorClass,
  },
  {
    icon: FluIcon,
    label: "종합감기",
    description: "감기 증상 전반",
    color: commonColorClass,
  },
  {
    icon: NoseIcon,
    label: "코감기",
    description: "콧물·코막힘",
    color: commonColorClass,
  },
  {
    icon:MaskIcon,
    label: "기침",
    description: "기침이 날 때",
    color: commonColorClass,
  },
  {
    icon: CoughIcon,
    label: "재채기",
    description: "재채기가 날 때",
    color: commonColorClass,
  },
  {
    icon: DigestiveIcon,
    label: "소화불량",
    description: "소화가 안 될 때",
    color: commonColorClass,
  },
  {
    icon: AllergyIcon,
    label: "알레르기",
    description: "알레르기 반응",
    color: commonColorClass,
  },
  {
    icon: TiredIcon,
    label: "육체피로",
    description: "피로·권태감",
    color: commonColorClass,
  },
  {
    icon: JointIcon,
    label: "관절통",
    description: "관절이 아플 때",
    color: commonColorClass,
  },
  {
    icon: MuscleIcon,
    label: "근육통",
    description: "근육이 아플 때",
    color: commonColorClass,
  },
];

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ name: "search", query: { q: searchQuery.value } });
  }
};

const handleSymptomClick = (label) => {
  router.push({ name: "search", query: { q: label } });
};
</script>

<template>
  <div class="min-vh-100">
    <section
      class="py-5 bg-light"
      style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)"
    >
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
              class="btn btn-primary rounded-pill px-5 fw-medium"
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
              @click="handleSymptomClick(symptom.label)"
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

    <section class="py-5 bg-white">
      <div class="container py-4">
        <h2 class="mb-5 text-center fw-bold text-dark">
          DrugSafe의 특별한 기능
        </h2>

        <div class="row g-4">
          <div class="col-12 col-md-4">
            <div
              class="card h-100 border p-4 shadow-sm"
              style="border-radius: 0.75rem"
            >
              <div class="card-body">
                <div
                  class="bg-primary bg-opacity-10 rounded-3 d-inline-flex align-items-center justify-content-center mb-3"
                  style="width: 3rem; height: 3rem"
                >
                  <Search class="text-primary" style="width: 1.5rem" />
                </div>
                <h3 class="h5 fw-bold text-dark mb-2">정확한 검색</h3>
                <p class="text-secondary mb-0">
                  증상이나 약품명으로 정확한 의약품 정보를 빠르게 찾을 수
                  있습니다.
                </p>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-4">
            <div
              class="card h-100 border p-4 shadow-sm"
              style="border-radius: 0.75rem"
            >
              <div class="card-body">
                <div
                  class="bg-primary bg-opacity-10 rounded-3 d-inline-flex align-items-center justify-content-center mb-3"
                  style="width: 3rem; height: 3rem"
                >
                  <Heart class="text-primary" style="width: 1.5rem" />
                </div>
                <h3 class="h5 fw-bold text-dark mb-2">복용 관리</h3>
                <p class="text-secondary mb-0">
                  복용 중인 약을 관리하고 일일 복용 여부를 체크할 수 있습니다.
                </p>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-4">
            <div
              class="card h-100 border p-4 shadow-sm"
              style="border-radius: 0.75rem"
            >
              <div class="card-body">
                <div
                  class="bg-primary bg-opacity-10 rounded-3 d-inline-flex align-items-center justify-content-center mb-3"
                  style="width: 3rem; height: 3rem"
                >
                  <Pill class="text-primary" style="width: 1.5rem" />
                </div>
                <h3 class="h5 fw-bold text-dark mb-2">약물 상호작용 확인</h3>
                <p class="text-secondary mb-0">
                  복용 중인 약물 간의 상호작용을 확인하여 안전한 복용을
                  도와줍니다.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-5 bg-primary bg-gradient text-white">
      <div class="container text-center" style="max-width: 56rem">
        <h2 class="mb-3 fw-bold text-white display-6">
          안전하고 정확한 의약품 정보
        </h2>
        <p class="mb-0 text-white-50 fs-5">DrugSafe와 함께 건강을 지키세요.</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
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
</style>
