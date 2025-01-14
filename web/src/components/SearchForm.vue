<script setup>
import { useCoreStore } from "../stores/core";

const core = useCoreStore();
</script>

<template>
  <q-form @submit="core.fetchTracks()">
    <q-input label="Поиск" dark outlined v-model="core.searchString" />
  </q-form>
</template>
