import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useDrugStore = defineStore('drug', () => {
  const drugs = ref([]) // 검색 결과 리스트
  const selectedDrug = ref(null) // 상세 페이지에 보여줄 단일 약 정보
  const API_URL = 'http://127.0.0.1:8000'

  // 1. 약 목록 가져오기
  const getDrugs = function (searchKeyword = '', symptomId = null) {
    console.log("스토어 호출됨 - keyword:", searchKeyword, "ID:", symptomId)
    axios({
      method: 'get',
      url: `${API_URL}/medicines/drugs/`,
      params: {
        search: searchKeyword,
        symptom: symptomId
      }
    })
      .then(res => {
        console.log(res)
        console.log(res.data)
        drugs.value = res.data
      })
      .catch(err => console.log(err))
  }

  // 2. 특정 약 상세 정보 가져오기
  const getDrugDetail = function (id) {
    // 페이지 이동 시 이전 데이터가 잠깐 보이는 것을 방지하기 위해 초기화
    selectedDrug.value = null 
    
    axios({
      method: 'get',
      url: `${API_URL}/medicines/drugs/${id}/`,
    })
      .then(res => {
        selectedDrug.value = res.data
      })
      .catch(err => {
        console.log("상세 정보 로드 실패:", err)
      })
  }

  return { drugs, selectedDrug, API_URL, getDrugs, getDrugDetail }
}, { persist: true })
