import { createApp } from "vue";
import App from "./App.vue";

import { useQuasarPlugin } from "./plugins/quasar";
import { usePiniaPlugin } from "./plugins/pinia";

const vueApp = createApp(App);

useQuasarPlugin(vueApp);
usePiniaPlugin(vueApp);

vueApp.mount("#app");
