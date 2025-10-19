#!/bin/bash
# Installation script for Broken Link Checker MCP Server

echo "🔧 Installing Broken Link Checker MCP Server..."

# Navigate to Documents directory
cd ~/Documents || exit 1

# Clone the repository
echo "📦 Cloning repository..."
git clone https://github.com/davinoishi/broken-link-checker-mcp.git

# Install dependencies
echo "📥 Installing dependencies..."
cd broken-link-checker-mcp || exit 1
npm install

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Add this to your Cline MCP settings:"
echo ""
echo '{
  "broken-link-checker": {
    "command": "node",
    "args": ["/Users/infiniteintelligence/Documents/broken-link-checker-mcp/index.js"],
    "disabled": false,
    "autoApprove": []
  }
}'
echo ""
echo "2. Restart VSCode"
echo "3. The broken-link-checker tools will then be available!"
