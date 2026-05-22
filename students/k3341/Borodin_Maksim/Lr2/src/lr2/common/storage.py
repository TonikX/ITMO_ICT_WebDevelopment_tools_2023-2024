from lr2.common.db import get_session
from lr2.common.models import ParsedPage


def save_parsed_page(
    *,
    url: str,
    title: str | None,
    status: str,
    concurrency_mode: str,
    http_status_code: int | None,
    error_message: str | None,
    duration_ms: int | None,
) -> ParsedPage:
    with get_session() as session:
        item = ParsedPage(
            url=url,
            title=title,
            status=status,
            concurrency_mode=concurrency_mode,
            http_status_code=http_status_code,
            error_message=error_message,
            duration_ms=duration_ms,
        )
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
