from aliceio.types import BufferedInputFile, FSInputFile, InputFile


class TestInputFile:
    def test_fs_input_file(self):
        file = FSInputFile(__file__)

        assert isinstance(file, InputFile)
        assert file.chunk_size > 0

    async def test_fs_input_file_readable(self):
        file = FSInputFile(__file__, chunk_size=1)

        assert file.chunk_size == 1

        size = 0
        async for chunk in file.read():
            chunk_size = len(chunk)
            assert chunk_size == 1
            size += chunk_size
        assert size > 0

    def test_buffered_input_file(self):
        file = BufferedInputFile(b"\f" * 10)

        assert isinstance(file, InputFile)
        assert isinstance(file.data, bytes)

    async def test_buffered_input_file_readable(self):
        file = BufferedInputFile(b"\f" * 10, chunk_size=1)

        size = 0
        async for chunk in file.read():
            chunk_size = len(chunk)
            assert chunk_size == 1
            size += chunk_size
        assert size == 10

    async def test_buffered_input_file_from_file(self):
        file = BufferedInputFile.from_file(__file__, chunk_size=10)

        assert isinstance(file, InputFile)
        assert isinstance(file.data, bytes)
        assert file.chunk_size == 10

    async def test_buffered_input_file_from_file_readable(self):
        file = BufferedInputFile.from_file(__file__, chunk_size=1)

        size = 0
        async for chunk in file.read():
            chunk_size = len(chunk)
            assert chunk_size == 1
            size += chunk_size
        assert size > 0

    # async def test_url_input_file(self, aresponses: ResponsesMockServer):
    #     aresponses.add(
    #         aresponses.ANY,
    #         aresponses.ANY,
    #         "get",
    #         aresponses.ApiResponse(status=200, body=b"\f" * 10),
    #     )
    #     async with Skill(skill_id="42:SKILL_ID").context() as skill:
    #         file = URLInputFile("https://test.org/", chunk_size=1)
    #
    #         size = 0
    #         async for chunk in file.read(skill):
    #             assert chunk == b"\f"
    #             chunk_size = len(chunk)
    #             assert chunk_size == 1
    #             size += chunk_size
    #         assert size == 10
