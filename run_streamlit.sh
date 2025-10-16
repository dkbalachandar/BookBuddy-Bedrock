#!/bin/bash
# Run Streamlit app accessible from network
echo "🚀 Starting BookBuddy Streamlit app..."
echo "📱 Access from any device on your network!"

# Get local IP
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

echo "🌐 Local access: http://localhost:8501"
echo "📱 Network access: http://$LOCAL_IP:8501"

# Run Streamlit with network access
streamlit run ui.py --server.address=0.0.0.0 --server.port=8501