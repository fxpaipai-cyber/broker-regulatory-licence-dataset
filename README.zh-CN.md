# 全球交易商监管授权与牌照数据集

交易商排排网（PAIPAI RANKING）发布的公开数据集：全球外汇差价合约、贵金属现货、
证券与期货经纪、加密资产交易商的**监管授权与牌照记录**。每一条牌照记录都是
「监管机构 + 持牌法人实体 + 牌照编号 + 层级」四元组，均可回到签发机构的公开注册表复核。

- 数据快照：2026-11-22
- 站点：https://paipaifx.com/open-data.html
- 许可：CC BY 4.0（署名 + 回链即可商用）
- 规模：机构 2,392 · 牌照记录 2,066 · 监管机构×辖区 86

## 文件

| 文件 | 行数 | 说明 |
|---|---|---|
| `data/brokers.csv` | 2,392 | 机构主表：名称、法人实体、总部、品类、层级、六维分、授权数与辖区 |
| `data/licences.csv` | 2,066 | 牌照记录：机构 × 监管机构 × 辖区 × 标识类型 × 编号（是 2,519 条授权的子集） |
| `data/regulators.csv` | 86 | 监管机构聚合：按（机构代码，辖区）统计家数与层级分布，三档合计 2,519 条授权 |
| `data/brokers.json` | 2,392 | 同内容 JSON 版，含 `meta` 块 |
| `FIELD_DICT.md` | — | 完整字段字典（中英对照） |

## 快速开始

```python
import pandas as pd

brokers = pd.read_csv("data/brokers.csv", encoding="utf-8-sig")
licences = pd.read_csv("data/licences.csv", encoding="utf-8-sig")

# 香港证监会持牌法团
sfc = licences[(licences.regulator_code == "SFC") & licences.licence_ref.notna()]
print(sfc[["broker_name", "legal_entity", "licence_kind", "licence_ref"]].head())
```

> **编码说明**：CSV 为 UTF-8 **带 BOM**（Excel 双击不乱码）。程序读取请用
> `encoding="utf-8-sig"`；若用纯 `utf-8`，第一列列名会带一个不可见的 `\ufeff`。

## 使用注意（下结论前务必读）

1. **`licence_count = 0` 不代表该机构无牌照**，只表示本数据集未采集到可核验授权：
   2,392 家机构中有 390 家处于该状态。请勿据此发布「某平台无牌照」的结论。
2. **两个 `verified` 列含义不同**。`licences.csv` 中标记单条牌照记录（1 条尚未
   逐条核对）；`brokers.csv` 中标记整家机构（134 家尚未完成全部核对）。
   这是数据快照，不是法律意见。
3. **`skipped_dims`** 列出「未采集」维度（如 `prod|plat`）。这些维度**不参与加权**，
   其权重按比例回补给其余维度，**不是记 0 分**。复算综合分时必须跳过。
4. **`licence_kind = LEI` 不是牌照号**。LEI 是 GLEIF 签发的法人机构识别码，
   标识主体身份而非授权状态，请勿并入牌照号统计。
5. **层级是本站的编辑标记**，不是法定分类。`T3` 不等于该机构不受监管，
   只表示其授权所在辖区对零售投资者的保护规则较弱。
6. **监管机构代码已归一**。源表中短码与全称并存（`CySEC` 与塞浦路斯证监会全称、
   `BaFin` 与德国联邦金融监管局全称）；跨辖区共用的代码带辖区后缀
   （`FMA` = 新西兰、`FMA-AT` = 奥地利、`FMA-LI` = 列支敦士登）。
   `regulator_code_raw` 保留原始写法以便追溯。
7. **`licences.csv` 行数不等于 `regulators.csv` 的授权数**。`regulators.csv` 三档层级
   合计为 **2,519 条授权条目**（机构×监管机构），而 `licences.csv` 是
   **2,066 行**。差额 453 条是「注册表确认持牌、但未给出独立编号」
   的授权，因此没有对应的逐条明细行。两张表不按行一一对应：
   要数量看 `regulators.csv`，要编号看 `licences.csv`。

## 许可与署名

以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 发布。可商用、可再分发，需署名并回链。署名格式：

> 数据来源：交易商排排网（PAIPAI RANKING），https://paipaifx.com/open-data.html，许可协议 CC BY 4.0。

任何公开使用只要带有指向首页的可见超链接，即满足署名要求。请勿将本数据集
另行打包成竞品下载，而不注明本仓库为原始来源。

## 联系

欢迎纠错：错误的牌照号比没有牌照号更糟。请提 issue，或发邮件到 fxpaipai@gmail.com，
附上机构名、监管机构和你在看的注册表链接。
