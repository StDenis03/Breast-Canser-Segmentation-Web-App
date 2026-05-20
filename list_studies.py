import requests
import json

API_URL = "http://localhost:8081/api/v1"

def list_studies():
    """Показывает все загруженные исследования."""
    try:
        response = requests.get(f"{API_URL}/studies/", timeout=10)

        if response.status_code == 200:
            studies = response.json()

            if not studies:
                print("📭 Нет загруженных исследований")
                return

            print("📊 Все исследования:\n")
            print(f"{'ID':<5} {'Файл':<30} {'Статус':<12} {'Результат':<40}")
            print("-" * 90)

            for study in studies:
                study_id = study.get('id', 'N/A')
                filename = study.get('filename', 'N/A')[:28]
                status = study.get('status', 'N/A')
                result = study.get('png_path', 'N/A')

                if result != 'N/A':
                    result = result.split('/')[-1][:38]

                print(f"{study_id:<5} {filename:<30} {status:<12} {result:<40}")
        else:
            print(f"❌ Ошибка: статус {response.status_code}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    list_studies()
