#!/bin/bash
# debug-pytorch-install.sh
# Script to debug PyTorch installation issues

echo "Debugging PyTorch Installation Issues"
echo "====================================="

# Check available PyTorch versions
echo "Checking available PyTorch versions from PyTorch repository..."
curl -s https://download.pytorch.org/whl/torch_stable.html | grep "torch==" | head -10

echo ""
echo "Checking available torchvision versions from PyTorch repository..."
curl -s https://download.pytorch.org/whl/torch_stable.html | grep "torchvision==" | head -10

echo ""
echo "Current environment information:"
echo "--------------------------------"
python --version
pip list | grep torch

echo ""
echo "Attempting to install PyTorch CPU version..."
pip install torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/torch_stable.html

echo ""
echo "Installation attempt completed."
echo "If you still have issues, try:"
echo "1. Checking if the exact version exists in the repository"
echo "2. Using a different PyTorch version that is available"
echo "3. Installing without the +cpu suffix if needed"