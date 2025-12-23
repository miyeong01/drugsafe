import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useAccountStore = defineStore("accounts", () => {
  const router = useRouter();
  const token = ref(localStorage.getItem("token") || null);
  const userInfo = ref(null);

  // API 서버 주소 (Django)
  const API_URL = "http://127.0.0.1:8000";

  const getUserInfo = function () {
    if (!token.value) return;

    axios({
      method: "get",
      url: `${API_URL}/accounts/user/`, // dj-rest-auth의 기본 유저 정보 경로
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
      .then((res) => {
        userInfo.value = res.data; // 서버에서 받은 유저 정보(pk, username 등) 저장
      })
      .catch((err) => {
        console.error("유저 정보 로드 실패:", err);
      });
  };

  // 회원가입 액션
  const signup = function (payload) {
    const {
      username,
      password,
      confirmPassword,
      name,
      birthdate,
      phone,
      carrier,
      email,
    } = payload;

    axios({
      method: "post",
      url: `${API_URL}/accounts/signup/`,
      data: {
        username,
        password1: password,
        password2: confirmPassword,
        name,
        birthdate,
        phone,
        carrier,
        email,
      },
    })
      .then((res) => {
        alert("회원가입이 완료되었습니다! 로그인해 주세요.");
        router.replace({ query: { mode: "login" } });
      })
      .catch((err) => {
        console.error("회원가입 에러:", err.response?.data);
        alert("회원가입에 실패했습니다. 정보를 다시 확인해주세요.");
      });
  };

  const login = function (payload) {
    const { username, password } = payload;

    axios({
      method: "post",
      url: `${API_URL}/accounts/login/`,
      data: { username, password },
    })
      .then((res) => {
        token.value = res.data.key;
        localStorage.setItem("token", res.data.key);

        // ✅ 로그인 직후 유저 정보를 바로 가져옵니다.
        getUserInfo();

        alert("반갑습니다! 로그인이 완료되었습니다.");
        router.push("/");
      })
      .catch((err) => {
        console.log(err);
        alert("아이디 또는 비밀번호를 확인해주세요.");
      });
  };

  const isLogin = computed(() => {
    return token.value ? true : false;
  });

  const logOut = function () {
    axios({
      method: "post",
      url: `${API_URL}/accounts/logout/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
      .then(() => {
        console.log("서버 로그아웃 성공");
      })
      .catch((err) => {
        console.error("서버 로그아웃 실패(이미 만료되었을 수 있음):", err);
      })
      .finally(() => {
        token.value = null;
        userInfo.value = null;
        localStorage.removeItem("token");
        router.push({ name: "home" });
      });
  };

  if (token.value && !userInfo.value) {
    getUserInfo();
  }

  const changePassword = function (passwordData) {
    return axios({
      method: "post",
      url: `${API_URL}/accounts/password/change/`,
      data: {
        old_password: passwordData.current,
        new_password: passwordData.new,
        confirm_password: passwordData.confirm,
      },
      headers: {
        Authorization: `Token ${token.value}`,
      },
    });
  };

  return { signup, login, token, userInfo, getUserInfo, isLogin, logOut, changePassword };
});
