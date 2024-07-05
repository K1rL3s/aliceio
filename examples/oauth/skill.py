from aliceio import F, Router
from aliceio.types import AccountLinkingComplete, Directives, Message, Response, User

router = Router()


@router.message(F.meta.interfaces.account_linking.is_(None))
async def auth_impossible(message: Message) -> str:
    return "Авторизация невозможна на вашем устройстве :("


@router.message(~F.user.access_token)
async def start_auth(message: Message) -> Response:
    return Response(
        text="Начало авторизации",
        directives=Directives(start_account_linking={}),
    )


@router.account_linking_complete()
async def complete_auth(account_linking_complete: AccountLinkingComplete) -> str:
    return "Круто!"


@router.message(F.user.access_token)
async def check_auth(message: Message, event_from_user: User) -> str:
    return f"Я вас знаю, вы - {event_from_user.access_token}"
