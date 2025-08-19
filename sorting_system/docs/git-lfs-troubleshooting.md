# Git LFS Troubleshooting Guide

## Common Git LFS Issues in CI/CD

### 1. "invalid load key, 'v'" Error

#### **Symptoms**:
- PyTorch model loading fails with `invalid load key, 'v'`
- Model file appears to be text instead of binary
- Error occurs only in CI environment, not locally

#### **Root Cause**:
The model file is a Git LFS pointer file (text) instead of the actual binary data. This happens when:
- Git LFS is not enabled during checkout
- LFS objects are not downloaded
- The file is not tracked properly with LFS

#### **Solution**:
Enable LFS in GitHub Actions workflow:
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    lfs: true
```

### 2. Pointer File Instead of Binary

#### **Symptoms**:
- Model file contains text like:
  ```
  version https://git-lfs.github.com/spec/v1
  oid sha256:abcdef1234567890...
  size 123456789
  ```
- Instead of actual binary model data

#### **Solution**:
Ensure proper LFS configuration:
```bash
# Locally, verify LFS tracking
git lfs ls-files

# Check if file is properly tracked
git lfs track "*.pth"
git add .gitattributes
```

## GitHub Actions Configuration

### 1. Enable LFS in Workflows

#### **Required Configuration**:
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    lfs: true
```

#### **Important**: 
- Add `lfs: true` to ALL checkout steps in your workflow
- This must be done for every job that needs LFS files

### 2. Verify LFS Files After Checkout

#### **Add Verification Step**:
```yaml
- name: Verify LFS files
  working-directory: ./sorting_system
  run: |
    # Check if model files are binary (not pointer files)
    head -c 10 classification/weights/best_fine_tuned_weights.pth
    # Should show binary data, not text pointer
    
    # Check file size
    ls -la classification/weights/best_fine_tuned_weights.pth
    # Should be large file size, not small pointer file
```

## Local Development Setup

### 1. Install Git LFS

#### **Windows**:
```bash
# Using Git for Windows (includes LFS)
# Or install separately:
git-lfs install
```

#### **macOS**:
```bash
# Using Homebrew
brew install git-lfs
git-lfs install
```

#### **Ubuntu/Debian**:
```bash
# Using apt
sudo apt-get install git-lfs
git-lfs install
```

### 2. Clone Repository with LFS

#### **Proper Cloning**:
```bash
# Clone normally (LFS files will be downloaded automatically)
git clone https://github.com/your-username/sorting_s.git

# Or if already cloned, pull LFS files
cd sorting_s
git lfs pull
```

### 3. Track Large Files with LFS

#### **Setup Tracking**:
```bash
# Track specific file types
git lfs track "*.pth"
git lfs track "*.pt"
git lfs track "*.onnx"
git lfs track "*.h5"
git lfs track "*.weights"

# Add .gitattributes to repository
git add .gitattributes
git commit -m "Track model files with Git LFS"
```

## Debugging LFS Issues

### 1. Check LFS Status

#### **Local Verification**:
```bash
# Check LFS installation
git lfs version

# List tracked files
git lfs ls-files

# Check file status
git lfs status
```

### 2. Verify File Content

#### **Check if File is Pointer**:
```bash
# Check first few bytes of model file
head -c 20 classification/weights/best_fine_tuned_weights.pth

# Pointer file will show:
# version https://git-lfs.gith...

# Binary file will show:
# PNG
# IHD...
```

### 3. CI Debugging

#### **Add Debug Steps to Workflow**:
```yaml
- name: Debug LFS files
  working-directory: ./sorting_system
  run: |
    echo "=== LFS File Information ==="
    ls -la classification/weights/
    echo ""
    
    echo "=== File Type Check ==="
    file classification/weights/best_fine_tuned_weights.pth
    echo ""
    
    echo "=== File Header ==="
    head -c 50 classification/weights/best_fine_tuned_weights.pth || true
    echo ""
    
    echo "=== File Size ==="
    du -h classification/weights/best_fine_tuned_weights.pth
```

