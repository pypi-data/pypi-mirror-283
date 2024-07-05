import os
import logging


from time import time
from typing import Callable

from fastapi import  Response, Request, HTTPException
from fastapi.routing import APIRoute

from .loggers import TNLogger, UnExpectedError


class FastAPILogger(APIRoute):
        

    def get_route_handler(self)  -> Callable:
        original_route_handler = super().get_route_handler()

        # resource = TNLogger.with_service_detail()
        error_logger = TNLogger.with_service_detail(name="error", level=logging.ERROR)

        # uvicorn_access = logging.getLogger("uvicorn.access")
        # uvicorn_access.addHandler(fast_logger.get_handler())

        async def custom_route_handler(request: Request) -> Response:
            
            try:
                response: Response = await original_route_handler(request)
                return response
            except HTTPException as http_exc:
                error_logger.error('{}'.format(http_exc.detail))
                raise HTTPException(http_exc.status_code, detail=str(http_exc.detail))

            except Exception as exc:
                obj_err = UnExpectedError("NO Handler Error", exc=exc)

                if obj_err.http_status == 500:
                    error_logger.error(obj_err.msg_body, stack_info=True, exc_info=True, extra=obj_err.attributes)
                else:
                    error_logger.error(obj_err.msg_body, extra=obj_err.attributes)
                    
                raise HTTPException(500, detail = str(exc))


        return custom_route_handler