#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "=== 1. 运行投针实验 ==="
uv run --locked python experiment.py

echo ""
echo "=== 2. 生成图表和表格 ==="
if [ -f render_results.py ]; then
    uv run --locked python render_results.py
fi

echo ""
echo "=== 3. 编译 LaTeX 报告 ==="
latexmk -xelatex -interaction=nonstopmode -halt-on-error report.tex

echo ""
echo "=== 完成！ ==="
echo "报告: report.pdf"
