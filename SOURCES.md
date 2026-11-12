# Sources and verification

The README shows the latest game version covered by this repository. Each JSON record has a `verified_against` value for the game data used to check that mapping. A newer game release does not invalidate older mappings.

| Verification | Meaning |
| --- | --- |
| `confirmed` | An in-game name and identifier were joined through source tables. |
| `tentative` | The match is based on visual evidence. The two Rover portraits are examples. |
| `placeholder` | The source has no usable name. The registry keeps the ID, stores a null name, and displays “Name unavailable”. |

These labels describe mapping evidence. Release status is independent and has not been audited. Exported assets can appear in game files before their public release.

## Data

- **Characters** joins the [Convene texture table](https://github.com/Arikatsu/WutheringWaves_Data/blob/a96f6c6e87717d528a340de37374d9fc5a5ba563/BinData/gacha/gachatextureinfo.json) to the [3.8 English character index](https://static.nanoka.cc/ww/3.8/character.json) by role ID. The [role table](https://github.com/Arikatsu/WutheringWaves_Data/blob/a96f6c6e87717d528a340de37374d9fc5a5ba563/BinData/role/roleinfo.json) provides export context.
- **Monsters** uses the [3.8 English monster index](https://static.nanoka.cc/ww/3.8/monster.json) and [monster configuration](https://github.com/Arikatsu/WutheringWaves_Data/blob/a96f6c6e87717d528a340de37374d9fc5a5ba563/BinData/monster_Info/monsterinfo.json). JSON retains one record per monster ID. The Markdown groups matching names and portraits, with each ID listed in full. Distinct names keep separate rows even when they share an image.
- **Weapons** joins the [3.8 English weapon index](https://static.nanoka.cc/ww/3.8/weapon.json) to the [weapon configuration](https://github.com/Arikatsu/WutheringWaves_Data/blob/a96f6c6e87717d528a340de37374d9fc5a5ba563/BinData/weapon/weaponconf.json) by item ID. Item IDs, model IDs, and icon names refer to different fields.
- Thumbnails come from local FModel exports. The wordmark is from [SteamGridDB](https://www.steamgriddb.com/game/5448373/logos). Game artwork and data belong to their respective rights holders. Earlier ID lists are credited to [Yuhki](https://github.com/yuhkix/wuwa-ids).

## Updating the tables

Edit the JSON files under `data/`, then run `python generate_tables.py` with Python 3.10 or later. Use `python generate_tables.py --check` to check the generated pages before committing. Keep identifier strings and export codenames exactly as recorded. Use `null` for a missing value. If a mapping is uncertain, keep the evidence visible and label it `tentative`.

The published Markdown pages retain their existing editorial text. The generator is available for a future table refresh. Its exact-output check expects generated pages, so it can report differences against the hand-edited public pages.
