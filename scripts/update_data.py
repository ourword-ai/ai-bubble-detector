#!/usr/bin/env python3
"""抓取 FRED 官方序列，写 data/auto.json。

仅覆盖有官方 API 的两条：核心 PCE 同比（PCEPILFE）、单 A 公司债 OAS 参考（BAMLC0A3CA）。
其余指标按页面「手抄清单」人工维护。纯 stdlib，无依赖。
"""
import csv, io, json, sys, urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "auto.json"
UA = {"User-Agent": "ai-bubble-detector-auto-data (github.com/ourword-ai/ai-bubble-detector)"}


def fred(series_id: str, days_back: int):
    cosd = (date.today() - timedelta(days=days_back)).isoformat()
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={cosd}"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode("utf-8")
    rows = []
    for row in csv.reader(io.StringIO(text)):
        if len(row) >= 2 and row[0][:1].isdigit() and row[1] not in (".", ""):
            try:
                rows.append((row[0], float(row[1])))
            except ValueError:
                pass
    if not rows:
        raise RuntimeError(f"no data for {series_id}")
    return rows


def main() -> int:
    series = {}

    # 核心 PCE 同比：月度指数，最新月 vs 12 个月前同月
    pce = fred("PCEPILFE", 430)
    latest_d, latest_v = pce[-1]
    base = dict(pce).get(f"{int(latest_d[:4]) - 1}{latest_d[4:]}")
    if base:
        series["pce_yoy"] = {
            "value": round((latest_v / base - 1) * 100, 1), "unit": "%",
            "asof": latest_d, "source": "FRED PCEPILFE (YoY)",
        }

    # 单 A 公司债 OAS（全体口径，仅参考）：FRED 给百分比 → bp
    d, v = fred("BAMLC0A3CA", 45)[-1]
    series["a_oas"] = {"value": round(v * 100), "unit": "bp", "asof": d, "source": "FRED BAMLC0A3CA"}

    old = {}
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text())
        except Exception:
            old = {}
    if old.get("series") == series:
        print("UNCHANGED")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "series": series,
        "note": "GitHub Actions 自动写入；仅官方 API 序列，其余指标见页面手抄清单。",
    }, ensure_ascii=False, indent=2) + "\n")
    print("CHANGED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
