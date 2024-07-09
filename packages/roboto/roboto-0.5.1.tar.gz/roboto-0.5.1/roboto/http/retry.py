import random
import typing

import tenacity.wait

RetryWaitFn = typing.Callable[
    [tenacity.RetryCallState, typing.Optional[BaseException]], float
]


def default_retry_wait_ms(
    retry_state: tenacity.RetryCallState, _exc: typing.Optional[BaseException]
) -> float:
    """
    Returns sleep time in ms using exponential backoff with full jitter, as described in:
    https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
    """
    base = 500
    cap = 30_000

    exponential_wait = min(cap, pow(2, retry_state.attempt_number) * base)
    jittered = random.uniform(0, exponential_wait)
    return jittered
