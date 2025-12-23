<script setup>
import { RouterLink } from 'vue-router';

// Footer는 표시할 데이터나 로직이 없어서 script 부분이 비어있어도 됩니다.
</script>

<template>
  <footer style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)">
    <div class="container py-5">
      
      <div class="row g-4">
        
        <div class="col-12 col-md-3">
          <h5 class="mb-4 fw-bold text-primary">DrugSafe</h5>
          <p class="text-secondary small">
            안전한 의약품 정보와 추천 서비스를 제공합니다.
          </p>
        </div>

        <div class="col-12 col-md-3">
          <h6 class="mb-4 fw-bold">서비스</h6>
          <ul class="list-unstyled text-secondary small">
            <li class="mb-2">
              <RouterLink to="/search" class="footer-link">
                약품 검색
              </RouterLink>
            </li>
            <li class="mb-2">
              <RouterLink to="/chatbot" class="footer-link">
                AI 챗봇
              </RouterLink>
            </li>
            <li class="mb-2">
              <RouterLink to="/community" class="footer-link">
                커뮤니티
              </RouterLink>
            </li>
          </ul>
        </div>

        <div class="col-12 col-md-3">
          <h6 class="mb-4 fw-bold">고객지원</h6>
          <ul class="list-unstyled text-secondary small">
            <li class="mb-2">
              <RouterLink to="/FAQ" class="footer-link">
                FAQ
              </RouterLink>
            </li>
          </ul>
        </div>

        <div class="col-12 col-md-3">
          <h6 class="mb-4 fw-bold">연락처</h6>
          <ul class="list-unstyled text-secondary small">
            <li class="mb-2">이메일: support@drugsafe.com</li>
            <li class="mb-2">전화: 1588-0000</li>
            <li class="mb-2">운영시간: 평일 9시-6시</li>
          </ul>
        </div>

      </div> <div class="mt-5 pt-4 border-top text-center text-secondary small">
        <p class="mb-0">&copy; 2025 DrugSafe. All rights reserved.</p>
      </div>
      
    </div>
  </footer>
</template>

<style scoped>
.footer-link {
  color: gray;
  text-decoration: none;
}
.footer-link:hover {
  color: gray;
  text-decoration: underline;
}
</style>