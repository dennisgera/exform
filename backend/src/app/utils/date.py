from pendulum import now as _now
from pendulum.parser import parse  # noqa: F401


def tz(timezone: str = None) -> str:
    return timezone or "America/Sao_Paulo"

def now():
    return _now(tz())