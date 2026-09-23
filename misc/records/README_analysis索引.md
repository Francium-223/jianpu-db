# _analysis/ —— 这一夜的工作台（2026-09-24）

> 这里的东西**不在 git 里**（除了已复制到 `jianpu-db/misc/records/` 的那几份文档，会跟着 push/HF 走）。
> 醒来先看 `夜间工作报告_2026-09-24.md`，再看 `修复记录_解析器丢音.md`。

| 文件 | 是什么 |
|---|---|
| `夜间工作报告_2026-09-24.md` | **先看这个**：这一夜干完的事、待你决定的、怎么复现 |
| `修复记录_解析器丢音.md` | 丢音事故完整记录（解析器/休止计拍/h 时值定案/收录页/git 事故救援） |
| `投稿漏斗排障_2026-09-24.md` | **投稿会不会被静默吃掉**：5 个坑 + 并发/口径隐患 + 一次自造污染事故的记录与复原 |
| `待办4_根因报告.md` | th10_06「3 2 / 5 6」翻转定案的证据链 |
| `tag_todo.tsv` | **人工补标签入口**：926 首待补，填 `human_tag` 列 → `propose_tags.py --from-tsv` |
| `title_proposal.tsv` | 曲名改名提案（138 条高置信度），`accepted` 列审完 → `refine_titles_from_pages.py --apply` |
| `arrangement_candidates.tsv` | §8-5 被纯度门挡下的 1835 个改编/器乐谱（图都在、都是新曲） |
| `tag_proposal.tsv` / `artist_proposal.tsv` | 标签/歌手的自动提案（含来源证据与页面标题，便于人工核对） |
| `quality_proposal.tsv` | 语料体检第三类："拿不准"的 68 首 + 18 组跨站重复（带 `recommend` 列） |
| `eval_baseline_before_fix.txt` / `eval_final_7321.txt` | 改动前后的榜单指标（**逐项一致**，无回归） |
| `eval_after_fix_20260924.txt` | 投稿漏斗修复后重跑 4 清单（与 7321 首基线比对） |
| `quality_proposal.tsv` / `_verify_report.txt` | 体检提案 / 10.4 GB 抢救包的 SHA-256 校验报告 |
| `推送.sh` | **醒来先跑这个**：`bash 推送.sh --check` 体检 → `bash 推送.sh` 推三个库（要凭据） |
| `上传HF.sh` | HuggingFace 上传：`--check` 重新导出+核对 → `HF_TOKEN=… bash 上传HF.sh` |
| `git救援/` | 三个 stash 的补丁备份（stash0 = 那次"改动全没了"的全部内容） |
| `backup/` | 关键快照（data.jsonl 各阶段、songs.jsonl.gz.bak、改前基线） |
| `probe_h_*.py` / `diag_*.py` / `verify_*.py` | h 时值定案与各项核对的实验脚本（可复现） |
| `fingerprint_*.json`（在 `jianpu-db/misc/records/`） | 全部曲谱的基线指纹：批量改写后 `corpus_fingerprint.py --check` 用 |

**工具都在 `jianpu2/tools/`**（`corpus_fingerprint.py`（批量写回安全网）/ `propose_tags.py` / `harvest_artists.py` / `audit_corpus_quality.py` /
`quarantine_short_scores.py` / `refine_titles_from_pages.py` / `audit_arrangements.py` /
`verify_source_urls.py` / `add_link.py`）—— 用法见各脚本头部 docstring 与 `jianpu2/STATE.md`。
