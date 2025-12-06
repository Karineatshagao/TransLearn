#!/bin/bash

# TransLearn - Run Script
# This script activates the conda environment and runs the Streamlit app

echo "🚀 Starting TransLearn - Learn While You Translate"
echo "=================================================="

# Activate conda environment
eval "$(${HOME}/miniconda3/bin/conda shell.bash hook)"
conda activate translearn

# Check if activation was successful
if [ $? -eq 0 ]; then
    echo "✅ Conda environment 'translearn' activated"
    echo "📱 Launching Streamlit app..."
    echo ""
    streamlit run app.py
else
    echo "❌ Failed to activate conda environment"
    echo "Please make sure conda is properly installed"
    exit 1
fi
