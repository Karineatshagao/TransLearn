#!/bin/bash

# TransLearn - Network Deployment Script
# Run this to make the app accessible to others on your network

echo "🚀 Starting TransLearn - Network Deployment"
echo "============================================"
echo ""

# Get the local IP address
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)

echo "📍 Your local IP address: $LOCAL_IP"
echo ""
echo "🌐 Share this URL with your friend:"
echo "   http://$LOCAL_IP:8501"
echo ""
echo "⚠️  Important:"
echo "   - Your friend must be on the SAME WiFi network"
echo "   - Keep this terminal window open"
echo "   - Press Ctrl+C to stop the server"
echo ""
echo "============================================"
echo ""

# Activate conda environment
eval "$(${HOME}/miniconda3/bin/conda shell.bash hook)"
conda activate translearn

# Run Streamlit with network access
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
