import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useDrugStore = defineStore('drug', () => {
  const drugs = ref([])
  const API_URL = 'http://127.0.0.1:8000'

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
  return { drugs, API_URL, getDrugs }
}, { persist: true })
