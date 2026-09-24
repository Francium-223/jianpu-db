# jianpu2 项目进度总结

## 一、模型

### jianpu-atom（= jianpu-lora-v15）
真实谱面单音符识别模型（LoRA, 基于 Qwen2.5-VL-3B）。
- 数字: 100%
- 低八度: 99%
- 高八度: 100%
- 附点: 99%
- 时值: 96%

训练链路: 合成原子数据(v4) → v13 从零 → 真实微调 → v15(=jianpu-atom)

## 二、端到端工具链

| 脚本 | 作用 |
|------|------|
| tools/transcribe.py | 简谱图片 → jianpu-ly 序列(拆分→jianpu-atom识别→拼回) |
| tools/batch_pipeline.py | 图片目录 → 批量转写 → score 文件 |
| tools/make_score.py | 序列+元数据 → 标准 jianpu-db 曲谱文件 |
| tools/mbz_lookup.py | MusicBrainz API 查 MBID/title/type |
| tools/verify_source_urls.py | **原谱站确切页**: `source=<站>-<id>` → 那一页的真实 URL, **逐条抓取核对页面标题**, 写 `jianpu-db/source_pages.json` |
| tools/add_link.py | **人工补收录页**(命令行): 把某站的具体页面写进 `scores/<file>.txt` 的 `link=`; 支持 `--show` / `--from-tsv` 批量 / `--dry` |
| ../jianpu-web/tools/refresh.sh | 重建索引链: `parse_scores.py` → `build_web_data.py`(网页「＋ 补收录页」保存后由服务端在后台调用) |
| tools/propose_tags.py | **按原谱站栏目提议/落盘分类标签**(映射表从既有数据反推; 低置信度只提案); `--emit-template` 导出人工补标签清单, `--from-tsv` 写回 |
| tools/harvest_artists.py | 从原谱站页面抽**歌手**(jianpucn 标题尾段 / jianpujia `…_<歌手>演唱_…`); 抓取结果缓存可断点续跑, `--reparse` 离线重跑规则, `--apply` 落盘 |
| tools/audit_arrangements.py | 审计**被纯度门挡下的改编/器乐谱**(锦囊 §8-5): 数量/图在哪/是否新曲, 出可审清单 |
| tools/audit_corpus_quality.py | **语料体检**: A 明确垃圾(单音占比>=90% / 音符占 token<25%) 隔离、B 同源逐字相同的重复 去重、C 拿不准的只出提案; 移动不删, 可逆 |
| tools/quarantine_short_scores.py | 隔离**旋律音 < 5**(检索下限)的垃圾曲谱, `--min` 可调 |
| tools/refine_titles_from_pages.py | 给 `todo=refine the filename` 的曲从原谱页提议官方曲名(`--offline` 用缓存, `--apply` 落地) |
| tools/coverage_gap.py | **榜单覆盖缺口量化**(只读): 复用 eval 的 norm/same 口径, 把每个榜单条目判成 命中/命中但太短/别名命中/模糊候选/真缺口, 出 TSV; 实测与 eval_golden 的覆盖率逐项一致 |
| tools/safeout.py | **默认输出路径的护栏**: `default_out(DB, name)` —— DB 是工作区的 jianpu-db 就写 `_analysis/`，隔离跑就写进那个 DB 目录（实测踩过"隔离跑把真工作台提案覆盖成 1 行表头"） |
| tools/set_artists.py | **歌手独立字段 + 撞名消歧**: 从 harvest_artists 的页面证据灌 `artist=`, 并给"同名不同曲"的文件改成 `曲名（歌手）.txt`; `--apply/--rename`, 默认 dry |
| tools/check_images.py | **送转写前验图**: 短边过小(细条/截断)、坏 PNG、HTML 错误页都会被报出来; `--queue` 直接验转写队列。实测可转写队列 317 张 100% 可用 |
| tools/check_transcribe_ready.py | **转写环境"差什么"清单**: 基座 VLM / LoRA 适配器 / 网格检测器 / 白名单 / Python 依赖 / CUDA / 内存 / 磁盘 —— 逐项 ✓✗ 并给出补法(2026-09-24 用它纠正了"models/ 空"的误判) |
| tools/check_jptok_parity.py | **两份 token 口径的等价性测试**: 用 ast 从 score.py 抽出兜底 `_FallbackJptok`, 拿全语料(723 万 token)比 `is_note/parse_token/duration_letter/beat` 与 `beats_per_bar_from/recover_bars` -> 任何一处不一致就退非 0(2026-09-23 两份一起漂过, 36 首受损) |
| —（自检门第 7 条）| `selfcheck.py` 现在核对**白名单不变量**: `data.jsonl` 里不许有 `status=midi`(多轨转储)/无 status/空谱 —— 对应 `parse_scores.py` 里那句"待整理已跳过 499" |
| tools/audit_meter.py | **拍号体检(否定结果)**: 实测"总拍数比拍号"不可辨识(弱起)、"逐小节验"没有对象(全语料仅 3 首含 `\|`) -> 降级为描述统计; 列出那 3 个含 `\|` 的异常文件 |
| tools/audit_melody_clones.py | **旋律克隆审计**(只读): 音高序列 K 窗口建索引 + 最长公共子串 -> 找同曲异名/重复转写/可借标签/残名未命名; 267 对, 分类出提案 TSV |
| tools/slice_systems.py | 把简谱扫描件按**谱表**切开并放大(自动找音符行) -> 给人眼/VLM 复核用; 顺带兼容"GIF 字节却叫 .jpg"的站点图 |
| tools/verify_crawl_matches.py | **定向爬的核对**: 爬回来的页面标题 vs 目标曲名(同一份 norm/same), 再按标题后缀判是不是器乐改编 -> 防止把《前尘如梦》当《前尘》塞进转写队列 |
| tools/corpus_fingerprint.py | **批量写回的安全网**: 给全部 `scores/*.txt` 存指纹(元数据键集合/值/正文 sha1/音高音数), 批量工具跑完 `--check` 一次 -> 键集合变了或文件消失就退非 0(能立刻抓到 `todo=` 被写成 `dtodo=` 这类事故) |

