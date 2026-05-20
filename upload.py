import requests
import sys
from pathlib import Path

API_URL = "http://localhost:8081/api/v1"

def upload_file(filepath):
    """Загружает файл на сервер."""
    filepath = Path(filepath)

    if not filepath.exists():
        print(f"❌ Ошибка: файл '{filepath}' не найден")
        sys.exit(1)

    supported = ('.dcm', '.nii', '.nii.gz')
    if not any(filepath.name.endswith(ext) for ext in supported):
        print(f"❌ Ошибка: поддерживаются только {supported}")
        sys.exit(1)

    print(f"📤 Загружаю {filepath.name}...")

    try:
        with open(filepath, 'rb') as f:
            files = {'file': (filepath.name, f)}
            response = requests.post(f"{API_URL}/upload/", files=files, timeout=300)

        if response.status_code == 200:
            data = response.json()
            study_id = data['study_id']
            print("✅ Успешно загружено!")
            print()
            print(f"Study ID: {study_id}")
            print(f"Статус: {data['status']}")
            print()
            print("📥 Получить результат:")
            print(f"   python download.py {study_id}")
            print()
            print("📊 Список всех загрузок:")
            print(f"   python list_studies.py")
        else:
            print(f"❌ Ошибка загрузки (код {response.status_code})")
            print(response.text)
            sys.exit(1)

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python upload.py <путь_к_файлу>")
        print()
        print("Поддерживаемые форматы:")
        print("  - .dcm (DICOM)")
        print("  - .nii (Nifti)")
        print("  - .nii.gz (Compressed Nifti)")
        print()
        print("Пример:")
        print("  python upload.py patient.nii.gz")
        print("  python upload.py scan.dcm")
        sys.exit(1)

    upload_file(sys.argv[1])
