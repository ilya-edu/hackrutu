<template>
  <q-list class="rooms" padding>
    <div class="rooms__search bg-dark">
      <q-input class="q-mb-md q-mx-sm" label-color="white" bg-color="white" color="transparent" dense outlined hide-hint
      @focus="searchFocused=true" @blur="searchFocused=false" @mouseover="searchHovered = true"
      @mouseleave ="searchHovered = false" v-model="search"
            placeholder="Поиск">
            <template v-slot:append>
              <q-icon :color="searchIconColor" name="search" />
            </template>
          </q-input>
    </div>
    <q-item class="rooms__room" :class="{'rooms__room-selected': messageStore.currentRoomId === room.id}" @click="roomsStore.changeRoom(room.id, room.assistant_room_id);router.push('/user')" clickable v-ripple="{color: 'background2'}" v-for="room in searchedRooms" :key="room.id">
      {{ room.name }}
      <div class="column q-ml-sm items-center">
        <q-icon v-if="room.human_need" color="negative" class="q-mb-xs" size="20px" name="help_outline" />
        <q-btn flat dense round padding="4px" @click.stop="handleDelete(room.id)">
          <q-icon color="negative" size="20px" name="delete_outline" />
        </q-btn>
      </div>
    </q-item>
  </q-list>
</template>
<script setup lang="ts">// Компонент всех добавленных комнат, по нажатию на комнату происходит установка значений в сторах для работы с комнатой
import { MessageService } from 'src/api/services/MessageService'
import { useMessageStore } from 'src/stores/MessageStore'
import { useRoomsStore } from 'src/stores/RoomsStore'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const messageStore = useMessageStore()

const roomsStore = useRoomsStore()
const searchedRooms = computed(() => {
  return roomsStore.rooms.filter((room) => {
    return room.name.toLowerCase().includes(search.value.trim().toLowerCase())
  }).sort((room1, room2) => {
    if (room1.human_need) {
      return -1
    }
    if (room2.human_need) {
      return 1
    }
    return 0
  })
})

const search = ref('')
const searchHovered = ref(false)
const searchFocused = ref(false)

const searchIconColor = computed(() => {
  if (searchFocused.value) {
    return 'accent'
  }
  if (searchHovered.value) {
    return 'black'
  }
  return 'grey-8'
})

onMounted(async () => {
  roomsStore.rooms = await MessageService.getRooms()
  setInterval(async () => {
    roomsStore.rooms = await MessageService.getRooms()
  }, 3000)
})

async function handleDelete (id: number) {
  await MessageService.deleteRoom(id)
  roomsStore.rooms = await MessageService.getRooms()
}
</script>
<style scoped lang="scss">
.rooms{
  padding: 0px 8px;
  &__search {
    position: sticky;
    top:0px;
    padding-top:16px;
    z-index: 1;
    margin-right: 2px;
  }
  &__room {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-right: 2px;
  }
  &__room-selected {
    background-color: rgba(255, 255, 255, 0.208);
  }
}
</style>
