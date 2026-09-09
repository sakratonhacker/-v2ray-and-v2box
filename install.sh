#!/data/data/com.termux/files/usr/bin/bash

echo "Installing Config Maker..."
pkg install python -y

chmod +x main.py
chmod +x install.sh

echo
echo "Installation completed!"
echo "Run with:"
echo "python main.py"
