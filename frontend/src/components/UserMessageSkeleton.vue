<template>
  <div class="user-message">
    <div>
      <q-icon
        class="user-message__avatar"
        :color="'primary'"
        :name="symRoundedNeurology
        "
        size="40px"
      />
      <div
        class="user-message__text-block"
      >
        <div class="user-message__text-block__name">
          Формируем ответ
        </div>
        <div
          class="user-message__text-block__text"
        >
          <q-spinner-dots
            color="primary"
            size="2em"
          />
        </div>
      </div>
    </div>
    <q-space />
  </div>
</template>
<script setup lang="ts">// Просто обёртка для ответа бота
import { symRoundedNeurology } from '@quasar/extras/material-symbols-rounded'

</script>
<style scoped lang="scss">
.user-message {
  display: flex;
  width: 100%;
  & > :first-child {
    display: flex;
  }
  &__text-block {
    background-color: white;
    margin: 0 16px;
    border-radius: 16px;
    padding: 8px 16px 12px 16px;
    &__name {
      font-size: 18px;
      color: $primary;
    }
    &__text {
      overflow-wrap: anywhere;
    }
  }
}
.reverse {
  flex-direction: row-reverse;
}
.reverse-color {
  background-color: rgb(227, 237, 255);
}
</style>
