<script setup>
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";
import IndexPage from "/src/pages/Index.vue";
</script>

<template>
  <q-layout view="hHh Lpr fFf" class="bg-grey-10">
    <Header />
    <Footer />
    <q-page-container>
      <IndexPage />
    </q-page-container>
  </q-layout>
</template>
