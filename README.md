# tickjoin.com

Statisk webbplats för Tickjoin, publicerad med GitHub Pages på tickjoin.com.

- `index.html` (engelska) och `sv/index.html` (svenska) – startsidan. **Redigera inte direkt**: de byggs
  från `src/template.html` och texterna i `src/<språk>.json` med `python3 src/build.py`.
  - Nytt språk: kopiera `src/en.json` till `src/<språk>.json`, översätt, lägg skärmbilder i
    `assets/screens/<språk>/` och bygg. Utan egna skärmbilder används de engelska.
  - En svensk webbläsare skickas till `/sv/` vid första besöket; ett val i språkväljaren sparas.
  - Skärmbilderna (590 px bred WebP) tas med `MarketingScreenshotsUITests` i Tickjoin-repot.
    Alarmet är taget på en telefon, med mötestiteln utbytt.
- `privacy/` – integritet. `it/` – information för IT (appregistrering, godkännande, Intune).
- `.well-known/microsoft-identity-association.json` – verifierar tickjoin.com som publisher domain för Tickjoins Entra-app.
- `.nojekyll` – krävs för att Pages ska publicera mappen `.well-known`.
- `CNAME` – egen domän.
