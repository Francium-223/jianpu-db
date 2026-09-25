# jianpu2 简谱转写生产线 —— 迁移与运行说明

简谱（数字谱）扫描图 → 文本 token 序列。
零样本管线：几何切块 + **Qwen3-VL-2B** 逐块识别 + 纯简谱过滤 + 同名版本择优。

---

## 一、迁移到新机器：4 步

```bash
# 1) 拷贝仓库(代码+图片+模型)
#    模型默认在 <仓库根>/models/Qwen3-VL-2B-Instruct, 一起拷过去即可
#    (或设环境变量 QWEN_VL_MODEL 指向别处)

# 2) 建环境(必须 Python 3.13 —— 3.14 没有 torch)
py -3.13 -m pip install -r requirements.txt

# 3) 改配置(只改这个文件; 全删了也能跑, 有默认值)
#    pipeline.toml: 模型路径 / batch / 阈值 / jianpu-db 仓库位置

# 4) 自检
py -3.13 run.py verify     # 交付物总验收(7 项)
```

**所有路径都从仓库根解析**，脚本从任何目录运行都能找到根
（`tools/jp_root.py` 用 `__file__` 推断，不再有硬编码绝对路径）。

---

## 二、常用命令

| 命令 | 作用 |
|---|---|
| `py -3.13 run.py crawl 400` | 爬 jianpu.cn 的流行歌（歌手页路线，约 400 首）|
| `py -3.13 run.py transcribe` | 增量转写（已存在的跳过；可传源目录或名单文件）|
| `py -3.13 run.py finalize` | 收尾：纯度过滤 → 版本择优 → 重建 scores → 来源映射 → 下游 |
| `py -3.13 run.py verify` | 交付物总验收（7 项，一条命令给结论）|
| `py -3.13 run.py stats` | 语料统计 |
| `py -3.13 run.py gt` | GT 评测（用 `train-work/gt/` 的图+同名 txt）|
| `py -3.13 run.py detect` | 重扫全库纯度 |
| `py -3.13 run.py eta` | 当前批次还剩多少 + ETA |
| `py -3.13 run.py find 33565653253` | **旋律反查**：只输数字、模糊匹配、段落加权 |
| `py -3.13 run.py all` | **全自动**：等转写 → 收尾 → GT 评测 → 再爬 → 转写 → 再收尾 → 总验收 |
| `py -3.13 run.py finish` | 手动一把收完（万一 `all` 被中断）|

### ⚠️ 显存保护

**同一时间只能有一个模型在跑**（单卡 8GB 装不下两个 2B）。
`run.py` 对 GPU 命令（`transcribe`/`gt`/`finalize`/`all`/`finish`）会**先检查**：
有别的 python 在跑、或显存已用 >5GB，就**拒绝执行**并提示。
（这是踩过坑加的：转写跑着时又起一个 GT 评测，显存冲到 7708/8188 MiB。）

确需强制跑：`set JP_FORCE=1`（Windows）/ `export JP_FORCE=1`。
转写进行中用 `run.py eta` 看进度，用 `nvidia-smi` 看显存。

---

## 三、数据流

```
images-prep/<源>/<歌名>__<源>-<id>/001.jpg      原图（爬来的）
        │
        │  run.py transcribe   ← 纯简谱门在这里挡掉五线谱/吉他谱
        ▼
batch-out/<目录名>.txt + .png                    转写结果 + 标注框图
        │
        │  run.py finalize
        │    1. kind_detect2      重扫纯度
        │    2. apply_kind_filter 非纯简谱 → batch-out-bad/
        │    2b quarantine_highx  念白 x 占比≥30% → batch-out-suspect/
        │    2c quarantine_empty  0 音符 → batch-out-empty/
        │    3. pick_best         同名多版本择优 → batch-out-dup/ 放落选
        │    5. to_jianpu_db      重建 jianpu-db 格式曲谱
        │    5b make_source_map   标题→来源站 映射（溯源）
        │    6. 下游 parse_scores + db_to_jsonl
        ▼
jianpu-db-out/scores/*.txt                       ★ 主交付物
train-work/jpdbtest/out.jsonl                    ★ HF 格式数据集
train-work/source_map.tsv                        来源溯源
```

**隔离区只移不删**（`batch-out-bad/ -dup/ -suspect/ -empty/`），便于人工复核。

---

## 四、token 格式

`[时值][低八度][数字][高八度][附点]`

| 部分 | 取值 |
|---|---|
| 时值 | 无 / `q` / `s` / `d` / `h` = 四分/八分/十六/三十二/六十四 |
| 低八度 | `,` × 1-3 |
| 数字 | `1`-`7` 音级 · `0` 休止 · `x` 念白 |
| 高八度 | `'` × 1 |
| 附点 | `.` |

例：`q,5.` = 低八度 5 的八分附点音符。

---

## 五、关键机制（改代码前先读）

### 1. 尺度归一化（`jp_transcribe._target_w`）
管线里**所有尺寸阈值都是绝对像素**，所以：
- 宽 > 2000px 的页缩到 2000（否则 90px 的音符会被 `高≤50` 滤光）
- 宽 < 950px 的页放大到 1200（否则 8px 的音符会被 `高≥14` 滤光；**前奏常用小一号字，靠这个救**）

### 2. 纯简谱门（`kind_detect2.measure`）
判据 = 「单行最长连续暗段 ≥ 55% 页宽」的行数 ≥ 5。
- 灰度阈值**自适应** `max(60, 页均值-25)` —— 固定 128 抓不到淡扫描件
- **不要**改用「整行横向覆盖」当判据：会被页面上的**照片**骗（实测误杀 341 个谱/33,595 音符）
- 已知漏检：被小节线打断的五线谱（但转出 0 音符，被收尾隔离）

