#!/bin/bash

echo "🐳 Docker Services Status Check"
echo "================================"
echo ""

echo "📊 Container Status:"
docker-compose ps

echo -e "\n🔗 Service Health:"
echo "---"

# Frontend
echo -n "Frontend (port 80):     "
if curl -s http://localhost/ > /dev/null 2>&1; then
  echo "✅ OK"
else
  echo "❌ Failed"
fi

# Backend
echo -n "Backend (port 8081):    "
if curl -s http://localhost:8081/docs > /dev/null 2>&1; then
  echo "✅ OK"
else
  echo "❌ Failed"
fi

# ML Service
echo -n "ML Service (port 8000): "
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
  echo "✅ OK"
else
  echo "❌ Failed"
fi

echo ""
echo "📋 Service URLs:"
echo "---"
echo "Frontend:   http://localhost"
echo "Backend:    http://localhost:8081/docs"
echo "ML API:     http://localhost:8000/docs"

echo ""
echo "📝 Recent Logs:"
docker-compose logs --tail=5
