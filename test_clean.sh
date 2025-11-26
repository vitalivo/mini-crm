#!/bin/bash
echo "ЧИСТЫЙ ТЕСТ МИНИ-CRM"
echo "========================"

echo "1. Создаём операторов"
anna_id=$(curl -s -X POST http://localhost:8000/admin/operators/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Анна","max_active":10}' | jq -r .id)

maxim_id=$(curl -s -X POST http://localhost:8000/admin/operators/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Максим","max_active":20}' | jq -r .id)

echo "   Анна → id=$anna_id"
echo "   Максим → id=$maxim_id"

echo "2. Создаём источник"
curl -s -X POST http://localhost:8000/admin/sources/ \
  -H "Content-Type: application/json" \
  -d '{"name":"telegram_sales"}' | jq .

echo "3. Назначаем веса (Анна=10, Максим=30)"
curl -s -X POST http://localhost:8000/admin/sources/telegram_sales/weights \
  -H "Content-Type: application/json" \
  -d "{\"weights\":{\"$anna_id\":10,\"$maxim_id\":30}}" | jq .

echo "4. Генерируем 50 обращений..."
for i in {1..50}; do
  curl -s -X POST http://localhost:8000/contacts/ \
    -H "Content-Type: application/json" \
    -d '{"external_id":"tg_12345","source_name":"telegram_sales","payload":{"test":true}}' > /dev/null
done

echo -e "\nФИНАЛЬНАЯ СТАТИСТИКА:"
curl -s http://localhost:8000/contacts/ > /tmp/c.json
anna=$(jq '[.[] | select(.operator_name == "Анна" and .is_active)] | length' /tmp/c.json)
maxim=$(jq '[.[] | select(.operator_name == "Максим" and .is_active)] | length' /tmp/c.json)
none=$(jq '[.[] | select(.operator_name == null and .is_active)] | length' /tmp/c.json)

echo "Анна:    $anna / 10 (лимит)"
echo "Максим:  $maxim / 20 (лимит)"
echo "Без оператора: $none"
echo "Всего:   $((anna + maxim + none))"
rm -f /tmp/c.json