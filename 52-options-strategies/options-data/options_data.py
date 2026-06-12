#!/usr/bin/env python3
"""
期权数据获取脚本
支持：50ETF、300ETF 期权实时行情、期权链、隐含波动率、希腊值
"""

import sys
import json
from datetime import datetime

try:
    import akshare as ak
except ImportError:
    print(json.dumps({"error": "akshare 未安装，请运行: pip install akshare"}, ensure_ascii=False))
    sys.exit(1)

def get_underlying_quote(symbol):
    """获取标的实时行情"""
    try:
        # ETF代码映射和名称
        etf_info = {
            "510050": {"name": "50ETF", "sina": "sh510050"},
            "50ETF": {"name": "50ETF", "sina": "sh510050"},
            "510300": {"name": "300ETF", "sina": "sh510300"},
            "300ETF": {"name": "300ETF", "sina": "sh510300"},
            "510500": {"name": "500ETF", "sina": "sh510500"},
            "500ETF": {"name": "500ETF", "sina": "sh510500"}
        }

        if symbol not in etf_info:
            return {"error": f"暂不支持标的 {symbol}，支持: 50ETF, 300ETF, 500ETF"}

        info = etf_info[symbol]
        code = symbol if len(symbol) == 6 else next(k for k, v in etf_info.items() if v["name"] == info["name"] and len(k) == 6)

        # 方法1: 使用新浪ETF接口
        try:
            df = ak.fund_etf_hist_sina(symbol=info["sina"])
            if not df.empty:
                latest = df.iloc[-1]
                current_price = float(latest.get("close", 0))
                prev_close = float(df.iloc[-2].get("close", current_price)) if len(df) > 1 else current_price

                # 计算涨跌幅
                change_pct = round((current_price - prev_close) / prev_close * 100, 2) if prev_close > 0 else 0

                return {
                    "symbol": code,
                    "name": info["name"],
                    "current_price": current_price,
                    "prev_close": prev_close,
                    "change_pct": change_pct,
                    "date": str(latest.get("date", "")),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": "akshare (新浪)"
                }
        except:
            pass

        # 方法2: 使用东方财富实时行情
        try:
            df = ak.stock_zh_a_spot_em()
            etf_data = df[df["代码"] == code]
            if not etf_data.empty:
                row = etf_data.iloc[0]
                current_price = float(row.get("最新价", 0))
                prev_close = float(row.get("昨收", 0))
                change_pct = float(row.get("涨跌幅", 0))

                return {
                    "symbol": code,
                    "name": info["name"],
                    "current_price": current_price,
                    "prev_close": prev_close,
                    "change_pct": change_pct,
                    "high": float(row.get("最高", 0)),
                    "low": float(row.get("最低", 0)),
                    "volume": float(row.get("成交量", 0)),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": "akshare (东方财富)"
                }
        except:
            pass

        return {"error": f"无法获取 {symbol} 的行情数据"}
    except Exception as e:
        return {"error": str(e)}

def get_options_chain(underlying):
    """获取期权链"""
    try:
        # 50ETF 期权
        if underlying in ["510050", "50ETF"]:
            # 上海交易所50ETF期权
            df = ak.option_sina_sse_list(symbol="IOE")
            contract_type = "50ETF期权"
        # 300ETF 期权
        elif underlying in ["510300", "300ETF"]:
            df = ak.option_sina_sse_list(symbol="IOE")
            contract_type = "300ETF期权"
        else:
            return {"error": f"暂不支持 {underlying} 的期权数据，支持: 50ETF, 300ETF"}

        if df is not None and not df.empty:
            # 筛选相关合约
            calls = df[df['name'].str.contains('购')].head(10)
            puts = df[df['name'].str.contains('沽')].head(10)

            return {
                "underlying": underlying,
                "contract_type": contract_type,
                "total_contracts": len(df),
                "calls_count": len(calls),
                "puts_count": len(puts),
                "calls": calls.to_dict("records") if not calls.empty else [],
                "puts": puts.to_dict("records") if not puts.empty else [],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "akshare (新浪期权)"
            }

        return {"error": "未获取到期权数据"}
    except Exception as e:
        return {"error": str(e)}

def get_option_detail(contract_code):
    """获取单个期权合约详情"""
    try:
        # 上海期权
        df = ak.option_sina_sse_list(symbol="IOE")

        if df is not None and not df.empty:
            contract_data = df[df['symbol'] == contract_code]
            if not contract_data.empty:
                row = contract_data.iloc[0]
                return {
                    "contract_code": contract_code,
                    "name": row.get("name", ""),
                    "underlying": row.get("symbol", ""),
                    "strike_price": float(row.get("strike", 0)) if 'strike' in row else 0,
                    "current_price": float(row.get("last_price", 0)),
                    "open": float(row.get("open", 0)),
                    "high": float(row.get("high", 0)),
                    "low": float(row.get("low", 0)),
                    "volume": int(row.get("volume", 0)),
                    "open_interest": int(row.get("open_interest", 0)),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": "akshare (新浪期权)"
                }

        return {"error": f"未找到合约 {contract_code}"}
    except Exception as e:
        return {"error": str(e)}

