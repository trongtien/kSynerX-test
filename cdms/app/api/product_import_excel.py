from typing import Annotated

from app.services.excel_file_service import ExcelFileService
from app.services.product_process_service import ProductProcessService
from core.database import DatabaseSession
from core.logger import logger
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

product_import_excel_router = APIRouter(prefix="/excel", tags=["Product"])


@product_import_excel_router.get(
    "/template-file-export", summary="Dowload file impoer receive product "
)
async def dowload_template_import_product():
    buffer = ExcelFileService.generator_template_product()
    file_name = "product_template.xlsx"
    return StreamingResponse(
        buffer,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )


@product_import_excel_router.post(
    "/product-import", summary="Receive Product Changes import file excel"
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

    if not ExcelFileService.is_valid_xlsx(file_name=file.filename, content=content):
        raise HTTPException(status_code=400, detail="File invalid")

    excel_service = ExcelFileService(content=content)
    dict_data_import = excel_service.extract_data_content_product()

    producr_process_service = ProductProcessService(connection=connection)
    producr_process_service.execute(
        products=dict_data_import["dict_data_import"],
        dict_check_skus=dict_data_import["list_sku"],
    )

    return dict_data_import
