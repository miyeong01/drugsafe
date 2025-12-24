<template>
  <div v-if="selectedReview" class="min-vh-100 bg-light py-5">
    <div class="container" style="max-width: 900px">
      <button class="btn btn-light shadow-sm rounded-pill px-3 mb-4 d-flex align-items-center gap-2" @click="goBack">
        <ArrowLeft :size="18" /> 목록으로
      </button>

      <div class="card border-0 shadow-sm p-4 p-md-5 mb-4">
        <div class="d-flex justify-content-between align-items-start mb-4">
          <div class="d-flex align-items-center gap-3 flex-grow-1">
            <div class="bg-primary bg-opacity-10 rounded-circle d-flex align-items-center justify-content-center"
              style="width: 50px; height: 50px">
              <span class="fs-4">👤</span>
            </div>

            <div class="flex-grow-1">
              <div class="d-flex align-items-center gap-2 mb-1">
                <span class="fw-bold">{{ selectedReview.username }}님</span>
                <span class="text-secondary small border-start ps-2">{{ selectedReview.drug_name }}</span>
                <span class="text-secondary small border-start ps-2">{{
                  formatDate(selectedReview.created_at)
                }}</span>

                <div v-if="accountStore.userInfo?.pk === selectedReview.user" class="ms-auto d-flex gap-2">
                  <button class="btn btn-outline-secondary btn-sm border-0 p-1" @click="onReviewEdit" title="수정">
                    <Edit3 :size="18" />
                  </button>
                  <button class="btn btn-outline-danger btn-sm border-0 p-1" @click="onReviewDelete" title="삭제">
                    <Trash2 :size="18" />
                  </button>
                </div>
              </div>

              <div class="d-flex align-items-center gap-2">
                <div class="text-warning small">
                  <span v-for="i in 5" :key="i" :class="i <= selectedReview.score
                    ? 'text-warning'
                    : 'text-secondary opacity-25'
                    ">
                    ★
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <h2 class="fw-bold mb-4">{{ selectedReview.title }}</h2>
        <div class="mb-2">
          <p class="text-dark lh-lg mb-0" style="white-space: pre-wrap">
            {{ selectedReview.content }}
          </p>
        </div>

        <div class="d-flex justify-content-start border-top pt-4">
          <button class="btn rounded-pill px-4 py-2 d-flex align-items-center gap-2 shadow-sm transition-all border"
            :class="selectedReview.is_helpful ? 'btn-danger text-white border-danger' : 'btn-light text-muted'"
            @click="onToggleHelpful(selectedReview.id)">
            <ThumbsUp :size="18" :fill="selectedReview.is_helpful ? 'white' : 'none'" />
            <span class="fw-bold">도움이 돼요</span>
            <span class="badge bg-white text-danger ms-1 px-2" v-if="selectedReview.helpful_count > 0">
              {{ selectedReview.helpful_count }}
            </span>
          </button>
        </div>
      </div>

      <div class="card border-0 shadow-sm p-4 p-md-5 mb-4">
        <h3 class="h5 fw-bold mb-4">
          댓글
          <span class="text-primary">{{
            selectedReview.comments?.length || 0
          }}</span>
        </h3>

        <div class="mb-5">
          <textarea v-model="newComment" class="form-control mb-2" rows="3" placeholder="댓글을 입력하세요..."></textarea>
          <div class="d-flex justify-content-end">
            <button class="btn btn-primary text-white px-4" @click="handleSubmitComment">
              댓글 작성
            </button>
          </div>
        </div>

        <div class="d-flex flex-column gap-3">
          <div v-for="comment in paginatedComments" :key="comment.id" class="p-3 bg-light rounded shadow-sm">
            <div class="d-flex gap-3">
              <div class="bg-white rounded-circle d-flex align-items-center justify-content-center border"
                style="width: 40px; height: 40px; flex-shrink: 0">
                <span>👤</span>
              </div>
              <div class="flex-grow-1">
                <div class="d-flex align-items-center gap-2 mb-2">
                  <span class="fw-bold small">{{ comment.username }}님</span>
                  <span class="text-secondary" style="font-size: 0.75rem">
                    {{ formatDate(comment.created_at) }}
                  </span>

                  <button v-if="accountStore.userInfo?.pk === comment.user"
                    class="btn btn-outline-danger btn-sm border-0 p-1 ms-auto" @click="onCommentDelete(comment.id)"
                    title="삭제">
                    <Trash2 :size="18" />
                  </button>
                </div>
                <p class="mb-0 small lh-base">{{ comment.content }}</p>
              </div>
            </div>
          </div>

          <nav v-if="totalPages > 1" class="d-flex justify-content-center mt-4">
            <div class="minimal-pagination d-flex align-items-center gap-3">
              <button class="btn-arrow" :disabled="currentPage === 1" @click="changePage(currentPage - 1)">
                <ChevronLeft :size="20" />
              </button>

              <div class="current-page-display shadow-sm">
                <span class="fw-bold text-primary">{{ currentPage }}</span>
                <span class="text-muted mx-1">/</span>
                <span class="text-secondary small">{{ totalPages }}</span>
              </div>

              <button class="btn-arrow" :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">
                <ChevronRight :size="20" />
              </button>
            </div>
          </nav>

          <div v-if="!selectedReview.comments?.length" class="text-center py-4 text-secondary small">
            첫 댓글을 남겨보세요!
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="min-vh-100 d-flex flex-column justify-content-center align-items-center">
    <div class="spinner-border text-primary mb-3"></div>
    <p class="text-secondary">리뷰 정보를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useDrugStore } from "@/stores/drug";
