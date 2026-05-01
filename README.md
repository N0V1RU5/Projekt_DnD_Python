# D&D API viewer

Tento projekt je backend pro spravu oblibenych dnd kouzel a priser. Umoznuje uzivatelum jednoduse vstupovat do aplikace, prochazet monstra a kouzla z dnd 5e api a ukladat si je do vlastniho profilu.

## Hlavni funkce
- **auto-registrace**: Staci zadat jmeno a jste uvnitr.
- **sqlite databaze**: Uklada uzivatele a jejich oblibene polozky.
- **dnd 5e api**: Taha aktualni data o monstrech a kouzlech.
- **oblibene**: Moznost pridavat a mazat oblibene polozky z vlastniho profilu.

## Instalace a spusteni

1. **Klonovani repozitare**:
   ```bash
   git clone "https://github.com/N0V1RU5/Projekt_DnD_Python"
   cd Projekt_DnD_Python
   ```

2. **Nainstalovani knihoven**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Spusteni serveru**:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Otevreni stranky**:
   Otevri [http://localhost:8000](http://localhost:8000) v prohlizeci.

## struktura kodu
- `app/main.py`: hlavni logika a routy aplikace.
- `app/models.py`: databazove tabulky (sqlalchemy).
- `app/api_client.py`: komunikace s dnd api.
- `app/database.py`: nastaveni pripojeni k sqlite.
- `app/templates/`: html sablony (jinja2 + pico.css).
