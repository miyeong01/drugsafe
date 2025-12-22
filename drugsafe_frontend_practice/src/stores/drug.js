import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAccountStore } from "./accounts";

export const useDrugStore = defineStore(
  "drug",
  () => {
    const drugs = ref([]); // 검색 결과 리스트
    const selectedDrug = ref(null); // 상세 페이지에 보여줄 단일 약 정보
    const API_URL = "http://127.0.0.1:8000";
    const accountStore = useAccountStore();
    const reviews = ref([]); // 리뷰 목록 저장

    // 1. 약 목록 가져오기
    const getDrugs = function (searchKeyword = "", symptomId = null) {
      console.log("스토어 호출됨 - keyword:", searchKeyword, "ID:", symptomId);
      axios({
        method: "get",
        url: `${API_URL}/medicines/drugs/`,
        params: {
          search: searchKeyword,
          symptom: symptomId,
        },
      })
        .then((res) => {
          console.log(res);
          console.log(res.data);
          drugs.value = res.data;
        })
        .catch((err) => console.log(err));
    };

    // 2. 특정 약 상세 정보 가져오기
    const getDrugDetail = function (id) {
      // 페이지 이동 시 이전 데이터가 잠깐 보이는 것을 방지하기 위해 초기화
      selectedDrug.value = null;

      axios({
        method: "get",
        url: `${API_URL}/medicines/drugs/${id}/`,
      })
        .then((res) => {
          console.log("서버 응답 데이터:", res.data);
          selectedDrug.value = res.data;
        })
        .catch((err) => {
          console.log("상세 정보 로드 실패:", err);
        });
    };

    // 3. 해당 약의 리뷰 목록 가져오기
    const getReviews = function (id) {
      axios({
        method: "get",
        url: `${API_URL}/medicines/drugs/${id}/reviews/`,
      })
        .then((res) => (reviews.value = res.data))
        .catch((err) => console.log(err));
    };

    // 4. 리뷰 등록하기
    const createReview = function (id, reviewData) {
      // 토큰이 실제로 담겨있는지 콘솔에서 확인합니다.
      console.log("전송되는 토큰:", accountStore.token);

      return axios({
        method: "post",
        url: `${API_URL}/medicines/drugs/${id}/reviews/`,
        data: reviewData,
        headers: {
          Authorization: `Token ${accountStore.token}`, // Token과 값 사이에 공백이 있는지 확인
        },
      });
    };

    const selectedReview = ref(null);

    // 5. 특정 리뷰 상세 정보(댓글 포함) 가져오기
    const getReviewDetail = function (drugId, reviewId) {
      selectedReview.value = null; // 초기화
      axios({
        method: "get",
        url: `${API_URL}/medicines/drugs/${drugId}/reviews/${reviewId}/`,
      })
        .then((res) => {
          selectedReview.value = res.data;
        })
        .catch((err) => console.log(err));
    };

    // 6. 댓글 등록하기
    const createComment = function (reviewId, content) {
      return axios({
        method: "post",
        url: `${API_URL}/medicines/reviews/${reviewId}/comments/`, // URL은 urls.py 설정에 맞춰 확인 필요
        data: { content },
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      });
    };

    // 7. 리뷰 삭제
    const deleteReview = function (drugId, reviewId) {
      return axios({
        method: "delete",
        url: `${API_URL}/medicines/drugs/${drugId}/reviews/${reviewId}/`,
        headers: { Authorization: `Token ${accountStore.token}` },
      });
    };

    // 8. 리뷰 수정
    const updateReview = function (drugId, reviewId, reviewData) {
      return axios({
        method: "put",
        url: `${API_URL}/medicines/drugs/${drugId}/reviews/${reviewId}/`,
        data: reviewData,
        headers: { Authorization: `Token ${accountStore.token}` },
      });
    };

    // 9. 댓글 삭제
    const deleteComment = function (reviewId, commentId) {
      return axios({
        method: "delete",
        url: `${API_URL}/medicines/reviews/${reviewId}/comments/${commentId}/`,
        headers: { Authorization: `Token ${accountStore.token}` },
      });
    };

    return {
      drugs,
      selectedDrug,
      API_URL,
      reviews,
      getDrugs,
      getDrugDetail,
      getReviews,
      createReview,
      selectedReview,
      getReviewDetail,
      createComment,
      deleteReview,
      updateReview,
      deleteComment
    };
  },
  { persist: true }
);
