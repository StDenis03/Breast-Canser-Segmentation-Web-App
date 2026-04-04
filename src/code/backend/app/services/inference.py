from pathlib import Path
import numpy as np
from PIL import Image

def run_inference(dicom_path: Path, output_path: Path) -> Path:
    #Заглушка модели сегментации.

    # Создаём случайную маску 512x512
    mask = np.random.randint(0, 255, (512, 512), dtype=np.uint8)
    img = Image.fromarray(mask)
    img.save(output_path)
    
    return output_path