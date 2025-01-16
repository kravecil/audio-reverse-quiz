<script setup>
import { onMounted, useTemplateRef } from "vue";
import { useCoreStore } from "../stores/core";

const core = useCoreStore();

// const audioPlayer = useTemplateRef("audioPlayer");
// onMounted(() => {
//   audioPlayer.value.playbackRate = -1;
// });
</script>

<template>
  <q-footer class="bg-grey-9">
    <audio controls>
      <!-- <source :src="core.currentTrack.filepath" /> -->
      <source
        src="https://rus.hitmotop.com/get/music/20180320/Giorgi_Latso_Klod_Debyussi_-_Prludes_Book_2_L_123_No_10_Canope_54700573.mp3"
        type="audio/mp3"
      />
      Not supported
    </audio>
  </q-footer>
</template>
