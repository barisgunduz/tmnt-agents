// The five characters of the mod, in picker order.
export const ORDER = ["leonardo", "raphael", "donatello", "michelangelo", "splinter"];
export const COUNT = ORDER.length;

export const NAMES = {
  leonardo: "Leonardo",
  raphael: "Raphael",
  donatello: "Donatello",
  michelangelo: "Michelangelo",
  splinter: "Splinter",
};

export const isValid = (id) => typeof id === "string" && ORDER.includes(id);
export const nameOf = (id) => NAMES[id] ?? "Turtle";
