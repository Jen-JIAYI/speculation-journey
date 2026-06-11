#!/usr/bin/env python3
"""
ETF期权数据获取脚本
可通过 Bash 工具调用来获取实时数据
"""

import sys
import json
import urllib.request
from datetime import datetime

def fetch_etf_quote(symbol):
    """从腾讯财经获取ETF实时行情"""
    try:
        prefix = "sh" if symbol.startswith("5") or symbol.startswith("6") else "sz"
        url = f"http://qt.gtimg.cn/q={prefix}{symbol}"

        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('gbk', errors='ignore')

            if content and '~' in content:
                data = content.strip().split('"')[1].split('~')
                if len(data) > 30:
                    result = {
                        "symbol": symbol,
                        "name": data[1],
                        "current_price": float(data[3]) if data[3] else 0,
                        "prev_close": float(data[4]) if data[4] else 0,
                        "open": float(data[5]) if data[5] else 0,
                        "high": float(data[6]) if data[6] else 0,
                        "low": float(data[7]) if data[7] else 0,
                        "volume": float(data[9]) if data[9] else 0,
                        "amount": float(data[10]) if data[10] else 0,
                        "change_pct": float(data[32]) if len(data) > 32 and data[32] else 0,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    # 简单技术分析
                    price = result["current_price"]
                    prev = result["prev_close"]
                    if prev > 0:
                        change_pct = (price - prev) / prev * 100
                        if change_pct > 1:
                            result["trend_signal"] = "强势上涨 🔼"
                        elif change_pct > 0.3:
                            result["trend_signal"] = "温和上涨 ↗️"
                        elif change_pct < -1:
                            result["trend_signal"] = "强势下跌 🔽"
                        elif change_pct < -0.3:
                            result["trend_signal"] = "温和下跌 ↘️"
                        else:
                            result["trend_signal"] = "震荡 ↔️"

                    return json.dumps(result, ensure_ascii=False, indent=2)

        return json.dumps({"error": "无法解析数据"}, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)

def fetch_qvix():
    """从期权论坛获取QVIX波动率指数"""
    try:
        url = "https://1.optbbs.com/d/csv/d/k.csv"

        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )

        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8', errors='ignore')
            lines = content.strip().split('\n')
            if lines:
                parts = lines[0].split(',')
                if len(parts) >= 2:
                    try:
                        qvix_value = float(parts[1])
                        result = {
                            "qvix": qvix_value,
                            "date": parts[0] if parts[0] else datetime.now().strftime("%Y-%m-%d"),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "source": "期权论坛 (optbbs.com)"
                        }

                        # 波动率环境判断
                        if qvix_value > 25:
                            result["environment"] = "高波动环境 ⚠️"
                        elif qvix_value > 18:
                            result["environment"] = "中等波动"
                        elif qvix_value > 12:
                            result["environment"] = "低波动环境"
                        else:
                            result["environment"] = "极低波动 😴"

                        return json.dumps(result, ensure_ascii=False, indent=2)
                    except ValueError:
                        pass

        return json.dumps({"error": "无法解析QVIX数据"}, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python fetch_etf_quote.py <symbol>|qvix"}, ensure_ascii=False))
        sys.exit(1)

    arg = sys.argv[1]

    if arg.lower() == "qvix":
        print(fetch_qvix())
    else:
        print(fetch_etf_quote(arg))
