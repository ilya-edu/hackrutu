<template>
  <div
    @click="
      model = formattedSearch;
      prompt = undefined;
    "
    v-if="prompt"
    class="prompt"
  >
    <a>
      Возможно вы имели ввиду: {{ formattedSearch }}?
    </a>
  </div>
  <div class="mark-editor-wrapper" :class="{'user-input-animated': !focused}">
    <MdEditor :placeholder="chatMessage" @keydown="keyPress" class='mark-editor-wrapper__editor' @focus="focused = true" :toolbars-exclude="['github', 'catalog', 'htmlPreview', 'preview', 'fullscreen', 'pageFullscreen', 'save', 'image', 'codeRow']" :preview="false" language="ru" v-model="model" />
    <q-btn
        ref="btn"
        @click="extended = !extended"
        flat
        color="rgb(63, 74, 84)"
        class="mark-editor-wrapper__btn-expand"
        padding="0 4px 0 4px"
      >
        <q-icon
          :name="symRoundedKeyboardArrowUp"
          :class="{'rotate-180': extended}"
          size="24px"
          class="mark-editor-wrapper__btn-expand__icon"
        />
    </q-btn>
    <q-btn
        ref="btn"
        @click="model = ''"
        flat
        color="rgb(63, 74, 84)"
        class="mark-editor-wrapper__btn-delete"
        padding="0 4px 0 4px"
      >
        <q-icon
          :name="symRoundedDelete"
          :class="{'rotate-180': extended}"
          size="24px"
          class="mark-editor-wrapper__btn-delete__icon"
        />
    </q-btn>
    <transition
      appear
      enter-active-class="animated fadeIn"
      leave-active-class="animated fadeOut"
    >
      <q-btn
        ref="btn"
        @click="send()"
        v-show="model.trim().length"
        flat
        rounded
        color="secondary"
        class="mark-editor-wrapper__btn"
        padding="5px 6px 7px 6px"
      >
        <q-icon
          :name="symRoundedSend"
          size="30px"
          class="mark-editor-wrapper__btn__icon"
        />
      </q-btn>
    </transition>
  </div>
</template>
<script setup lang="ts">// поле для ввода сообщения, много стилей для красоты и отправка сообщений в комнату
import { symRoundedSend, symRoundedKeyboardArrowUp, symRoundedDelete } from '@quasar/extras/material-symbols-rounded'
import { QBtn, debounce } from 'quasar'
import { MessageService } from 'src/api/services/MessageService'
import { spellcheck } from 'src/api/services/SpellCheck'
import { computed, ref, watch } from 'vue'
import { MdEditor, config } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import ru from '@vavt/cm-extension/dist/locale/ru'
import { StoreDefinition } from 'pinia'
import { useTextStore } from 'src/stores/copyTextStore'

const focused = ref(false)

const model = computed({
  get () {
    return props.modelValue
  },
  set (v: string) {
    emit('update:modelValue', v)
  }
})

const extended = computed({
  get () {
    return props.extended
  },
  set (v: string) {
    emit('update:extended', v)
  }
})

const chatMessage = computed(() => {
  if (isNotLlmChat()) {
    return 'Чат с пользователем'
  }
  return 'Чат с ботом'
})

config({
  editorConfig: {
    languageUserDefined: {
      ru
    }
  }
})

const emit = defineEmits(['update:modelValue', 'update:extended', 'send'])

const props = defineProps<{
  modelValue: string;
  extended: boolean;
  store: StoreDefinition;
  llmEnabled?:true
}>()

async function send () {
  if (model.value) {
    await MessageService.sendMessage(model.value, props.store, props.llmEnabled)
    emit('send')
    setTimeout(() => {
      model.value = ''
      prompt.value = undefined
    }, 200)
  }
}

const prompt = ref<
  | {
      pos: number;
      len: number;
      s: string[];
    }[]
  | undefined
>(undefined)

const formattedSearch = computed(() => {
  let str = model.value
  if (prompt.value) {
    prompt.value.forEach((v) => {
      str = str.slice(0, v.pos) + v.s[0] + str.slice(v.pos + v.len)
    })
  } else {
    str = ''
  }
  return str
})
const store = props.store()
const textStore = useTextStore()

const searchHandle = async (v: string) => {
  const resp = await spellcheck(v)
  prompt.value = resp
  if (prompt.value && !prompt.value.length) {
    prompt.value = undefined
  }
}

const keyPress = (k: KeyboardEvent) => {
  if (k.shiftKey && k.key === 'Enter') {
    const event = new KeyboardEvent('keydown', {
      key: 'Enter',
      code: 'Enter',
      which: 13,
      keyCode: 13
    })
    document.getElementsByClassName('cm-content')[0].dispatchEvent(event)
    return
  }
  if (k.key === 'Enter') {
    send()
  }
}
function isNotLlmChat () {
  return store.$id === 'messages'
}

const debouncedSearch = debounce(searchHandle, 400)

const inputHeight = computed(() => {
  if (extended.value) {
    return '400px'
  }
  return '108px'
})

watch(() => textStore.copyText, () => {
  if (isNotLlmChat()) {
    const text = textStore.getText
    if (text) {
      model.value = text
    }
  }
})

watch(model, (v: string) => {
  if (v) {
    debouncedSearch(v)
  }
})
</script>
<style scoped lang="scss">
@use "sass:color";
@import "../css/quasar.variables.scss";

.mark-editor-wrapper{
  :deep(.md-editor-icon){
    fill: black !important;
  }

  :deep(.q-icon){
    fill: $secondary;
  }

  overflow: auto !important;
  border-radius: 16px;
  &__editor{
    position: static;
    overflow: auto !important;
    height: v-bind(inputHeight);
    transition: height 0.55s ease;
    border-radius: 16px;
    & :deep(.md-editor-footer){
      display: none;
    }
  }
  &__btn {
    position: absolute;
    right: 28px;
    top: 40px;
    &__icon {
      position: relative;
      top: 2px;
      left: 2px;
    }
  }
  &__btn-expand {
    position: absolute;
    right: 84px;
    top: 6px;
  }
  &__btn-delete {
    position: absolute;
    right: 114px;
    top: 6px;
  }
}

:deep(.cm-content *){
  color: black !important;

}
:deep(p){
    color: black !important;
}
:deep(.cm-placeholder){
  font-size: 20px;
  color: rgb(115, 115, 115) !important;
}

.user-input {
  background-color: white;
  border-radius: 28px;
  & :deep(.q-field__control:before) {
    border: none !important;
  }
  & :deep(.q-field__control) {
    padding-left: 24px;
  }
  & :deep(*) {
    font-size: 1.2rem;
  }
}

.prompt {
  position: absolute;
  top: -28px;
  left: 24px;
  background-color: $secondary;
  border-radius: 12px;
  padding: 2px 6px 2px 6px;
  cursor: pointer;
  &:hover {
    text-decoration: underline;
  }
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  max-width: 90%;
}

.category {
  border: 1px solid $primary;
  height: min-content;
  border-radius: 4px;
  padding: 0 8px;
  color: $primary;
}

.user-input-animated {
  animation: pulse-animation 1.5s infinite;
}

@keyframes pulse-animation {
  0% {
    box-shadow: 0 0 0 0 color.adjust($primary, $alpha: -0.8);
  }
  100% {
    box-shadow: 0 0 10px 20px color.adjust($primary, $alpha: -1);
  }
}
</style>
