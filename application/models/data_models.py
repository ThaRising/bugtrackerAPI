PRIORITY = [
    (1, "TRIVIAL", "Trivial"),
    (2, "MINOR", "Minor"),
    (3, "NORMAL", "Normal"),
    (4, "MAJOR", "Major"),
    (5, "CRITICAL", "Critical")
]

STATUS = [
    (1, "OPEN", "Open"),
    (2, "PROGRESS", "Progress"),
    (3, "REVIEW", "Review"),
    (4, "TEST", "Test"),
    (5, "DONE", "Done")
]

TYPE = [
    (1, "BUG", "Bug"),
    (2, "FEATURE", "Feature"),
    (3, "MEETING", "Meeting"),
    (4, "REFACTOR", "Refactor")
]


def validate_priority(value: int) -> bool:
    return False if value > len(PRIORITY) or value < 1 else True


def validate_status(value: int) -> bool:
    return False if value > len(STATUS) or value < 1 else True


def validate_type(value: int) -> bool:
    return False if value > len(TYPE) or value < 1 else True
