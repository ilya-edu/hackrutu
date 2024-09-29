<template>
  <div class="user-chat" ref="scrollContainer">
    <div
      class="user-chat__scroll-item"
      v-for="message in messages"
      :key="message.id"
    >
      <UserMessage :reverse="message.user.name === userStore.user.username" v-bind="message" :refs="message.references" />
    </div>
  </div>
</template>
<script setup lang="ts">// просто сгруппированные сообщения в комнате, реализована дозагрузка сообщений при прокручивании и поиск
import UserMessage from './UserMessage.vue'
import { Message, useMessageStore } from 'src/stores/MessageStore'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { MessageService } from 'src/api/services/MessageService'
import { useUserStore } from 'src/stores/UserStore'
import { debounce } from 'quasar'
import { useStorage } from '@vueuse/core'
import { useSearchStore } from 'src/stores/searchStore'
const currentRoomId = useStorage('currentRoom', -1)

const userStore = useUserStore()
const messageStore = useMessageStore()

const oldMessages = ref<Message[]>([])
let oldMessagesOffset = 0
const oldMessagesLoading = ref(false)
let lastMessagesLength = 0

const searchStore = useSearchStore()

const messages = computed<Message[]>(() => {
  if (lastMessagesLength !== searchStore.searchedMessages.length) {
    nextTick(() => {
      scrollBottom()
    })
  }
  lastMessagesLength = searchStore.searchedMessages.length
  if (lastMessagesLength) {
    return searchStore.searchedMessages
  }

  return [...[...messageStore.messages].reverse(), ...oldMessages.value]
})

const scrollContainer = ref<HTMLDivElement>()

function scrollBottom () {
  if (scrollContainer.value) {
    scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight
  }
}

function listenScroll () {
  if (scrollContainer.value?.clientHeight && scrollContainer.value.scrollHeight) {
    if (scrollContainer.value.clientHeight - scrollContainer.value.scrollHeight + 100 > scrollContainer.value?.scrollTop) {
      fetchMessages()
    }
  }
}

const fetchMessages = debounce(async function () {
  if (!oldMessagesLoading.value) {
    oldMessagesLoading.value = true
    oldMessages.value = [...oldMessages.value, ...(await MessageService.getMessages(oldMessagesOffset, useMessageStore))]
    oldMessagesOffset += 20
    oldMessagesLoading.value = false
  }
}, 500)

watch(() => messageStore.currentRoomId, (v) => {
  currentRoomId.value = v
  oldMessagesOffset = 0
  oldMessages.value = []
  fetchMessages()
})
onMounted(() => {
  if (messageStore.currentRoomId === -1 && currentRoomId.value !== -1) {
    messageStore.currentRoomId = currentRoomId.value
  }
  messageStore.connect()
  fetchMessages()
  if (scrollContainer.value) {
    scrollContainer.value.addEventListener('scroll', listenScroll)
  }
})
onBeforeUnmount(() => {
  scrollContainer.value?.removeEventListener('scroll', listenScroll)
})

defineExpose({
  scrollBottom
})
</script>
<style scoped lang="scss">
.user-chat {
  display: flex;
  flex-direction: column-reverse;
  max-height: 100%;
  overflow-y: scroll;
  &__scroll-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 20px;
    & > * {
      max-width: 1000px;
    }
  }
}
</style>
