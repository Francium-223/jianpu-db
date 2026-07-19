### 仓库结构

[data.json](data.json)：存储歌曲信息、标签的文件。

[scores](scores/)：存放曲谱的文件夹。

[tag_imply.json](tag_imply.json)：标签间的蕴涵关系，如`东方星莲船`蕴涵`东方原曲`。

[by_artist](by_artist/)：按艺术家寻找曲谱（通过软链接）。

[by_tag](by_artist/)：按标签寻找曲谱（通过软链接）。同一首曲子可以有多个标签。

[by_artist](by_artist/)：按艺术家寻找曲谱（通过软链接）。

### 规范

#### 曲谱文件

文件/标签命名采用“先到先得”的原则。如果命名时发现了冲突/歧义，请将引起歧义的原有命名和你即将采用的命名一并改成**有标记**的名称。

记谱使用[jianpu-ly](https://github.com/ssb22/jianpu-ly/blob/master/README_zh-Hans.md)语言。原则上，只记**具有特征性的，响度最大**的旋律。记谱时，以**小调的一度音为`6,`；大调的一度音为`1`**（就是你听到这段声音后凭直觉写出来的样子），以此类推为原则。

例如，[东方主旋律](https://thbwiki.cc/Theme_of_Eastern_Story)转写出来是：

`,6 2 3 5 3 2 ,6 2 3 5 3 2 ,6 2 3 5 3 2 ,7 1 ,7 ,5`

一般的曲谱文件结构应该是这样：

```
% MBID: （这首歌在MusicBrainz中的编号，可以不写，提交后由开发者补充）
% tag: （这首歌的标签，用半角逗号隔开）
% alias: （这首歌的标签别名，用半角逗号隔开）
% transcriber: （转写者）
title=标题
subtitle=副标题（如果你想写的话）
subsubtitle=三级标题（如果你想写的话）
instrument=乐器（如果你想写的话）
poet=作词人（如果你想写的话）
composer=作曲家（如果你想写的话）
meter=节拍（如果你想写的话）
arranger=编曲家（如果你想写的话）
tagline=标语（如果你想写的话）
copyright=版权（如果你想写的话）
piece=作品（如果你想写的话）
opus=作品编号（如果你想写的话）
（你的曲谱）
```

MBID、tag、alias可以不写（当然如果会写最好），提交后由开发者补充。

#### data.json（高级）

因为本数据集记的是旋律，在[MusicBrainz](https://musicbrainz.org/)中的索引应以**work**为单位。如需声明某首歌不属于某一蕴涵的tag（如：属于`ZUN`但不属于`东方原曲`），请在data.json中这样写：

`tag: ["ZUN", "!东方"]`

### 目前进度

#### 东方原曲

### 贡献者

<a href="https://github.com/Francium-223"><img src="https://avatars.githubusercontent.com/u/286506063?s=400&v=4" height="40px" width="40px"></a>

### 鸣谢

[ssb22/jianpu-ly](https://github.com/ssb22/jianpu-ly/blob/master/README_zh-Hans.md)：规范的记谱语言

[MusicBrainz](https://musicbrainz.org/)：为歌曲提供唯一且确定的序号

[上海アリス幻樂団](https://www16.big.or.jp/~zun/)：th06-th09tr所有原曲

[Touhou Midi Collection](https://github.com/AyHa1810/touhou-midi-collection)：之后的东方原曲

### 友情链接

[ACGMuse](https://www.acgmuse.com/)

[Justice Eternal（zytx121/je）](https://github.com/zytx121/je)