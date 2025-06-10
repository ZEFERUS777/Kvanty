# Kvanty
## Описанние
**Kvanty**-это сайт для образовательных организаций, вы можете взять данный проект как основу для своего сайта
## Структура проекта
File path|Appointment
---------|-----------
**instance//kvant.sqlite3**|База данных сайта
**src//models.py**|Файл с таблицами Sqlite3
**src//wtf_m**|WTF формы
**static//main.css**|CSS стили для base.html
**templates//.html**|HTML страницы сайта
**main.py**|Главный файл сайта, серверный файл
**req.txt**|Список библиотек

## Запуск сервера
В терминале пропишите команду

```Cmd
python -m venv venv
```
Установите необходимые библиотеки 
```Python
pip install -r req.txt
```