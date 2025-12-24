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
    const myFavorites = ref([]); // 즐겨찾기 목록 담을 변수
    const myReviews = ref([]); // 실제 리뷰 데이터를 담을 변수
    const myReviewsPage = ref(1)
    const myReviewsTotal = ref(0)
    const myReviewsNext = ref(null)
    const myReviewsPrev = ref(null)
    const myComments = ref([]); // 댓글 저장용 변수
    const myCommentsPage = ref(1)
    const myCommentsTotal = ref(0)
    const myCommentsNext = ref(null)
    const myCommentsPrev = ref(null)
    const nextPage = ref(null);
    const prevPage = ref(null);
    const totalCount = ref(0);
    const reviewCount = ref(0);
    const reviewPage = ref(1);

    // 1. 약 목록 가져오기
    const getDrugs = function (
      searchKeyword = "",
      symptomId = null,
      page = 1,
      filters = {}
    ) {
      console.log(
        "스토어 호출됨 - keyword:",
        searchKeyword,
        "ID:",
        symptomId,
        "filters:",
        filters
      );

      const token = localStorage.getItem("token");
      const headers = token ? { Authorization: `Token ${token}` } : {};

      // ✅ params 객체 생성
      const params = {
        page: page,
      };

      // 검색어 또는 증상 ID 추가
      if (symptomId) {
        params.symptom = symptomId;
      } else if (searchKeyword) {
        params.search = searchKeyword;
      }

      // ✅ 제형 필터 추가 (배열을 콤마로 연결)
      if (filters.forms && filters.forms.length > 0) {
        params.form = filters.forms.join(",");
      }

      // ✅ 정렬 추가
      if (filters.sort) {
        params.sort = filters.sort;
      }

      console.log("최종 params:", params); // 디버깅용

      axios({
        method: "get",
        url: `${API_URL}/medicines/drugs/`,
        params: params,
        headers: headers,
      })
        .then((res) => {
          console.log("검색 결과:", res.data);
          drugs.value = res.data.results;
          nextPage.value = res.data.next;
          prevPage.value = res.data.previous;
          totalCount.value = res.data.count;
        })
        .catch((err) => console.log(err));
    };

    // 2. 특정 약 상세 정보 가져오기
    const getDrugDetail = function (id) {
      selectedDrug.value = null;

      // ✅ 로컬 스토리지에서 현재 로그인한 유저의 토큰을 가져옵니다.
      const token = localStorage.getItem("token");
      const headers = token ? { Authorization: `Token ${token}` } : {};

      axios({
        method: "get",
        url: `${API_URL}/medicines/drugs/${id}/`,
        headers: headers, // ✅ 반드시 헤더를 포함해야 장고가 '나'를 인식합니다.
      })
        .then((res) => {
          selectedDrug.value = res.data;
        })
        .catch((err) => {
          console.log("상세 정보 로드 실패:", err);
        });
    };

    // 3. 해당 약의 리뷰 목록 가져오기
    const getReviews = async (drugId = null, page = 1, params = {}) => {
      try {
        const token = localStorage.getItem("token");
        const headers = token ? { Authorization: `Token ${token}` } : {};

        const res = await axios.get(
          drugId
            ? `${API_URL}/medicines/drugs/${drugId}/reviews/`
            : `${API_URL}/medicines/reviews/`,
          {
            params: {
              page,
              ...params,
            },
            headers: headers,
          }
        );

        reviews.value = res.data.results;
        reviewPage.value = page;
        totalCount.value = res.data.count;
        nextPage.value = res.data.next;
        prevPage.value = res.data.previous;
      } catch (err) {
        console.error("리뷰 로드 실패", err);
      }
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
      selectedReview.value = null;

      // 1. 전달받은 인자가 유효한지 확인
      if (!drugId || !reviewId) {
        console.error(
          "ID가 누락되었습니다. drugId:",
          drugId,
          "reviewId:",
          reviewId
        );
        return;
      }

      const token = localStorage.getItem("token");
      const url = `${API_URL}/medicines/drugs/${drugId}/reviews/${reviewId}/`;

      // 2. 실제 요청 주소를 콘솔에서 클릭해 보세요.
      console.log("요청 URL:", url);

      axios({
        method: "get",
        url: url,
        headers: token ? { Authorization: `Token ${token}` } : {},
      })
        .then((res) => {
          selectedReview.value = res.data;
        })
        .catch((err) => {
          // 3. 서버가 보내주는 정확한 에러 코드를 확인합니다.
          console.error(`에러 발생! 상태 코드: ${err.response?.status}`);
          console.dir(err);
        });
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

    // 내 리뷰 조회 함수 수정
    const getMyReviews = async (page = 1) => {
      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        const res = await axios.get(`${API_URL}/medicines/user-reviews/`, {
          params: { page },
          headers: { Authorization: `Token ${token}` }
        });
        
        myReviews.value = res.data.results;
        myReviewsPage.value = page;
        myReviewsTotal.value = res.data.count;
        myReviewsNext.value = res.data.next;
        myReviewsPrev.value = res.data.previous;
      } catch (err) {
        console.error("내 리뷰 조회 실패:", err);
      }
    };

    // 내 댓글 조회 함수 수정
    const getMyComments = async (page = 1) => {
      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        const res = await axios.get(`${API_URL}/medicines/user-comments/`, {
          params: { page },
          headers: { Authorization: `Token ${token}` }
        });
        
        myComments.value = res.data.results;
        myCommentsPage.value = page;
        myCommentsTotal.value = res.data.count;
        myCommentsNext.value = res.data.next;
        myCommentsPrev.value = res.data.previous;
      } catch (err) {
        console.error("내 댓글 조회 실패:", err);
      }
    };

    // 12. 즐겨찾기 토글 함수
    const toggleFavorite = function (drugId) {
      // ✅ 반드시 return을 추가해야 컴포넌트에서 await가 작동합니다.
      return axios({
        method: "post",
        url: `${API_URL}/medicines/drugs/${drugId}/favorite/`,
        headers: {
          // accountStore의 토큰을 사용하거나 직접 가져옵니다.
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => {
          // 상세 정보 및 목록의 상태 업데이트
          if (selectedDrug.value && selectedDrug.value.id === drugId) {
            selectedDrug.value.is_favorite = !selectedDrug.value.is_favorite;
          }
          const drugInList = drugs.value.find((d) => d.id === drugId);
          if (drugInList) {
            drugInList.is_favorite = !drugInList.is_favorite;
          }
        })
        .catch((err) => {
          console.error("즐겨찾기 토글 실패:", err);
          throw err; // 에러를 상위(컴포넌트)로 전달
        });
    };

    // 13. 즐겨찾기 목록 가져오기 함수
    const getFavorites = function () {
      return axios({
        method: "get",
        url: `${API_URL}/medicines/user-favorites/`,
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => {
          myFavorites.value = res.data;
        })
        .catch((err) => {
          console.error("즐겨찾기 로드 실패:", err);
          throw err;
        });
    };

    // 14. 리뷰 '도움이 돼요' 토글 함수 추가
    const toggleHelpful = function (reviewId) {
      const token = localStorage.getItem("token");
      if (!token) return Promise.reject("로그인이 필요합니다.");

      return axios({
        method: "post",
        url: `${API_URL}/medicines/reviews/${reviewId}/helpful/`,
        headers: {
          Authorization: `Token ${token}`,
        },
      })
        .then((res) => {
          // ✨ 실시간으로 스토어의 reviews 배열 내 데이터를 업데이트합니다.
          const review = reviews.value.find((r) => r.id === reviewId);
          if (review) {
            review.helpful_count = res.data.helpful_count;
            review.is_helpful = res.data.is_helpful;
          }

          if (selectedReview.value && selectedReview.value.id === reviewId) {
            selectedReview.value.helpful_count = res.data.helpful_count;
            selectedReview.value.is_helpful = res.data.is_helpful;
          }
          return res.data;
        })
        .catch((err) => {
          console.error("도움이 돼요 토글 실패:", err);
          throw err;
        });
    };

    return {
      drugs,
      nextPage,
      prevPage,
      reviewPage,
      totalCount,
      selectedDrug,
      API_URL,
      reviews,
      nextPage,
      prevPage,
      reviewCount,
      getDrugs,
      getDrugDetail,
      getReviews,
      createReview,
      selectedReview,
      getReviewDetail,
      createComment,
      deleteReview,
      updateReview,
      deleteComment,
      myReviews,
      myReviewsPage,
      myReviewsTotal,
      myReviewsNext,
      myReviewsPrev,
      getMyReviews,
      myComments,
      myCommentsPage,
      myCommentsTotal,
      myCommentsNext,
      myCommentsPrev,
      getMyComments,
      toggleFavorite,
      myFavorites,
      getFavorites,
      toggleHelpful,
    };
  },
  { persist: true }
);