import { useAccountStore } from "@/stores/accounts";
import {
  ArrowLeft,
  Trash2,
  Edit3,
  ChevronLeft,
  ChevronRight,
  ThumbsUp
} from "lucide-vue-next";

const route = useRoute();
const router = useRouter();
const drugStore = useDrugStore();
const accountStore = useAccountStore();

const { selectedReview } = storeToRefs(drugStore);
const newComment = ref("");

const drugId = route.params.drugId;
const reviewId = route.params.reviewId;

const currentPage = ref(1);
const itemsPerPage = 10;

onMounted(async () => {
  // 1. 로그인 상태인데 내 정보(userInfo)가 없다면 서버에서 가져오기
  if (accountStore.token && !accountStore.userInfo) {
    try {
      // accountStore에 getUserInfo라는 함수가 있는지 확인해보세요!
      await accountStore.getUserInfo();
    } catch (err) {
      console.error("유저 정보를 가져오는데 실패했습니다:", err);
    }
  }

  // 2. 그 다음 리뷰 상세 데이터 불러오기
  drugStore.getReviewDetail(drugId, reviewId);
});

const goBack = () => router.back();

const formatDate = (dateString) => {
  if (!dateString) return "";
  return new Date(dateString).toLocaleDateString();
};

const handleSubmitComment = () => {
  if (!accountStore.isLogin) {
    alert("댓글 작성을 위해 로그인이 필요합니다.");
    return;
  }
  if (!newComment.value.trim()) return;

  drugStore
    .createComment(reviewId, newComment.value)
    .then(() => {
      newComment.value = "";
      // 댓글 작성 후 목록을 새로고침하기 위해 다시 호출
      drugStore.getReviewDetail(drugId, reviewId);
    })
    .catch((err) => {
      console.error(err);
      alert("댓글 등록에 실패했습니다.");
    });
};

// 리뷰 삭제 함수
const onReviewDelete = () => {
  if (confirm("정말로 이 리뷰를 삭제하시겠습니까?")) {
    drugStore
      .deleteReview(drugId, reviewId)
      .then(() => {
        alert("리뷰가 삭제되었습니다.");
        router.push({ name: "drug-detail", params: { drugId: drugId } });
      })
      .catch((err) => console.error(err));
  }
};

// 리뷰 수정 페이지 이동
const onReviewEdit = () => {
  router.push({
    name: "ReviewWrite",
    params: { drugId: drugId },
    query: { edit: true, reviewId: reviewId },
  });
};

// 댓글 삭제 함수
const onCommentDelete = (commentId) => {
  if (confirm("댓글을 삭제하시겠습니까?")) {
    drugStore
      .deleteComment(reviewId, commentId)
      .then(() => {
        drugStore.getReviewDetail(drugId, reviewId); // 목록 새로고침
      })
      .catch((err) => console.error(err));
  }
};

// 전체 페이지 수 계산
const totalPages = computed(() => {
  const count = selectedReview.value?.comments?.length || 0;
  return Math.ceil(count / itemsPerPage) || 1;
});

// 현재 페이지에 해당하는 댓글만 추출 (v-for 대상)
const paginatedComments = computed(() => {
  const list = selectedReview.value?.comments || [];
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return list.slice(start, end);
});

// 페이지 변경 함수
const changePage = (page) => {
  currentPage.value = page;
};

// 리뷰가 바뀌거나 댓글이 삭제/추가되어 데이터가 갱신될 때 페이지 번호 유효성 체크
watch(() => selectedReview.value?.comments?.length, (newVal) => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = Math.max(1, totalPages.value);
  }
});

const onToggleHelpful = (reviewId) => {
  if (!accountStore.isLogin) {
    if (confirm("로그인이 필요한 기능입니다. 로그인 페이지로 이동하시겠습니까?")) {
      router.push({ path: "/auth", query: { mode: "login" } });
    }
    return;
  }
  // 스토어의 액션 호출 (서버와 통신 후 selectedReview 상태가 자동으로 업데이트됩니다)
  drugStore.toggleHelpful(reviewId);
};
</script>

<style scoped>
.btn-primary {
  background-color: #0d6efd;
  border: none;
}

.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
}

/* 페이지네이션 컨테이너 스타일 */
.minimal-pagination {
  background-color: white;
  padding: 8px 16px;
  border-radius: 50px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5f0ff;
}

/* 화살표 버튼 */
.btn-arrow {
  border: none;
  background: none;
  color: #0d6efd;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.btn-arrow:hover:not(:disabled) {
  background-color: #f0f7ff;
  transform: scale(1.1);
}

.btn-arrow:disabled {
  color: #dee2e6;
  cursor: not-allowed;
}

/* 중앙 번호 표시 박스 */
.current-page-display {
  background-color: #f8f9fa;
  padding: 6px 18px;
  border-radius: 20px;
  min-width: 80px;
  text-align: center;
  border: 1px solid #edf2f7;
}

.current-page-display span {
  font-size: 0.9rem;
}
</style>
