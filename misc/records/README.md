# _analysis/ —— 这一夜的工作台（2026-09-24）

> 这里的东西**不在 git 里**（除了已复制到 `jianpu-db/misc/records/` 的那几份文档，会跟着 push/HF 走）。
> 醒来先看 `夜间工作报告_2026-09-24.md`，再看 `修复记录_解析器丢音.md`。

| 文件 | 是什么 |
|---|---|
| `夜间工作报告_2026-09-24.md` | **先看这个**：这一夜干完的事、待你决定的、怎么复现 |
| `修复记录_解析器丢音.md` | 丢音事故完整记录（解析器/休止计拍/h 时值定案/收录页/git 事故救援） |
| `投稿漏斗排障_2026-09-24.md` | **投稿会不会被静默吃掉**：5 个坑 + 并发/口径隐患 + 一次自造污染事故的记录与复原 |
| `解析副作用与输入校验_2026-09-24.md` | **读一份谱会不会改坏仓库**：parse 的副作用、两处 cwd 依赖、标签校验漏掉全部换行符、gzip 非确定性 |
| `前后端检索等价性_2026-09-24.md` | **报告指标 vs 浏览器实际**：把 Python 侧的查询在 JS 侧重放，四榜单 Top-3/5 全 100% |
| `人工补标签链路修复_2026-09-24.md` | **补标签这条路曾经是断的**：`--emit-template`/`--from-tsv` 的 NameError、修法、两道新防线、借标签提案 |
| `tag_todo_借标签.tsv` | 3 首"同一首的另一个转写有标签"的借标签提案（格式同 tag_todo，human_tag 已预填） |
| `同名不同曲_2026-09-24.md` | **同名未必同曲**：248 个"多版本"标题里 169 个版本间毫不相似；这解释了"多版本留一"指标为何低（真同曲时 100%） |
| `同名不同曲提案.tsv` | 每个可疑同名组的文件清单 + 最像/最不像的证据 |
| `旋律克隆与重复_2026-09-24.md` | **按旋律找重复**：267 对克隆（重复-异名 32 / 未命名 14 / 残名 9 / 可借标签 7） |
| `旋律克隆提案.tsv` | 每对的类别、两边文件·曲名·标签、LCS、覆盖率与建议 |
| `金曲缺口与转写队列_2026-09-24.md` | **覆盖瓶颈在哪**：48 首真缺口 + 已爬 18 首可转写简谱；含「这台机器不能转写」的实测 |
| `金曲缺口清单.tsv` / `金曲缺口_转写队列.tsv` | 榜单每条目的判定 / 爬到的页面（id、类型、本地目录） |
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

**工具都在 `jianpu2/tools/`**（`corpus_fingerprint.py`（批量写回安全网）/ `check_sideeffects.py`（解析副作用）/ `coverage_gap.py`（榜单缺口量化）/ `verify_crawl_matches.py`（爬回来的谱是不是这首歌）/ `propose_tags.py` / `harvest_artists.py` / `audit_corpus_quality.py` /
`quarantine_short_scores.py` / `refine_titles_from_pages.py` / `audit_arrangements.py` /
`verify_source_urls.py` / `add_link.py`）—— 用法见各脚本头部 docstring 与 `jianpu2/STATE.md`。
