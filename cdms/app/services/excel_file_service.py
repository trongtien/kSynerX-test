import io
import zipfile
from io import BytesIO

import pandas as pd
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter


class ExcelFileService:
    def __init__(self, content: bytes) -> None:
        self.content = content
        self.errors: list[dict] = []

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
                "sku": ["ABC001"],
                "name": ["Sản phẩm A"],
                "price": [123500],
            }
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

    def extract_data_content_product(self) -> dict[str, list]:
        """
        -> Format columns: Trim and replace name columns
        -> Format data:
            -> remove row colums none value
            -> remove row duplicate value sku
            -> trim value, tranform data number
            -> remove row numberic value is NaN

        -> convert data object, list sku current
        """
        try:
            data_frame = pd.read_excel(
                BytesIO(self.content),
                sheet_name=0,
                engine="openpyxl",
                dtype=str,
            )

            data_frame.columns = (
                data_frame.columns.str.strip().str.lower().str.replace(" ", "_")
            )

            data_frame = data_frame.dropna(subset=["sku", "name", "price"])

            data_frame["sku"] = data_frame["sku"].str.strip().str.upper()
            data_frame["name"] = data_frame["name"].str.strip().str.upper()
            data_frame["price"] = pd.to_numeric(
                data_frame["price"].astype(str).str.strip(), errors="coerce"
            )

            data_frame = data_frame.dropna(subset=["price"])
            data_frame = data_frame.drop_duplicates(subset=["sku"], keep="last")

            data_frame = data_frame.reset_index(drop=True)

            dict_data_import = data_frame[["sku", "name", "price"]].to_dict(
                orient="records"
            )

            list_sku = data_frame["sku"].tolist()
            return {"list_sku": list_sku, "dict_data_import": dict_data_import}

        except (ValueError, KeyError, zipfile.BadZipFile) as e:
            raise ValueError(
                f"Read file is not a valid Excel with error \n --> {e} "
            ) from e