## Common Pitfalls

### 1. Forgetting LFS Enablement

#### **Issue**: 
Files are pointer files instead of binaries in CI

#### **Solution**:
Always add `lfs: true` to checkout steps:
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    lfs: true  # ← CRITICAL!
```

### 2. Large File Limits

#### **Issue**:
GitHub has bandwidth limits for LFS downloads

#### **Solution**:
- Consider using Git LFS with a dedicated server for large files
- Monitor bandwidth usage
- Optimize model file sizes when possible

### 3. Incorrect File Tracking

#### **Issue**:
Files committed before LFS tracking remain as regular Git files

#### **Solution**:
```bash
# Fix incorrectly tracked files
git lfs migrate import --include="*.pth,*.pt,*.onnx"
```

## Best Practices

### 1. Repository Organization

#### **Structure**:
```
sorting_system/
├── classification/
│   └── weights/
│       ├── best_fine_tuned_weights.pth  # LFS tracked
│       └── EfficientNetB0.h5            # LFS tracked
├── detection/
│   └── weights/
│       ├── best_2.pt                    # LFS tracked
│       └── yolov8n.pt                   # LFS tracked
└── .gitattributes                       # LFS configuration
```

### 2. .gitattributes Configuration

#### **Proper Setup**:
```gitattributes
# Machine learning models
*.pth filter=lfs diff=lfs merge=lfs -text
*.pt filter=lfs diff=lfs merge=lfs -text
*.onnx filter=lfs diff=lfs merge=lfs -text
*.h5 filter=lfs diff=lfs merge=lfs -text
*.weights filter=lfs diff=lfs merge=lfs -text
```

### 3. Model Loading Robustness

#### **Defensive Programming**:
```python
def load_model_safely(model_path):
    try:
        # Check if file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Check file size (should be substantial for model files)
        file_size = os.path.getsize(model_path)
        if file_size < 1000:  # Less than 1KB is suspicious
            raise ValueError(f"Model file appears to be too small: {file_size} bytes")
        
        # Attempt to load model
        model = torch.load(model_path, map_location=torch.device('cpu'))
        return model
        
    except Exception as e:
        logger.error(f"Failed to load model from {model_path}: {str(e)}")
        # Log file info for debugging
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                header = f.read(100)
                logger.error(f"File header: {header}")
        raise
```

## Emergency Recovery

### 1. Manual LFS Pull in CI

#### **Fallback Solution**:
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    lfs: true

- name: Manual LFS pull (fallback)
  if: failure()
  run: |
    git lfs pull
    git lfs checkout
```

### 2. Alternative Model Loading

#### **For Development Purposes**:
```python
# Fallback to downloading model from external source
def download_model_if_needed(model_path):
    if not os.path.exists(model_path) or os.path.getsize(model_path) < 1000:
        logger.warning("Model file missing or invalid, attempting download...")
        # Download from cloud storage, model hub, etc.
        download_from_backup_source(model_path)
```

## Monitoring and Alerts

### 1. File Integrity Checks

#### **Add to CI Pipeline**:
```yaml
- name: Verify model files integrity
  working-directory: ./sorting_system
  run: |
    # Check if critical model files exist and are reasonably sized
    for model in classification/weights/best_fine_tuned_weights.pth detection/weights/best_2.pt; do
      if [ ! -f "$model" ]; then
        echo "ERROR: Model file missing: $model"
        exit 1
      fi
      
      size=$(stat -c%s "$model")
      if [ $size -lt 1000000 ]; then  # Less than 1MB is suspicious
        echo "ERROR: Model file too small: $model ($size bytes)"
        exit 1
      fi
    done
    
    echo "All model files verified successfully"
```

This approach ensures that Git LFS files are properly downloaded in CI environments, resolving the "invalid load key, 'v'" error you encountered.