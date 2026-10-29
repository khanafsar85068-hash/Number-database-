import os
import sys
import json
import pandas as pd

def excel_to_json(file_path):
    if not os.path.isfile(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return

    try:
        # Automatically detect all Excel sheets
        excel = pd.ExcelFile(file_path)
        sheet_names = excel.sheet_names

        print(f"\n[+] File: {os.path.basename(file_path)}")
        print(f"[+] Total sheets detected: {len(sheet_names)}")

        output_dir = os.path.splitext(file_path)[0] + "_json"
        os.makedirs(output_dir, exist_ok=True)

        all_sheets = {}

        for index, sheet in enumerate(sheet_names, start=1):
            print(f"[{index}/{len(sheet_names)}] Converting: {sheet}")

            df = pd.read_excel(
                excel,
                sheet_name=sheet,
                dtype=object
            )

            # Replace missing values and make JSON-safe records
            df = df.astype(object).where(pd.notna(df), None)

            records = df.to_dict(orient="records")
            all_sheets[sheet] = records

            # Save individual sheet JSON
            safe_name = "".join(
                c if c.isalnum() or c in "-_ " else "_"
                for c in sheet
            ).strip() or f"sheet_{index}"

            output_file = os.path.join(
                output_dir, f"{safe_name}.json"
            )

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(
                    records,
                    f,
                    indent=4,
                    ensure_ascii=False,
                    default=str
                )

            print(f"    Saved: {output_file}")
            print(f"    Rows: {len(records)}")

        # Save all sheets in one combined JSON file
        combined_file = os.path.join(output_dir, "all_sheets.json")

        with open(combined_file, "w", encoding="utf-8") as f:
            json.dump(
                all_sheets,
                f,
                indent=4,
                ensure_ascii=False,
                default=str
            )

        print("\n[SUCCESS] Conversion completed!")
        print(f"[+] Sheets converted: {len(sheet_names)}")
        print(f"[+] Output folder: {output_dir}")
        print(f"[+] Combined JSON: {combined_file}")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python excel_to_json.py <excel_file>")
        sys.exit(1)

    excel_to_json(sys.argv[1])