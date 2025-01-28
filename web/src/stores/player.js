import { Player, getTransport, start } from "tone";

const transport = getTransport();

export const player = new Player().toDestination();
player.sync().start(0);
player.reverse = true;
// player.restart();

export const loadUrl = async (url) => {
  console.log("Loading URL...");
  await player.load(url);
  console.log("URL loaded!");
};

export const playAudio = () => {
  console.log("Starting player...");
  // player.reverse = true;
  // player.autostart = true;
  // player.start();
  transport.start();
};

export const pauseAudio = () => {
  console.log("Player pausing...");
  // player.stop(player);
  transport.pause();
};

export const stopAudio = () => {
  console.log("Player stopping...");
  // player.stop(0);
  transport.stop();
};
