#!/bin/bash

# Test API endpoints script

echo "🧪 Testing Breast Cancer Segmentation Web App API"
echo "=================================================="
echo ""

# Backend URL
BACKEND_URL="http://localhost:8081"
API_V1="$BACKEND_URL/api/v1"

echo "📡 Testing Backend Connectivity"
echo "---"

# Test root endpoint
echo -n "GET $BACKEND_URL/ ... "
if curl -s "$BACKEND_URL/" > /dev/null; then
  echo "✅"
else
  echo "❌"
fi

# Test API docs
echo -n "GET $BACKEND_URL/docs ... "
if curl -s "$BACKEND_URL/docs" > /dev/null; then
  echo "✅"
else
  echo "❌"
fi

echo ""
echo "📤 Testing Upload Endpoint"
echo "---"

# Create a dummy DICOM file for testing
echo "Creating test file..."
TEST_FILE="/tmp/test_dicom.dcm"
echo "DUMMY DICOM CONTENT" > "$TEST_FILE"

echo -n "POST $API_V1/upload/ ... "
RESPONSE=$(curl -s -X POST \
  -F "file=@$TEST_FILE" \
  "$API_V1/upload/")

echo "$RESPONSE" | grep -q "study_id"
if [ $? -eq 0 ]; then
  echo "✅"
  STUDY_ID=$(echo "$RESPONSE" | grep -o '"study_id":[0-9]*' | grep -o '[0-9]*')
  echo "   Study ID: $STUDY_ID"
else
  echo "❌"
  echo "   Response: $RESPONSE"
fi

echo ""
echo "📊 Testing Studies Endpoint"
echo "---"

echo -n "GET $API_V1/studies/ ... "
RESPONSE=$(curl -s "$API_V1/studies/")
echo "$RESPONSE" | grep -q "studies"
if [ $? -eq 0 ]; then
  echo "✅"
else
  echo "❌"
  echo "   Response: $RESPONSE"
fi

echo ""
echo "✅ Tests Complete"
