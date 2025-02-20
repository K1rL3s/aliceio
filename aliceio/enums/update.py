from aliceio.enums.base import StrEnum, ValuesEnum


class EventType(StrEnum, ValuesEnum):
    AUDIO_PLAYER = "audio_player"
    BUTTON_PRESSED = "button_pressed"
    ERROR = "error"
    MESSAGE = "message"
    SHOW_PULL = "show_pull"
    PURCHASE = "purchase"
    ACCOUNT_LINKING_COMPLETE = "account_linking_complete_event"
    UPDATE = "update"
    TIMEOUT = "timeout"


class RequestType(StrEnum, ValuesEnum):
    AUDIO_PLAYER_FAILED = "AudioPlayer.PlaybackFailed"
    AUDIO_PLAYER_FINISHED = "AudioPlayer.PlaybackFinished"
    AUDIO_PLAYER_NEARLY_FINISHED = "AudioPlayer.PlaybackNearlyFinished"
    AUDIO_PLAYER_STARTED = "AudioPlayer.PlaybackStarted"
    AUDIO_PLAYER_STOPPED = "AudioPlayer.PlaybackStopped"
    BUTTON_PRESSED = "ButtonPressed"
    PURCHASE_CONFIRMATION = "Purchase.Confirmation"
    SHOW_PULL = "Show.Pull"
    SIMPLE_UTTERANCE = "SimpleUtterance"
    ACCOUNT_LINKING_COMPLETE = "AccountLinkingCompleteEvent"  # Нужен ли?


class ShowType(StrEnum, ValuesEnum):
    MORNING = "MORNING"
