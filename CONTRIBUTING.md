# Contributing

Thanks for considering a contribution to **flutter-ios-launch-icons**.

## Ways to contribute

- **Bug reports** — if the skill produced an incorrect storyboard, a failed build, or wrong icon appearances, please open an issue with:
  - Flutter version (`flutter --version`)
  - Xcode version
  - The relevant section of `LaunchScreen.storyboard` or `Contents.json`
  - A screenshot/screen recording of the problem if possible
- **Feature requests** — e.g. Android adaptive icon parity, more icon appearance presets, additional brand token flags.
- **Pull requests** — fixes to `SKILL.md`, the reference docs, or the generation scripts.
- **Real-world reports** — if you used this on a shipping app, a before/after screenshot is genuinely useful for the README/docs.

## Project layout

```
skills/flutter-ios-launch-icons/
├── SKILL.md            # the agent-facing playbook — keep this concise (<500 lines)
├── references/         # longer-form docs the agent reads on demand
└── scripts/            # standalone Python/Pillow generators
```

## Guidelines for editing `SKILL.md`

- Keep it **actionable** — numbered steps, explicit file paths, copy-pasteable commands.
- Push long reference material (full XML templates, Contents.json shapes) into `references/` and link to it — don't inline it.
- Call out failure modes explicitly (what *looks* like it should work but doesn't) — that's the highest-value content in this skill.
- Avoid inventing new commands/flags without updating both scripts and docs together.

## Guidelines for the scripts

- Pure Python 3 + Pillow, no extra dependencies.
- Keep CLI flags backward compatible; add new ones with sane defaults.
- Scripts should be runnable **standalone**, without an agent, for anyone who just wants the images.

## Testing your changes

1. Run both scripts against a sample 1024×1024 icon and a logo PNG to confirm they still produce valid output.
2. If you change the storyboard template in `references/launch-storyboard.md`, validate it compiles:
   ```bash
   xcrun actool --compile /tmp/out --platform iphonesimulator path/to/Assets.xcassets
   ```
3. Where possible, verify on a real `flutter build ios --simulator --debug` + `xcrun simctl install` round trip before opening a PR.

## Code of conduct

Be respectful, assume good intent, and keep discussion focused on the technical problem. No harassment, no spam.
