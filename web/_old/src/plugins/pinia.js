import { createPinia } from 'pinia'

const pinia = createPinia()

export const usePiniaPlugin = (vueApp) => {
    vueApp.use(pinia)
}