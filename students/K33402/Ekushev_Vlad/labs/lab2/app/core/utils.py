from app.core.config import settings
import slugify as slugify_lib


def slugify(initial_string: str) -> str:
    return slugify_lib.slugify(
        initial_string, lowercase=False, regex_pattern=settings.SLUGIFY_REGEXP
    )
