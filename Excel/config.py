# ===== CLIENT CONFIGURATION =====

REQUIRED_COLUMNS = ["Date", "Amount"]
DROP_COLUMNS = ["Notes", "Comments"]
BANNED_CUSTOMER = ["Sahra", "Jane"]
UNIQUE_COLUMN = "Names"

FILL_MISSING_NUMERIC_WITH = 0
FILL_MISSING_TEXT_WITH = ""

ADD_TOTAL_ROW = True
TOTAL_LABEL = "TOTAL"
INPUT_FOLDER = "Input"
OUTPUT_FOLDER = "Output"
OUTPUT_FILENAME = "cleaned_output.xlsx"