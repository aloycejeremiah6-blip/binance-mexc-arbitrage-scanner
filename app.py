from flask import Flask, jsonify, request, send_from_directory
import requests, os, time, threading

app = Flask(__name__, static_folder='static')
BINANCE = 'https://api.binance.com/api/v3/ticker/bookTicker'
MEXC = 'https://api.mexc.com/api/v3/ticker/bookTicker'
TIMEOUT = 12

def get_json(url):
    r = requests.get(url, timeout=TIMEOUT, headers={'User-Agent':'ArbitrageScanner/1.0'})
    r.raise_for_status()
    return r.json()

def rows_to_map(data):
    if isinstance(data, dict): data = [data]
    out = {}
    for x in data:
        sym = x.get('symbol','')
        try:
            bid, ask = float(x.get('bidPrice', 0)), float(x.get('askPrice', 0))
        except (TypeError, ValueError):
            continue
        if sym.endswith('USDT') and bid > 0 and ask > 0:
            out[sym] = {'bid': bid, 'ask': ask}
    return out

@app.get('/')
def home():
    return send_from_directory('static', 'index.html')

@app.get('/api/scan')
def scan():
    # Fetch both exchanges' best bid/ask. Buy at Binance ask; sell at MEXC bid.
    try:
        b_raw = get_json(BINANCE)
        m_raw = get_json(MEXC)
        b, m = rows_to_map(b_raw), rows_to_map(m_raw)
        common = b.keys() & m.keys()
        buy_fee = max(0, float(request.args.get('buy_fee', '0.001')))
        sell_fee = max(0, float(request.args.get('sell_fee', '0.0005')))
        min_spread = float(request.args.get('min_spread', '0'))
        capital = max(0, float(request.args.get('capital', '100')))
        results = []
        for sym in common:
            buy, sell = b[sym]['ask'], m[sym]['bid']
            if buy <= 0: continue
            gross_pct = (sell / buy - 1) * 100
            net_factor = (sell * (1-sell_fee)) / (buy * (1+buy_fee))
            net_pct = (net_factor - 1) * 100
            qty = capital / (buy * (1+buy_fee)) if capital else 0
            net_profit = qty * sell * (1-sell_fee) - capital if capital else 0
            if gross_pct >= min_spread:
                results.append({'coin':sym[:-4], 'symbol':sym, 'binance_buy':buy, 'mexc_sell':sell,
                                'gross_pct':gross_pct, 'net_pct':net_pct, 'net_profit':net_profit,
                                'buy_qty':qty, 'binance_ask_qty':b[sym]['ask'], 'mexc_bid_qty':m[sym]['bid']})
        results.sort(key=lambda x:x['net_pct'], reverse=True)
        return jsonify({'updated_at': int(time.time()), 'count':len(results), 'capital':capital,
                        'assumptions': {'binance_fee':buy_fee,'mexc_fee':sell_fee,
                                        'note':'Fees are estimates; transfer/network fees, slippage, depth and withdrawal availability are not included.'},
                        'opportunities':results[:250]})
    except requests.RequestException as e:
        return jsonify({'error':f'Could not fetch exchange data: {e}'}), 502
    except Exception as e:
        return jsonify({'error':str(e)}), 500

@app.get('/health')
def health(): return jsonify({'ok':True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT','5000')), debug=False)
