<script setup>
import { ref } from 'vue'

const ERROR_IMG_SRC =
  'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODgiIGhlaWdodD0iODgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgc3Ryb2tlPSIjMDAwIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBvcGFjaXR5PSIuMyIgZmlsbD0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIzLjciPjxyZWN0IHg9IjE2IiB5PSIxNiIgd2lkdGg9IjU2IiBoZWlnaHQ9IjU2IiByeD0iNiIvPjxwYXRoIGQ9Im0xNiA1OCAxNi0xOCAzMiAzMiIvPjxjaXJjbGUgY3g9IjUzIiBjeT0iMzUiIHI9IjciLz48L3N2Zz4KCg=='

// props 정의 (src와 alt는 명시적으로 받고, 나머지는 $attrs로 자동 처리됩니다)
defineProps({
  src: {
    type: String,
    required: true
  },
  alt: {
    type: String,
    default: ''
  }
})

const didError = ref(false)

const handleError = () => {
  didError.value = true
}
</script>

<template>
  <div
    v-if="didError"
    class="inline-block bg-gray-100 text-center align-middle"
  >
    <div class="flex items-center justify-center w-full h-full">
      <img 
        :src="ERROR_IMG_SRC" 
        alt="Error loading image" 
        :data-original-url="src"
      />
    </div>
  </div>

  <img
    v-else
    :src="src"
    :alt="alt"
    @error="handleError"
  />
</template>

<style scoped>
/* Vue는 부모에서 전달된 class와 style을 
  자동으로 현재 렌더링된 루트 요소(div 또는 img)에 합쳐줍니다.
*/
</style>