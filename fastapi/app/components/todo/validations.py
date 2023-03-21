def title_must_max_500(v):
    if not (len(v) <= 500):
        raise ValueError("title must not be longer than 500 characters")
    return v

def contents_must_max_1000(v):
    if not (len(v) <= 1000):
        raise ValueError("contents must not be longer than 1000 characters")
    return v