<template>
  <div class="index-page">
    <UserChat ref="chat" class="index-page__chat" />
    <div class="index-page__input-wrapper">
      <UserInput @send="chat.scrollBottom()" :store="useMessageStore" v-model:extended="expanded" v-model="input" />
    </div>
  </div>
</template>
<script setup lang="ts">// Страница для пользователя provider
import UserChat from 'src/components/UserChat.vue'
import UserInput from 'src/components/UserInput.vue'
import { useMessageStore } from 'src/stores/MessageStore'
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
    padding-right: 8px;
    padding-left: 20px;
    width: 100%;
    transition: padding 0.55s ease;
    padding-bottom: v-bind(chatPadding)
  }
  &__input-wrapper {
    @extend .background;
    position: absolute;
    border-radius: 1px;
    bottom: 0;
    width: calc(100% - 16px);
    padding: 0 16px 24px 16px;
    max-width: 1088px;
  }
}
</style>
