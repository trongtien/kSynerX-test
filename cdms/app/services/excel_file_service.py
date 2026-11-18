import zipfile
from io import BytesIO

import pandas as pd


class ExcelFileService:
    def __init__(self, content: bytes) -> None:
        self.content = content
        self.errors: list[dict] = []

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
            data_frame = data_frame.drop_duplicates(subset=["sku"], keep="last")

            data_frame["sku"] = data_frame["sku"].str.strip().str.upper()
            data_frame["name"] = data_frame["name"].str.strip().str.upper()
            data_frame["price"] = pd.to_numeric(
                data_frame["price"].astype(str).str.strip(), errors="coerce"
            )

            data_frame = data_frame.dropna(subset=["price"])
            data_frame = data_frame.reset_index(drop=True)

            dict_data_import = data_frame[["sku", "name", "price"]].to_dict(
                orient="records"
            )

            list_sku = data_frame["sku"].tolist()
            return {"list_sku": list_sku, "dict_data_import": dict_data_import}

        except (ValueError, KeyError, zipfile.BadZipFile) as e:
            raise ValueError(f"Read file is not a valid Excel with error \n --> ${e} ")
