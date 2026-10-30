#!/usr/bin/env bash
# Bilderna till avsnittet om plattformar på startsidan: Mac och Android per språk.
#
#     src/platform-shots.sh ~/Development/Mötesappen
#
# Källorna ligger i Tickjoin-repot:
#   Mac:     fastlane/screenshots-mac/<App Store-språk>/Mac-01-next.png (2880×1800)
#   Android: android/fastlane/metadata/android/<Play-språk>/images/phoneScreenshots/01-next.png (1080×1920)
# Resultatet hamnar i assets/screens/<språk>/mac.webp och android.webp. iPhone-kortet använder next.webp.
# Kräver ImageMagick (magick) och cwebp.
set -euo pipefail

repo="${1:?Ange sökvägen till Tickjoin-repot}"
site="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# Webbplatsens språk, App Store-språk (Mac), Google Play-språk (Android).
langs=(
  "sv sv sv-SE"
  "en en-US en-US"
  "da da da-DK"
  "de de-DE de-DE"
  "es es-ES es-ES"
  "fi fi fi-FI"
  "fr fr-FR fr-FR"
  "it it it-IT"
  "ja ja ja-JP"
  "ko ko ko-KR"
  "nb no no-NO"
  "nl nl-NL nl-NL"
  "pl pl pl-PL"
  "pt-BR pt-BR pt-BR"
  "zh-Hant zh-Hant zh-TW"
)

for row in "${langs[@]}"; do
  read -r lang mac play <<< "$row"
  out="$site/assets/screens/$lang"
  mkdir -p "$out"

  # Menyradsfönstret ligger uppe till höger (ungefär x 2160–2840, y 60–1065 på alla språk).
  # Beskärningen tar med lite menyrad och skrivbordets gradient runt fönstret så att det ser ut som en Mac.
  src="$repo/fastlane/screenshots-mac/$mac/Mac-01-next.png"
  if [[ -f "$src" ]]; then
    magick "$src" -crop 840x1140+2040+0 +repage -resize 590x "$tmp/mac.png"
    cwebp -quiet -q 82 "$tmp/mac.png" -o "$out/mac.webp"
  else
    echo "saknas: $src (visas på engelska)" >&2
  fi

  src="$repo/android/fastlane/metadata/android/$play/images/phoneScreenshots/01-next.png"
  if [[ -f "$src" ]]; then
    magick "$src" -resize 590x "$tmp/android.png"
    cwebp -quiet -q 82 "$tmp/android.png" -o "$out/android.webp"
  else
    echo "saknas: $src (visas på engelska)" >&2
  fi
done

ls -l "$site"/assets/screens/*/{mac,android}.webp