## 三、爬虫

| 脚本 | 网站 | 状态 |
|------|------|------|
| tools/crawl_jianpujia.py | jianpujia.com 简谱之家 | 全链路通, 431链接, 下载中 |
| tools/crawl_qupu123.py | qupu123.com 中国曲谱网(30万篇) | 全链路通, 分页已修, 抓取中 |

后续可选数据源(未做):
- sooopu.com 搜谱网(33万首, /html/组/ID.html, indexN.html 分页, 但 GBK 编码 + dl.asp 脚本下载, 较复杂)
- jianpu.cn 歌谱简谱网
- jian-pu.com 简谱大全
- qupumao.com 曲谱猫

数据目录:
- images-prep/jianpujia-crawl/ (每首歌一个文件夹 歌名__jianpujia-<ID>/001.jpg) — 已下载 493 首/738图
- images-prep/qupu123-crawl/ — 3893 链接, 下载中
- images-prep/test-jianpujia/ (已有 2077 文件)
- images-prep/ready* (已有 1767 文件)

## 四、端到端验证(澎湖湾)

- 转写 219 音, 单音符质量 96-100%
- 序列对齐 61.4% (差异来自图片展开反复段 vs GT 循环记号, 非识别错误)

## 四点五、本地转写的可行性(2026-09-25 实测, 补记)

* 本机**没有 GPU**(核显 + Radeon)、内存 6.9GB -> VLM(jianpu-atom/Qwen2.5-VL-3B) **跑不了**
  (`check_transcribe_ready.py`: 缺基座 7GB + 依赖, 内存也不够)。
* 多任务 CNN 那条路**实测不可用**: `tools/infer_multitask.py` 原来丢了, 2026-09-25 才复原;
  用新工具 `tools/check_cnn_accuracy.py`(1355 个"图+库里已有转写"的同源样本)量下来,
  四个 checkpoint 相似度 0.00–0.04、前 20 音命中 26–50%(盲猜 14%) -> 等于随机。
  真实音符训练图 `train-work/real_notes_v4/` 也已丢失, 要复活必须重造数据+重训。
* CPU 版 torch 的装法(本机只有 py3.14, PyPI 的 Linux 轮子硬要 CUDA 库)见
  `_analysis/本地转写可行性_2026-09-25.md`: 用上交镜像的 `torch-2.14.0+cpu-cp314` + 配对 `torchvision-0.29.0+cpu`。

## 五、下一步(待定)

1. 扩大爬取规模(多分类/多网站)
2. 下载完成后批量转写
3. 转写结果人工校验
