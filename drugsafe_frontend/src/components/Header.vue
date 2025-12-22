<script setup>
import { useRouter, useRoute } from "vue-router";
import { Heart, User, Menu, Pill } from "lucide-vue-next";
import { useAccountStore } from "@/stores/accounts";
import { storeToRefs } from "pinia";
import { handleError } from "vue";

const router = useRouter();
const route = useRoute();
const accountStore = useAccountStore();

const { isLogin } = storeToRefs(accountStore);

const isActive = (pageName) => route.name === pageName;
const goHome = () => router.push("/");

const goAuth = (mode) => {
  router.push({ path: "/auth", query: { mode: mode } });
};

const handleLogout = () => {
  accountStore.logOut();
};
</script>

<template>
  <header class="border-bottom bg-white sticky-top py-3">
    <div class="container-fluid px-4">
      <div
        class="d-flex align-items-center justify-content-between"
        style="height: 40px"
      >
        <div
          class="d-flex align-items-center gap-2"
          @click="goHome"
          style="cursor: pointer"
        >
          <div
            class="rounded-circle bg-primary d-flex align-items-center justify-content-center"
            style="width: 36px; height: 36px"
          >
            <Pill class="text-white" :size="20" />
          </div>
          <span class="text-primary fw-bold fs-5">DrugSafe</span>
        </div>

        <nav class="d-none d-md-flex align-items-center gap-5">
          <RouterLink
            to="/"
            class="text-decoration-none fw-medium"
            :class="isActive('home') ? 'text-primary' : 'text-dark'"
          >
            Home
          </RouterLink>

          <RouterLink
            to="/chatbot"
            class="text-decoration-none fw-medium"
            :class="isActive('chatbot') ? 'text-primary' : 'text-dark'"
          >
            ChatBot
          </RouterLink>

          <RouterLink
            to="/community"
            class="text-decoration-none fw-medium"
            :class="isActive('community') ? 'text-primary' : 'text-dark'"
          >
            Community
          </RouterLink>

          <RouterLink
            to="/FAQ"
            class="text-decoration-none fw-medium"
            :class="isActive('FAQ') ? 'text-primary' : 'text-dark'"
          >
            FAQ
          </RouterLink>
        </nav>

        <div class="d-flex align-items-center gap-2">
          <template v-if="!isLogin">
            <button
              @click="goAuth('signup')"
              class="btn btn-outline-secondary btn-sm fw-medium px-3 ms-2"
              style="border-color: #dee2e6; color: #495057"
            >
              SignUp
            </button>

            <button
              @click="goAuth('login')"
              class="btn btn-primary btn-sm fw-medium px-3 text-white"
            >
              Login
            </button>
          </template>

          <template v-else>
            <button
              class="btn p-2 border-0 text-dark"
              @click="router.push('/profile')"
            >
              <User :size="20" />
            </button>
            
            <button @click="handleLogout" class="btn btn-primary btn-sm fw-medium px-3 text-white">
              LogOut
            </button>
          </template>

          <button class="btn p-2 border-0 text-dark d-md-none">
            <Menu :size="20" />
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.gap-2 {
  gap: 0.5rem;
}
.gap-5 {
  gap: 3rem;
}
</style>
