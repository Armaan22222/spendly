# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run the application: `python app.py` (runs on port 5001)
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `pytest`

## Architecture
- **Framework**: Flask web application.
- **Routing**: Defined in `app.py`.
- **Database**: Intended to be managed in `database/db.py` using SQLite.
- **Frontend**: 
  - HTML templates located in `templates/`.
  - Static assets (CSS, JS) located in `static/`.
- **Structure**:
  - `app.py`: Main entry point and route definitions.
  - `database/`: Database connection and initialization logic.
  - `static/`: Frontend assets.
  - `templates/`: Jinja2 HTML templates.
