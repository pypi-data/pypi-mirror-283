"""Module for working with Google Sheets."""

from googleapiclient.discovery import build
from googleapiclient.errors import Error as GoogleError
from gspread.utils import MergeType, a1_range_to_grid_range, rowcol_to_a1
from retry import retry

from ..columns_blocks import ColumnsBlock
from ..goole_api.account import Account
from ..goole_api.goolge_services import GoogleServices


class GoogleSheet(GoogleServices):
    """Google Sheet class."""

    def __init__(self, account: Account) -> None:
        """Initialize the Google Sheet."""
        self.service = build("sheets", "v4", credentials=self._get_credentials(account), cache_discovery=False)
        self.header = []
        self.sub_header = []
        self.body = {
            "requests": [],
        }

    def check_or_create_headers(self, file_id: str) -> None:
        """Check or create the headers."""
        if not self.is_header_exist(file_id):
            self.create_header(file_id)

    @retry(tries=3, delay=1, exceptions=GoogleError)
    def is_header_exist(self, file_id: str) -> bool:
        """Check the headers."""
        header = self.service.spreadsheets().values().get(spreadsheetId=file_id, range="1:2").execute()
        header = header.get("values", [])
        if not header:
            return False
        for row in header:
            if not row:
                return False
        else:
            return True

    def get_range(
        self,
        start_row: int,
        start_column: int,
        end_row: int,
        end_column: int,
    ) -> dict:
        """Get the range."""
        range_start = rowcol_to_a1(start_row, start_column)
        range_end = rowcol_to_a1(end_row, end_column)
        return a1_range_to_grid_range(f"{range_start}:{range_end}")

    @retry(tries=3, delay=1, exceptions=GoogleError)
    def create_header(self, file_id: str) -> None:
        """Create the header."""
        self.service.spreadsheets().values().update(
            spreadsheetId=file_id,
            range="1:2",
            valueInputOption="RAW",
            body={"values": [self.header, self.sub_header]},
        ).execute()

    def get_header_block(self, block: ColumnsBlock, block_start_column: int = 0) -> None:
        """Get the header block."""
        if not block.column_names:
            return
        block_end_column = block_start_column + len(block.column_names) - 1
        header = [""] * len(block.column_names)
        header[0] = block.name
        merge_range = self.get_range(1, block_start_column, 1, block_end_column)
        format_range = self.get_range(1, block_start_column, 2, block_end_column)
        self.body["requests"].append({"mergeCells": {"mergeType": MergeType.merge_all, "range": merge_range}})
        alignment = self.get_aligments("CENTER", "MIDDLE")
        bg_color = self.get_bg_color(block.color)
        text_format = self.get_text_format(font_size=10, bold=True, italic=False)
        self.body["requests"].append(
            {
                "repeatCell": {
                    "range": format_range,
                    "cell": {
                        "userEnteredFormat": {
                            **alignment,
                            **bg_color,
                            **text_format,
                        }
                    },
                    "fields": "userEnteredFormat(horizontalAlignment, verticalAlignment, textFormat, backgroundColor)",
                }
            }
        )
        self.header.extend(header)
        self.sub_header.extend(block.column_names)

    @retry(tries=3, delay=1, exceptions=GoogleError)
    def write_to_google_sheet(self, all_cells: list, file_id: str) -> None:
        """Write to the Google Sheet."""
        all_cells.sort(key=lambda x: x.column_number)
        values = [all_cells.value for all_cells in all_cells]
        last_row = self.get_last_row(file_id)
        for index, cell in enumerate(all_cells, start=1):
            format_range = self.get_range(last_row, index, last_row, index)
            alignment = self.get_aligments(cell.alignment, "MIDDLE")
            bg_color = self.get_bg_color(cell.bg_color)
            text_format = self.get_text_format(font_size=10, bold=False, italic=False)
            self.body["requests"].append(
                {
                    "repeatCell": {
                        "range": format_range,
                        "cell": {"userEnteredFormat": {**alignment, **bg_color, **text_format, "wrapStrategy": "WRAP"}},
                        "fields": "userEnteredFormat(horizontalAlignment, verticalAlignment, textFormat,"
                        " backgroundColor, wrapStrategy)",
                    }
                }
            )
        self.service.spreadsheets().values().update(
            spreadsheetId=file_id,
            range=f"{last_row}:{last_row}",
            valueInputOption="RAW",
            body={"values": [values]},
        ).execute()
        self.service.spreadsheets().batchUpdate(spreadsheetId=file_id, body=self.body).execute()

    def get_last_row(self, file_id: str) -> int:
        """Get the last row."""
        header = self.service.spreadsheets().values().get(spreadsheetId=file_id, range="A:A").execute()
        last_row = len(header.get("values", [])) + 1
        return last_row

    def get_aligments(self, vertical: str, horizontal: str) -> dict:
        """Get the alignments block."""
        return {
            "horizontalAlignment": vertical,
            "verticalAlignment": horizontal,
        }

    def get_bg_color(self, color: str) -> dict:
        """Get the background color block."""
        if color is None:
            return {}
        hex_color = color[-6:]
        red, green, blue = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
        red = red / 255
        green = green / 255
        blue = blue / 255
        return {"backgroundColor": {"red": red, "green": green, "blue": blue}}

    def get_text_format(self, font_size: int, bold: bool, italic: bool) -> dict:
        """Get the text format block."""
        return {
            "textFormat": {
                "fontSize": font_size,
                "bold": bold,
                "italic": italic,
            }
        }
