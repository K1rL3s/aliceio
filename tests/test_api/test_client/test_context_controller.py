from aliceio.client.context_controller import SkillContextController
from tests.mocked.mocked_skill import MockedSkill


class MyModel(SkillContextController):
    id: int


class TestSkillContextController:
    def test_via_model_validate(self, skill: MockedSkill):
        my_model = MyModel.model_validate({"id": 1}, context={"skill": skill})
        assert my_model.id == 1
        assert my_model._skill == skill

    def test_via_model_validate_none(self):
        my_model = MyModel.model_validate({"id": 1}, context={})
        assert my_model.id == 1
        assert my_model._skill is None

    def test_as(self, skill: MockedSkill):
        my_model = MyModel(id=1).as_(skill)
        assert my_model.id == 1
        assert my_model._skill == skill

    def test_as_none(self):
        my_model = MyModel(id=1).as_(None)
        assert my_model.id == 1
        assert my_model._skill is None

    def test_replacement(self, skill: MockedSkill):
        my_model = MyModel(id=1).as_(skill)
        assert my_model.id == 1
        assert my_model._skill == skill
        my_model = my_model.as_(None)
        assert my_model.id == 1
        assert my_model._skill is None
