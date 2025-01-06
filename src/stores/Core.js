import { defineStore, acceptHMRUpdate } from 'pinia'
import { ref } from 'vue'

const SOURCES_URL = ''

export const useCoreStore = defineStore('core', () => {
  const search = ref('')
  const songs = ref([])

  return {
    search,
    songs,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useCoreStore, import.meta.hot))
}
