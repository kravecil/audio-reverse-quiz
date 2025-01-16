<script setup>
import { onMounted, useTemplateRef, computed } from "vue";
import { useCoreStore } from "../stores/core";

const core = useCoreStore();

// const audioPlayer = useTemplateRef("audioPlayer");
// onMounted(() => {
//   audioPlayer.value.playbackRate = -1;
// });
</script>

<template>
  <q-footer class="bg-grey-9">
    <audio controls preload="auto">
      <source :src="core.currentTrack.filepath" />
      Not supported
    </audio>
  </q-footer>
</template>
