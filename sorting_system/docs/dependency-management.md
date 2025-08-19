# Dependency Management Best Practices

## Common Dependency Issues and Solutions

### 1. Missing Dependencies

#### **Symptom**: `ModuleNotFoundError: No module named 'package_name'`

#### **Diagnosis**:
```bash
# Check if package is in requirements.txt
grep -i "package_name" requirements.txt

# Check if package is installed
pip list | grep -i "package_name"
```

#### **Solution**:
1. Add missing package to `requirements.txt`:
   ```txt
   package-name==1.2.3
   ```

2. Install the package:
   ```bash
   pip install -r requirements.txt
   ```

### 2. Version Compatibility Issues

#### **Symptom**: `ERROR: No matching distribution found for package==version`

#### **Diagnosis**:
```bash
# Check available versions
pip index versions package-name

# Check PyPI for available versions
curl -s https://pypi.org/pypi/package-name/json | jq '.releases | keys'
```

#### **Solution**:
1. Use a compatible version from PyPI:
   ```txt
   package-name==1.2.0  # Use available version
   ```

2. For special packages (like PyTorch with CPU/GPU variants):
   ```bash
   # Install from specific repository
   pip install torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
   ```

### 3. Import Errors

#### **Symptom**: `ImportError: cannot import name 'function_name' from 'module_name'`

#### **Diagnosis**:
```bash
# Check package version
python -c "import module_name; print(module_name.__version__)"

# Check available attributes
python -c "import module_name; print(dir(module_name))"
```

#### **Solution**:
1. Check documentation for correct import path
2. Update to compatible version:
   ```txt
   # Update requirements.txt with correct version
   module-name==compatible_version
   ```

## Requirements.txt Management

### 1. Adding New Dependencies

#### **Process**:
```bash
# Install package locally
pip install package-name

# Freeze current environment (temporarily)
pip freeze > temp-requirements.txt

# Extract new package version
grep "package-name" temp-requirements.txt >> requirements.txt

# Clean up
rm temp-requirements.txt
```

#### **Best Practice**:
```txt
# Pin exact versions for reproducibility
package-name==1.2.3

# Or use compatible release for minor updates
package-name~=1.2.3  # Equivalent to >=1.2.3, ==1.2.*
```

### 2. Updating Dependencies

#### **Process**:
```bash
# Update specific package
pip install --upgrade package-name

# Update requirements.txt
pip freeze | grep "package-name" > temp-version.txt
sed -i "s/^package-name.*/$(cat temp-version.txt)/" requirements.txt
rm temp-version.txt
```

### 3. Removing Unused Dependencies

#### **Process**:
```bash
# Check if package is used in codebase
grep -r "import package_name" .

# If not found, remove from requirements.txt
# Edit requirements.txt manually
```

## CI/CD Pipeline Considerations

### 1. Special Package Handling

#### **PyTorch and Machine Learning Libraries**:
```yaml
- name: Install Python dependencies
  run: |
    # Install special packages first from their repositories
    pip install torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
    # Install remaining dependencies
    pip install -r <(grep -v "torch" requirements.txt)
```

#### **Platform-Specific Packages**:
```yaml
- name: Install platform-specific dependencies
  run: |
    # Install common dependencies
    pip install -r requirements-common.txt
    # Install platform-specific packages
    if [ "$RUNNER_OS" == "Linux" ]; then
      pip install -r requirements-linux.txt
    elif [ "$RUNNER_OS" == "Windows" ]; then
      pip install -r requirements-windows.txt
    fi
```

### 2. Dependency Verification

#### **Pre-flight Checks**:
```bash
# Verify all dependencies can be imported
python -c "
import sys
import pkg_resources

# Read requirements.txt
with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Try importing each package
failed_imports = []
for req in requirements:
    if '==' in req:
        package_name = req.split('==')[0]
    else:
        package_name = req.split('>')[0].split('<')[0].split('~')[0]
    
    try:
        __import__(package_name.replace('-', '_'))
        print(f'✓ {package_name}')
    except ImportError as e:
        failed_imports.append((package_name, str(e)))

if failed_imports:
    print('Failed imports:')
    for package, error in failed_imports:
        print(f'✗ {package}: {error}')
    sys.exit(1)
"
```

## Troubleshooting Checklist

### 1. Immediate Actions

#### **When facing any dependency issue**:
```bash
# 1. Check current environment
pip list
python --version

# 2. Verify requirements.txt
cat requirements.txt

# 3. Try reinstalling
pip install -r requirements.txt --force-reinstall

# 4. Check for conflicts
pip check
```

### 2. Common Patterns

#### **Missing System Dependencies**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y package-name

# CentOS/RHEL
sudo yum install -y package-name

# macOS (Homebrew)
brew install package-name
```

#### **Virtual Environment Issues**:
```bash
# Recreate virtual environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 3. Validation Steps

#### **Before committing changes**:
```bash
# 1. Verify all dependencies install
pip install -r requirements.txt

# 2. Check Django configuration
python manage.py check

# 3. Run a simple test
python manage.py test --verbosity=0

# 4. Verify imports
python -c "
import django
import rest_framework
import torch
import cv2
import corsheaders
print('All critical dependencies imported successfully')
"
```

## Best Practices Summary

### 1. **Version Pinning**
- Pin exact versions for production environments
- Use compatible release operators (`~=`) for development
- Document why specific versions are required

### 2. **Separation of Concerns**
- Separate core, development, and testing requirements
- Use environment markers for platform-specific dependencies
- Keep requirements files organized and documented

### 3. **Testing and Validation**
- Test dependency changes in isolated environments
- Verify imports and basic functionality after updates
- Include dependency verification in CI/CD pipelines

### 4. **Documentation**
- Document special installation procedures
- Note platform-specific requirements
- Keep a changelog of dependency updates