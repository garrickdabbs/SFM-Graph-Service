#!/bin/bash

# Pre-commit hook to enforce SFM enum naming conventions

echo "Checking enum naming conventions..."

# Run the naming convention linter
python tools/naming_convention_linter.py core/sfm_enums.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Naming convention violations found!"
    echo "Please fix the violations above before committing."
    echo "See docs/naming-conventions.md for guidelines."
    exit 1
fi

echo "✅ All naming convention checks passed!"
exit 0