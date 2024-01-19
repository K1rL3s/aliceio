<p align="center">
  <a href="https://github.com/vkbottle/vkbottle">
    <img width="150px" height="150px" alt="VKBottle" src="https://raw.githubusercontent.com/vkbottle/vkbottle/master/docs/logo.svg"> # сюда свою лого
  </a>
</p>
<h1 align="center">
  Aliceio
</h1>

## Hello World
#### # TODO сделать для алисы
```python
from vkbottle.bot import Bot

bot = Bot("GroupToken")

@bot.on.message()
async def handler(_) -> str:
    return "Hello world!"

bot.run_forever()
```

[Смотреть больше примеров!](https://github.com/aliceio/aliceio/tree/master/examples)

## Документация

[Техническая документация](https://aliceio.rtfd.io)

## Установка

Установить новейшую версию можно командой:

```shell
pip install aliceio
```

## Лицензия

Copyright © 2023-2024 [K1rL3s](https://github.com/K1rL3s).\
Copyright © 2023-2024 [ZloyKobra](https://github.com/ZloyKobra).\
Этот проект имеет [MIT](https://github.com/K1rL3s/aliceio/blob/master/LICENSE) лицензию.декс Алисы - aliceio "Алисио"