### 3. 版本择优（`pick_best.score`）
打分顺序：纯简谱 → 标题带"简谱" → 分辨率 → **已转出音符数** → nline → 标题短。
只按几何会选中"图大但转不出东西"的版本。
标题归并**不能**砍破折号后缀（`合集-编号+歌名` 会并成一首）、**不能**剥含词曲信息的括号。

### 4. 调号行过滤（`jp_transcribe` 装配阶段）
`1=F 3/4` 这类行长得像记号，连模型都会判成"音符行"。装配时丢掉"前两个行带里数字<4 个"的。

---

## 六、旋律反查（给不懂简谱语法的人用）

```bash
py -3.13 run.py find "3356 5653253"          # 只输数字, 空格/竖线/汉字都会自动忽略
py -3.13 run.py find 33575653253 --fuzzy 2   # 允许 2 处不同(记错/转写错都能救)
py -3.13 run.py find 33565653253 --top 20
```

三条设计原则：

1. **只输数字** —— 用户不需要知道 `q`/时值/八度/附点。
   而且**简谱是首调记法**（`1` 永远是该调的 do），所以数字串**天然与调无关**，
   同一首歌换个调唱，数字不变 —— 不需要额外做转调归一化。
2. **模糊匹配** —— 转写约 64% 准确、人手记谱也会错，整串精确相等会全丢。
   容忍 k 处不同，并按错音数扣分。
3. **段落加权** —— `subtitle=` 的段落名带权重。（**2026-09-25 已落地**：三个引擎
   `jianpu2/tools/melody_search.py`(机器人/命令行)、`jianpu-web/static/search.js`(网页)、
   `skills/jianpu-melody-lookup/lookup.py`(技能) 都用了这张表 —— 口径只有一份：权重表与
   `sec_weight/sec_at/section_map` 都在 `melody_search.py`，另两处**引用**它，不复制。
   落地方式：代价/错音相同时按 `-段落权` 排序（副歌优先于前奏），并**在同分窗口里挑权重最高的那一处出现**
   —— 用户当年的例子现在真的成立：`33565653253` 在《神々が恋した幻想郷》里前奏(0)与副歌(141)都有，
   现在取副歌(第 34–36 小节)，回话里也标出「（副歌）」。
   注：语料里目前只有 36 首带真分段（其余是 `subtitle=score`），所以这一条眼下只影响这 36 首；
   要让它覆盖全库，得先有"自动分段"（按重复结构找副歌）—— 那是下一步。）

   | 段落 | 权重 | 理由 |
   |---|---|---|
   | `chorus` / `refrain` | **1.6** | 副歌是"记得住的那句"，最可能是用户哼的 |
   | `verse` | 1.25 | 主歌 |
   | `pre-chorus` / `bridge` / `interlude` | 1.10 | |
   | `score`（未分段） | 1.00 | 我转换的谱都是这个 |
   | `intro` / `outro` / `layer` / `crazy-piano` | 0.80 | 前奏尾奏，被记住的概率低 |

   组合标签（如 `intro,chorus`）取**最大**权重。段落名来自 `subtitle=`，
   词汇表见 `tools/survey_sections.py` 的普查（用户仓库实际用到 11 种）。

打分 = `匹配长度 × 段落权 × 覆盖率 − 错音惩罚`；输出**歌名（含中文别名）+ 段落 + 权重 + 错音数 + 匹配位置上下文**，便于人工核对。

> 实测：《神々が恋した幻想郷》(东方风神录 th10-06) 的 `3356 5653253` 同时出现在
> **副歌**和**前奏**，加权后副歌排前（17.6 vs 8.8）。

---

## 七、目录约定

| 目录 | 内容 |
|---|---|
| `tools/` | 全部脚本（生产线用的约 20 个 + 历史诊断脚本）|
| `images-prep/<源>/` | 原图，每个子目录一首（目录名 = `<歌名>__<源>-<id>`）|
| `batch-out/` | 转写结果（`progress.txt`/`skipped.txt` 是批处理的状态文件）|
| `batch-out-{bad,dup,suspect,empty}/` | 隔离区 |
| `jianpu-db-out/scores/` | ★ jianpu-db 格式曲谱 |
| `train-work/` | 中间产物：名单、统计、GT、`jpdbtest/out.jsonl` |
| `train-work/gt/` | 人工 GT（`.txt` + `.ly/.mid/.pdf/.jpg`）|
| `models/` | Qwen3-VL-2B（迁移时一起拷）|
| `rank-out/` | 热度榜（决定批处理顺序）|

---

## 八、已知限制

1. **非人工校对**：以 spring《春天在哪里》GT 为锚点约 **76%**
2. **八度偶误**：低八度点有时漏读/多读
3. **前奏/小字**：靠放大救，字号再小就丢
4. **混排谱**：吉他弹唱谱过滤后仍可能有少量六线谱数字混入
5. **流行歌不全**：源站有就收，没有就没有

---

## 九、状态与日志

| 文件 | 内容 |
|---|---|
| `train-work/autopilot.log` | 无人值守流程日志 |
| `train-work/finish.log` | 手动收尾日志 |
| `batch-out/progress.txt` | 批处理进度 |
| `train-work/kind2.tsv` | 全库纯度明细（nline/wide/pure）|
| `train-work/pick_best.tsv` | 版本择优结果 |
| `train-work/source_map.tsv` | 来源溯源 |
| `醒来汇报_v9.md` | 这一轮工作的完整汇报（含 14 个 bug 的根因与修法）|
| `DATASET.md` | 数据集说明卡 |
