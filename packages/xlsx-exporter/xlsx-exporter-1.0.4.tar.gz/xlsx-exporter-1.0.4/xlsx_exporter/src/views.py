# src/views.py
import pandas as pd
import logging
from django.shortcuts import render
from django.http import HttpResponse
from .models import TestCase, TestSuite, TestCaseStep, Project
from .forms import UploadFileForm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            project = Project.objects.first()  # Здесь нужно определить проект, например, первый проект
            try:
                xls = pd.ExcelFile(excel_file)
                logger.info(f"Opened file: {excel_file.name}")

                all_test_cases = []
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    test_cases = process_sheet(sheet_name, df)
                    all_test_cases.extend(test_cases)

                created_test_cases = []
                created_test_suites = set()

                for case_data in all_test_cases:
                    suite_name = case_data.pop('suite')
                    suite, created = TestSuite.objects.get_or_create(name=suite_name, project=project)
                    if created:
                        created_test_suites.add(suite.name)

                    steps_data = case_data.pop('steps')
                    try:
                        test_case = TestCase.objects.create(suite=suite, project=project, **case_data)
                        created_test_cases.append(test_case)

                        for step_data in steps_data:
                            TestCaseStep.objects.create(test_case=test_case, **step_data)

                    except Exception as e:
                        logger.error(f"Error creating test case: {e}")
                        continue

                context = {
                    'created_test_cases': created_test_cases,
                    'created_test_suites': list(created_test_suites),
                }

                return render(request, 'xlsxExporter/success.html', context)

            except Exception as e:
                logger.error(f"Error processing file: {e}")
                return HttpResponse('Error processing file', status=500)

    else:
        form = UploadFileForm()

    return render(request, 'xlsxExporter/upload.html', {'form': form})

def process_sheet(sheet_name, df):
    df = df.dropna(how='all').reset_index(drop=True)
    if len(df) > 0:
        df.columns = df.columns.str.strip()
        test_cases = []
        headers = {}

        current_header = None
        steps = []

        for _, row in df.iterrows():
            if pd.isna(row[0]):
                continue

            if row[0] in ["Памятка по обозначению тест-кейсов, по которым делаются автотесты.",
                          "Проще красить поле с идентификатором, так лучше видно."]:
                logger.info(f"Skipping header row: {row[0]}")
                break

            if row[0] == "Идентификатор":
                if row[1] in ["FAI-INS-S3-1 - в работе", "FAI-INS-S3-1 - выполнен"]:
                    logger.info(f"Skipping identifier row: {row[1]}")
                    break

                headers[row[0]] = row[1] if pd.notna(row[1]) else ""
                if current_header:
                    test_cases.append({"header": current_header, "steps": steps})
                current_header = headers.copy()
                steps = []
            elif row[0] in ["Заголовок", "Окружение", "Предусловие"]:
                headers[row[0]] = row[1] if pd.notna(row[1]) else ""
            elif pd.notna(row[0]) and isinstance(row[0], int):
                if current_header is None:
                    current_header = headers.copy()

                step = {
                    "name": f"Step {row[0]}",
                    "scenario": row[1] if pd.notna(row[1]) else "",
                    "expected": row[3] if pd.notna(row[3]) else "",
                    "sort_order": row[0]
                }
                steps.append(step)
            else:
                if current_header and steps:
                    test_cases.append({"header": current_header, "steps": steps})
                    current_header = headers.copy()
                    steps = []

        if current_header and steps:
            test_cases.append({"header": current_header, "steps": steps})

        return format_test_cases(sheet_name, test_cases)

    return []

def format_test_cases(sheet_name, test_cases):
    formatted_cases = []

    for case in test_cases:
        header = case["header"]
        steps = case["steps"]

        name = header.get("Заголовок", "")
        setup = header.get("Предусловие", "") + '\n' + header.get("Окружение", "")
        description = header.get("Комментарий", "")

        test_case = {
            "name": name,
            "suite": sheet_name,
            "setup": setup,
            "scenario": "Scenario details included in steps",
            "expected": "\n".join([step["expected"] for step in steps if step["expected"]]),
            "description": description,
            "steps": steps
        }

        formatted_cases.append(test_case)

    return formatted_cases

def success_view(request):
    return HttpResponse('File uploaded successfully!')
