# Br. Söderbergs Bygg AB

Webbplatsen byggs med Jekyll och publiceras på GitHub Pages av arbetsflödet `.github/workflows/pages.yml` vid varje push till `main`.

## Lägga upp nya referensbilder

1. Öppna mappen för kategorin på GitHub, till exempel `references/kok/`.
2. Välj **Add file → Upload files**, dra in bilderna och tryck på **Commit changes**.
3. Efter någon minut syns bilderna i galleriet.

Bilderna visas i filnamnsordning (`2.jpg` före `10.jpg`). JPG, PNG, WebP och GIF fungerar. Stora bilder får automatiskt en miniatyr i galleriet, och originalet öppnas när man klickar.

## Lägga till en ny kategori

1. Skapa mappen `references/<kategori>/` med en `index.html` som bara innehåller titeln:

   ```
   ---
   title: Golv
   ---
   ```

2. Lägg till kategorin i `_data/references.yml` med en omslagsbild. Då kommer den med på startsidan och i "Fler referenser".

## Bygget

- `scripts/build_gallery.py` körs först. Det skapar miniatyrer i `references/<kategori>/thumbs/` för bilder som är större än 960 px eller 300 kB, vänder bilder enligt kamerans orientering och skriver bildlistan till `_data/gallery.json`. Miniatyrerna och bildlistan committas inte.
- Jekyll bygger sedan sidorna. `_layouts/default.html` innehåller `<head>`, `_includes/header.html` och `_includes/footer.html`. `_layouts/reference.html` bygger referenssidornas galleri.
- I GitHub under **Settings → Pages** ska **Source** vara **GitHub Actions**.

Förhandsgranska lokalt (kräver Python med Pillow och Jekyll 3.10):

```
python3 scripts/build_gallery.py
jekyll serve
```

## Struktur

- `index.html`, `about/`, `contact/`: startsida, Om oss och Kontakt
- `references/<kategori>/`: referenssidor, gemensam stil i `references/style.css`
- `_data/navigation.yml`: huvudmenyn
- `_data/references.yml`: kategorierna och deras omslagsbilder
- `media/`: logotyp, slogan, ikoner, faviconer och bilder

## Stilmallar

- `base.css` laddas av alla webbläsare och innehåller bara CSS 2.1 (inga variabler, ingen flexbox), så att sidorna går att läsa även i mycket gamla webbläsare.
- `style.css` laddas med `media="only screen"`, som gamla webbläsare ignorerar, och lägger den moderna layouten ovanpå. En selektor i `style.css` måste vara minst lika specifik som motsvarande selektor i `base.css`, annars vinner `base.css`.
- Färger, hörnrundning och skugga styrs av variablerna i `:root` i `style.css`. `base.css` har samma färger hårdkodade och måste uppdateras separat. Sloganen `media/slogan-accent.svg` har också färgen inbakad.
- Alla mått utgår från `font-size` på `:root`.

## Kvarstående uppgifter

- Byt platshållaren `mail@mail.mail` i `_includes/header.html` och på startsidan och kontaktsidan.
