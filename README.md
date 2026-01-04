# asistente-ia

Asistente local en Python para experimentar con IA (pipeline + utilidades).

## Requisitos
- Python 3.11+

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

python app.py
pytest -q
## 3) `pyproject.toml` (formato + lint + tests)
Esto te deja **ruff** (lint + formatter) y **pytest**.

```bash
cat > pyproject.toml << 'EOF'
[project]
name = "asistente-ia"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py311"
extend-exclude = [".venv"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
