import pandas as pd
import os
from datetime import datetime
import config

# ---------- LOGGING ----------
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

# ---------- LOAD FILE ----------        


files = [f for f in os.listdir(config.INPUT_FOLDER) if f.endswith(".xlsx")]

if not files:
    log("No Excel file found in Input folder.")
    exit()
processed_dfs = []
for file in files:
    input_path = os.path.join(config.INPUT_FOLDER, file)
    log(f"Loading file: {file}")

    try:
        df = pd.read_excel(input_path)
    except Exception as e:
        log(f"Failed to read Excel file: {e}")
        exit()

    # ---------- VALIDATION ----------
    missing_cols = [c for c in config.REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        log(f"Missing required columns: {missing_cols}")
        exit()

    # ---------- CLEANING ----------
    for c in config.DROP_COLUMNS:
        if c in df.columns:
            existing_drop_cols = [c for c in config.DROP_COLUMNS if c in df.columns]
            df.drop(columns=existing_drop_cols, inplace=True)
            log(f"Dropped columns: {existing_drop_cols}")

    for b in config.BANNED_CUSTOMER:
        if b in df['Names'].values:
            df.drop(index= df.loc[(df['Names'] == b)].index[0] , inplace=True)
            log(F"Customer:'{b}' is banned")

    # ---------- MISSING VALUES ----------
    num_cols = df.select_dtypes(include="number").columns
    text_cols = df.select_dtypes(exclude="number").columns

    df[num_cols] = df[num_cols].fillna(config.FILL_MISSING_NUMERIC_WITH)
    df[text_cols] = df[text_cols].fillna(config.FILL_MISSING_TEXT_WITH)
    df.dropna(inplace=True)
    processed_dfs.append(df)

    log("Missing values handled")
    
final_df = pd.concat(processed_dfs, ignore_index=True)
log("All files processed and combined")

# ---------- DUPLICATES ----------
if config.UNIQUE_COLUMN in final_df.columns:
    before = len(final_df)
    final_df = final_df.drop_duplicates(subset=config.UNIQUE_COLUMN, inplace=False)
    removed = before - len(final_df)
    log(f"Removed {removed} duplicate rows")
else:
    log(f"Unique column '{config.UNIQUE_COLUMN}' not found; skipping duplicate removal")    

# ----------ADD TOTAL ROW ----------
if config.ADD_TOTAL_ROW:
    final_df.dropna(inplace=True)
    
    total = {}
    for c in final_df.columns:
        if c in num_cols:
            total[c] = final_df[c].sum()
        else:
            total[c] = config.FILL_MISSING_TEXT_WITH
    final_df.loc["Total"] = total

    first_text_col = text_cols[0] if len(text_cols) > 0 else None
    if first_text_col:
        final_df.loc["Total", first_text_col] = config.TOTAL_LABEL

    log("Total row added")

# ---------- SAVE OUTPUT ----------
os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
output_path = os.path.join(config.OUTPUT_FOLDER, config.OUTPUT_FILENAME)

try:
    final_df.to_excel(output_path, index=False)
    log(f"Output saved to {output_path}")
except Exception as e:
    log(f"Failed to save output: {e}")
    exit()
    
log("Total rows in file: " + str(len(final_df)-1))
log("*___________________________________*")
log("| Automation completed successfully |")
log("|___________________________________|")