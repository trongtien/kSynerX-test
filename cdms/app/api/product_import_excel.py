from typing import Annotated

from core.database import DatabaseSession
from core.logger import logger
from fastapi import APIRouter, File, HTTPException, UploadFile

product_import_excel_router = APIRouter(prefix="/import", tags=["Product"])


@product_import_excel_router.post(
    "/import-xlsx", summary="Receive Product Changes import file excel"
)
async def import_file_receive_product(
    file: Annotated[UploadFile, File()],
    connection: DatabaseSession,
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File invalid")

    try:
        content = await file.read()

    except OSError as e:
        logger.info(f"Failed to read uploaded file \n --> {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process import file: \n {e}"
        ) from e

    if not is_valid_xlsx(file_name=file.filename, content=content):
        raise HTTPException(status_code=400, detail="File invalid")

    return {"filename": file.filename, "size": len(content)}


def is_valid_xlsx(file_name: str, content: bytes) -> bool:
    allowed_file_exception = {"xlsx", "xlsm"}
    if "." not in file_name:
        return False

    ext_file = file_name.rsplit(".", 1)[1].lower()
    return ext_file in allowed_file_exception
