<script setup>
import { useCoreStore } from "../stores/core";
import TrackItem from "../components/TrackItem.vue";

const core = useCoreStore();
</script>

<template>
  <q-page class="row justify-center">
    <div class="container column q-gutter-sm">
      <div
        v-if="core.tracks !== undefined && core.tracks.length === 0"
        class="text-grey-4"
      >
        Композиции не найдены!
      </div>
      <TrackItem v-for="(info, index) in core.tracks" :key="index" :info="info" />
    </div>
  </q-page>
</template>

<style lang="sass">
.container
  max-width: 400px
  width: 100%
  padding: 1em
</style>
