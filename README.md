# dnd notebook - simple encounter builder

tento projekt je backend pro spravu dnd oblibenych polozek. umoznuje uzivatelum jednoduse vstupovat do aplikace, prochazet monstra a kouzla z dnd 5e api a ukladat si je do vlastniho profilu.

## hlavni funkce
- **auto-registrace**: staci zadat jmeno a jste uvnitr.
- **sqlite databaze**: uklada uzivatele a jejich oblibene polozky.
- **dnd 5e api**: taha aktualni data o monstrech a kouzlech.
- **oblibene**: moznost pridavat a mazat polozky z vlastniho profilu.

## instalace a spusteni

1. **klonovani repozitare**:
   ```bash
   git clone <url-tveho-repozitare>
   cd Projekt_DnD_Python1
   ```

2. **nainstalovani knihoven**:
   ```bash
   pip install -r requirements.txt
   ```

3. **spusteni serveru**:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **pouzivani**:
   otevri [http://localhost:8000](http://localhost:8000) v prohlizeci.

## struktura kodu
- `app/main.py`: hlavni logika a routy aplikace.
- `app/models.py`: databazove tabulky (sqlalchemy).
- `app/api_client.py`: komunikace s dnd api.
- `app/database.py`: nastaveni pripojeni k sqlite.
- `app/templates/`: html sablony (jinja2 + pico.css).
