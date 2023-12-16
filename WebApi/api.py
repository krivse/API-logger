from fastapi import Depends, FastAPI, status
from starlette.responses import JSONResponse

from crud import create_log, get_log, update_response_status
from schemas import LogBase, validate
from database import get_db

app = FastAPI()


@app.post('/api/data/', status_code=status.HTTP_201_CREATED, response_model=LogBase)
async def save_log(data: LogBase, session=Depends(get_db)):
    """Обработка строки / валидация / запись в бд."""
    validate_data = await validate(data.log.split())
    await create_log(session, validate_data)
    return JSONResponse('Лог Сохранен')


@app.get('/api/data/', status_code=status.HTTP_200_OK)
async def get_list_log(session=Depends(get_db)):
    """Обработка GET запроса и выдача данных за период."""
    # Получаем все логи за период со статусом False
    result = await get_log(session)
    # Обновляем признак status_response на True
    await update_response_status(session, result)
    # Собираем необходимую структуру для ответа
    logs = []
    for log in result:
        logs.append({
            'id': str(log.id),
            'created': log.created.timestamp(),
            'log': {
                'ip_address': str(log.ip_address),
                'http_method': log.http_method,
                'uri': log.uri,
                'http_status_code': log.http_status_code
            }
        })

    return JSONResponse(logs)
