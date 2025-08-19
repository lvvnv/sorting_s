# PyTorch Installation Troubleshooting Guide

## Common Issue

**Error Message**: `ERROR: No matching distribution found for torch==2.7.1+cpu`

## Root Cause

The issue occurs because:
1. PyTorch versions with `+cpu` suffix are not available directly on PyPI
2. These versions must be installed from PyTorch's wheel repository
3. Version 2.7.1+cpu may not exist in the repository

## Solution

### 1. Use PyTorch Wheel Repository

Always install PyTorch CPU versions using the `-f` flag:

```bash
pip install torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
```

### 2. Check Available Versions

To see what versions are actually available:

```bash
# For torch
curl -s https://download.pytorch.org/whl/torch_stable.html | grep "torch==" | head -10

# For torchvision
curl -s https://download.pytorch.org/whl/torch_stable.html | grep "torchvision==" | head -10
```

### 3. CI/CD Pipeline Fix

In GitHub Actions workflows, use this approach:

```yaml
- name: Install Python dependencies
  run: |
    python -m pip install --upgrade pip
    # Install CPU version of PyTorch first
    pip install torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
    # Install other dependencies, excluding torch from requirements.txt
    cat requirements.txt | grep -v "torch" > requirements-ci.txt
    pip install -r requirements-ci.txt
    rm requirements-ci.txt
```

## Compatible PyTorch Versions

### CPU Versions (Recommended for CI)
- ✅ `torch==2.0.1+cpu` with `torchvision==0.15.2+cpu`
- ✅ `torch==1.13.1+cpu` with `torchvision==0.14.1+cpu`
- ✅ `torch==1.12.1+cpu` with `torchvision==0.13.1+cpu`

### GPU Versions (Not recommended for CI)
- ⚠️ Require CUDA drivers
- ⚠️ Much larger download size
- ⚠️ Longer installation time

## Requirements.txt Best Practices

### 1. Separate PyTorch Dependencies
In your `requirements.txt`, list PyTorch separately:

```txt
# Core dependencies
Django==5.2.3
djangorestframework==3.15.2
# ... other dependencies

# PyTorch dependencies - COMMENT THESE OUT FOR CI
# torch==2.0.1+cpu
# torchvision==0.15.2+cpu
```

### 2. Use Environment-Specific Installation

```bash
# For development/local
pip install -r requirements.txt

# For CI (skip torch dependencies)
pip install torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
cat requirements.txt | grep -v "torch" > requirements-ci.txt
pip install -r requirements-ci.txt
```

## Debugging Steps

### 1. Check Current Installation
```bash
python -c "import torch; print(torch.__version__)"
```

### 2. Verify PyTorch Installation
```bash
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"
```

### 3. Reinstall if Needed
```bash
pip uninstall torch torchvision -y
pip install torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
```

## Alternative Solutions

### 1. Use Different PyTorch Version
If 2.0.1 is not available, try:
```bash
pip install torch==1.13.1+cpu torchvision==0.14.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
```

### 2. Install Without CPU Suffix
```bash
pip install torch==2.0.1 torchvision==0.15.2 -f https://download.pytorch.org/whl/torch_stable.html
```

### 3. Use Conda (Alternative Package Manager)
```bash
conda install pytorch torchvision cpuonly -c pytorch
```

## GitHub Actions Specific Fixes

### 1. Update Workflow File
Ensure your workflow uses the correct installation approach:

```yaml
steps:
- name: Install Python dependencies
  run: |
    python -m pip install --upgrade pip
    # Install PyTorch first from wheel repository
    pip install torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
    # Then install other dependencies
    pip install -r <(grep -v "torch" requirements.txt)
```

### 2. Handle Shell Compatibility
Some shell commands may not work on all systems. Use this compatible approach:

```yaml
steps:
- name: Install Python dependencies
  run: |
    python -m pip install --upgrade pip
    # Install PyTorch first from wheel repository
    pip install torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
    # Create temporary file without torch dependencies
    grep -v "torch" requirements.txt > temp-requirements.txt
    # Install remaining dependencies
    pip install -r temp-requirements.txt
    # Clean up
    rm temp-requirements.txt
```

## Prevention

### 1. Regular Testing
- Test CI pipeline regularly
- Monitor for PyTorch version deprecations
- Keep dependencies updated

### 2. Version Pinning Strategy
- Pin major.minor versions (e.g., 2.0.x)
- Avoid pinning patch versions unless necessary
- Document why specific versions are needed

### 3. Fallback Versions
Always have backup versions that are known to work:

```bash
# Primary choice
pip install torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/torch_stable.html || \
# Fallback choice
pip install torch==1.13.1+cpu torchvision==0.14.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
```

## Support Resources

- [PyTorch Installation Guide](https://pytorch.org/get-started/locally/)
- [PyTorch Wheel Repository](https://download.pytorch.org/whl/torch_stable.html)
- [PyTorch GitHub Issues](https://github.com/pytorch/pytorch/issues)