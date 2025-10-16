#!/bin/bash
# Deploy BookBuddy with ngrok for instant public access

echo "🚀 Setting up BookBuddy with public access via ngrok..."

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "📦 Installing ngrok..."
    # For macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ngrok/ngrok/ngrok
    else
        echo "Please install ngrok from https://ngrok.com/download"
        exit 1
    fi
fi

# Start Streamlit in background
echo "🎯 Starting Streamlit app..."
streamlit run ui.py --server.port=8501 &
STREAMLIT_PID=$!

# Wait for Streamlit to start
sleep 5

# Start ngrok tunnel
echo "🌐 Creating public tunnel..."
ngrok http 8501 &
NGROK_PID=$!

echo "✅ BookBuddy is now publicly accessible!"
echo "📱 Check the ngrok URL in the terminal above"
echo "🛑 Press Ctrl+C to stop both services"

# Wait for user to stop
wait $STREAMLIT_PID $NGROK_PID