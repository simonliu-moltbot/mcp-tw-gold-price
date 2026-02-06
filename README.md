# Taiwan Gold Price MCP Server (mcp-tw-gold-price)

A Model Context Protocol (MCP) server that provides real-time Gold Passbook rates (TWD) from the **Bank of Taiwan**.

## 🌟 Features
- **Real-time Rates**: Fetches Buying and Selling prices for 1 Gram of gold.
- **Value Calculator**: Calculates the total value of your gold holdings based on current rates.
- **Reliable Source**: Data directly from Bank of Taiwan (rate.bot.com.tw).

## 🛠 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/simonliu-moltbot/mcp-tw-gold-price.git
    cd mcp-tw-gold-price
    ```

2.  **Create a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

### Claude Desktop
Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tw-gold": {
      "command": "/absolute/path/to/mcp-tw-gold-price/.venv/bin/python",
      "args": ["/absolute/path/to/mcp-tw-gold-price/src/server.py"]
    }
  }
}
```

### 🛠 Dive Configuration
- **Type**: `stdio`
- **Command**: `/absolute/path/to/mcp-tw-gold-price/.venv/bin/python`
- **Args**: `/absolute/path/to/mcp-tw-gold-price/src/server.py`

## 📦 Tools

### `get_gold_passbook_twd`
Get current Gold Passbook buying and selling prices in TWD from Bank of Taiwan.
- **Returns**: JSON object with unit, currency, selling_price, buying_price, timestamp.

### `calculate_gold_value`
Calculate the total value of gold in TWD based on weight (grams).
- **Arguments**:
    - `grams` (number): Weight of gold in grams.
    - `rate_type` (string): 'buying' (Bank buys from you) or 'selling' (Bank sells to you). Default: 'buying'.

## 📜 License
MIT
