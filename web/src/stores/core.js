import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import { Loading } from "quasar";

const BASE_URL = import.meta.env.VITE_BASE_URL;
const REAL_BASE_URL = "https://s3.deliciouspeaches.com";

export const useCoreStore = defineStore("core", () => {
  const tracks = ref();
  const currentTrack = ref();

  const searchString = ref("");

  const fetchTracks = async () => {
    if (!searchString.value.length) return;

    Loading.show({ message: "Идёт поиск..." });
    try {
      const response = await axios.get(`${BASE_URL}/api/get-tracks`, {
        params: { q: searchString.value },
      });
      tracks.value = response.data;
    } catch (error) {
      console.error(error);
    } finally {
      Loading.hide();
    }
  };

  return {
    tracks,
    currentTrack,
    searchString,
    fetchTracks,
  };
});
