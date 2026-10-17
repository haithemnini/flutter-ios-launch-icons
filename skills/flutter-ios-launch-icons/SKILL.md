---
name: flutter-ios-launch-icons
description: >-
  Implements Flutter iOS native LaunchScreen with immediate light/dark logos and
  iOS 18+ home-screen AppIcon appearances (Default, Dark, Tinted, Clear). Use when
  the user asks for iOS launch logo, splash storyboard, cold-start white screen,
  dark mode app icon, tinted/clear icons, or appearance-aware branding on iOS.
license: MIT
compatibility: Flutter iOS projects; Xcode actool; Python 3 + Pillow for asset generation
metadata:
  author: kounoz
  version: "1.0.0"
---

# Flutter iOS Launch Screen & App Icons

Battle-tested pattern for Flutter apps: native launch logo on the **first frame**, plus home-screen icons that follow iOS Customize → Default / Dark / Clear / Tinted.

## When to use

- Cold start shows a blank white/ivory screen before Flutter loads
- Need light + dark launch logos that follow **system** appearance (not in-app ThemeCubit)
- Need App Icon Dark / Tinted / Clear variants on iOS 18+

## When not to use

- Android splash / Flutter in-app SplashScreen only
- Changing in-app theme toggle (HydratedBloc) — that does not drive LaunchScreen or SpringBoard icons

## Critical rules (do not skip)

1. **Launch logos must be loose PNGs in the app bundle**, not Asset Catalog imagesets. SplashBoard often fails `UIImage imageNamed` from Assets.car on the first snapshot → blank canvas for 2–3s.
2. **Do not put BrandLogo in Assets.xcassets** if the same basename exists as a loose file — the catalog wins and loading fails.
3. **Background colors on LaunchScreen must be explicit sRGB** in the storyboard. Named colors (e.g. `LaunchBackground`) often fail to switch on the launch snapshot.
4. **Trait variation key** is `userInterfaceStyle=dark` (not `interfaceStyle`, not `luminosity=dark`).
5. **Never verify launch by copying a standalone `ibtool` storyboardc** into an already-built `.app` — that yields a black flash. Always `flutter build ios --simulator` (or device) then uninstall + reinstall.
6. **Do not run `flutter_launcher_icons` after adding Dark/Tinted** — it overwrites `Contents.json` and drops appearances.
7. Home icon follows **iPhone appearance / Customize**, not the Flutter theme. Clear is **derived from Tinted**; there is no separate Clear slot.

## Workflow checklist

```
Progress:
- [ ] 1. Generate light + night launch PNGs (@1x/@2x/@3x)
- [ ] 2. Copy into ios/Runner/ and add to Copy Bundle Resources (pbxproj)
- [ ] 3. Remove any BrandLogo*.imageset from Assets.xcassets
- [ ] 4. Update LaunchScreen.storyboard (loose image names + explicit colors)
- [ ] 5. Optional: LaunchBackground.colorset for Main.storyboard / SceneDelegate handoff only
- [ ] 6. Generate AppIcon dark + tinted 1024 (and home sizes if keeping legacy entries)
- [ ] 7. Update AppIcon.appiconset/Contents.json with luminosity dark + tinted
- [ ] 8. flutter build ios --simulator --debug
- [ ] 9. simctl uninstall + install; verify launch <0.5s and icon appearances in Assets.car
```

## Step 1 — Generate launch logos

Use [scripts/generate_launch_logos.py](scripts/generate_launch_logos.py).

Inputs:

- Source logo with dark studio background (typical `assets/logo/logo.png`)
- Light: knockout black → two-tone brand colors preserved
- Dark: same alpha mask, solid gold `#E0B45D` (or project primary)
- Sizes: 400×363 @1x, 800×727 @2x, 1200×1090 @3x (adjust aspect to your logo)

Knockout formula (match Flutter `SplashLogo` if present):

```text
alpha_out = min(255, 4 * (R + G + B), source_alpha)
```

Output files into `ios/Runner/`:

- `BrandLogo.png`, `BrandLogo@2x.png`, `BrandLogo@3x.png`
- `BrandLogoNight.png`, `BrandLogoNight@2x.png`, `BrandLogoNight@3x.png`

## Step 2 — Bundle resources

In `ios/Runner.xcodeproj/project.pbxproj`:

- Add `PBXFileReference` + `PBXBuildFile` for all six PNGs
- List them in the Runner group and in **Copy Bundle Resources**
- `lastKnownFileType = image.png`; quote `@2x` / `@3x` paths

