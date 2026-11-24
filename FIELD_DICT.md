# 字段字典 / Field dictionary

数据集：全球交易商监管授权与牌照数据集
快照：2026-11-22

`data/*.csv` 均为 UTF-8 with BOM。程序读取请用 `utf-8-sig`。


## brokers.csv — 机构主表

| 字段 / Field | 类型 / Type | 说明 | Description |
|---|---|---|---|
| `slug` | string | 站内唯一标识（URL 片段） | Stable slug used in profile URLs |
| `name` | string | 机构常用名称 | Common brand name |
| `legal_entity` | string | 法人实体名称（注册表口径） | Legal entity as registered |
| `headquarters` | string | 总部所在地 | Headquarters location |
| `category` | string | 品类：外汇差价合约/贵金属现货/证券与期货经纪/加密资产交易商 | Category: FX CFD / precious metals spot / securities & futures / crypto |
| `tier` | string | 层级标记 | Tier label |
| `score_total` | number | 综合分（百分制） | Composite score, 0-100 |
| `score_grade` | string | 综合评级 | Grade derived from score_total |
| `score_reg` | number | 监管维度分（权重 35） | Regulatory dimension (weight 35) |
| `score_breadth` | number | 授权广度维度分（权重 20） | Licence breadth (weight 20) |
| `score_prod` | number | 产品维度分（权重 20） | Product dimension (weight 20) |
| `score_platform` | number | 平台维度分（权重 10） | Platform dimension (weight 10) |
| `score_type` | number | 类型维度分（权重 8） | Business type dimension (weight 8) |
| `score_source` | number | 来源可核验度（权重 7） | Source verifiability (weight 7) |
| `skipped_dims` | string | 未采集维度，竖线分隔；**不计加权，分母扣减** | Dimensions not collected, pipe-separated; excluded from weighting |
| `licence_count` | integer | 采集到的授权条目数（0 不代表无牌照） | Licence records collected (0 does NOT mean unlicensed) |
| `regulator_count` | integer | 去重监管机构数 | Distinct regulators |
| `regions` | string | 辖区列表，竖线分隔 | Regions, pipe-separated |
| `platforms` | string | 交易平台列表，竖线分隔 | Trading platforms, pipe-separated |
| `has_conditions` | boolean | 是否有交易条件记录 | Trading conditions recorded |
| `verified` | boolean | 是否已在官方注册表逐条核对 | Verified against official registers |
| `source` | string | 该机构数据的来源说明 | Provenance note |
| `profile_url` | string | 站内详情页绝对地址 | Absolute URL of profile page |

## licences.csv — 牌照记录

| 字段 / Field | 类型 / Type | 说明 | Description |
|---|---|---|---|
| `broker_slug` | string | 关联 brokers.csv 的 slug | Foreign key to brokers.slug |
| `broker_name` | string | 机构常用名称 | Brand name |
| `legal_entity` | string | 持牌法人实体 | Licensed legal entity |
| `regulator_code` | string | 监管机构代码（已归一，跨辖区带后缀如 FMA-AT） | Normalised regulator code (region suffix when shared, e.g. FMA-AT) |
| `regulator_code_raw` | string | 源表中的原始写法 | Raw code as found in source |
| `regulator_label` | string | 监管机构展示名 | Regulator display label |
| `region` | string | 该授权所属辖区 | Jurisdiction of this authorisation |
| `tier` | string | 层级：T1/T2/T3 | Tier: T1 / T2 / T3 |
| `licence_kind` | string | 标识类型：FRN/AFSL/CE/CIF/FSP/LEI/VASP/MFSA/ref | Identifier kind: FRN / AFSL / CE / CIF / FSP / LEI / VASP / MFSA / ref |
| `licence_ref` | string | 可定位到官方记录的编号；LEI 不是牌照号 | Identifier resolvable in the official register; LEI is not a licence number |
| `licence_note` | string | 原文中的持牌类别清单等说明 | Notes from source (activity classes etc.) |
| `licence_raw` | string | 源表原文，用于追溯 | Raw source string, for traceability |
| `verified` | boolean | 是否已核对 | Verified |

## regulators.csv — 监管机构聚合

| 字段 / Field | 类型 / Type | 说明 | Description |
|---|---|---|---|
| `regulator_code` | string | 监管机构代码（已归一） | Normalised regulator code |
| `region` | string | 辖区 | Jurisdiction |
| `brokers_count` | integer | 该机构在该辖区的持牌机构数 | Brokers authorised here |
| `tier_t1` | integer | T1 条目数 | Count of T1 records |
| `tier_t2` | integer | T2 条目数 | Count of T2 records |
| `tier_t3` | integer | T3 条目数 | Count of T3 records |
| `licence_ref_count` | integer | 该组中带可定位编号的条目数 | Records carrying a resolvable identifier |
| `distinct_licence_ref` | integer | 去重编号数 | Distinct identifiers |

## 行数口径 / Row-count semantics

`licences.csv` 为 2066 行牌照明细；`regulators.csv` 三档层级合计 2519 条授权条目（机构×监管机构）。差额 453 条是「注册表确认持牌、但未给出独立编号」的授权，因此没有对应的逐条明细行。**两表不按行一一对应**：要数量看 `regulators.csv`，要编号看 `licences.csv`。

## 枚举值 / Enumerations

`licence_kind`：`FRN`(英国 FCA) · `AFSL`(澳洲 ASIC) · `CE`(香港 SFC) · `CIF`(塞浦路斯 CySEC) · `FSP`(南非 FSCA) · `VASP` · `MFSA` · `LEI`(**法人识别码，非牌照号**) · `ref`(其他)

`tier`：`T1` / `T2` / `T3` —— 本站编辑标记，非法定分类。`T3` 不等于不受监管。

`category`：外汇差价合约 / 贵金属现货 / 证券与期货经纪 / 加密资产交易商 / 机构服务

`skipped_dims`：竖线分隔的维度键，取自 `reg|breadth|prod|plat|type|source` 的子集，表示该维度**未采集**（不计加权、权重回补），不是 0 分。

