<template>
  <div></div>
</template>
<script setup lang="ts">// Страница для тг бота, просто устанавливает все необходимые сторы и редиректит
import { MessageService } from 'src/api/services/MessageService'
import { useMessageStore } from 'src/stores/MessageStore'
import { useUserStore } from 'src/stores/UserStore'
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const userStore = useUserStore()
const messageStore = useMessageStore()

const route = useRoute()
const router = useRouter()

onMounted(async () => {
  messageStore.disconnect()
  messageStore.currentRoomId = null
  const text = route.query.message + ''
  userStore.user.username = route.query.username?.slice(1) + ''
  await router.push({ name: 'User' })
  setTimeout(() => {
    MessageService.sendMessage(text, useMessageStore)
  }, 300)
})
</script>
