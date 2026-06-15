#!/bin/bash

BASE_URL=${1:-"http://localhost:8000"}

echo "Running smoke tests against: $BASE_URL"

PASS=0
FAIL=0

check() {
    local description=$1
    local url=$2
    local expected=$3

    code=$(curl -s -o /dev/null -w "%{http_code}" "$url")

    if [ "$code" = "$expected" ]; then
        echo "PASS — $description (HTTP $code)"
        PASS=$((PASS + 1))
    else
        echo "FAIL — $description (expected $expected, got $code)"
        FAIL=$((FAIL + 1))
    fi
}

check "Health check"    "$BASE_URL/health" "200"
check "Metrics"         "$BASE_URL/metrics" "200"
check "Ready check"     "$BASE_URL/ready" "200"
check "Weather current" "$BASE_URL/weather/current?city=Banska%20Bystrica" "200"
check "Weather status"  "$BASE_URL/weather/status?city=Banska%20Bystrica" "200"

echo ""
echo "Results: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
    echo "Smoke test FAILED"
    exit 1
fi

echo "Smoke test PASSED"
exit 0