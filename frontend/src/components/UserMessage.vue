<template>
  <div class="user-message" :class="{ reverse: reverse }">
    <div :class="{ reverse: reverse }">
      <q-icon
        color="rgb(210, 210, 210)"
        :name="
          setIcon()
        "
        size="40px"
      />
      <div class="user-message__thumbs" >
        <template v-if="userStore.user.username !== props.user.name && userStore.user.username !== 'admin'">
          <q-btn :flat="!like" class="q-mb-xs" dense round color="positive" @click="setLike()">
            <q-icon size="24px" :name="symRoundedThumbUp" />
          </q-btn>
        </template>
        <q-btn v-if="props.user.name==='llm'" :icon="symRoundedCopyAll" round dense size="md" class="q-mt-sm" flat @click="copyText()" />
      </div>
      <div class="user-message__content" :style="{alignItems: reverse?'end':'start'}">
        <div class="q-mx-md q-mb-xs text-grey-8" :style="{textAlign: reverse?'right': 'start'}">
          {{ timeFormat() }}
        </div>
        <div
          class="user-message__text-block"
          :class="{ 'reverse-color': reverse }"
        >
          <div
            class="user-message__text-block__text"
            ref="preview"
            :class="{ 'q-mt-xs': reverse }"
          >
            <MdPreview style="background-color: transparent;" :modelValue="formatMessageText()" language="ru"/>
          </div>
        </div>
        <div class="user-message__links q-gutter-sm" :style="{justifyContent: reverse?'end':'start'}">

          <div v-for="ref in props.refs" :key="ref" class="row no-wrap items-center">
            <q-btn :ripple="false" :icon="symRoundedCopyAll" round dense size="md" flat @click="copyText(parseRef(ref).name)" />
            <div @click="handleRefClick(JSON.parse(ref).url)"  class="user-message__links__link relative-position" v-ripple="{ color: 'blue-3' }" :style="{ borderRadius: reverse?'24px 6px 24px 24px':'6px 24px 24px 24px'}">
              {{ parseRef(ref).name }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">// Одно из сообщений пользователя\бота\админа. Много логики для работы маркдауна и много стилей для корректного отображения
import { symRoundedSupportAgent, symRoundedNeurology, symRoundedPerson, symRoundedThumbUp, symRoundedCopyAll } from '@quasar/extras/material-symbols-rounded'
import { Message } from 'src/stores/MessageStore'
import { MdPreview, config } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import ru from '@vavt/cm-extension/dist/locale/ru'
import { onMounted, ref } from 'vue'
import { useUserStore } from 'src/stores/UserStore'
import { useTextStore } from 'src/stores/copyTextStore'
import { useStorage } from '@vueuse/core'

const textStore = useTextStore()

function setIcon () {
  if (props.user.name === 'admin') {
    return symRoundedSupportAgent
  }
  if (props.user.name === 'llm') {
    return symRoundedNeurology
  }
  return symRoundedPerson
}

config({
  editorConfig: {
    languageUserDefined: {
      ru
    }
  }
})

const userStore = useUserStore()

const like = ref(false)
const likes = useStorage('likes', [] as number[])

const preview = ref<HTMLDivElement>()

const timeFormat = () => {
  const tIndex = props.created_at.indexOf('T')
  const commaIndex = props.created_at.indexOf('.')
  return props.created_at.slice(tIndex + 1, commaIndex - 3)
}

const parseRef = (reference: string) => {
  return JSON.parse(reference)
}

const formatMessageText = () => {
  return props.text.replaceAll('\'\'\'', '```')
}

function handleRefClick (url: string) {
  window.open(url, '_blank')
}

function copyText (text?:string) {
  navigator.clipboard.writeText(props.text)
  textStore.copyText = text || props.text
}

function setLike () {
  like.value = true
  if (!likes.value.includes(props.id) && likes.value) {
    likes.value.push(props.id)
  }
}

onMounted(() => {
  const links = preview.value?.querySelectorAll('a') as HTMLLinkElement[] | undefined
  links?.forEach((link) => {
    if (link.href.slice(-4) === '.svg' || link.href.slice(-4) === '.jpg' || link.href.slice(-4) === '.png' || link.href.slice(-4) === 'webp') {
      const img = document.createElement('img')
      img.src = link.href
      link.replaceWith(img)
    }
  })
  if (likes.value.includes(props.id)) {
    like.value = true
  }
})

const props = defineProps<Message & { reverse?: boolean, refs: string[] | null }>()
</script>
<style scoped lang="scss">
:deep(blockquote){
  background-color: $dark-page;
}
:deep(code){
  max-width: calc(100% - 49px);
}
.user-message {
  display: flex;
  position: relative;
  width: 100%;
  padding-right: 56px;
  & * {
    max-width: 100%;
  }
  & > :first-child {
    display: flex;
  }
  &__text-block {
    background-color: $secondary;
    margin: 0 16px;
    border-radius: 4px 16px 16px 4px;
    padding: 8px 16px 12px 16px;

    &__name {
      font-size: 18px;
      color: $primary;
    }
    &__text {
      & :deep(.md-editor-preview-wrapper){
        padding: 0;
      }
      & :deep(.md-editor-preview){
        word-break: normal;
      }
      & :deep(.md-editor-preview > :first-child){
        margin-top: 0;
      }
      & :deep(.md-editor-preview > :last-child){
        margin-bottom: 0;
      }
    }
  }
  &__content{
    display: flex;
    flex-direction: column;
    position: relative;
  }
  &__thumbs {
    position: absolute;
    display: flex;
    flex-direction: column;
    margin-left: 2px;
    margin-right: 2px;
    top:42px;
  }
  &__links{
    display: flex;
    flex-wrap: wrap;
    margin: 8px 16px 0 8px;
    &__link{
      background-color: $secondary;
      color:white;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      cursor: pointer;
      padding: 8px 12px;
      &:hover{
        filter: brightness(110%);
      }
    }
  }
}
.reverse {
  flex-direction: row-reverse;
  padding-right: 0;
  padding-left: 56px;
  & .user-message__text-block{
    border-radius: 16px 4px 4px 16px;
  }
}
.reverse-color {
  background-color: $secondary;
}

</style>
