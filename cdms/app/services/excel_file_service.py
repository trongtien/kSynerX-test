import io
import zipfile
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO

import pandas as pd
from app.utils.category_builder import CategoryItemBuilder
from app.utils.format_str import FormatString
from app.utils.product_builder_factory import ProductBuilder
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
from pydantic import BaseModel

colums_teamplate: list[str] = [
    "sku",
    "partner_sku",
    "product_name",
    "asset_type",
    "color",
    "size",
    "description",
    "is_active",
    "has_serial",
    "has_expiration",
    "units",
    "categories",
]


@dataclass(frozen=True, slots=True)
class ResultReadExcel(BaseModel):
    list_sku: list[str]
    products: list[ProductBuilder]


class ExcelFileService:
    def __init__(self, content: bytes) -> None:
        self.content = content

    @staticmethod
    def is_valid_xlsx(file_name: str, content: bytes) -> bool:
        allowed_file_exception = {"xlsx", "xlsm"}
        if "." not in file_name:
            return False

        ext_file = file_name.rsplit(".", 1)[1].lower()
        return ext_file in allowed_file_exception

    @staticmethod
    def generator_template_product() -> BytesIO:
        teamplate = pd.DataFrame(
            {
                "SKU": "SKU-00001",
                "Partner Sku": "P-00001",
                "Product Name": "Sản phẩm A",
                "Asset Type": "Single",
                "Color": "Red",
                "Size": "M",
                "Description": "Mô tả",
                "Is Active": "TRUE",
                "Has Serial": "FALSE",
                "Has Expiration": "FALSE",
                "Units": "PCS,BOX",
                "Categories": "CAT01:Điện thoại;CAT02:Phụ kiện",
            },
            index=[0],
        )

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            sheet_name = "Sheet 1"
            teamplate.to_excel(writer, index=False, sheet_name=sheet_name)
            ws = writer.sheets[sheet_name]

            header_fill = PatternFill(
                start_color="4472C4", end_color="4472C4", fill_type="solid"
            )
            for col_idx, _ in enumerate(teamplate.columns, 1):
                cell = ws.cell(row=1, column=col_idx)
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = header_fill
                ws.column_dimensions[get_column_letter(col_idx)].width = 20

        buffer.seek(0)

        return buffer

    def extract_data_content_product(self, update_at: datetime) -> ResultReadExcel:
        """
        -> Format columns: Trim and replace name columns
        -> Format data:
            -> remove row colums none value
            -> remove row duplicate value sku
            -> trim value, tranform data number
            -> remove row numberic value is NaN

        -> convert data object, list sku current
        """
        data_frame = self._load_data_frame()
        list_sku: list[str] = data_frame["sku"].tolist()
        dict_data_frame = data_frame.to_dict(orient="records")

        products: list[ProductBuilder] = []

        for _, row in enumerate(dict_data_frame):
            mapping_row = ProductBuilder(
                sku=row.get("sku") or "",
                product_name=row.get("product_name") or "",
                source_updated_at=update_at,
                partner_sku=row.get("partner_sku"),
                asset_type=row.get("asset_type"),
                color=row.get("color"),
                size=row.get("size"),
                description=row.get("description"),
                is_active=FormatString.format_bool(
                    row.get("is_active"), default_value=True
                ),
                has_serial=FormatString.format_bool(
                    row.get("has_serial"), default_value=False
                ),
                has_expiration=FormatString.format_bool(
                    row.get("has_expiration"), default_value=False
                ),
                units=FormatString.split_string_tuple(row.get("units")),
                categories=CategoryItemBuilder.tranform_with_string(
                    row.get("categories")
                ),
            )
            products.append(mapping_row)

        return ResultReadExcel(list_sku=list_sku, products=products)

    def _load_data_frame(self):
        try:
            data_frame = pd.read_excel(
                BytesIO(self.content),
                sheet_name=0,
                engine="openpyxl",
                dtype=str,
            )
        except (ValueError, KeyError, zipfile.BadZipFile) as e:
            raise ValueError(
                f"Read file is not a valid Excel with error \n --> {e} "
            ) from e

        data_frame.columns = (
            data_frame.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r"\s+", "_", regex=True)
        )

        data_frame = data_frame.dropna(subset=["sku", "product_name"])
        data_frame["sku"] = data_frame["sku"].str.strip().str.upper()
        data_frame["product_name"] = data_frame["product_name"].str.strip()
        data_frame = data_frame.drop_duplicates(subset=["sku"], keep="last")
        data_frame = data_frame.reset_index(drop=True)

        if data_frame.empty:
            raise ValueError("File data invalid")

        return data_frame.astype(object).where(pd.notna(data_frame), None)
