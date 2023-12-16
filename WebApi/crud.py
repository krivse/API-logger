from datetime import datetime
from typing import List

from sqlalchemy import select, update

from models import Log
from schemas import LogCheck


async def create_log(session, log: LogCheck) -> None:
    """Запись лога."""
    result = Log(
        ip_address=log.ip_address,
        http_method=log.http_method.value,
        uri=str(log.uri),
        http_status_code=log.http_status_code
    )
    session.add(result)

    await session.commit()


async def get_log(session) -> List[Log]:
    """Получение списка логов, которые не были ещё отправлены."""
    result = (await session.execute(
        select(
            Log
        ).where(
            Log.updated == None
        )
    )).scalars().fetchall()

    return result


async def update_response_status(session, logs: List[Log]) -> None:
    """Фиксация даты отправки ответа."""
    for log in logs:
        await session.execute(
            update(
                Log
            ).where(
                Log.id == log.id
            ).values(
                updated=datetime.now()
            )
        )

    await session.commit()
