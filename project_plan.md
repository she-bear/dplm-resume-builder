## Тема проекта и примерный функционал
Конструктор резюме

- авторизация (ввод и проверка пароля, регистрация)
- загрузка профиля (хранение изображения)
- конструктор (форма с полями - ФИО, зарплата, навыки, участие в проектах и т.д.)
- интерфейс только для чтения (данные те же, представление другое, версия для печати) - постоянная ссылка для резюме (резюме обновилось - по ссылке новая версия)

## Планирование

- Методология разработки (итеративная) - планируется сразу всё
- Kanban-доска (список задач, по каждой задаче - когда выполнена и какие были трудности)
- Картинки в Figma (разрисовать все страницы на сайте - окно пароля, окно редактирования, окно просмотра, все размеры окон (3 breakpoint) и т.д.) - что было изначально vs что получилось

### Backend

- Выбор технологии и обоснование выбора
- DataBase Engine
    - БД для хранения (mySQL, postgresgl, **SQLite**)
    - Структура БД (scheme) с объяснением всех таблиц с ключами и связями
    - Обоснование выбора (SQLite для начала, не нужен отдельный сервер БД)
- Выбор frameworkа и обоснование выбора
- REST API (специальные ссылки для конкретных действий, интерфейс между frontend и backend)
    - Тестирование API (Swagger - http-запросы, для того, чтобы разделить тестирование frontend и backend)
    - Документация на REST API (ссылки, параметры)
    - Документация на markdown
    

### Frontend

- Выбор framework и обоснование выбора
- Figma (картинки)
- Компоненты - зачем они нужны и что делают


### Инфраструктура

- GitHub (/frontend, /backend, /notes, /doc + readme)
- Продвинутые методологии git (ветки)
- CI/CD
- Docker
- Yandex облако
- Домен 
- Serverless-контейнер (Docker-контейнер → хранение → запуск контейнера по требованию), экономия при небольшом количестве клиентов или для отдельных задач - для дальнейшего развития
- Общая диаграмма проекта (что где запущено, взаимодействия между разными частями проекта)

**ИТОГО ИНФРАСТРУКТУРА:** после выбора framework и языка для backend запуск в Яндекс-облаке всего вместе (автоматическая сборка и запуск).