import typing

JsonablePrimitive = typing.Union[int, str, float, bool]
UserMetadata = dict[str, JsonablePrimitive]
