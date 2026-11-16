// Loads the sprite sets that ship inside the mod (made by tools/make_sprites.py).
// Nothing is downloaded and no external program is needed. Herdr resolves image paths
// against ~/.config/herdr-app, so the mod's own files are addressed from there.
import { appHome } from "herdr";
import * as fs from "fs/promises";

export const MOD_REL = "mods/tmnt-agents";

// Reads one character's meta.json: { walkR, walkL, idleR, idleL, sleep }, each
// { path, w, h, box }. Paths are rewritten so image() can use them directly.
export async function loadSprite(id) {
  const meta = JSON.parse(await fs.readFile(`${appHome()}/${MOD_REL}/sprites/${id}/meta.json`, "utf8"));
  for (const key of ["walkR", "walkL", "idleR", "idleL", "sleep"]) {
    if (!meta[key]) throw new Error(`missing ${key} for ${id}`);
    meta[key].path = `${MOD_REL}/${meta[key].path}`;
  }
  return meta;
}

export const iconPath = (id) => `${MOD_REL}/icons/${id}.png`;

export const PIZZA = `${MOD_REL}/pizza.png`; // the loading placeholder
