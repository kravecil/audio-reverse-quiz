import axios from "axios";
import { defineStore } from "pinia";
import { Loading, Notify } from "quasar";
import { ref } from "vue";

import { player } from "./player";

const BASE_URL = import.meta.env.VITE_BASE_URL;

const api = axios.create({ baseURL: BASE_URL });

export const useCoreStore = defineStore("core", () => {
  const tracks = ref();
  const currentTrack = ref();

  const searchString = ref("");

  const fetchTracks = async () => {
    if (!searchString.value.length) return;

    Loading.show({ message: "Идёт поиск..." });
    try {
      const response = await api.get("/api/get-tracks", {
        params: { q: searchString.value },
      });
      tracks.value = response.data;
    } catch (error) {
      Notify.create({ message: "Ошибка при загрузке списка треков" });
      console.error(error);
    } finally {
      Loading.hide();
    }
  };

  const setCurrentTrack = async (info) => {
    Loading.show({ message: "Загружаем трек..." });
    currentTrack.value = info;
    try {
      currentTrack.value.duration = (
        await player.loadUrl(`${BASE_URL}/api/get-track?url=${info.filepath}`)
      ).buffer.duration;
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
    setCurrentTrack,
  };
});
