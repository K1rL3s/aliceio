# Роутеры

Далее в туториале регистрация хэндлеров будет происходить через роутеры.
Подробнее про них и существующие события Алисы можно узнать [здесь](../aliceio/dispatcher/router.md){:target="_blank"}.

Роутеры нужны для разделения проекта на несколько файлов и гибкой установки мидлварей и фильтров, но об этом подробнее к концу гайда.

!!! note "Примечание"
    Диспетчер - тоже роутер.

## Примеры

Создание роутера:
```python
from aliceio import Router

router = Router(name=__name__)
# __name__ - имя текущего модуля. Указывать `name=...` необязательно
```

* [multi_file_skill](https://github.com/K1rL3s/aliceio/tree/master/examples/multi_file_skill){:target="_blank"}
