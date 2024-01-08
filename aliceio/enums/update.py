from aliceio.enums.base import StrEnum, ValuesEnum


class EventType(StrEnum, ValuesEnum):
    AUDIO_PLAYER = "audio_player"
    BUTTON = "button"
    ERROR = "error"
    MESSAGE = "message"
    PULL = "pull"
    PURCHASE = "purchase"
    UPDATE = "update"


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


class ShowType(StrEnum, ValuesEnum):
    MORNING = "MORNING"
