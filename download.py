import requests
import sys
from pathlib import Path

API_URL = "http://localhost:8081/api/v1"

def download_result(study_id, output_file=None):
    try:
        response = requests.get(f"{API_URL}/result/{study_id}", timeout=30)

        if response.status_code == 200:
            if output_file is None:
                output_file = f"result_study_{study_id}.nii.gz"

            with open(output_file, 'wb') as f:
                f.write(response.content)

            file_size = Path(output_file).stat().st_size / (1024 * 1024)
            print(f"✅ Результат скачан: {output_file}")
            print(f"   Размер: {file_size:.2f} MB")
        else:
            print(f"❌ Ошибка: статус {response.status_code}")
            print(response.text)
            sys.exit(1)

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python download.py <study_id> [output_file]")
        print()
        print("Пример:")
        print("  python download.py 1")
        print("  python download.py 1 my_result.nii.gz")
        sys.exit(1)

    study_id = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    download_result(study_id, output_file)
