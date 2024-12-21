<template>
  <transition
    enter-active-class="animate-enter"
    leave-active-class="animate-leave"
    appear
  >
    <slot></slot>
  </transition>
</template>

<script setup>
// Tidak ada logika yang diperlukan
</script>

<style scoped>
.animate-enter {
  animation: slideIn 0.5s ease-out;
}

.animate-leave {
  animation: slideOut 0.5s ease-in;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideOut {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(20px);
  }
}
</style> 