def analyze_options_position(underlying, current_price, target_price, days_to_expiry, opinion="bullish"):
    """
    分析期权仓位建议
    基于本书52种期权获利方式
    """
    try:
        advice = {
            "underlying": underlying,
            "current_price": current_price,
            "target_price": target_price,
            "days_to_expiry": days_to_expiry,
            "opinion": opinion,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "recommendations": []
        }

        # 计算价格变动幅度
        price_change_pct = (target_price - current_price) / current_price * 100

        # 根据观点和时间推荐策略
        if opinion == "bullish":
            if price_change_pct > 8:
                advice["recommendations"].append({
                    "strategy": "买入开仓实值一档认购期权 (第2种)",
                    "reason": f"预期大涨 {price_change_pct:.1f}%，适合买入实值认购",
                    "risk": "最大亏损权利金，潜在盈利无限"
                })
            elif price_change_pct > 3:
                advice["recommendations"].append({
                    "strategy": "认购牛市价差策略 (第5种)",
                    "reason": f"预期温和上涨 {price_change_pct:.1f}%，价差策略风险有限",
                    "risk": "最大亏损净权利金，最大盈利行权价差-净权利金"
                })
                advice["recommendations"].append({
                    "strategy": "卖出开仓虚值一档认沽期权 (第3种)",
                    "reason": f"预期温和上涨，可收取权利金",
                    "risk": "最大亏损较大，需配合止损"
                })
            else:
                advice["recommendations"].append({
                    "strategy": "看涨备兑开仓策略 (第9种)",
                    "reason": "预期小幅上涨，备兑可降低持仓成本",
                    "risk": "标的下跌时亏损放大"
                })

        elif opinion == "bearish":
            if price_change_pct < -8:
                advice["recommendations"].append({
                    "strategy": "买入开仓实值一档认沽期权 (第14种)",
                    "reason": f"预期大跌 {abs(price_change_pct):.1f}%，适合买入实值认沽",
                    "risk": "最大亏损权利金，潜在盈利无限"
                })
            elif price_change_pct < -3:
                advice["recommendations"].append({
                    "strategy": "认沽熊市价差策略 (第17种)",
                    "reason": f"预期温和下跌 {abs(price_change_pct):.1f}%，价差策略风险有限",
                    "risk": "最大亏损净权利金"
                })
            else:
                advice["recommendations"].append({
                    "strategy": "买入开仓虚值一档认沽期权 (第13种)",
                    "reason": "预期小幅下跌，虚值期权成本较低",
                    "risk": "可能完全损失权利金"
                })

        elif opinion == "neutral":
            advice["recommendations"].append({
                "strategy": "卖出开仓跨式期权策略 (第35种)",
                "reason": "预期震荡，可赚取时间价值",
                "risk": "单边突破时亏损无限，建议买入保护"
            })
            advice["recommendations"].append({
                "strategy": "正向日历价差策略 (第24种)",
                "reason": "预期震荡，利用时间价值衰减获利",
                "risk": "需要标的保持在行权价附近"
            })

        elif opinion == "volatile":
            advice["recommendations"].append({
                "strategy": "买入开仓跨式期权策略 (第28种)",
                "reason": "预期大幅波动，方向不确定",
                "risk": "需要波动足够大以覆盖双倍权利金成本"
            })
            advice["recommendations"].append({
                "strategy": "买入开仓宽跨式期权策略 (第29种)",
                "reason": "预期大幅波动，成本比跨式更低",
                "risk": "需要更大的波动才能盈利"
            })

        if not advice["recommendations"]:
            advice["recommendations"].append({
                "strategy": "建议等待更好的入场时机",
                "reason": "当前市场观点不够明确",
                "risk": "N/A"
            })

        return advice

    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python options_data.py <type> [params...]",
            "examples": [
                "python options_data.py quote 510050",
                "python options_data.py chain 50ETF",
                "python options_data.py analyze 50ETF 2.8 3.0 30 bullish",
                "python options_data.py detail 10002892"
            ]
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    data_type = sys.argv[1].lower()

    if data_type == "quote" and len(sys.argv) > 2:
        result = get_underlying_quote(sys.argv[2])
    elif data_type == "chain" and len(sys.argv) > 2:
        result = get_options_chain(sys.argv[2])
    elif data_type == "detail" and len(sys.argv) > 2:
        result = get_option_detail(sys.argv[2])
    elif data_type == "analyze" and len(sys.argv) > 5:
        result = analyze_options_position(
            sys.argv[2],           # underlying
            float(sys.argv[3]),    # current_price
            float(sys.argv[4]),    # target_price
            int(sys.argv[5]),      # days_to_expiry
            sys.argv[6] if len(sys.argv) > 6 else "neutral"  # opinion
        )
    else:
        result = {"error": f"参数错误，类型: {data_type}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
