BINANCE x MEXC ARBITRAGE SCANNER (STARTER)

WHAT IT DOES
- Reads public Binance and MEXC spot order-book top prices for USDT pairs.
- Calculates buy at Binance ASK and sell at MEXC BID.
- Estimates net spread after the fee percentages entered in the web page.
- Refreshes every 30 seconds.
- No exchange API keys required; it does not place trades.

RUN ON WINDOWS / MAC / LINUX
1. Install Python 3.10+.
2. Extract this folder.
3. Open terminal/command prompt inside the folder.
4. Run: python -m pip install -r requirements.txt
5. Run: python app.py
6. Open http://127.0.0.1:5000 in your browser.

RUN ON ANDROID
Use a Python environment that supports Flask (for example Termux), install Python,
then run the same pip install and python app.py commands. Open http://127.0.0.1:5000
in the phone browser. Keep the terminal session running.

IMPORTANT LIMITATIONS
- This is a starter web scanner, not a hosted public website and not a Telegram bot yet.
- Public exchange endpoints may rate-limit, change, or be inaccessible from some networks.
- The code compares only USDT spot pairs common to both exchanges.
- The displayed profit is an estimate, not guaranteed executable profit.
- It excludes withdrawal/network fees, deposit/withdrawal availability, order-book depth,
  slippage, minimum order sizes, token/network mismatches, and price movement during transfer.
- Before transferring, verify the same asset and supported network on both exchanges.
- Never share exchange passwords, API secrets, or seed phrases. Do not enable withdrawals
  on API keys for a scanner. This version does not need API keys.
