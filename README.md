# Create: New Age Tags Fix

A small fix for [Create: New Age](https://modrinth.com/mod/create-new-age) **1.2.0** (NeoForge, Minecraft 1.21.1).

**The problem:** New Age doesn't add any of the common `c:` tags that other mods use to recognise ores and materials.
So thorium ore isn't an ore as far as other mods can tell: vein miners skip it, ore-processing and drill mods ignore
it, and recipe viewers don't list it under ores. The same goes for New Age's overcharged ingots, diamond, sheets and
wires. This is New Age issue [#13](https://gitlab.com/antarcticgardens/create-new-age/-/work_items/13), open since 2023.

**The fix:** it adds those tags. It adds nothing else and changes nothing else: no recipes, drops or worldgen.

## What it tags

| New Age item | Tags added |
|---|---|
| Thorium Ore (block and item) | `c:ores`, `c:ores/thorium`, `c:ores_in_ground/stone`, `c:ore_rates/singular` |
| Thorium | `c:raw_materials`, `c:raw_materials/thorium` |
| Overcharged Iron | `c:ingots`, `c:ingots/overcharged_iron` |
| Overcharged Gold | `c:ingots`, `c:ingots/overcharged_gold` |
| Overcharged Diamond | `c:gems`, `c:gems/overcharged_diamond` |
| Overcharged Iron Sheet | `c:plates`, `c:plates/overcharged_iron` |
| Overcharged Golden Sheet | `c:plates`, `c:plates/overcharged_gold` |
| Copper Wire | `c:wires`, `c:wires/copper` |
| Overcharged Iron / Golden / Diamond Wire | `c:wires`, `c:wires/overcharged_iron` / `overcharged_gold` / `overcharged_diamond` |

Every entry is optional, so if New Age isn't installed the tags just stay empty and nothing breaks.

**Left out on purpose:**
- **Radioactive Thorium:** no common tag fits it (it isn't an ingot, gem or dust).
- **The wire blocks:** they hold 4 wires, not 9, so they aren't storage blocks in the usual sense.
- **Reactor Glass:** tagging it as glass would let recipes that take any glass use it up.

## What changes in game

- Thorium ore works with anything that looks for ores: vein miners (like VeinMiner), ore drills (like the one in
  Create: Dreams & Desires), ore tags in recipe viewers (EMI, JEI), and so on.
- New Age's copper wire counts as copper wire in other mods' recipes that ask for `c:wires/copper` (for example Create
  Crafts & Additions, Create: Pantographs & Wires and Create: Power Grid). New Age's own recipes still want New Age's
  wire, because they name the item directly.

## Download

Get it from [Releases](https://github.com/Pelly-the-Crafter/create-new-age-tags-fix/releases). Pick whichever suits
you; you only need one:

| File | Where it goes | Applies to |
|---|---|---|
| `create-new-age-tags-fix-1.0.0.jar` | your `mods` folder (modpacks, servers) | every world |
| `create-new-age-tags-fix-1.0.0.zip` | a world's `datapacks` folder, or **Data Packs** when creating a world | that world |

It's data only, so it only matters on the server (or in singleplayer). Players joining a server don't need it.
A datapack added to an existing world needs `/reload` (and `/datapack enable "file/create-new-age-tags-fix-1.0.0.zip"`
if it doesn't switch on by itself), or a restart.

### Using VeinMiner?

VeinMiner reads its ore list once, when it loads, so it doesn't notice tags added while the game is running. If you
added the datapack with `/reload`, also run this (as an operator, or in singleplayer with cheats on):

```
/veinminer reload
```

After that, thorium ore vein-mines like any other ore. If you restart the server or the world instead, or use the jar,
you don't need to do this: VeinMiner picks the tags up when it starts.

## Tested with

| | Version |
|---|---|
| Minecraft | 1.21.1 |
| NeoForge | 21.1.251 |
| Create: New Age | 1.2.0+neoforge-mc1.21.1 |
| Create | 6.0.10 |

Tested on a dedicated server: without the fix, thorium ore and the items above have no `c:` tags at all. With the
datapack, every tag in the table is there (checked with `/neoforge tags`), the reload logs no errors from it, and after
`/veinminer reload` (VeinMiner 2.11.2) a whole thorium vein breaks at once. The jar was tested on its own too (datapack
removed, server restarted): it loads cleanly and gives the same tags.

## Good to know

- Once New Age adds these tags itself, you won't need this anymore. It doesn't touch anything else, so it's safe to remove.
- Not affiliated with Create: New Age. This contains none of its files, only tag lists.

## Reporting problems

I'm happy to look at problems raised in [Issues](https://github.com/Pelly-the-Crafter/create-new-age-tags-fix/issues)
until New Age adds these tags itself. Please give a proper bug report: your Minecraft, NeoForge, Create and New Age
versions, whether you used the jar or the datapack, what you did and what happened, and your `logs/latest.log`.
And please be considerate: I'm doing this in my free time.

## Building

`build.py` writes both files into `build/`. The datapack is the `datapack/` folder zipped. The jar is the same data
plus one empty class so NeoForge loads it as a mod, compiled with the Java 21 compiler and mod loader jar that
[Prism Launcher](https://prismlauncher.org/) already has.

```
python build.py
```

## License

MIT, see [LICENSE](LICENSE).
