import axios from "axios";
import { defineStore } from "pinia";
import { Loading, Notify } from "quasar";
import { ref, useTemplateRef } from "vue";

const BASE_URL = import.meta.env.VITE_BASE_URL;

const api = axios.create({ baseURL: BASE_URL });

export const useCoreStore = defineStore("core", () => {
  const tracks = ref();
  const currentTrack = ref();

  const searchString = ref("");

  const audioPlayerRef = useTemplateRef(null);

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

  const fetchTrack = async (url) => {
    Loading.show({ message: "Загружаем трек..." });
    try {
      const response = await api.get("/api/get-track", { params: { url } });
      // console.log(response.data);
      return response.data;
    } catch (error) {
      Notify.create({ message: "Ошибка при загрузке трека" });
      console.error(error);
    } finally {
      Loading.hide();
    }
  };

  const setCurrentTrack = async (info) => {
    currentTrack.value = info;
    const storageFile = await fetchTrack(info.filepath);
    currentTrack.value.storageFile = `${BASE_URL}/storage/${storageFile}`;

    // audioPlayerRef.value.src = currentTrack.value.storageFile;
    // audioPlayerRef.value.playbackRate = -1
    const audio = new Audio(currentTrack.value.storageFile);
    // audio.playbackRate = -1;
    audio.play();
  };

  return {
    tracks,
    currentTrack,
    searchString,
    audioPlayerRef,
    fetchTracks,
    setCurrentTrack,
  };
});
