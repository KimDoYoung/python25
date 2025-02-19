import xlrd 
import openpyxl
import csv

from logger import Logger

log = Logger()

def xlsx_to_csv(xlsx_file, csv_file, sheet_name=0):
    """
    pandas 없이 openpyxl을 사용하여 .xlsx 파일을 .csv로 변환하는 함수

    :param xlsx_file: 변환할 .xlsx 파일 경로 (예: "data.xlsx")
    :param csv_file: 저장할 .csv 파일 경로 (예: "output.csv")
    :param sheet_name: 변환할 시트 이름 또는 인덱스 (기본값: 첫 번째 시트)
    """
    try:
        # 🔹 엑셀 파일 열기
        workbook = openpyxl.load_workbook(xlsx_file, data_only=True)  # data_only=True -> 수식 대신 값 읽기
        
        # 🔹 시트 선택
        if isinstance(sheet_name, int):
            sheet = workbook.worksheets[sheet_name]  # 인덱스로 시트 선택
        else:
            sheet = workbook[sheet_name]  # 이름으로 시트 선택

        # 🔹 CSV 파일로 저장
        # with open(csv_file, "w", newline="", encoding="utf-8-sig") as csvfile:
        with open(csv_file, "w", newline="", encoding='cp949') as csvfile:
            writer = csv.writer(csvfile)

            # 🔹 모든 행을 CSV로 변환
            for row in sheet.iter_rows(values_only=True):
                writer.writerow(row)

        log.info(f"✅ 변환 완료: {csv_file}")

    except Exception as e:
        log.info(f"❌ 변환 실패: {e}")

def xls_to_csv(xls_file, csv_file):
    """
    pandas 없이 xlrd만 사용하여 .xls 파일을 .csv로 변환하는 함수

    :param xls_file: 변환할 .xls 파일 경로 (예: "data.xls")
    :param csv_file: 저장할 .csv 파일 경로 (예: "output.csv")
    """
    try:
        # 🔹 .xls 파일 열기
        workbook = xlrd.open_workbook(xls_file)
        sheet = workbook.sheet_by_index(0)  # 첫 번째 시트 선택

        # 🔹 CSV 파일로 저장
        # with open(csv_file, "w", newline="", encoding="utf-8-sig") as csvfile:
        with open(csv_file, "w", newline="", encoding='cp949') as csvfile:
            writer = csv.writer(csvfile)

            # 🔹 시트의 모든 행을 CSV로 변환
            for row_idx in range(sheet.nrows):
                writer.writerow(sheet.row_values(row_idx))

        log.info(f"✅ 변환 완료: {csv_file}")

    except Exception as e:
        log.info(f"❌ 변환 실패: {e}")

def excel_to_csv(excel_file, csv_file, sheet_name=0, encoding="utf-8-sig"):
    """
    Excel (.xls, .xlsx) 파일을 CSV로 변환하는 함수.
    """
    # 파일 확장자 확인
    file_extension = excel_file.split(".")[-1].lower()

    if file_extension == "xls":
        xls_to_csv(excel_file, csv_file)
    elif file_extension == "xlsx":
        xlsx_to_csv(excel_file, csv_file, sheet_name)
