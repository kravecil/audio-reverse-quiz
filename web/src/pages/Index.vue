<script setup>
import SearchForm from "/src/components/SearchForm.vue";
</script>

<template>
  <q-page padding>
    <div class="container">
      <SearchForm />
    </div>
  </q-page>
</template>

<style lang="sass">
.container
  min-width: 800px
  width: 100%
</style>
