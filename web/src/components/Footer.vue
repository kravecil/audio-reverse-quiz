<script setup>
import { useTemplateRef } from "vue";
import { useCoreStore } from "../stores/core";

const core = useCoreStore();

core.audioPlayerRef = useTemplateRef("audioPlayer");
</script>

<template>
  <q-footer class="bg-grey-9">
    <audio controls ref="audioPlayer" v-if="core.currentTrack !== undefined">
      <source :src="core.currentTrack.storageFile" />
      Not supported
    </audio>
  </q-footer>
</template>
