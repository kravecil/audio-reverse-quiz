import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import { Loading } from "quasar";

const BASE_URL = import.meta.env.VITE_BASE_URL;

export const useCoreStore = defineStore("core", () => {
  const tracks = ref([]);

  const searchString = ref("");

  const fetchTracks = async () => {
    Loading.show({ message: "Идёт поиск..." });
    try {
      const response = await axios.get(`${BASE_URL}/api/get-tracks`, {
        params: { q: searchString.value },
      });
      tracks.value = response.data;
      console.log(tracks.value);
    } catch (error) {
      console.error(error);
    } finally {
      Loading.hide();
    }
  };

  return {
    tracks,
    searchString,
    fetchTracks,
  };
});
