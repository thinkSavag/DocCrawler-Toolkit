from bs4 import Tag
from typing import Any, List, cast

def safe_find_all(tag: Any, *args, **kwargs) -> List[Tag]:
    """Only call .find_all() if it's a valid BeautifulSoup Tag."""
    if isinstance(tag, Tag):
        tag = cast(Tag, tag)
        return tag.find_all(*args, **kwargs)
    return []

def safe_attr(tag: Any, attr: str, fallback: str = "") -> str:
    """Safely get an attribute from a tag or return fallback."""
    if isinstance(tag, Tag):
        tag = cast(Tag, tag)
        return tag.get(attr, fallback)
    return fallback

def safe_text(tag: Any, fallback: str = "") -> str:
    """Safely get the stripped text from a tag or fallback."""
    if isinstance(tag, str):
        return tag.strip()
    elif isinstance(tag, Tag) and tag.string:
        return tag.string.strip()
    return fallback
