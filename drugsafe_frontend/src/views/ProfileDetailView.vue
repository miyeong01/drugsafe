<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ArrowLeft, Trash2, Pill, SprayCan, Droplet, Bandage } from "lucide-vue-next";
import { useAccountStore } from "@/stores/accounts";
import { useDrugStore } from "@/stores/drug";
import { storeToRefs } from "pinia";

import film from "@/assets/icons/film.svg?component";
import lotion from "@/assets/icons/lotion.svg?component";
import cream from "@/assets/icons/cream.svg?component";
import ointment from "@/assets/icons/ointment.svg?component";
import powder from "@/assets/icons/powder.svg?component";

const router = useRouter();
const accountStore = useAccountStore();
const drugStore = useDrugStore();

const { myFavorites } = storeToRefs(drugStore);

const getFormIcon = (form) => {
  const map = {
    1: Pill,
    2: powder,
    3: Droplet,
    4: Droplet,
    5: SprayCan,
    6: film,
    7: cream,
    8: ointment,
    9: Bandage,
    10: lotion,
  };
  return map[form] || Pill;
}

// 현재 활성화된 탭
const activeTab = ref("password");

// 비밀번호 데이터
const passwordData = reactive({
  current: "",
  new: "",
  confirm: "",
});

onMounted(async () => {
  if (accountStore.token) {
    await drugStore.getFavorites();
  }
});

// 뒤로가기
const goBack = () => {
  router.back();
};

// 비밀번호 변경
const handlePasswordChange = async () => {
  try {
    await accountStore.changePassword(passwordData);

    alert("비밀번호가 변경되었습니다. 다시 로그인해주세요.");

    await accountStore.logOut();
  } catch (error) {
    console.error("변경 실패:", error);
    alert("현재 비밀번호가 일치하지 않거나 오류가 발생했습니다.");
  }
};

// 삭제 핸들러 (브라우저 기본 confirm 사용)
const handleDeleteItem = async (drugId) => {
  if (confirm(`정말 즐겨찾기에서 삭제하시겠습니까?`)) {
    try {
      await drugStore.toggleFavorite(drugId);

      myFavorites.value = myFavorites.value.filter(item => item.id !== drugId);

      alert("삭제되었습니다.");
    } catch (error) {
      console.error("삭제 실패:", error);
      alert("즐겨찾기 해제에 실패했습니다. 다시 시도해 주세요.");
    }
  }
};

</script>

<template>
  <div class="min-vh-100 bg-light py-5">
    <div class="container" style="max-width: 800px">
      <div class="d-flex align-items-center gap-3 mb-4">
        <button
          class="btn btn-white border rounded-circle p-2 shadow-sm"
          @click="goBack"
        >
          <ArrowLeft :size="20" class="text-dark" />
        </button>
        <h2 class="h4 fw-bold mb-0">설정 및 관리</h2>
      </div>

      <div class="mb-4 overflow-auto">
        <ul
          class="nav nav-pills flex-nowrap bg-white p-1 rounded shadow-sm"
          style="min-width: 500px"
        >
          <li class="nav-item flex-fill">
            <button
              class="nav-link fw-bold text-center w-100"
              :class="{ active: activeTab === 'password' }"
              @click="activeTab = 'password'"
            >
              비밀번호
            </button>
          </li>
          <li class="nav-item flex-fill">
            <button
              class="nav-link fw-bold text-center w-100"
              :class="{ active: activeTab === 'favorites' }"
              @click="activeTab = 'favorites'"
            >
              즐겨찾기
            </button>
          </li>
        </ul>
      </div>

      <div v-if="activeTab === 'password'">
        <div class="card shadow-sm border-0">
          <div class="card-body p-4">
            <h3 class="h5 fw-bold mb-4">비밀번호 변경</h3>
            <form @submit.prevent="handlePasswordChange" class="w-100">
              <div class="mb-3">
                <label class="form-label fw-medium">현재 비밀번호</label>
                <input
                  type="password"
                  class="form-control"
                  v-model="passwordData.current"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label fw-medium">새 비밀번호</label>
                <input
                  type="password"
                  class="form-control"
                  v-model="passwordData.new"
                  required
                />
                <div class="form-text">8자 이상, 영문/숫자/특수문자 조합</div>
              </div>
              <div class="mb-4">
                <label class="form-label fw-medium">새 비밀번호 확인</label>
                <input
                  type="password"
                  class="form-control"
                  v-model="passwordData.confirm"
                  required
                />
              </div>
              <button type="submit" class="btn btn-primary w-100 py-2 fw-bold">
                비밀번호 변경
              </button>
            </form>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'favorites'">
        <div class="card shadow-sm border-0">
          <div class="card-body p-4">
            <h3 class="h5 fw-bold mb-4">즐겨찾기 관리</h3>
            <div class="d-flex flex-column gap-3">
              <div
                v-for="item in myFavorites"
                :key="item.id"
                class="border rounded p-3 d-flex justify-content-between align-items-center bg-white hover-bg shadow-sm"
              >
                <div class="d-flex align-items-center gap-3">
                  <div
                    class="bg-light rounded d-flex align-items-center justify-content-center"
                    style="width: 50px; height: 50px; overflow: hidden"
                  >
                    <img
                      v-if="item.image_url"
                      :src="item.image_url"
                      class="w-100 h-100 object-fit-contain"
                    />
                    <div v-else class="text-secondary opacity-50" :size="20">
                      <component :is="getFormIcon(item.form)" class="text-primary drug-icon"/>
                    </div>
                  </div>

                  <div>
                    <h4 class="h6 fw-bold mb-1">{{ item.name }}</h4>
                    <p class="text-secondary small mb-0">{{ item.company }}</p>
                  </div>
                </div>

                <button
                  class="btn btn-light text-danger btn-sm border"
                  @click="handleDeleteItem(item.id)"
                >
                  <Trash2 :size="18" />
                </button>
              </div>

              <div
                v-if="!myFavorites?.length"
                class="text-center py-5 text-secondary"
              >
                등록된 즐겨찾기가 없습니다.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.nav-pills .nav-link.active {
  background-color: #f8f9fa;
  color: #0d6efd;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
.nav-pills .nav-link {
  color: #6c757d;
}

.hover-bg:hover {
  background-color: #f8f9fa;
  transition: background-color 0.2s;
}

.btn-white {
  background-color: white;
}
.btn-white:hover {
  background-color: #f8f9fa;
}
.drug-icon {
  width: 25px;
  height: 25px;
}
</style>
