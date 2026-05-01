# D&D Encounter Builder (Python + FastAPI)

Tento projekt je backend pro správu D&D encounterů. Umožňuje uživatelům se registrovat, přihlásit a vytvářet si vlastní sady monster, předmětů a kouzel vytažených z D&D 5e API.

## Funkce
- **Registrace a Login**: Zabezpečeno pomocí JWT tokenů a hashování hesel (bcrypt).
- **SQLite Databáze**: Ukládá uživatele a jejich vytvořené encountery.
- **D&D 5e API**: Dynamické načítání seznamu monster a detailů.
- **CRUD**: Vytváření a prohlížení vlastních encounterů.

## Jak spustit
1. Nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```
2. Vytvořte `.env` soubor (podle `.env.template`):
   ```bash
   cp .env.template .env
   ```
3. Spusťte server:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Otevřete prohlížeč na:
   - [http://localhost:8000](http://localhost:8000) - API root
   - [http://localhost:8000/docs](http://localhost:8000/docs) - **Swagger UI (interaktivní dokumentace)**

## Struktura projektu
- `app/main.py`: Entry point a definice rout.
- `app/models.py`: Databázové entity (User, Encounter).
- `app/auth.py`: Autentizace a bezpečnost.
- `app/api_client.py`: Komunikace s externím D&D API.
- `app/database.py`: Připojení k SQLite.
