<script setup>
// Footer는 표시할 데이터나 로직이 없어서 script 부분이 비어있어도 됩니다.
</script>

<template>
  <footer class="bg-white border-t border-border mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <h3 class="mb-4 font-bold text-lg">DrugSafe</h3>
          <p class="text-muted-foreground text-sm">
            안전한 의약품 정보와 추천 서비스를 제공합니다.
          </p>
        </div>

        <div>
          <h4 class="mb-4 font-medium">서비스</h4>
          <ul class="space-y-2 text-muted-foreground text-sm">
            <li>약품 검색</li>
            <li>증상별 추천</li>
            <li>복용 관리</li>
            <li>리뷰 커뮤니티</li>
          </ul>
        </div>

        <div>
          <h4 class="mb-4 font-medium">고객지원</h4>
          <ul class="space-y-2 text-muted-foreground text-sm">
            <li>FAQ</li>
            <li>이용약관</li>
            <li>개인정보처리방침</li>
            <li>문의하기</li>
          </ul>
        </div>

        <div>
          <h4 class="mb-4 font-medium">연락처</h4>
          <ul class="space-y-2 text-muted-foreground text-sm">
            <li>이메일: support@drugsafe.com</li>
            <li>전화: 1588-0000</li>
            <li>운영시간: 평일 9시-6시</li>
          </ul>
        </div>
      </div>

      <div class="mt-8 pt-8 border-t border-border text-center text-muted-foreground text-sm">
        <p>&copy; 2025 DrugSafe. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>