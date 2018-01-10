def __atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    import re
    return [__atoi(c) for c in re.split('(\d+)', text)]