Delete `ios/Runner/Assets.xcassets/BrandLogo.imageset` and `BrandLogoNight.imageset` if they exist.

After build, confirm:

```bash
# BrandLogo must NOT be in Assets.car; PNGs must exist in Runner.app
find build/ios/iphonesimulator/Runner.app -name 'BrandLogo*.png'
xcrun assetutil --info build/ios/iphonesimulator/Runner.app/Assets.car | grep -i BrandLogo || true
```

## Step 3 — LaunchScreen.storyboard

Use modern IB format (`toolsVersion` ≥ 21701, `useTraitCollections`, capability “documents saved in the Xcode 8 format”).

Pattern (full template: [references/launch-storyboard.md](references/launch-storyboard.md)):

- `UIImageView` `contentMode="scaleAspectFit"`, image `BrandLogo`
- Variation: `key="userInterfaceStyle=dark" image="BrandLogoNight"`
- Width ≈ `0.28`–`0.40` of superview (start ~0.32); height = width × logo aspect
- Center X/Y constraints
- Light background explicit sRGB (e.g. ivory `#FFFCF7`)
- Dark background variation explicit sRGB (e.g. `#17120E`)
- `<resources>` must declare both image names with intrinsic sizes

Info.plist: `UILaunchStoryboardName` = `LaunchScreen`.

## Step 4 — Flutter handoff (optional but recommended)

Prevent white flash when Flutter takes over:

- `LaunchBackground.colorset` with light + dark luminosity (OK for **non-launch** UI)
- Main.storyboard VC background → named `LaunchBackground`
- SceneDelegate / custom `FlutterViewController`: set `view.backgroundColor` and `window.backgroundColor` from `UIColor(named: "LaunchBackground")` in `viewDidLoad` / `viewDidLayoutSubviews`

## Step 5 — App Icon appearances (iOS 18+)

Generate with [scripts/generate_app_icon_variants.py](scripts/generate_app_icon_variants.py) from the 1024 marketing icon (cream background + logo).

| Appearance | Artwork |
|------------|---------|
| Default (Any) | Existing light icon |
| Dark | Gold logo on dark plate (`#17120E`) or transparent bg per Apple HIG |
| Tinted | Grayscale: white/gray logo on black (system applies tint) |
| Clear | Auto-derived from Tinted — **no Contents.json entry** |

Update `AppIcon.appiconset/Contents.json` — see [references/appicon-contents.md](references/appicon-contents.md).

Prefer Single Size universal 1024 entries with:

```json
"appearances": [{ "appearance": "luminosity", "value": "dark" }]
"appearances": [{ "appearance": "luminosity", "value": "tinted" }]
```

Keep legacy per-size iPhone entries if the project still uses them; add dark/tinted for 60pt @2x/@3x + marketing 1024 at minimum.

Validate:

```bash
xcrun actool ios/Runner/Assets.xcassets --compile /tmp/icons \
  --platform iphonesimulator --minimum-deployment-target 15.0 \
  --app-icon AppIcon --output-partial-info-plist /tmp/icon-partial.plist
xcrun assetutil --info /tmp/icons/Assets.car | grep -E 'UIAppearanceDark|ISAppearanceTintable'
```

Built app should list `AppIcon` with `UIAppearanceDark` and `ISAppearanceTintable`.

## Step 6 — Verify on simulator

```bash
flutter build ios --simulator --debug
xcrun simctl uninstall booted <bundle.id>
xcrun simctl install booted build/ios/iphonesimulator/Runner.app
# Launch: expect logo by ~0.4–0.5s (not multi-second blank)
# Icon: Customize → Dark / Tinted; may need delete+reinstall for SpringBoard cache
```

`simctl` needs full permissions in sandboxed agent environments.

Do **not** `rm -rf` SplashBoard caches; uninstall + reinstall clears launch snapshots.

## Brand defaults (override per project)

| Token | Default |
|-------|---------|
| Light launch bg | `#FFFCF7` |
| Dark launch bg | `#17120E` |
| Dark logo gold | `#E0B45D` |
| Launch logo width | 32% of screen |
| Dark icon plate | `#17120E` |

Ask the user for brand hex values when the project differs.

## Additional resources

- Storyboard XML template: [references/launch-storyboard.md](references/launch-storyboard.md)
- AppIcon Contents.json shapes: [references/appicon-contents.md](references/appicon-contents.md)
- Launch logo script: [scripts/generate_launch_logos.py](scripts/generate_launch_logos.py)
- Icon variant script: [scripts/generate_app_icon_variants.py](scripts/generate_app_icon_variants.py)
