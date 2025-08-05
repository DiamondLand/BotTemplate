## poetry
```commandline
sudo apt install python3-venv
python3 -m venv myenv
source myenv/bin/activate
pip install poetry

poetry init
poetry add "package"
poetry install
poetry run start
```
💡 Важно: Для корректного запуска с использованием `poetry` необходимо вставить следующие строчки:
```commandline
[tool.poetry]
packages = [{include = "src"}]


[tool.poetry.scripts]
start = "src.main:main"
```
в файл `pyproject.toml`
## Создание миграций
```commandline
aerich init -t src.config.db.TORTOISE_ORM
aerich init-db
aerich migrate --name "My migration"
aerich upgrade
```
## Соглашение о именовании коммитов:
```commandline
feature — используется при добавлении новой функциональности уровня приложения
fix — если исправили какую-то серьезную багу
docs — всё, что касается документации
style — исправляем опечатки, исправляем форматирование
refactor — рефакторинг кода приложения
test — всё, что связано с тестированием
chore — обычное обслуживание кода
```
