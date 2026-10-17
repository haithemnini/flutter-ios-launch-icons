# AppIcon Contents.json appearances

## Recommended: Single Size + appearances

Replace or supplement legacy per-size entries. `actool` generates smaller sizes from 1024.

```json
{
  "images": [
    {
      "filename": "Icon-App-1024x1024@1x.png",
      "idiom": "universal",
      "platform": "ios",
      "size": "1024x1024"
    },
    {
      "appearances": [{ "appearance": "luminosity", "value": "dark" }],
      "filename": "Icon-App-1024x1024-dark.png",
      "idiom": "universal",
      "platform": "ios",
      "size": "1024x1024"
    },
    {
      "appearances": [{ "appearance": "luminosity", "value": "tinted" }],
      "filename": "Icon-App-1024x1024-tinted.png",
      "idiom": "universal",
      "platform": "ios",
      "size": "1024x1024"
    }
  ],
  "info": { "author": "xcode", "version": 1 }
}
```

## Hybrid: keep legacy sizes + add appearances

If the project still ships the old 20/29/40/60/ipad/marketing set, **append** (do not delete working light entries) at least:

```json
{
  "size": "60x60",
  "idiom": "iphone",
  "filename": "Icon-App-60x60@2x-dark.png",
  "scale": "2x",
  "appearances": [{ "appearance": "luminosity", "value": "dark" }]
}
```

Repeat for `@3x` dark, `@2x`/`@3x` tinted, and marketing `1024x1024` dark + tinted. Also add the three universal Single Size entries above so modern actool wires `UIAppearanceDark` / `ISAppearanceTintable`.

## Clear

No `clear` appearance value. iOS derives Clear (light/dark glass) from the **tinted** grayscale artwork.

## flutter_launcher_icons

Config often points at a single `image_path_ios`. Regenerating wipes Dark/Tinted. After enabling appearances, either:

- Stop using the generator for iOS, or
- Patch `Contents.json` after every regenerate

## Expected Assets.car markers

```text
AppIcon  Appearance=None
AppIcon  Appearance=UIAppearanceDark
AppIcon  Appearance=ISAppearanceTintable
```
