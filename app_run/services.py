from geopy.distance import distance
from .models import Position
import openpyxl

def calculate_distance(run_id):
    """
    Функция для расчёта расстояния забега.
    Активируется в момент перевода забега в состояние FINISHED.
    """
    total_distance_km = 0

    positions = Position.objects.filter(run=run_id)

    coords = [(p.latitude, p.longitude) for p in positions]

    if len(coords) < 2:
        return 0.0

    for i in range(len(coords) - 1):
        total_distance_km += distance(coords[i], coords[i + 1]).km

    return total_distance_km


def parse_xlsx_to_list(xlsx_file):
    wb = openpyxl.load_workbook(xlsx_file, read_only=True, data_only=True)
    ws = wb.active

    summary_list = []

    file_rows = ws.iter_rows(values_only=True)
    headers = next(file_rows)

    for row in file_rows:
        temp_dict = {}

        for idx, cell in enumerate(row):
            temp_dict[headers[idx]] = cell

        if any(temp_dict.values()):
            summary_list.append(temp_dict)

    return summary_list
