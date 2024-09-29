<template>
  <div class="missing-page-wrapper">
    <div class="missing-page-wrapper__text">
      Страница не найдена
    </div>
    <q-btn filled @click="router.go(-1)" color="primary">Назад</q-btn>
  </div>
</template>
<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>
<style lang="scss" scoped>
@import "../css/quasar.variables.scss";

.missing-page-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;

  &__text{
    margin-top:20%;
    color: $primary;
    margin-bottom: 48px;
    font-size: 32px;
  }
}
</style>
