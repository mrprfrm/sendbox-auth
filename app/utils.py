def to_camelcase(data: dict) -> dict:
    "Convert data snake_case keys to camelCase."
    for key, value in data.items():
        key_parts = key.split("_")
        key_start = key_parts[0].lower()
        key_last = ''.join(map(lambda prt: prt.title(), key_parts[1:]))
        value = dict(to_camelcase(value)) if isinstance(value, dict) else value
        yield f"{key_start}{key_last}", value
