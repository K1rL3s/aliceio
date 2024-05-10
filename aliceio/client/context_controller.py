from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, PrivateAttr
from typing_extensions import Self

if TYPE_CHECKING:
    from aliceio.client.skill import Skill


class SkillContextController(BaseModel):
    _skill: Optional["Skill"] = PrivateAttr()

    if TYPE_CHECKING:

        def __init__(
            __pydantic_self__,
            *,
            _skill: Optional["Skill"],
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                _skill=_skill,
                **__pydantic_kwargs,
            )

    def model_post_init(self, __context: Any) -> None:
        self._skill = __context.get("skill") if __context else None

    def as_(self, skill: Optional["Skill"]) -> Self:
        """
        Привязка объекта к экземпляру навыка.

        :param skill: Навыка.
        :return: self
        """
        self._skill = skill
        return self

    @property
    def skill(self) -> Optional["Skill"]:
        return self._skill
