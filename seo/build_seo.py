#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO/GEO build for AI 泡沫检测仪. Run from the repo root: python seo/build_seo.py

This one is a single deep report, not a list. Splitting it into fragment pages would
only create thin URLs competing with each other, so it keeps one canonical page and
gets what a long report actually needs: correct canonical, Article + FAQPage schema
built from its own section headings, and the whole text in llms-full.txt where an
answer engine can read and cite it.
"""
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo_kit as G

SITE = G.Site(
    path="ai-bubble-detector",
    name="AI Bubble Monitor", name_zh="AI 泡沫检测仪",
    tagline="20 falsifiable red lines on the AI build-out, checked against live numbers",
    tagline_zh="20 条红线实时监测 AI 基建泡沫，环境 / 结构 / 引爆三级判定",
    description=(
        "A falsifiable monitor of the AI infrastructure build-out: twenty named red lines, "
        "each with a threshold written down in advance, graded into environment risk, "
        "structural fragility and detonation. It states what would prove it wrong, keeps a "
        "public log of every time it changed its mind, and lists the blind spots it knows "
        "it has. It is a monitor, not investment advice."),
    description_zh=(
        "一份可证伪的 AI 基建泡沫监测：20 条具名红线，每条的阈值都事先写死，分成"
        "「环境风险 / 结构脆弱 / 引爆事件」三级判定。它写明自己什么情况下算错、"
        "公开记录每一次改口、并列出自己已知的盲点。这是一份监测表，不是投资建议。"),
    keywords=("AI 泡沫, AI 基建 泡沫, 英伟达 需求, 数据中心 资本开支, 算力 过剩, 甲骨文 债务, "
              "AI capex bubble, AI infrastructure bubble indicators, circular financing"),
    item_type="Article", item_noun="report", item_noun_zh="报告",
    lang="zh-Hans", changefreq="daily",
)

HOW = ("Thresholds are written down before the data arrives, so each line can only be broken "
       "or not broken. Numbers come from public filings, exchange data and vendor disclosures, "
       "refreshed automatically into data/auto.json; every revision is logged in public, "
       "including the ones where the author was wrong.")

CITE = ("Cite this page with the date — the grading changes as lines break and un-break. "
        "Attribute to \"AI 泡沫检测仪 / AI Bubble Monitor (OurWord AI)\". "
        "It is a falsifiable monitor, not investment advice.")


def updated_at():
    try:
        d = json.load(open("data/auto.json", encoding="utf-8"))
        return str(d.get("updated_at") or "")[:10]
    except Exception:
        return datetime.date.today().isoformat()


def main():
    today = datetime.date.today().isoformat()
    up = updated_at() or today
    secs = G.sections_from_html("index.html", min_chars=240)

    doc = G.Item(slug="ai-bubble-detector", title=SITE.name, summary=SITE.description,
                 blocks=secs, title_zh=SITE.name_zh, summary_zh=SITE.description_zh,
                 blocks_zh=secs, updated=up, url_override=SITE.base,
                 source_url="https://github.com/ourword-ai/ai-bubble-detector")

    ld = [G.article_ld(SITE, SITE.base, SITE.name_zh + " — " + SITE.tagline_zh,
                       SITE.description_zh, secs, zh=True, updated=up)]
    f = G.faq_ld(doc, True)
    if f:
        ld.append(f)

    rep = G.build(SITE, [doc], root=".", today=today, how_built=HOW, cite_as=CITE,
                  item_pages=False, extra_ld=ld,
                  extra_urls=["https://ourword.ai/ai-bubble-detector/monitor.html"],
                  extra_sitemaps=["https://ourword.ai/sitemap.xml"])
    rep["sections"] = len(secs)
    print("ai-bubble-detector seo/geo:", json.dumps(rep, ensure_ascii=False))
    return rep


if __name__ == "__main__":
    main()
