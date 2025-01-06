<script setup>
import { useCoreStore } from "../stores/core";
import { ref } from "vue";
import { player } from "../stores/player";

const ICON_PLAY = "play_arrow";
const ICON_PAUSE = "pause";

const core = useCoreStore();

const playedTime = ref(0);

player.onStateChanged(() => {
  if (player.getState() == "started") playIcon.value = ICON_PAUSE;
  else playIcon.value = ICON_PLAY;

  console.log("State changed: ", player.getState())
});

const onPlay = () => {
  console.log("onPlay", player.getState());
  if (player.getState() == "stopped") {
    player.playAudio();
  } else {
    player.pauseAudio();
  }
};
const onStop = () => {
  console.log("onStop", player.getState());
  player.stopAudio();
};

const playIcon = ref(ICON_PLAY);
</script>

<template>
  <q-footer class="bg-grey-9 q-pa-sm" v-if="core.currentTrack !== undefined">
    <q-toolbar
      >1{{ core.currentTrack.duration }}2
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

      <q-slider v-model="playedTime" :min="0" :max="10" />

      <q-btn :icon="playIcon" rounded dense flat @click="onPlay" />
      <q-btn icon="stop" rounded dense flat @click="onStop" />
    </q-toolbar>
  </q-footer>
</template>
