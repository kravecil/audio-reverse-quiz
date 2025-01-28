<script setup>
import { useCoreStore } from "../stores/core";
import { playAudio, pauseAudio, stopAudio } from "../stores/player";
import { ref } from "vue";
import { player } from "../stores/player";

const ICON_PLAY = "play_arrow";
const ICON_PAUSE = "pause";

const core = useCoreStore();

const onPlay = () => {
  if ([player.state] == "stopped") {
    playAudio();
    playIcon.value = ICON_PAUSE;
  } else {
    pauseAudio();
    playIcon.value = ICON_PLAY;
  }
};
const onStop = () => {
  stopAudio();
  playIcon.value = ICON_PLAY;
};

const playIcon = ref(ICON_PLAY);
</script>

<template>
  <q-footer class="bg-grey-9 q-pa-sm" v-if="core.currentTrack !== undefined">
    <q-toolbar
      >1{{ core.playerState }}2
      <q-item>
        <q-item-section class="text-white">
          <q-item-label class="text-grey-5">
            {{ core.currentTrack.desc }}</q-item-label
          >
          <q-item-label class="text-h6 text-weight-bold">{{
            core.currentTrack.title
          }}</q-item-label>
        </q-item-section>
      </q-item>

      <q-space />

      <q-btn :icon="playIcon" rounded dense flat @click="onPlay" />
      <q-btn icon="stop" rounded dense flat @click="onStop" />
    </q-toolbar>
  </q-footer>
</template>
