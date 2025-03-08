import { Player, getTransport } from "tone";
import { ref } from "vue";

const usePlayer = () => {
  const tonePlayer = new Player().toDestination();
  tonePlayer.sync().start(0);
  tonePlayer.reverse = true;

  const transport = getTransport();

  const title = ref("");
  const desc = ref("");

  async function loadUrl(url) {
    console.log("Loading URL...");
    return await tonePlayer.load(url);
  }

  const playAudio = () => {
    console.log("Starting player...");
    transport.start();
  };

  const pauseAudio = () => {
    console.log("Player pausing...");
    transport.pause();
  };

  const stopAudio = () => {
    console.log("Player stopping...");
    transport.stop();
  };

  const onStateChanged = (callback) =>
    transport.on("statechange", callback);

  const getState = () => transport.state;

  return {
    loadUrl,
    playAudio,
    pauseAudio,
    stopAudio,
    onStateChanged,
    getState,
  };
};

export const player = usePlayer();
