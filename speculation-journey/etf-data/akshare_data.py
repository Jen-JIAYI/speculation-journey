#!/usr/bin/env python3
"""
基于 akshare 的金融数据获取脚本
支持：股票、ETF、期货、期权、宏观数据
"""

import sys
import json
import asyncio
from datetime import datetime

try:
    import akshare as ak
except ImportError:
    print(json.dumps({"error": "akshare 未安装，请运行: pip install akshare"}, ensure_ascii=False))
    sys.exit(1)

def get_stock_realtime(symbol):
    """获取股票/ETF实时行情"""
    try:
        # akshare 获取实时行情
        if symbol.startswith("5") or symbol.startswith("51"):
            # ETF
            df = ak.fund_etf_fund_daily_em(symbol=symbol)
        else:
            # 股票 - 使用实时行情接口
            df = ak.stock_zh_a_spot_em()

        # 查找对应股票
        if not df.empty:
            if symbol.startswith("5") or symbol.startswith("51"):
                # ETF 数据直接返回
                if not df.empty:
                    latest = df.iloc[-1]
                    return {
                        "symbol": symbol,
                        "name": symbol,
                        "current_price": float(latest.get("收盘", 0)),
                        "date": str(latest.get("date", "")),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source": "akshare (东方财富)"
                    }
            else:
                # 股票数据需要筛选
                stock_data = df[df["代码"] == symbol]
                if not stock_data.empty:
                    row = stock_data.iloc[0]
                    current_price = float(row.get("最新价", 0))
                    prev_close = float(row.get("昨收", 0))

                    # 计算涨跌幅
                    change_pct = 0
                    if prev_close > 0:
                        change_pct = (current_price - prev_close) / prev_close * 100

                    return {
                        "symbol": symbol,
                        "name": row.get("名称", ""),
                        "current_price": current_price,
                        "prev_close": prev_close,
                        "open": float(row.get("今开", 0)),
                        "high": float(row.get("最高", 0)),
                        "low": float(row.get("最低", 0)),
                        "volume": float(row.get("成交量", 0)),
                        "amount": float(row.get("成交额", 0)),
                        "change_pct": change_pct,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source": "akshare (东方财富)"
                    }

        return {"error": f"未找到 {symbol} 的数据"}
    except Exception as e:
        return {"error": str(e)}

def get_index_realtime(symbol):
    """获取指数实时行情"""
    try:
        # 常见指数代码映射
        index_map = {
            "000001": "上证指数",
            "399001": "深证成指",
            "399006": "创业板指",
            "000300": "沪深300",
            "000016": "上证50",
            "000905": "中证500",
        }

        df = ak.stock_zh_index_spot_em()
        if not df.empty:
            index_data = df[df["代码"] == symbol]
            if not index_data.empty:
                row = index_data.iloc[0]
                current_price = float(row.get("最新价", 0))
                prev_close = float(row.get("昨收", 0))
                change_pct = (current_price - prev_close) / prev_close * 100 if prev_close > 0 else 0

                return {
                    "symbol": symbol,
                    "name": row.get("名称", index_map.get(symbol, "")),
                    "current_price": current_price,
                    "prev_close": prev_close,
                    "change_pct": change_pct,
                    "high": float(row.get("最高", 0)),
                    "low": float(row.get("最低", 0)),
                    "volume": float(row.get("成交量", 0)),
                    "amount": float(row.get("成交额", 0)),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": "akshare (东方财富)"
                }
        return {"error": f"未找到指数 {symbol}"}
    except Exception as e:
        return {"error": str(e)}

def get_futures_realtime(symbol):
    """获取期货实时行情"""
    try:
        # 获取期货实时行情
        df = ak.futures_zh_spot()
        if not df.empty:
            futures_data = df[df["symbol"] == symbol]
            if not futures_data.empty:
                row = futures_data.iloc[0]
                return {
                    "symbol": symbol,
                    "name": row.get("name", ""),
                    "current_price": float(row.get("last_price", 0)),
                    "open": float(row.get("open", 0)),
                    "high": float(row.get("high", 0)),
                    "low": float(row.get("low", 0)),
                    "volume": float(row.get("volume", 0)),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": "akshare (新浪期货)"
                }
        return {"error": f"未找到期货 {symbol}"}
    except Exception as e:
        return {"error": str(e)}

def get_etf_options_chain(underlying):
    """获取ETF期权链"""
    try:
        # 50ETF 期权
        if underlying == "510050" or underlying == "50ETF":
            df = ak.option_sina_sse_list(symbol="IOE")
        # 300ETF 期权
        elif underlying == "510300" or underlying == "300ETF":
            df = ak.option_sina_sse_list(symbol="IOE")
        else:
            return {"error": f"暂不支持 {underlying} 的期权数据"}

        if df is not None and not df.empty:
            return {
                "underlying": underlying,
                "count": len(df),
                "contracts": df.head(20).to_dict("records"),  # 返回前20个合约
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "akshare (新浪期权)"
            }
        return {"error": "未获取到期权数据"}
    except Exception as e:
        return {"error": str(e)}

def get_macro_data(indicator="GDP"):
    """获取宏观数据"""
    try:
        if indicator == "GDP":
            df = ak.macro_china_gdp()
        elif indicator == "CPI":
            df = ak.macro_china_cpi()
        elif indicator == "PMI":
            df = ak.macro_china_pmi()
        else:
            return {"error": f"暂不支持 {indicator}，支持: GDP, CPI, PMI"}

        if df is not None and not df.empty:
            latest = df.iloc[-1]
            return {
                "indicator": indicator,
                "date": str(latest.iloc[0]) if len(latest) > 0 else "",
                "value": latest.iloc[-1] if len(latest) > 1 else 0,
                "data": df.tail(5).to_dict("records"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "akshare (国家统计局)"
            }
        return {"error": f"未获取到 {indicator} 数据"}
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python akshare_data.py <type> <symbol>",
            "examples": [
                "python akshare_data.py stock 600519",
                "python akshare_data.py index 000001",
                "python akshare_data.py futures RB0",
                "python akshare_data.py options 510050",
                "python akshare_data.py macro GDP"
            ]
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    data_type = sys.argv[1].lower()
    symbol = sys.argv[2] if len(sys.argv) > 2 else ""

    if data_type == "stock":
        result = get_stock_realtime(symbol)
    elif data_type == "index":
        result = get_index_realtime(symbol)
    elif data_type == "futures":
        result = get_futures_realtime(symbol)
    elif data_type == "options":
        result = get_etf_options_chain(symbol)
    elif data_type == "macro":
        result = get_macro_data(symbol)
    else:
        result = {"error": f"未知类型: {data_type}，支持: stock, index, futures, options, macro"}

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
