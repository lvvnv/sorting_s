#!/bin/bash
# verify-lfs-files.sh
# Script to verify Git LFS files are properly downloaded

echo "Verifying Git LFS Files"
echo "======================="

# Check if git-lfs is installed
if ! command -v git-lfs &> /dev/null; then
    echo "WARNING: git-lfs is not installed"
    echo "This may cause issues with large file handling"
else
    echo "✓ git-lfs is installed"
    git-lfs version
fi

# Check current directory
echo ""
echo "Current directory: $(pwd)"

# Look for common model file patterns
MODEL_FILES=$(find . -name "*.pth" -o -name "*.pt" -o -name "*.h5" -o -name "*.onnx" -o -name "*.weights" 2>/dev/null)

if [ -z "$MODEL_FILES" ]; then
    echo "No model files found"
    exit 0
fi

echo ""
echo "Found model files:"
echo "$MODEL_FILES"

echo ""
echo "Verifying each model file..."

PROBLEMS_FOUND=0

for file in $MODEL_FILES; do
    echo ""
    echo "Checking: $file"
    echo "----------"
    
    # Check if file exists
    if [ ! -f "$file" ]; then
        echo "  ✗ FILE MISSING"
        PROBLEMS_FOUND=$((PROBLEMS_FOUND + 1))
        continue
    fi
    
    # Check file size
    SIZE=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
    HUMAN_SIZE=$(numfmt --to=iec-i --suffix=B --padding=7 $SIZE 2>/dev/null || echo "${SIZE} bytes")
    
    echo "  Size: $HUMAN_SIZE"
    
    # Check if file is suspiciously small (likely a pointer file)
    if [ $SIZE -lt 200 ]; then
        echo "  ⚠️  WARNING: File is very small - might be a pointer file"
        echo "  First 100 characters:"
        head -c 100 "$file" | tr '\0' '.' | head -c 100
        echo ""
        PROBLEMS_FOUND=$((PROBLEMS_FOUND + 1))
        continue
    fi
    
    # Check file header for binary content
    HEADER=$(head -c 20 "$file")
    
    # Simple heuristic: if it starts with printable ASCII, it might be a pointer
    if [[ $HEADER =~ ^[[:print:]]{10,} ]]; then
        # Check if it looks like an LFS pointer
        if grep -q "version https://git-lfs" "$file" 2>/dev/null; then
            echo "  ⚠️  WARNING: File appears to be an LFS pointer, not the actual binary"
            echo "  File content (first 200 chars):"
            head -c 200 "$file"
            echo ""
            PROBLEMS_FOUND=$((PROBLEMS_FOUND + 1))
            continue
        fi
    fi
    
    echo "  ✓ File appears to be valid binary data"
done

echo ""
echo "Verification complete"

if [ $PROBLEMS_FOUND -gt 0 ]; then
    echo "⚠️  Found $PROBLEMS_FOUND potential issues with LFS files"
    echo "   Make sure 'lfs: true' is set in your GitHub Actions checkout step"
    exit 1
else
    echo "✓ All model files appear to be valid"
    exit 0
fi