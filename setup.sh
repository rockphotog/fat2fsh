#!/bin/bash

# Setup script for fat2fsh converter

echo "Setting up fat2fsh converter..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Check if pip is available
if ! python3 -m pip --version &> /dev/null; then
    echo "Error: pip is not available for Python 3"
    echo "Please install pip first"
    exit 1
fi

echo "Installing dependencies to user Python environment..."

# Install packages directly
echo "Installing requests..."
python3 -m pip install --user "requests>=2.31.0" || {
    echo "Failed to install requests with --user. Trying --break-system-packages..."
    python3 -m pip install --break-system-packages "requests>=2.31.0" || {
        echo "Failed to install requests"
        exit 1
    }
}

echo "Installing click..."
python3 -m pip install --user "click>=8.1.0" || {
    echo "Failed to install click with --user. Trying --break-system-packages..."
    python3 -m pip install --break-system-packages "click>=8.1.0" || {
        echo "Failed to install click"
        exit 1
    }
}

echo "Installing pydantic..."
python3 -m pip install --user "pydantic>=2.0.0" || {
    echo "Failed to install pydantic with --user. Trying --break-system-packages..."
    python3 -m pip install --break-system-packages "pydantic>=2.0.0" || {
        echo "Failed to install pydantic"
        exit 1
    }
}

echo "Setup complete!"
echo ""
echo "You can now run the tool directly:"
echo "python3 fat2fsh.py --help"
echo "python3 fat2fsh.py -c system1 -c system2 -v"
echo ""
echo "Note: Dependencies are installed to your user Python environment"