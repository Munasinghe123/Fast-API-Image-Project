def build_line_id(start: str, end: str) -> str:
    if not start or not end:
        raise ValueError("start and end pole codes are required")

    return f"{start.strip().upper()}_{end.strip().upper()}"