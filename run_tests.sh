#!/bin/bash
# script to run tests for Modular Data Lab
# This script requires `uv` to be installed for managing dependencies and running tests

set -e

echo "🧪 Modular Data Lab - Test Suite"
echo "================================"

# verify if `uv` is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "📦 Installing test dependencies..."
uv add --dev pytest pytest-cov pytest-mock

# Function to print a section
print_section() {
    echo ""
    echo "🔹 $1"
    echo "$(printf '%.0s-' {1..50})"
}

print_section "Unit Tests"
uv run pytest tests/ -v --tb=short

print_section "Coverage Tests"
uv run pytest tests/ --cov=src/modular_data_lab --cov-report=term-missing --cov-report=html
