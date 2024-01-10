from dataclasses import dataclass


@dataclass(frozen=True)
class AliceAPIServer:
    """Базовый конфиг для энподинтов API Алисы."""

    base: str
    file: str

    def api_url(self, method: str) -> str:
        """
        Генерирует URL для независящих от навыка методов API Алисы (status итп).

        :param method: Название метода API (case sensitive).
        :return: URL
        """
        return self.base.format(method=method)

    def upload_url(self, skill_id: str, file_type: str) -> str:
        """
        Генерирует URL для загрузки файла на сервер API Алисы.

        :param skill_id: Айди навыка.
        :param file_type: Тип, изображение или аудио.
        :return: URL
        """
        return self.file.format(skill_id=skill_id, file_type=file_type, file_id="")

    def get_file_url(self, skill_id: str, file_type: str, file_id: str) -> str:
        """
        Генерирует URL для получения информации о файле на сервере API Алисы.

        :param skill_id: Айди навыка.
        :param file_type: Тип, изображение или аудио.
        :param file_id: Айди файла. Если пустая строка, то API вернёт все файлы типа.
        :return: URL
        """
        return self.file.format(skill_id=skill_id, file_type=file_type, file_id=file_id)

    @classmethod
    def from_base(cls, base: str) -> "AliceAPIServer":
        """
        Use this method to auto-generate AliceAPIServer instance from base URL

        :param base: Base URL
        :return: instance of :class:`AliceAPIServer`
        """
        base = base.rstrip("/")
        return cls(
            base=f"{base}/{{method}}",
            file=f"{base}/skills/{{skill_id}}/{{file_type}}/{{file_id}}",
        )


PRODUCTION = AliceAPIServer.from_base(base="https://dialogs.yandex.net/api/v1/")
