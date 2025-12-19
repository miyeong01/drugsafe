<script setup>
  import { RouterView, useRoute } from 'vue-router'
  import Header from './components/Header.vue' 
  import Footer from './components/Footer.vue'

  const route = useRoute()
</script>

<template>
  <div class="min-vh-100 d-flex flex-column">
    
    <Header v-if="!route.meta.hideHeader" />

    <main class="flex-grow-1">
      <RouterView />
    </main>

    <Footer v-if="!route.meta.hideFooter" /> 
    
  </div>
</template>

<style>
</style>