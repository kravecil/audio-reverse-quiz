<template>
  <q-input v-model="core.search" label="Поиск" color="white" label-color="white" />
</template>

<script setup>
import { useCoreStore } from 'src/stores/Core'

const core = useCoreStore()
</script>
