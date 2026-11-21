#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""复算综合分（reference implementation）。

这个脚本存在的意义是**防止误读**：`skipped_dims` 列出的维度是「未采集」，
不计加权、权重按比例回补其余维度，不是记 0 分。忽略这一点复算出来的分数
会系统性偏低，而且在 1851 家只采集了部分维度的机构上偏差非常大。

用法：
    python scripts/recompute_score.py                      # 用 data/brokers.csv
    python scripts/recompute_score.py path/to/brokers.csv
"""
import csv
import sys

WEIGHTS = [35, 20, 20, 10, 8, 7]                     # reg, breadth, prod, plat, type, src
DIMS = ['reg', 'breadth', 'prod', 'plat', 'type', 'source']


def total(scores, skipped):
    """按 build_data 的口径还原综合分：跳过未采集维度，权重归一化。"""
    num = 0.0
    den = 0.0
    for w, dim, sc in zip(WEIGHTS, DIMS, scores):
        if dim in skipped or sc is None:
            continue
        num += w * sc
        den += w
    return None if den == 0 else round(num / den, 2)


def main(path='data/brokers.csv'):
    with open(path, encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    bad = 0
    for r in rows:
        skipped = [s for s in (r['skipped_dims'] or '').split('|') if s]
        scores = [float(r['score_' + d]) if r['score_' + d] else None
                  for d in ['reg', 'breadth', 'prod', 'platform', 'type', 'source']]
        got = total(scores, skipped)
        want = float(r['score_total']) if r['score_total'] else None
        if got is None or want is None or abs(got - want) > 0.02:
            bad += 1
            if bad <= 5:
                print('  差异 %-28s 复算=%s 原文=%s 跳过=%s' % (r['slug'], got, want, skipped))
    print('共 %d 行，复算不一致 %d 行' % (len(rows), bad))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:2]))
