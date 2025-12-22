import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useAccountStore = defineStore("accounts", () => {
  const router = useRouter();
  const token = ref(localStorage.getItem('token') || null);
  const userData = ref(null);

  // API 서버 주소 (Django)
  const API_URL = "http://127.0.0.1:8000";

  // 회원가입 액션
  const signup = function (payload) {
    const { username, password, confirmPassword, name, birthdate, phone, carrier, email } = payload

    axios({
        method: 'post',
        url: `${API_URL}/accounts/signup/`,
        data: {
            username,
            password1: password,
            password2: confirmPassword,
            name,
            birthdate,
            phone,
            carrier,
            email
        }
    })
        .then(res => {
            alert('회원가입이 완료되었습니다! 로그인해 주세요.')
            router.replace({ query: {mode: 'login' } })
        })
        .catch(err => {
            console.error('회원가입 에러:', err.response?.data)
            alert('회원가입에 실패했습니다. 정보를 다시 확인해주세요.')
        })
  }

  const login = function (payload) {
    const { username, password } = payload

    axios({
        method: 'post',
        url: `${API_URL}/accounts/login/`,
        data: {
            username, password
        }
    })
        .then(res => {
            token.value = res.data.key
            localStorage.setItem('token', res.data.key)
            alert('반갑습니다! 로그인이 완료되었습니다.')
            router.push('/')
        })
        .catch(err => {
            console.log(err)
            alert('아이디 또는 비밀번호를 확인해주세요.')
        })
  }

  const isLogin = computed(() => {
    return token.value ? true : false
  })

  const logOut = function () {
    token.value = null
    localStorage.removeItem('token')

    axios({
        method: 'post',
        url: `${API_URL}/accounts/logout/`
    })
        .then((res) => {
            token.value = null
            router.push({ name: 'home' })
        })
        .catch((err) => console.log(err))
  }

  return { signup, login, token, userData, isLogin, logOut }
});
