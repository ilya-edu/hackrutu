<template>
  <div class="index-page">
    <ModelChat ref="chat" class="index-page__chat" />
    <div class="index-page__input-wrapper">
      <UserInput llm-enabled @send="chat.scrollBottom()" :store="useModelMessageStore" v-model:extended="expanded" v-model="input" />
    </div>
  </div>
</template>
<script setup lang="ts">// Компонент как UserPage, только для боковой панели, небольшие отличия
import ModelChat from './ModelChat.vue'
import UserInput from 'src/components/UserInput.vue'
import { useModelMessageStore } from 'src/stores/ModelMessageStore'
import { computed, ref } from 'vue'

const chat = ref()

const expanded = ref(false)
const input = ref('')
const chatPadding = computed(() => {
  if (expanded.value) {
    return '448px'
  }
  return '156px'
})
</script>
<style scoped lang="scss">
@import "../css/app.scss";

.index-page {
  height: calc(100vh - 58px);
  display: flex;
  align-items: center;
  flex-direction: column;
  &__chat{
    flex: 1 0 auto;
    width: 100%;
    transition: padding 0.55s ease;
    padding-right: 12px;
    padding-left: 18px;
    padding-bottom: v-bind(chatPadding)
  }
  &__input-wrapper {
    background-color: rgb(34, 34, 34);
    position: absolute;
    border-radius: 1px 1px 0 0;
    bottom: 0;
    width: calc(100% - 17px);
    padding: 0 12px 24px 12px;
    max-width: 1088px;
  }
}
</style>
