# import logging
# from typing import List

# import ujson as json
# from fastapi import APIRouter, HTTPException
# from fastapi.encoders import jsonable_encoder

# from app.api import service
# from app.api.models import Log

# router = APIRouter()


# @router.get("/logs", status_code=200)
# def get_all_audit_logs():
#     try:
#         response = service.get_all_audit_logs()
#     except Exception as exp:
#         logging.exception("unhandled error in get_all_audit_logs")
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "status": "error",
#                 "message": "Oops, something went wrong. Try again in a moment.",
#             },
#         )
#     return json.loads(response)


# @router.get("/logs/{app}", status_code=200)
# def get_audit_logs(app: str):
#     try:
#         response = service.get_audit_logs(app)
#     except Exception as exp:
#         logging.exception("unhandled error in get_audit_logs")
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "status": "error",
#                 "message": "Oops, something went wrong. Try again in a moment.",
#             },
#         )
#     return json.loads(response)


# @router.post("/logs", status_code=201)
# async def insert_audit_log(log: List[Log]):
#     try:
#         response = service.insert_audit_log(jsonable_encoder(log))
#     except Exception as exp:
#         logging.exception("unhandled error in insert_audit_log")
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "status": "error",
#                 "message": "Oops, something went wrong. Try again in a moment.",
#             },
#         )
#     return response
