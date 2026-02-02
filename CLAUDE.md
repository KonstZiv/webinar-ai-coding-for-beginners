# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python project for a webinar about AI-assisted coding for beginners. Uses the `tic-tac-toe-3x3` library with `rich` for terminal UI.

## Commands

```bash
# Install dependencies
uv sync

# Run the game
uv run python -m my_tic_tac_toe

# Run tests
uv run pytest

# Run a single test file
uv run pytest tests/test_renderer.py

# Run a specific test class
uv run pytest tests/test_renderer.py::TestWinningCellsHighlight -v

# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Fix linting issues automatically
uv run ruff check . --fix
```

## Architecture

- `src/my_tic_tac_toe/` - Main application source code
  - `__init__.py` - Package exports (RichRenderer)
  - `__main__.py` - Entry point for running the game
  - `renderer.py` - RichRenderer class with ASCII art display
- `tests/` - Test files (pytest)
  - `test_renderer.py` - Tests for RichRenderer (43 tests)

## Tech Stack

- Python 3.14+
- `uv` - Dependency and virtual environment management
- `pytest` - Testing framework
- `ruff` - Linting and formatting
- `rich` - Terminal UI library
- `tic-tac-toe-3x3` - Game logic library
- `hatchling` - Build backend (editable install)

---

## Task 1: Rich Renderer — красиве відображення дошки

### Мета
Замінити базове текстове відображення гри на візуально привабливий інтерфейс з кольорами та рамками.

### Вимоги
- Клас `RichRenderer` наслідує `tic_tac_toe_3x3.game.renderers.Renderer`
- Кожна клітинка поля — матриця 17×7 символів (ширина × висота)
- Символи малюються блоками █:
  - X (червоний) — з перетином в центрі
  - O (синій) — симетричне коло
- Пуста клітинка — пробіли 17×7
- Сітка поля — подвійні лінії (╔ ╗ ╚ ╝ ╦ ╩ ╠ ╣ ╬ ═ ║)
- Зверху підписані колонки: A, B, C (центровані над клітинками)
- Зліва підписані ряди: 1, 2, 3 (центровані по висоті клітинки)
- Введення ходу — координати типу a1, b3, c2
- Під полем — статус гри: чий хід / переможець / нічия
- Кольори: X — red, O — blue, статус — yellow
- Виграшні клітинки підсвічуються (reverse style)

### Статус: ✅ ЗАВЕРШЕНО

### Критерії приймання
- [x] Файл `src/my_tic_tac_toe/renderer.py` створено
- [x] Клас `RichRenderer` коректно наслідує базовий `Renderer`
- [x] Гра запускається з новим рендерером без помилок
- [x] Візуально: кольори, рамки, статус відображаються коректно
- [x] Код проходить `ruff check`
- [x] Тести написані та проходять (43 тести)

### Реалізовані файли

#### `src/my_tic_tac_toe/renderer.py`
- `CELL_WIDTH = 17`, `CELL_HEIGHT = 7`
- `X_ART` — ASCII art для X (17×7)
- `O_ART` — ASCII art для O (17×7)
- `RichRenderer` клас:
  - `render(game_state)` — основний метод рендерингу
  - `_build_board(game_state)` — будує дошку як Rich Text
  - `_create_column_headers()` — заголовки A, B, C
  - `_build_row(row, cells, winning_cells)` — один рядок дошки
  - `_get_cell_line(cell, line_idx, is_winning)` — одна лінія клітинки
  - `_get_status_text(game_state)` — статус гри

#### `tests/test_renderer.py`
Тестові класи:
- `TestRichRendererInheritance` — перевірка наслідування
- `TestAsciiArtConstants` — розміри X_ART та O_ART
- `TestGetStatusText` — статуси гри
- `TestGetCellLine` — рендеринг клітинок та стилі
- `TestBuildBoard` — структура дошки
- `TestRender` — рендеринг без помилок
- `TestCreateColumnHeaders` — заголовки колонок
- `TestBuildRow` — структура рядків
- `TestWinningCellsHighlight` — параметризовані тести для 8 виграшних комбінацій

### Приклад візуалізації

```
            A                 B                 C
   ╔═════════════════╦═════════════════╦═════════════════╗
   ║███           ███║    █████████    ║███           ███║
   ║████         ████║  ███       ███  ║████         ████║
   ║  ████     ████  ║ ██           ██ ║  ████     ████  ║
 1 ║     ███████     ║██             ██║     ███████     ║
   ║  ████     ████  ║ ██           ██ ║  ████     ████  ║
   ║████         ████║  ███       ███  ║████         ████║
   ║███           ███║    █████████    ║███           ███║
   ╠═════════════════╬═════════════════╬═════════════════╣
   ...
```

---

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`):
- **Lint job**: `ruff check` + `ruff format --check`
- **Test job**: `pytest --verbose`
- **AI Review job**: `KonstZiv/ai-code-reviewer@v1` (тільки для PR, після lint+test)
  - Потребує secret `GOOGLE_API_KEY` для Google Gemini API
  - `LANGUAGE: uk` — ревью українською мовою
- Triggers:
  - push to `main`
  - PR to `main` з типами `opened`, `synchronize`
- Python 3.14 via `uv python install`

---

## Session Log

### Session 1 (2026-01-29)

**Виконано:**
1. ✅ Ініціалізація проєкту — створено CLAUDE.md
2. ✅ Task 1: RichRenderer
   - Досліджено бібліотеку tic-tac-toe-3x3
   - Реалізовано RichRenderer з ASCII art 17×7
   - Налаштовано editable install (hatchling)
3. ✅ Тестування — 43 тести для renderer
4. ✅ CI/CD — GitHub Actions (lint, test, ai-review)

**Створені файли:**
- `src/my_tic_tac_toe/__init__.py`
- `src/my_tic_tac_toe/__main__.py`
- `src/my_tic_tac_toe/renderer.py`
- `tests/test_renderer.py`
- `.github/workflows/ci.yml`

**Оновлені файли:**
- `pyproject.toml` — додано build-system
- `CLAUDE.md` — документація

### Session 2 (2026-01-30)

**Виконано:**
1. ✅ Оновлення CI workflow відповідно до актуальної документації ai-code-reviewer
   - Додано `types: [opened, synchronize]` для точнішого тригера PR
   - Додано `LANGUAGE: uk` для ревью українською мовою

**Оновлені файли:**
- `.github/workflows/ci.yml` — оновлено конфігурацію ai-code-reviewer
- `CLAUDE.md` — оновлено документацію

---

## Наступні задачі

(Тут буде опис Task 2, Task 3, тощо)
