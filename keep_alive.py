"""
Keep-alive server module for hosting Discord bots.
This creates a simple HTTP server that can be pinged to keep the bot alive
when deployed on platforms like Replit, Heroku, or similar hosting services.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

class KeepAliveHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler for keep-alive pings."""
    
    def do_GET(self):
        """Handle GET requests."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Simple HTML response
        uptime = format_uptime()
        last_ping = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        
        html_response = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Doro Bot Status</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #2c3e50;
                    color: white;
                    text-align: center;
                    padding: 50px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .status {{
                    background-color: #27ae60;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                }}
                .doro-text {{
                    font-size: 24px;
                    color: #f39c12;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Doro Bot Status</h1>
                <div class="status">
                    <h2>✅ Bot is Running!</h2>
                    <p>The Doro Discord bot is currently active and responding.</p>
                </div>
                <div class="doro-text">
                    <p>DORO DORO DORO! 🎵</p>
                </div>
                <p><strong>Uptime:</strong> {uptime}</p>
                <p><strong>Last Ping:</strong> {last_ping}</p>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(html_response.encode())
    
    def do_POST(self):
        """Handle POST requests."""
        self.do_GET()
    
    def log_message(self, format, *args):
        """Override to suppress default HTTP server logging."""
        # Print minimal logging
        print(f"Keep-alive ping received at {time.strftime('%H:%M:%S')}")

# Global variable to track start time
start_time = time.time()

def format_uptime():
    """Format uptime in a human-readable way."""
    uptime_seconds = int(time.time() - start_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def run_server():
    """Run the HTTP server in a separate thread."""
    try:
        server = HTTPServer(('0.0.0.0', 5000), KeepAliveHandler)
        print("🌐 Keep-alive server started on http://0.0.0.0:5000")
        print("📡 Server is ready to receive keep-alive pings")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Error starting keep-alive server: {e}")

def keep_alive():
    """
    Start the keep-alive server in a background thread.
    This function should be called before starting the Discord bot.
    """
    print("🚀 Starting keep-alive server...")
    
    # Create and start the server thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Give the server a moment to start
    time.sleep(1)
    
    print("✅ Keep-alive server is running in background")
    print("🔗 Access the status page at: http://localhost:5000")
    
    return server_thread

if __name__ == "__main__":
    # If run directly, start the server and keep it running
    print("🎯 Running keep-alive server in standalone mode")
    keep_alive()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(60)
            print(f"⏰ Keep-alive server uptime: {format_uptime()}")
    except KeyboardInterrupt:
        print("\n🛑 Shutting down keep-alive server...")
