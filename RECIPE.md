# Recipe

How to put the strip into a Herdr layout.

## Layout block

Add one block at the bottom of the main column of your layout (the one that
holds the tab content), above the status bar if you have one:

```json
{
  "type": "block",
  "content": { "mod": "tmnt-agents" },
  "size": { "px": 112 }
}
```

`mod.json` asks for `{ "place": "bottom", "size": 112 }`. In a layout whose
root is a row, Herdr docks the mod as a right-hand column instead, so move the
block into the column by hand.

## Scale

Set `content.props.scale` to a positive number. `1` is the default, `0.5` is
half size, `2` is double. Give the block more height when you enlarge the
characters so their heads fit:

```json
{
  "type": "block",
  "content": { "mod": "tmnt-agents", "props": { "scale": 1.5 } },
  "size": { "px": 160 }
}
```

Shadows and the loading pizza scale with the sprites. Name tags and picker
icons keep their size.

## Key

Merge [keys.json](keys.json) into `~/.config/herdr-app/keys.json`.
`alt-shift-t` opens the picker for the focused agent, or for the first one if
none is focused.

## Turning it off

Delete the block from your layout and the `tmnt-agents.pick` line from
`keys.json`. Nothing else depends on the mod.
