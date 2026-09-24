# GitHub Actions 一直报错: jianpu2 的**假 submodule 记录**（2026-09-25）

用户贴的报错（在 `actions/checkout@v4` **checkout 阶段**）：

```
Fetching submodules
  /usr/bin/git submodule sync --recursive
  /usr/bin/git -c protocol.version=2 submodule update --init --force --depth=1 --recursive
  Error: fatal: No url found for submodule path 'jianpu2' in .gitmodules
  Error: The process '/usr/bin/git' failed with exit code 128
```

## 根因：**CI 自己提交进来的**

* `jianpu-db` 的树里有一条 `160000 commit b7c7826a…　jianpu2`（**gitlink**，即"子模块"记录），
  但仓库里**没有 `.gitmodules`** —— git 于是不知道去哪取它，`submodule update` 直接 128。
* 这条记录来自 **bot 提交 `2f60fb58`**（`github-actions[bot]`，`chore: auto-regenerate folder [skip ci]`），
  而它**只改了这一个条目**（`jianpu2 | 1 +`，`data.jsonl` 没变）：
  `parse.yaml` 第 35 行那步"Checkout sibling jianpu2"把兄弟仓库 checkout 到**本仓库内**的 `jianpu2/`，
  紧接着 Commit 步骤的 `git add -A` 就把这个嵌套仓库当 submodule 记了下来（git 会给一句 warning 然后照样 add）。
* 危害是**隐蔽**的：错误出在 checkout 阶段，跟"当次改了什么"八竿子打不着；而且一旦进了树，
  **之后每次**带 `submodules: recursive` 的运行都必挂（`publish-hf.yaml` 没写 `submodules:`，所以它反而一直是绿的）。
* 本地 `jianpu-db/jianpu2/` 是个**空目录**（当年目录搬走后留下的），git 不跟踪空目录，索引条目却还在。

## 修法（`51af08ff`）

1. `git rm --cached jianpu2` —— 索引/树里不再有 gitlink（工作区空目录一并删掉）。
2. `.gitignore` 加 `jianpu2/`（挡住 `git add -A` 再犯），并写清真口径：
   **jptok 在兄弟目录 `<repo>/../jianpu2/skills/jianpu-melody-lookup`**（`score.py` 就是按这个路径找），
   本仓库里不该有任何 `jianpu2` 条目。
3. `parse.yaml` 的 Commit 步骤加**响亮兜底**：`git add -A` 之后若索引里出现 `160000`，直接
   `::error::` 并 `exit 1`（这种错必须在"提交那一刻"炸，而不是下次 checkout 时炸）。
   该步骤显式 `shell: bash`（本 job 默认 `pwsh`，兜底是 bash 语法）。
4. 顺手在 sibling checkout 那步注明：`path: jianpu2` 其实**落错了地方** —— `score.py` 找的是
   `<repo>/../jianpu2`，而 checkout 落在 `<repo>/jianpu2`，所以 CI 实际上一直走的是
   `JIANPU_ALLOW_FALLBACK_JTOK=1` 的兜底口径。要真用上唯一实现得改 path 或加软链（未做，避免动 CI 行为）。

## 验过什么

* 远端树里已无 gitlink：`git fetch Francium-223 master && git ls-tree -r FETCH_HEAD | awk '$2=="commit"'` → 空。
* 兜底脚本两种情形都对：无 gitlink → 不报；有 → 打印并 `exit 1`。
* `parse.yaml` 能被 YAML 解析，5 个 step 的 shell 符合预期。
* 本地 `data.jsonl` md5 全程 `21d9709ce2b0c6fb3537d5f1c83d8938`（这次一个字没动）。

## 教训（写给以后的自己）

* **CI 里的 `git add -A` 是危险动作**：runner 工作区里被 checkout 进来的东西（兄弟仓库、缓存、临时产物）
  会被顺手提交。凡是往仓库目录里 checkout 别的东西，必须同时 `.gitignore` + 提交前兜底检查。
* 报错位置（checkout）和病因（树里一条历史条目）可以完全没有关系；遇到"莫名其妙必挂"的 CI，
  先看 `git ls-tree -r HEAD | awk '$2=="commit"'` 有没有不认识的 gitlink。
