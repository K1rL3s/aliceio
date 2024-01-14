from aliceio.client.alice import PRODUCTION, AliceAPIServer


class TestAPIServer:
    def test_method_url(self):
        url = PRODUCTION.api_url(method="METHOD")
        assert url == "https://dialogs.yandex.net/api/v1/METHOD"

    def test_upload_url(self):
        url = PRODUCTION.upload_file_url(skill_id="SKILL", file_type="TYPE")
        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL/TYPE"

    def test_get_all_url(self):
        file_url = PRODUCTION.get_all_files_url(skill_id="SKILL", file_type="TYPE")
        assert file_url == "https://dialogs.yandex.net/api/v1/skills/SKILL/TYPE"

    def test_get_url(self):
        url = PRODUCTION.get_file_url(
            skill_id="SKILL", file_type="TYPE", file_id="FILE"
        )
        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL/TYPE/FILE"

    def test_delete_url(self):
        url = PRODUCTION.delete_file_url(
            skill_id="SKILL", file_type="TYPE", file_id="FILE"
        )
        assert url == "https://dialogs.yandex.net/api/v1/skills/SKILL/TYPE/FILE"

    def test_from_base(self):
        local_server = AliceAPIServer.from_base("http://localhost:8081")

        method_url = local_server.api_url(method="apiMethod")
        upload_url = local_server.upload_file_url(skill_id="SKILL", file_type="TYPE")
        all_url = local_server.get_all_files_url(skill_id="SKILL", file_type="TYPE")
        get_url = local_server.get_file_url(
            skill_id="SKILL", file_type="TYPE", file_id="FILE"
        )
        delete_url = local_server.delete_file_url(
            skill_id="SKILL", file_type="TYPE", file_id="FILE"
        )

        assert method_url == "http://localhost:8081/apiMethod"
        assert upload_url == "http://localhost:8081/skills/SKILL/TYPE"
        assert all_url == "http://localhost:8081/skills/SKILL/TYPE"
        assert get_url == "http://localhost:8081/skills/SKILL/TYPE/FILE"
        assert delete_url == "http://localhost:8081/skills/SKILL/TYPE/FILE"
