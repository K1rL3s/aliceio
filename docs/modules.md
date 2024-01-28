# Dependencies customisation

## Logging

Только `logging`

!!! info "Примечание"

    По умолчанию уровень логирования выставлен на `DEBUG`.
    Изменить это вы можете так:

    === "logging"

        ```python
        import logging
        logging.getLogger("aliceio").setLevel(logging.INFO)
        ```
