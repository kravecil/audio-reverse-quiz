<script setup>
import { useCoreStore } from "../stores/core";

const core = useCoreStore();

defineProps(["info"]);

const onClick = (info) => {
  core.setCurrentTrack(info);
  // console.log(core.currentTrack); ////
};
</script>

<template>
  <q-item dark clickable v-ripple @click="onClick(info)">
    <q-item-section avatar>
      <q-icon name="music_note" />
    </q-item-section>
    <q-item-section>
      <q-item-label class="text-weight-bold">{{ info.desc }}</q-item-label>
      <q-item-label caption>{{ info.title }}</q-item-label>
    </q-item-section>
  </q-item>
</template>
