# tickjoin.com

Statisk webbplats för Tickjoin, publicerad med GitHub Pages på tickjoin.com.

- `index.html` (engelska) och `<språk>/index.html` för de övriga 14 språken – startsidan. **Redigera inte direkt**: de byggs
  från `src/template.html` och texterna i `src/<språk>.json` med `python3 src/build.py`.
  - Nytt språk: kopiera `src/en.json` till `src/<språk>.json`, översätt, lägg skärmbilder i
    `assets/screens/<språk>/` och bygg. En skärmbild som saknas på språket visas på engelska.
  - Italienska ligger på `/it-it/` eftersom `/it/` är IT-sidan.
  - Vid första besöket i roten skickas webbläsaren till sitt språk om det finns; ett val i språkväljaren sparas.
  - Texterna är maskinöversatta med samma ordlista som appen (`docs/lokalisering.md` i Tickjoin-repot).
  - Skärmbilderna (590 px bred WebP) tas med `MarketingScreenshotsUITests` i Tickjoin-repot
    (`TEST_RUNNER_SCREENSHOT_LANG=de,fr,…`).
    Alarmet är taget på en telefon, med mötestiteln utbytt.
  - Avsnittet om plattformar (iPhone, Mac, Android) visar `next.webp` i telefonram, `mac.webp` i skärmram och
    `android.webp` i Android-ram. Mac- och Android-bilderna görs från butiksbilderna i Tickjoin-repot med
    `src/platform-shots.sh <sökväg till Tickjoin-repot>`: Mac från `fastlane/screenshots-mac/<språk>/Mac-01-next.png`
    (menyradsfönstret beskärs ut med lite skrivbord runt), Android från
    `android/fastlane/metadata/android/<språk>/images/phoneScreenshots/01-next.png`. Båda blir 590 px breda.
    Skriptet har tabellen över webbplatsens språk och butikernas språkkoder. Ändras bildernas mått: uppdatera
    `PLATFORM_SHOTS` i `src/build.py`.
- `privacy/` – integritet. `it/` – information för IT (appregistrering, godkännande, Intune).
  `support/` – kontakt, krav per plattform och vanliga frågor. Alla tre är handskrivna, svenska först och engelska
  under `#english`, och länkas från sidfoten på startsidan.
- `.well-known/microsoft-identity-association.json` – verifierar tickjoin.com som publisher domain för Tickjoins Entra-app.
- `.nojekyll` – krävs för att Pages ska publicera mappen `.well-known`.
- `CNAME` – egen domän.
- `review/device-name/` – skärmbilder (påhittad demodata) till Apples ansökan om enhetens namn (`user-assigned-device-name`), för att tysta andra enheter (Tickjoin #207). Länkas inte från sidan.
