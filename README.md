# webinar-ai-coding-for-beginners

---

**My Tic-Tac-Toe: Красива консольна гра на базі tic-tac-toe-3x3**

---

**Опис проєкту:**
Консольна гра "Хрестики-нолики" з покращеним візуальним інтерфейсом. Побудована на базі бібліотеки `tic-tac-toe-3x3`, яка надає ігровий рушій та AI-опонента (minimax).

**Мета:**
Продемонструвати процес розробки з використанням AI — від планування до CI/CD. Проєкт створюється в рамках вебінару для початківців.

**Функціонал:**
- Красива Rich-консоль: кольори, рамки, емодзі
- Режими гри: human vs human, human vs AI, AI vs AI
- Меню: вибір режиму, рестарт, вихід
- Відображення результату: переможець або нічия

**Технології:**
- Python 3.14
- tic-tac-toe-3x3 — ігровий рушій
- Rich — візуалізація в консолі
- pytest — тестування
- ruff — лінтинг
- GitHub Actions + ai-code-reviewer — CI/CD з AI-рев'ю

**Встановлення:**
```bash
# Клонувати репозиторій
git clone https://github.com/your-username/webinar-ai-coding-for-beginners.git
cd webinar-ai-coding-for-beginners

# Встановити залежності
uv sync
```

**Запуск гри:**
```bash
# Два гравці (human vs human)
uv run python -m my_tic_tac_toe

# Грати проти Minimax AI (непереможний)
uv run python -m my_tic_tac_toe --ai

# Грати проти Random AI (легкий рівень)
uv run python -m my_tic_tac_toe --ai random

# AI ходить першим (грає за X)
uv run python -m my_tic_tac_toe --ai --ai-first

# Зберегти історію ходів (без Live display)
uv run python -m my_tic_tac_toe --no-live
```

**Опції командного рядка:**
| Опція | Опис |
|-------|------|
| `--ai` | Грати проти AI (за замовчуванням: minimax) |
| `--ai minimax` | Грати проти Minimax AI (непереможний) |
| `--ai random` | Грати проти Random AI |
| `--ai-first` | AI ходить першим (грає за X) |
| `--no-live` | Вимкнути Live display (зберігає історію в терміналі) |
| `-h, --help` | Показати довідку |

