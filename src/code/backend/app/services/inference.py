from pathlib import Path
import httpx
from app.core.config import settings
import os

async def run_inference(dicom_path: Path, output_path: Path) -> Path:
    """Отправляет DICOM на ML service и получает результат."""

    ml_service_url = settings.LHUNET_URL.replace('/predict', '')
    token = os.getenv('LTS_TOKEN', 'change-me')

    try:
        with open(dicom_path, 'rb') as f:
            file_data = f.read()

        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{ml_service_url}/predict",
                files={'file': (dicom_path.name, file_data, 'application/octet-stream')},
                data={'model': 'v2'},
                headers={'Authorization': f'Bearer {token}'}
            )
            response.raise_for_status()

        with open(output_path, 'wb') as out:
            out.write(response.content)

        return output_path

    except Exception as e:
        raise Exception(f"ML inference failed: {str(e)}")