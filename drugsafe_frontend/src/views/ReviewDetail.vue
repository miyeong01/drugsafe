<template>
  <div v-if="selectedReview" class="min-vh-100 bg-light py-5">
    <div class="container" style="max-width: 900px">
      <button
        class="btn btn-light shadow-sm rounded-pill px-3 mb-4 d-flex align-items-center gap-2"
        @click="goBack"
      >
        <ArrowLeft :size="18" /> 목록으로
      </button>

      <div class="card border-0 shadow-sm p-4 p-md-5 mb-4">
        <div class="d-flex justify-content-between align-items-start mb-4">
          <div class="d-flex align-items-center gap-3 flex-grow-1">
            <div
              class="bg-primary bg-opacity-10 rounded-circle d-flex align-items-center justify-content-center"
              style="width: 50px; height: 50px"
            >
              <span class="fs-4">👤</span>
            </div>

            <div class="flex-grow-1">
              <div class="d-flex align-items-center gap-2 mb-1">
                <span class="fw-bold">{{ selectedReview.username }}님</span>
                <span class="text-secondary small border-start ps-2">{{
                  formatDate(selectedReview.created_at)
                }}</span>

                <div
                  v-if="accountStore.userInfo?.pk === selectedReview.user"
                  class="ms-auto d-flex gap-2"
                >
                  <button
                    class="btn btn-outline-secondary btn-sm border-0 p-1"
                    @click="onReviewEdit"
                    title="수정"
                  >
                    <Edit3 :size="18" />
                  </button>
                  <button
                    class="btn btn-outline-danger btn-sm border-0 p-1"
                    @click="onReviewDelete"
                    title="삭제"
                  >
                    <Trash2 :size="18" />
                  </button>
                </div>
              </div>

              <div class="d-flex align-items-center gap-2">
                <div class="text-warning small">
                  <span
                    v-for="i in 5"
                    :key="i"
                    :class="
                      i <= selectedReview.score
                        ? 'text-warning'
                        : 'text-secondary opacity-25'
                    "
                  >
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
      </div>

      <div class="card border-0 shadow-sm p-4 p-md-5 mb-4">
        <h3 class="h5 fw-bold mb-4">
          댓글
          <span class="text-primary">{{
            selectedReview.comments?.length || 0
          }}</span>
        </h3>

        <div class="mb-5">
          <textarea
            v-model="newComment"
            class="form-control mb-2"
            rows="3"
            placeholder="댓글을 입력하세요..."
          ></textarea>
          <div class="d-flex justify-content-end">
            <button
              class="btn btn-primary text-white px-4"
              @click="handleSubmitComment"
            >
              댓글 작성
            </button>
          </div>
        </div>

        <div class="d-flex flex-column gap-3">
          <div
            v-for="comment in selectedReview.comments"
            :key="comment.id"
            class="p-3 bg-light rounded shadow-sm"
          >
            <div class="d-flex gap-3">
              <div
                class="bg-white rounded-circle d-flex align-items-center justify-content-center border"
                style="width: 40px; height: 40px; flex-shrink: 0"
              >
                <span>👤</span>
              </div>
              <div class="flex-grow-1">
                <div class="d-flex align-items-center gap-2 mb-2">
                  <span class="fw-bold small">{{ comment.username }}님</span>
                  <span class="text-secondary" style="font-size: 0.75rem">
                    {{ formatDate(comment.created_at) }}
                  </span>

                  <button
                    v-if="accountStore.userInfo?.pk === comment.user"
                    class="btn btn-outline-danger btn-sm border-0 p-1 ms-auto"
                    @click="onCommentDelete(comment.id)"
                    title="삭제"
                  >
                    <Trash2 :size="18" />
                  </button>
                </div>
                <p class="mb-0 small lh-base">{{ comment.content }}</p>
              </div>
            </div>
          </div>
          <div
            v-if="!selectedReview.comments?.length"
            class="text-center py-4 text-secondary small"
          >
            첫 댓글을 남겨보세요!
          </div>
        </div>
      </div>
    </div>
  </div>

  <div
    v-else
    class="min-vh-100 d-flex flex-column justify-content-center align-items-center"
  >
    <div class="spinner-border text-primary mb-3"></div>
    <p class="text-secondary">리뷰 정보를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useDrugStore } from "@/stores/drug";
import { useAccountStore } from "@/stores/accounts";
import {
  ArrowLeft,
  ThumbsUp,
  Share2,
  MoreVertical,
  Trash2,
  Edit3,
} from "lucide-vue-next";

const route = useRoute();
const router = useRouter();
const drugStore = useDrugStore();
const accountStore = useAccountStore();

const { selectedReview } = storeToRefs(drugStore);
const newComment = ref("");

const drugId = route.params.drugId;
const reviewId = route.params.reviewId;

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
</style>
