#!/bin/bash


API_URL="http://localhost:8081/api/v1"

if [ $# -eq 0 ]; then
    echo "Использование: ./upload.sh <путь_к_файлу>"
    echo ""
    echo "Поддерживаемые форматы:"
    echo "  - .dcm (DICOM)"
    echo "  - .nii (Nifti)"
    echo "  - .nii.gz (Compressed Nifti)"
    echo ""
    echo "Пример:"
    echo "  ./upload.sh patient.nii.gz"
    echo "  ./upload.sh scan.dcm"
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "❌ Ошибка: файл '$FILE' не найден"
    exit 1
fi

echo "📤 Загружаю $FILE..."

RESPONSE=$(curl -s -X POST "$API_URL/upload/" \
    -F "file=@$FILE" \
    -w "\n%{http_code}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" -eq 200 ]; then
    STUDY_ID=$(echo "$BODY" | grep -o '"study_id":[0-9]*' | grep -o '[0-9]*')
    echo "✅ Успешно загружено!"
    echo ""
    echo "Study ID: $STUDY_ID"
    echo "Статус: $(echo "$BODY" | grep -o '"status":"[^"]*' | cut -d'"' -f4)"
    echo ""
    echo "📥 Получить результат:"
    echo "   curl http://localhost:8081/api/v1/result/$STUDY_ID > result.nii.gz"
    echo ""
    echo "📊 Список всех загрузок:"
    echo "   curl http://localhost:8081/api/v1/studies/"
else
    echo "❌ Ошибка загрузки (код $HTTP_CODE)"
    echo "$BODY"
    exit 1
fi
