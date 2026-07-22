# jianpu-db

## 简介

**jianpu-db**是基于[jianpu-ly](https://github.com/ssb22/jianpu-ly/blob/master/README_zh-Hans.md)语法和[MusicBrainz](https://musicbrainz.org/)唯一标识符构建的、面向大语言模型训练及严谨学术研究的高度规范化可读数字音乐简谱旋律数据集。旨在解决大语言模型面对简谱束手无措的痛点、填补网络上以简谱记载的旋律信息量不足、规范度不够的缺口。

本项目正在开发基础架构中，亟待能人异士的加入（无论是开发代码还是转写旋律）……

## 仓库结构

[scores](scores/)：存放曲谱及其元数据的文件夹。

[data.json](data.json)：存储歌曲元数据的文件，由脚本将score文件夹中的元数据自动拼接生成。

[tag_imply.json](tag_imply.json)：标签间的蕴涵关系，如`东方星莲船`蕴涵`东方原曲`。

[tag_equal.json](tag_equal.json)：标签间的等同关系，如`东方星莲船`等同`th12`。

[by_title](by_title/)：按标题寻找曲谱（通过软链接）的文件夹。

[by_tag](by_artist/)：按标签寻找曲谱（通过软链接）的文件夹。同一首曲子可以有多个标签。

[by_xxx](by_artist/)：按xxx寻找曲谱（通过软链接）的文件夹。（见后面）

## 目前进度

⬛=无文件，🟥=自动生成，待人工审核

（转写完成后，请将对应位置的方块换成前面的emoji。）

### 东方原曲：

☯️东方灵异传：<abbr title="th01_01.txt">[☯️](scores/th01_01.txt)</abbr><abbr title="th01_02.txt">[☯️](scores/th01_02.txt)</abbr><abbr title="th01_03.txt">[⬛](scores/th01_03.txt)</abbr><abbr title="th01_04.txt">[⬛](scores/th01_04.txt)</abbr><abbr title="th01_05.txt">[⬛](scores/th01_05.txt)</abbr><abbr title="th01_06.txt">[⬛](scores/th01_06.txt)</abbr><abbr title="th01_07.txt">[⬛](scores/th01_07.txt)</abbr><abbr title="th01_08.txt">[⬛](scores/th01_08.txt)</abbr><abbr title="th01_09.txt">[⬛](scores/th01_09.txt)</abbr><abbr title="th01_10.txt">[⬛](scores/th01_10.txt)</abbr><abbr title="th01_11.txt">[⬛](scores/th01_11.txt)</abbr><abbr title="th01_12.txt">[⬛](scores/th01_12.txt)</abbr><abbr title="th01_13.txt">[⬛](scores/th01_13.txt)</abbr><abbr title="th01_14.txt">[⬛](scores/th01_14.txt)</abbr><abbr title="th01_15.txt">[⬛](scores/th01_15.txt)</abbr>

🐢东方封魔录：<abbr title="th02_01.txt">[⬛](scores/th02_01.txt)</abbr><abbr title="th02_02.txt">[⬛](scores/th02_02.txt)</abbr><abbr title="th02_03.txt">[⬛](scores/th02_03.txt)</abbr><abbr title="th02_04.txt">[⬛](scores/th02_04.txt)</abbr><abbr title="th02_05.txt">[⬛](scores/th02_05.txt)</abbr><abbr title="th02_06.txt">[⬛](scores/th02_06.txt)</abbr><abbr title="th02_07.txt">[⬛](scores/th02_07.txt)</abbr><abbr title="th02_08.txt">[⬛](scores/th02_08.txt)</abbr><abbr title="th02_09.txt">[⬛](scores/th02_09.txt)</abbr><abbr title="th02_10.txt">[⬛](scores/th02_10.txt)</abbr><abbr title="th02_11.txt">[⬛](scores/th02_11.txt)</abbr><abbr title="th02_12.txt">[⬛](scores/th02_12.txt)</abbr><abbr title="th02_13.txt">[⬛](scores/th02_13.txt)</abbr><abbr title="th02_14.txt">[⬛](scores/th02_14.txt)</abbr><abbr title="th02_15.txt">[⬛](scores/th02_15.txt)</abbr><abbr title="th02_16.txt">[⬛](scores/th02_16.txt)</abbr><abbr title="th02_17.txt">[⬛](scores/th02_17.txt)</abbr><abbr title="th02_18.txt">[⬛](scores/th02_18.txt)</abbr>

🚀东方梦时空：<abbr title="th03_01.txt">[⬛](scores/th03_01.txt)</abbr><abbr title="th03_02.txt">[⬛](scores/th03_02.txt)</abbr><abbr title="th03_03.txt">[⬛](scores/th03_03.txt)</abbr><abbr title="th03_04.txt">[⬛](scores/th03_04.txt)</abbr><abbr title="th03_05.txt">[⬛](scores/th03_05.txt)</abbr><abbr title="th03_06.txt">[⬛](scores/th03_06.txt)</abbr><abbr title="th03_07.txt">[⬛](scores/th03_07.txt)</abbr><abbr title="th03_08.txt">[⬛](scores/th03_08.txt)</abbr><abbr title="th03_09.txt">[⬛](scores/th03_09.txt)</abbr><abbr title="th03_10.txt">[⬛](scores/th03_10.txt)</abbr><abbr title="th03_11.txt">[⬛](scores/th03_11.txt)</abbr><abbr title="th03_12.txt">[⬛](scores/th03_12.txt)</abbr><abbr title="th03_13.txt">[⬛](scores/th03_13.txt)</abbr><abbr title="th03_14.txt">[⬛](scores/th03_14.txt)</abbr><abbr title="th03_15.txt">[⬛](scores/th03_15.txt)</abbr><abbr title="th03_16.txt">[⬛](scores/th03_16.txt)</abbr><abbr title="th03_17.txt">[⬛](scores/th03_17.txt)</abbr><abbr title="th03_18.txt">[⬛](scores/th03_18.txt)</abbr><abbr title="th03_19.txt">[⬛](scores/th03_19.txt)</abbr><abbr title="th03_20.txt">[⬛](scores/th03_20.txt)</abbr><abbr title="th03_21.txt">[⬛](scores/th03_21.txt)</abbr><abbr title="th03_22.txt">[⬛](scores/th03_22.txt)</abbr><abbr title="th03_23.txt">[⬛](scores/th03_23.txt)</abbr><abbr title="th03_24.txt">[⬛](scores/th03_24.txt)</abbr>

🌂东方幻想乡：<abbr title="th04_01.txt">[⬛](scores/th04_01.txt)</abbr><abbr title="th04_02.txt">[⬛](scores/th04_02.txt)</abbr><abbr title="th04_03.txt">[⬛](scores/th04_03.txt)</abbr><abbr title="th04_04.txt">[⬛](scores/th04_04.txt)</abbr><abbr title="th04_05.txt">[⬛](scores/th04_05.txt)</abbr><abbr title="th04_06.txt">[⬛](scores/th04_06.txt)</abbr><abbr title="th04_07.txt">[⬛](scores/th04_07.txt)</abbr><abbr title="th04_08.txt">[⬛](scores/th04_08.txt)</abbr><abbr title="th04_09.txt">[⬛](scores/th04_09.txt)</abbr><abbr title="th04_10.txt">[⬛](scores/th04_10.txt)</abbr><abbr title="th04_11.txt">[⬛](scores/th04_11.txt)</abbr><abbr title="th04_12.txt">[⬛](scores/th04_12.txt)</abbr><abbr title="th04_13.txt">[⬛](scores/th04_13.txt)</abbr><abbr title="th04_14.txt">[⬛](scores/th04_14.txt)</abbr><abbr title="th04_15.txt">[⬛](scores/th04_15.txt)</abbr><abbr title="th04_16.txt">[⬛](scores/th04_16.txt)</abbr><abbr title="th04_17.txt">[⬛](scores/th04_17.txt)</abbr><abbr title="th04_18.txt">[⬛](scores/th04_18.txt)</abbr><abbr title="th04_19.txt">[⬛](scores/th04_19.txt)</abbr><abbr title="th04_20.txt">[⬛](scores/th04_20.txt)</abbr><abbr title="th04_21.txt">[⬛](scores/th04_21.txt)</abbr><abbr title="th04_22.txt">[⬛](scores/th04_22.txt)</abbr><abbr title="th04_23.txt">[⬛](scores/th04_23.txt)</abbr><abbr title="th04_24.txt">[⬛](scores/th04_24.txt)</abbr><abbr title="th04_25.txt">[⬛](scores/th04_25.txt)</abbr><abbr title="th04_26.txt">[⬛](scores/th04_26.txt)</abbr><abbr title="th04_27.txt">[⬛](scores/th04_27.txt)</abbr><abbr title="th04_28.txt">[⬛](scores/th04_28.txt)</abbr><abbr title="th04_29.txt">[⬛](scores/th04_29.txt)</abbr>

🪽东方怪绮谈：<abbr title="th05_01.txt">[⬛](scores/th05_01.txt)</abbr><abbr title="th05_02.txt">[⬛](scores/th05_02.txt)</abbr><abbr title="th05_03.txt">[⬛](scores/th05_03.txt)</abbr><abbr title="th05_04.txt">[⬛](scores/th05_04.txt)</abbr><abbr title="th05_05.txt">[⬛](scores/th05_05.txt)</abbr><abbr title="th05_06.txt">[⬛](scores/th05_06.txt)</abbr><abbr title="th05_07.txt">[⬛](scores/th05_07.txt)</abbr><abbr title="th05_08.txt">[⬛](scores/th05_08.txt)</abbr><abbr title="th05_09.txt">[⬛](scores/th05_09.txt)</abbr><abbr title="th05_10.txt">[⬛](scores/th05_10.txt)</abbr><abbr title="th05_11.txt">[⬛](scores/th05_11.txt)</abbr><abbr title="th05_12.txt">[⬛](scores/th05_12.txt)</abbr><abbr title="th05_13.txt">[⬛](scores/th05_13.txt)</abbr><abbr title="th05_14.txt">[⬛](scores/th05_14.txt)</abbr><abbr title="th05_15.txt">[⬛](scores/th05_15.txt)</abbr><abbr title="th05_16.txt">[⬛](scores/th05_16.txt)</abbr><abbr title="th05_17.txt">[⬛](scores/th05_17.txt)</abbr><abbr title="th05_18.txt">[⬛](scores/th05_18.txt)</abbr><abbr title="th05_19.txt">[⬛](scores/th05_19.txt)</abbr><abbr title="th05_20.txt">[⬛](scores/th05_20.txt)</abbr><abbr title="th05_21.txt">[⬛](scores/th05_21.txt)</abbr><abbr title="th05_22.txt">[⬛](scores/th05_22.txt)</abbr><abbr title="th05_23.txt">[⬛](scores/th05_23.txt)</abbr>

🦇东方红魔乡：<abbr title="th06_01.txt">[⬛](scores/th06_01.txt)</abbr><abbr title="th06_02.txt">[⬛](scores/th06_02.txt)</abbr><abbr title="th06_03.txt">[⬛](scores/th06_03.txt)</abbr><abbr title="th06_04.txt">[⬛](scores/th06_04.txt)</abbr><abbr title="th06_05.txt">[⬛](scores/th06_05.txt)</abbr><abbr title="th06_06.txt">[⬛](scores/th06_06.txt)</abbr><abbr title="th06_07.txt">[⬛](scores/th06_07.txt)</abbr><abbr title="th06_08.txt">[⬛](scores/th06_08.txt)</abbr><abbr title="th06_09.txt">[⬛](scores/th06_09.txt)</abbr><abbr title="th06_10.txt">[⬛](scores/th06_10.txt)</abbr><abbr title="th06_11.txt">[⬛](scores/th06_11.txt)</abbr><abbr title="th06_12.txt">[⬛](scores/th06_12.txt)</abbr><abbr title="th06_13.txt">[⬛](scores/th06_13.txt)</abbr><abbr title="th06_14.txt">[⬛](scores/th06_14.txt)</abbr><abbr title="th06_15.txt">[⬛](scores/th06_15.txt)</abbr><abbr title="th06_16.txt">[⬛](scores/th06_16.txt)</abbr><abbr title="th06_17.txt">[⬛](scores/th06_17.txt)</abbr>

🌸东方妖妖梦：<abbr title="th07_01.txt">[⬛](scores/th07_01.txt)</abbr><abbr title="th07_02.txt">[⬛](scores/th07_02.txt)</abbr><abbr title="th07_03.txt">[⬛](scores/th07_03.txt)</abbr><abbr title="th07_04.txt">[⬛](scores/th07_04.txt)</abbr><abbr title="th07_05.txt">[⬛](scores/th07_05.txt)</abbr><abbr title="th07_06.txt">[⬛](scores/th07_06.txt)</abbr><abbr title="th07_07.txt">[⬛](scores/th07_07.txt)</abbr><abbr title="th07_08.txt">[⬛](scores/th07_08.txt)</abbr><abbr title="th07_09.txt">[⬛](scores/th07_09.txt)</abbr><abbr title="th07_10.txt">[⬛](scores/th07_10.txt)</abbr><abbr title="th07_11.txt">[⬛](scores/th07_11.txt)</abbr><abbr title="th07_12.txt">[⬛](scores/th07_12.txt)</abbr><abbr title="th07_13.txt">[⬛](scores/th07_13.txt)</abbr><abbr title="th07_14.txt">[⬛](scores/th07_14.txt)</abbr><abbr title="th07_15.txt">[⬛](scores/th07_15.txt)</abbr><abbr title="th07_16.txt">[⬛](scores/th07_16.txt)</abbr><abbr title="th07_17.txt">[⬛](scores/th07_17.txt)</abbr><abbr title="th07_18.txt">[⬛](scores/th07_18.txt)</abbr><abbr title="th07_19.txt">[⬛](scores/th07_19.txt)</abbr><abbr title="th07_20.txt">[⬛](scores/th07_20.txt)</abbr>

🍾东方萃梦想：<abbr title="th075_01.txt">[⬛](scores/th075_01.txt)</abbr><abbr title="th075_16.txt">[⬛](scores/th075_16.txt)</abbr><abbr title="th075_17.txt">[⬛](scores/th075_17.txt)</abbr><abbr title="th075_18.txt">[⬛](scores/th075_18.txt)</abbr><abbr title="th075_19.txt">[⬛](scores/th075_19.txt)</abbr><abbr title="th075_20.txt">[⬛](scores/th075_20.txt)</abbr><abbr title="th075_21.txt">[⬛](scores/th075_21.txt)</abbr><abbr title="th075_22.txt">[⬛](scores/th075_22.txt)</abbr><abbr title="th075_23.txt">[⬛](scores/th075_23.txt)</abbr><abbr title="th075_24.txt">[⬛](scores/th075_24.txt)</abbr><abbr title="th075_25.txt">[⬛](scores/th075_25.txt)</abbr><abbr title="th075_26.txt">[⬛](scores/th075_26.txt)</abbr><abbr title="th075_27.txt">[⬛](scores/th075_27.txt)</abbr><abbr title="th075_28.txt">[⬛](scores/th075_28.txt)</abbr><abbr title="th075_29.txt">[⬛](scores/th075_29.txt)</abbr><abbr title="th075_30.txt">[⬛](scores/th075_30.txt)</abbr><abbr title="th075_31.txt">[⬛](scores/th075_31.txt)</abbr><abbr title="th075_32.txt">[⬛](scores/th075_32.txt)</abbr><abbr title="th075_33.txt">[⬛](scores/th075_33.txt)</abbr><abbr title="th075_34.txt">[⬛](scores/th075_34.txt)</abbr>

🌕东方永夜抄：<abbr title="th08_01.txt">[⬛](scores/th08_01.txt)</abbr><abbr title="th08_02.txt">[⬛](scores/th08_02.txt)</abbr><abbr title="th08_03.txt">[⬛](scores/th08_03.txt)</abbr><abbr title="th08_04.txt">[⬛](scores/th08_04.txt)</abbr><abbr title="th08_05.txt">[⬛](scores/th08_05.txt)</abbr><abbr title="th08_06.txt">[⬛](scores/th08_06.txt)</abbr><abbr title="th08_07.txt">[⬛](scores/th08_07.txt)</abbr><abbr title="th08_08.txt">[⬛](scores/th08_08.txt)</abbr><abbr title="th08_09.txt">[⬛](scores/th08_09.txt)</abbr><abbr title="th08_10.txt">[⬛](scores/th08_10.txt)</abbr><abbr title="th08_11.txt">[⬛](scores/th08_11.txt)</abbr><abbr title="th08_12.txt">[⬛](scores/th08_12.txt)</abbr><abbr title="th08_13.txt">[⬛](scores/th08_13.txt)</abbr><abbr title="th08_14.txt">[⬛](scores/th08_14.txt)</abbr><abbr title="th08_15.txt">[⬛](scores/th08_15.txt)</abbr><abbr title="th08_16.txt">[⬛](scores/th08_16.txt)</abbr><abbr title="th08_17.txt">[⬛](scores/th08_17.txt)</abbr><abbr title="th08_18.txt">[⬛](scores/th08_18.txt)</abbr><abbr title="th08_19.txt">[⬛](scores/th08_19.txt)</abbr><abbr title="th08_20.txt">[⬛](scores/th08_20.txt)</abbr><abbr title="th08_21.txt">[⬛](scores/th08_21.txt)</abbr>

💐东方花映塚：<abbr title="th09_01.txt">[⬛](scores/th09_01.txt)</abbr><abbr title="th09_02.txt">[⬛](scores/th09_02.txt)</abbr><abbr title="th09_03.txt">[⬛](scores/th09_03.txt)</abbr><abbr title="th09_04.txt">[⬛](scores/th09_04.txt)</abbr><abbr title="th09_10.txt">[⬛](scores/th09_10.txt)</abbr><abbr title="th09_11.txt">[⬛](scores/th09_11.txt)</abbr><abbr title="th09_12.txt">[⬛](scores/th09_12.txt)</abbr><abbr title="th09_13.txt">[⬛](scores/th09_13.txt)</abbr><abbr title="th09_14.txt">[⬛](scores/th09_14.txt)</abbr><abbr title="th09_15.txt">[⬛](scores/th09_15.txt)</abbr><abbr title="th09_16.txt">[⬛](scores/th09_16.txt)</abbr><abbr title="th09_17.txt">[⬛](scores/th09_17.txt)</abbr><abbr title="th09_18.txt">[⬛](scores/th09_18.txt)</abbr><abbr title="th09_19.txt">[⬛](scores/th09_19.txt)</abbr>

📷东方文花帖：<abbr title="th095_01.txt">[⬛](scores/th095_01.txt)</abbr><abbr title="th095_02.txt">[⬛](scores/th095_02.txt)</abbr><abbr title="th095_03.txt">[⬛](scores/th095_03.txt)</abbr><abbr title="th095_04.txt">[⬛](scores/th095_04.txt)</abbr><abbr title="th095_05.txt">[⬛](scores/th095_05.txt)</abbr><abbr title="th095_06.txt">[⬛](scores/th095_06.txt)</abbr>

🍁东方风神录：<abbr title="th10_01.txt">[⬛](scores/th10_01.txt)</abbr><abbr title="th10_02.txt">[⬛](scores/th10_02.txt)</abbr><abbr title="th10_03.txt">[⬛](scores/th10_03.txt)</abbr><abbr title="th10_04.txt">[⬛](scores/th10_04.txt)</abbr><abbr title="th10_05.txt">[⬛](scores/th10_05.txt)</abbr><abbr title="th10_06.txt">[⬛](scores/th10_06.txt)</abbr><abbr title="th10_07.txt">[⬛](scores/th10_07.txt)</abbr><abbr title="th10_08.txt">[⬛](scores/th10_08.txt)</abbr><abbr title="th10_09.txt">[⬛](scores/th10_09.txt)</abbr><abbr title="th10_10.txt">[⬛](scores/th10_10.txt)</abbr><abbr title="th10_11.txt">[⬛](scores/th10_11.txt)</abbr><abbr title="th10_12.txt">[⬛](scores/th10_12.txt)</abbr><abbr title="th10_13.txt">[⬛](scores/th10_13.txt)</abbr><abbr title="th10_14.txt">[⬛](scores/th10_14.txt)</abbr><abbr title="th10_15.txt">[⬛](scores/th10_15.txt)</abbr><abbr title="th10_16.txt">[⬛](scores/th10_16.txt)</abbr><abbr title="th10_17.txt">[⬛](scores/th10_17.txt)</abbr><abbr title="th10_18.txt">[⬛](scores/th10_18.txt)</abbr>

🪨东方绯想天：<abbr title="th105_01.txt">[⬛](scores/th105_01.txt)</abbr><abbr title="th105_02.txt">[⬛](scores/th105_02.txt)</abbr><abbr title="th105_03.txt">[⬛](scores/th105_03.txt)</abbr><abbr title="th105_04.txt">[⬛](scores/th105_04.txt)</abbr><abbr title="th105_05.txt">[⬛](scores/th105_05.txt)</abbr><abbr title="th105_06.txt">[⬛](scores/th105_06.txt)</abbr><abbr title="th105_07.txt">[⬛](scores/th105_07.txt)</abbr><abbr title="th105_08.txt">[⬛](scores/th105_08.txt)</abbr><abbr title="th105_09.txt">[⬛](scores/th105_09.txt)</abbr><abbr title="th105_10.txt">[⬛](scores/th105_10.txt)</abbr><abbr title="th105_11.txt">[⬛](scores/th105_11.txt)</abbr><abbr title="th105_12.txt">[⬛](scores/th105_12.txt)</abbr><abbr title="th105_13.txt">[⬛](scores/th105_13.txt)</abbr><abbr title="th105_14.txt">[⬛](scores/th105_14.txt)</abbr><abbr title="th105_15.txt">[⬛](scores/th105_15.txt)</abbr><abbr title="th105_16.txt">[⬛](scores/th105_16.txt)</abbr><abbr title="th105_17.txt">[⬛](scores/th105_17.txt)</abbr><abbr title="th105_18.txt">[⬛](scores/th105_18.txt)</abbr>

☢️东方地灵殿：<abbr title="th11_01.txt">[⬛](scores/th11_01.txt)</abbr><abbr title="th11_02.txt">[⬛](scores/th11_02.txt)</abbr><abbr title="th11_03.txt">[⬛](scores/th11_03.txt)</abbr><abbr title="th11_04.txt">[⬛](scores/th11_04.txt)</abbr><abbr title="th11_05.txt">[⬛](scores/th11_05.txt)</abbr><abbr title="th11_06.txt">[⬛](scores/th11_06.txt)</abbr><abbr title="th11_07.txt">[⬛](scores/th11_07.txt)</abbr><abbr title="th11_08.txt">[⬛](scores/th11_08.txt)</abbr><abbr title="th11_09.txt">[⬛](scores/th11_09.txt)</abbr><abbr title="th11_10.txt">[⬛](scores/th11_10.txt)</abbr><abbr title="th11_11.txt">[⬛](scores/th11_11.txt)</abbr><abbr title="th11_12.txt">[⬛](scores/th11_12.txt)</abbr><abbr title="th11_13.txt">[⬛](scores/th11_13.txt)</abbr><abbr title="th11_14.txt">[⬛](scores/th11_14.txt)</abbr><abbr title="th11_15.txt">[⬛](scores/th11_15.txt)</abbr><abbr title="th11_16.txt">[⬛](scores/th11_16.txt)</abbr><abbr title="th11_17.txt">[⬛](scores/th11_17.txt)</abbr>

🛸东方星莲船：<abbr title="th12_01.txt">[⬛](scores/th12_01.txt)</abbr><abbr title="th12_02.txt">[⬛](scores/th12_02.txt)</abbr><abbr title="th12_03.txt">[⬛](scores/th12_03.txt)</abbr><abbr title="th12_04.txt">[⬛](scores/th12_04.txt)</abbr><abbr title="th12_05.txt">[⬛](scores/th12_05.txt)</abbr><abbr title="th12_06.txt">[⬛](scores/th12_06.txt)</abbr><abbr title="th12_07.txt">[⬛](scores/th12_07.txt)</abbr><abbr title="th12_08.txt">[⬛](scores/th12_08.txt)</abbr><abbr title="th12_09.txt">[⬛](scores/th12_09.txt)</abbr><abbr title="th12_10.txt">[⬛](scores/th12_10.txt)</abbr><abbr title="th12_11.txt">[⬛](scores/th12_11.txt)</abbr><abbr title="th12_12.txt">[⬛](scores/th12_12.txt)</abbr><abbr title="th12_13.txt">[⬛](scores/th12_13.txt)</abbr><abbr title="th12_14.txt">[⬛](scores/th12_14.txt)</abbr><abbr title="th12_15.txt">[⬛](scores/th12_15.txt)</abbr><abbr title="th12_16.txt">[⬛](scores/th12_16.txt)</abbr><abbr title="th12_17.txt">[⬛](scores/th12_17.txt)

🤖东方非想天则：</abbr><abbr title="th123_01.txt">[⬛](scores/th123_01.txt)</abbr><abbr title="th123_03.txt">[⬛](scores/th123_03.txt)</abbr><abbr title="th123_04.txt">[⬛](scores/th123_04.txt)</abbr><abbr title="th123_05.txt">[⬛](scores/th123_05.txt)</abbr><abbr title="th123_06.txt">[⬛](scores/th123_06.txt)</abbr><abbr title="th123_12.txt">[⬛](scores/th123_12.txt)</abbr><abbr title="th123_13.txt">[⬛](scores/th123_13.txt)</abbr><abbr title="th123_19.txt">[⬛](scores/th123_19.txt)</abbr><abbr title="th125_01.txt">[⬛](scores/th125_01.txt)</abbr><abbr title="th125_02.txt">[⬛](scores/th125_02.txt)</abbr><abbr title="th125_03.txt">[⬛](scores/th125_03.txt)

📟东方文花帖DS：</abbr><abbr title="th125_04.txt">[⬛](scores/th125_04.txt)</abbr><abbr title="th125_05.txt">[⬛](scores/th125_05.txt)</abbr><abbr title="th125_07.txt">[⬛](scores/th125_07.txt)

☀️🌙⭐妖精大战争：</abbr><abbr title="th128_01.txt">[⬛](scores/th128_01.txt)</abbr><abbr title="th128_02.txt">[⬛](scores/th128_02.txt)</abbr><abbr title="th128_03.txt">[⬛](scores/th128_03.txt)</abbr><abbr title="th128_04.txt">[⬛](scores/th128_04.txt)</abbr><abbr title="th128_05.txt">[⬛](scores/th128_05.txt)</abbr><abbr title="th128_06.txt">[⬛](scores/th128_06.txt)</abbr><abbr title="th128_07.txt">[⬛](scores/th128_07.txt)</abbr><abbr title="th128_08.txt">[⬛](scores/th128_08.txt)</abbr><abbr title="th128_09.txt">[⬛](scores/th128_09.txt)</abbr>

👑东方神灵庙：<abbr title="th13_01.txt">[⬛](scores/th13_01.txt)</abbr><abbr title="th13_02.txt">[⬛](scores/th13_02.txt)</abbr><abbr title="th13_03.txt">[⬛](scores/th13_03.txt)</abbr><abbr title="th13_04.txt">[⬛](scores/th13_04.txt)</abbr><abbr title="th13_05.txt">[⬛](scores/th13_05.txt)</abbr><abbr title="th13_06.txt">[⬛](scores/th13_06.txt)</abbr><abbr title="th13_07.txt">[⬛](scores/th13_07.txt)</abbr><abbr title="th13_08.txt">[⬛](scores/th13_08.txt)</abbr><abbr title="th13_09.txt">[⬛](scores/th13_09.txt)</abbr><abbr title="th13_10.txt">[⬛](scores/th13_10.txt)</abbr><abbr title="th13_11.txt">[⬛](scores/th13_11.txt)</abbr><abbr title="th13_12.txt">[⬛](scores/th13_12.txt)</abbr><abbr title="th13_13.txt">[⬛](scores/th13_13.txt)</abbr><abbr title="th13_14.txt">[⬛](scores/th13_14.txt)</abbr><abbr title="th13_15.txt">[⬛](scores/th13_15.txt)</abbr><abbr title="th13_16.txt">[⬛](scores/th13_16.txt)</abbr><abbr title="th13_17.txt">[⬛](scores/th13_17.txt)

👺东方心绮楼：</abbr><abbr title="th135_10.txt">[⬛](scores/th135_10.txt)</abbr><abbr title="th135_11.txt">[⬛](scores/th135_11.txt)</abbr><abbr title="th135_12.txt">[⬛](scores/th135_12.txt)</abbr><abbr title="th135_13.txt">[⬛](scores/th135_13.txt)</abbr><abbr title="th135_14.txt">[⬛](scores/th135_14.txt)</abbr><abbr title="th135_15.txt">[⬛](scores/th135_15.txt)</abbr><abbr title="th135_16.txt">[⬛](scores/th135_16.txt)</abbr><abbr title="th135_17.txt">[⬛](scores/th135_17.txt)</abbr><abbr title="th135_18.txt">[⬛](scores/th135_18.txt)</abbr><abbr title="th135_19.txt">[⬛](scores/th135_19.txt)</abbr>

🔨东方辉针城：<abbr title="th14_01.txt">[⬛](scores/th14_01.txt)</abbr><abbr title="th14_02.txt">[⬛](scores/th14_02.txt)</abbr><abbr title="th14_03.txt">[⬛](scores/th14_03.txt)</abbr><abbr title="th14_04.txt">[⬛](scores/th14_04.txt)</abbr><abbr title="th14_05.txt">[⬛](scores/th14_05.txt)</abbr><abbr title="th14_06.txt">[⬛](scores/th14_06.txt)</abbr><abbr title="th14_07.txt">[⬛](scores/th14_07.txt)</abbr><abbr title="th14_08.txt">[⬛](scores/th14_08.txt)</abbr><abbr title="th14_09.txt">[⬛](scores/th14_09.txt)</abbr><abbr title="th14_10.txt">[⬛](scores/th14_10.txt)</abbr><abbr title="th14_11.txt">[⬛](scores/th14_11.txt)</abbr><abbr title="th14_12.txt">[⬛](scores/th14_12.txt)</abbr><abbr title="th14_13.txt">[⬛](scores/th14_13.txt)</abbr><abbr title="th14_14.txt">[⬛](scores/th14_14.txt)</abbr><abbr title="th14_15.txt">[⬛](scores/th14_15.txt)</abbr><abbr title="th14_16.txt">[⬛](scores/th14_16.txt)</abbr><abbr title="th14_17.txt">[⬛](scores/th14_17.txt)

👹弹幕天邪鬼：</abbr><abbr title="th143_01.txt">[⬛](scores/th143_01.txt)</abbr><abbr title="th143_02.txt">[⬛](scores/th143_02.txt)</abbr><abbr title="th143_03.txt">[⬛](scores/th143_03.txt)</abbr><abbr title="th143_04.txt">[⬛](scores/th143_04.txt)</abbr><abbr title="th143_05.txt">[⬛](scores/th143_05.txt)

🃏东方深秘录：</abbr><abbr title="th145_13.txt">[⬛](scores/th145_13.txt)</abbr><abbr title="th145_14.txt">[⬛](scores/th145_14.txt)</abbr><abbr title="th145_15.txt">[⬛](scores/th145_15.txt)</abbr><abbr title="th145_16.txt">[⬛](scores/th145_16.txt)</abbr><abbr title="th145_17.txt">[⬛](scores/th145_17.txt)</abbr><abbr title="th145_18.txt">[⬛](scores/th145_18.txt)</abbr><abbr title="th145_19.txt">[⬛](scores/th145_19.txt)</abbr><abbr title="th145_20.txt">[⬛](scores/th145_20.txt)</abbr><abbr title="th145_21.txt">[⬛](scores/th145_21.txt)</abbr><abbr title="th145_22.txt">[⬛](scores/th145_22.txt)</abbr><abbr title="th145_23.txt">[⬛](scores/th145_23.txt)</abbr><abbr title="th145_24.txt">[⬛](scores/th145_24.txt)</abbr><abbr title="th145_25.txt">[⬛](scores/th145_25.txt)</abbr><abbr title="th145_26.txt">[⬛](scores/th145_26.txt)</abbr><abbr title="th145_27.txt">[⬛](scores/th145_27.txt)</abbr><abbr title="th145_28.txt">[⬛](scores/th145_28.txt)</abbr><abbr title="th145_29.txt">[⬛](scores/th145_29.txt)</abbr><abbr title="th145_30.txt">[⬛](scores/th145_30.txt)</abbr><abbr title="th145PS4_02.txt">[⬛](scores/th145PS4_02.txt)</abbr><abbr title="th145PS4_03.txt">[⬛](scores/th145PS4_03.txt)</abbr><abbr title="th145PS4_04.txt">[⬛](scores/th145PS4_04.txt)</abbr><abbr title="th145PS4_05.txt">[⬛](scores/th145PS4_05.txt)</abbr><abbr title="th145PS4_06.txt">[⬛](scores/th145PS4_06.txt)</abbr><abbr title="th145PS4_07.txt">[⬛](scores/th145PS4_07.txt)</abbr><abbr title="th145PS4_08.txt">[⬛](scores/th145PS4_08.txt)</abbr>

💊东方绀珠传：<abbr title="th15_01.txt">[⬛](scores/th15_01.txt)</abbr><abbr title="th15_02.txt">[⬛](scores/th15_02.txt)</abbr><abbr title="th15_03.txt">[⬛](scores/th15_03.txt)</abbr><abbr title="th15_04.txt">[⬛](scores/th15_04.txt)</abbr><abbr title="th15_05.txt">[⬛](scores/th15_05.txt)</abbr><abbr title="th15_06.txt">[⬛](scores/th15_06.txt)</abbr><abbr title="th15_07.txt">[⬛](scores/th15_07.txt)</abbr><abbr title="th15_08.txt">[⬛](scores/th15_08.txt)</abbr><abbr title="th15_09.txt">[⬛](scores/th15_09.txt)</abbr><abbr title="th15_10.txt">[⬛](scores/th15_10.txt)</abbr><abbr title="th15_11.txt">[⬛](scores/th15_11.txt)</abbr><abbr title="th15_12.txt">[⬛](scores/th15_12.txt)</abbr><abbr title="th15_13.txt">[⬛](scores/th15_13.txt)</abbr><abbr title="th15_14.txt">[⬛](scores/th15_14.txt)</abbr><abbr title="th15_15.txt">[⬛](scores/th15_15.txt)</abbr><abbr title="th15_16.txt">[⬛](scores/th15_16.txt)</abbr><abbr title="th15_17.txt">[⬛](scores/th15_17.txt)

🥣东方凭依华：</abbr><abbr title="th155_13.txt">[⬛](scores/th155_13.txt)</abbr><abbr title="th155_20.txt">[⬛](scores/th155_20.txt)</abbr><abbr title="th155_21.txt">[⬛](scores/th155_21.txt)</abbr><abbr title="th155_22.txt">[⬛](scores/th155_22.txt)</abbr><abbr title="th155_23.txt">[⬛](scores/th155_23.txt)</abbr><abbr title="th155_24.txt">[⬛](scores/th155_24.txt)</abbr><abbr title="th155_25.txt">[⬛](scores/th155_25.txt)</abbr><abbr title="th155_26.txt">[⬛](scores/th155_26.txt)</abbr><abbr title="th155_27.txt">[⬛](scores/th155_27.txt)</abbr><abbr title="th155_28.txt">[⬛](scores/th155_28.txt)</abbr><abbr title="th155_29.txt">[⬛](scores/th155_29.txt)</abbr><abbr title="th155_30.txt">[⬛](scores/th155_30.txt)</abbr><abbr title="th155_31.txt">[⬛](scores/th155_31.txt)</abbr><abbr title="th155_32.txt">[⬛](scores/th155_32.txt)</abbr><abbr title="th155_33.txt">[⬛](scores/th155_33.txt)</abbr><abbr title="th155_34.txt">[⬛](scores/th155_34.txt)</abbr><abbr title="th155_35.txt">[⬛](scores/th155_35.txt)</abbr><abbr title="th155_36.txt">[⬛](scores/th155_36.txt)</abbr><abbr title="th155_37.txt">[⬛](scores/th155_37.txt)</abbr><abbr title="th155_38.txt">[⬛](scores/th155_38.txt)</abbr><abbr title="th155_39.txt">[⬛](scores/th155_39.txt)</abbr><abbr title="th155_40.txt">[⬛](scores/th155_40.txt)</abbr><abbr title="th155_41.txt">[⬛](scores/th155_41.txt)</abbr><abbr title="th155_42.txt">[⬛](scores/th155_42.txt)</abbr><abbr title="th155_43.txt">[⬛](scores/th155_43.txt)</abbr><abbr title="th155_44.txt">[⬛](scores/th155_44.txt)</abbr><abbr title="th155_45.txt">[⬛](scores/th155_45.txt)</abbr><abbr title="th155_46.txt">[⬛](scores/th155_46.txt)</abbr><abbr title="th155_47.txt">[⬛](scores/th155_47.txt)</abbr><abbr title="th155_48.txt">[⬛](scores/th155_48.txt)</abbr><abbr title="th155_49.txt">[⬛](scores/th155_49.txt)</abbr><abbr title="th155_50.txt">[⬛](scores/th155_50.txt)</abbr><abbr title="th155_51.txt">[⬛](scores/th155_51.txt)</abbr><abbr title="th155_52.txt">[⬛](scores/th155_52.txt)</abbr><abbr title="th155_53.txt">[⬛](scores/th155_53.txt)</abbr><abbr title="th155_54.txt">[⬛](scores/th155_54.txt)</abbr><abbr title="th155_55.txt">[⬛](scores/th155_55.txt)</abbr><abbr title="th155_56.txt">[⬛](scores/th155_56.txt)</abbr><abbr title="th155_57.txt">[⬛](scores/th155_57.txt)</abbr><abbr title="th155_58.txt">[⬛](scores/th155_58.txt)</abbr>

🚪东方天空璋：<abbr title="th16_01.txt">[⬛](scores/th16_01.txt)</abbr><abbr title="th16_02.txt">[⬛](scores/th16_02.txt)</abbr><abbr title="th16_03.txt">[⬛](scores/th16_03.txt)</abbr><abbr title="th16_04.txt">[⬛](scores/th16_04.txt)</abbr><abbr title="th16_05.txt">[⬛](scores/th16_05.txt)</abbr><abbr title="th16_06.txt">[⬛](scores/th16_06.txt)</abbr><abbr title="th16_07.txt">[⬛](scores/th16_07.txt)</abbr><abbr title="th16_08.txt">[⬛](scores/th16_08.txt)</abbr><abbr title="th16_09.txt">[⬛](scores/th16_09.txt)</abbr><abbr title="th16_10.txt">[⬛](scores/th16_10.txt)</abbr><abbr title="th16_11.txt">[⬛](scores/th16_11.txt)</abbr><abbr title="th16_12.txt">[⬛](scores/th16_12.txt)</abbr><abbr title="th16_13.txt">[⬛](scores/th16_13.txt)</abbr><abbr title="th16_14.txt">[⬛](scores/th16_14.txt)</abbr><abbr title="th16_15.txt">[⬛](scores/th16_15.txt)</abbr><abbr title="th16_16.txt">[⬛](scores/th16_16.txt)</abbr><abbr title="th16_17.txt">[⬛](scores/th16_17.txt)

📱秘封噩梦日记：</abbr><abbr title="th165_01.txt">[⬛](scores/th165_01.txt)</abbr><abbr title="th165_02.txt">[⬛](scores/th165_02.txt)</abbr><abbr title="th165_03.txt">[⬛](scores/th165_03.txt)</abbr><abbr title="th165_04.txt">[⬛](scores/th165_04.txt)</abbr><abbr title="th165_05.txt">[⬛](scores/th165_05.txt)</abbr><abbr title="th165_06.txt">[⬛](scores/th165_06.txt)</abbr>

🏺东方鬼形兽：<abbr title="th17_01.txt">[⬛](scores/th17_01.txt)</abbr><abbr title="th17_02.txt">[⬛](scores/th17_02.txt)</abbr><abbr title="th17_03.txt">[⬛](scores/th17_03.txt)</abbr><abbr title="th17_04.txt">[⬛](scores/th17_04.txt)</abbr><abbr title="th17_05.txt">[⬛](scores/th17_05.txt)</abbr><abbr title="th17_06.txt">[⬛](scores/th17_06.txt)</abbr><abbr title="th17_07.txt">[⬛](scores/th17_07.txt)</abbr><abbr title="th17_08.txt">[⬛](scores/th17_08.txt)</abbr><abbr title="th17_08.txt">[⬛](scores/th17_08.txt)</abbr><abbr title="th17_10.txt">[⬛](scores/th17_10.txt)</abbr><abbr title="th17_11.txt">[⬛](scores/th17_11.txt)</abbr><abbr title="th17_12.txt">[⬛](scores/th17_12.txt)</abbr><abbr title="th17_13.txt">[⬛](scores/th17_13.txt)</abbr><abbr title="th17_14.txt">[⬛](scores/th17_14.txt)</abbr><abbr title="th17_14.txt">[⬛](scores/th17_14.txt)</abbr><abbr title="th17_16.txt">[⬛](scores/th17_16.txt)</abbr><abbr title="th17_17.txt">[⬛](scores/th17_17.txt)</abbr>

🛢️东方刚欲异闻：<abbr title="th175_01.txt">[⬛](scores/th175_01.txt)</abbr><abbr title="th175_02.txt">[⬛](scores/th175_02.txt)</abbr><abbr title="th175_03.txt">[⬛](scores/th175_03.txt)</abbr><abbr title="th175_04.txt">[⬛](scores/th175_04.txt)</abbr><abbr title="th175_09.txt">[⬛](scores/th175_09.txt)</abbr><abbr title="th175_25.txt">[⬛](scores/th175_25.txt)</abbr><abbr title="th175_26.txt">[⬛](scores/th175_26.txt)</abbr>

💰东方虹龙洞：<abbr title="th18_01.txt">[⬛](scores/th18_01.txt)</abbr><abbr title="th18_02.txt">[⬛](scores/th18_02.txt)</abbr><abbr title="th18_03.txt">[⬛](scores/th18_03.txt)</abbr><abbr title="th18_04.txt">[⬛](scores/th18_04.txt)</abbr><abbr title="th18_05.txt">[⬛](scores/th18_05.txt)</abbr><abbr title="th18_06.txt">[⬛](scores/th18_06.txt)</abbr><abbr title="th18_07.txt">[⬛](scores/th18_07.txt)</abbr><abbr title="th18_08.txt">[⬛](scores/th18_08.txt)</abbr><abbr title="th18_09.txt">[⬛](scores/th18_09.txt)</abbr><abbr title="th18_10.txt">[⬛](scores/th18_10.txt)</abbr><abbr title="th18_11.txt">[⬛](scores/th18_11.txt)</abbr><abbr title="th18_12.txt">[⬛](scores/th18_12.txt)</abbr><abbr title="th18_13.txt">[⬛](scores/th18_13.txt)</abbr><abbr title="th18_14.txt">[⬛](scores/th18_14.txt)</abbr><abbr title="th18_15.txt">[⬛](scores/th18_15.txt)</abbr><abbr title="th18_16.txt">[⬛](scores/th18_16.txt)</abbr><abbr title="th18_17.txt">[⬛](scores/th18_17.txt)

💵弹幕狂们的黑市：</abbr><abbr title="th185_01.txt">[⬛](scores/th185_01.txt)</abbr><abbr title="th185_02.txt">[⬛](scores/th185_02.txt)</abbr><abbr title="th185_03.txt">[⬛](scores/th185_03.txt)</abbr><abbr title="th185_04.txt">[⬛](scores/th185_04.txt)</abbr><abbr title="th185_05.txt">[⬛](scores/th185_05.txt)</abbr><abbr title="th185_06.txt">[⬛](scores/th185_06.txt)</abbr>

💀东方兽王园：<abbr title="th19_01.txt">[⬛](scores/th19_01.txt)</abbr><abbr title="th19_02.txt">[⬛](scores/th19_02.txt)</abbr><abbr title="th19_03.txt">[⬛](scores/th19_03.txt)</abbr><abbr title="th19_04.txt">[⬛](scores/th19_04.txt)</abbr><abbr title="th19_05.txt">[⬛](scores/th19_05.txt)</abbr><abbr title="th19_06.txt">[⬛](scores/th19_06.txt)</abbr><abbr title="th19_07.txt">[⬛](scores/th19_07.txt)</abbr><abbr title="th19_08.txt">[⬛](scores/th19_08.txt)</abbr><abbr title="th19_09.txt">[⬛](scores/th19_09.txt)</abbr><abbr title="th19_21.txt">[⬛](scores/th19_21.txt)</abbr><abbr title="th19_22.txt">[⬛](scores/th19_22.txt)</abbr><abbr title="th19_23.txt">[⬛](scores/th19_23.txt)</abbr><abbr title="th19_24.txt">[⬛](scores/th19_24.txt)</abbr>

🏜️东方锦上京：<abbr title="th20_01.txt">[⬛](scores/th20_01.txt)</abbr><abbr title="th20_02.txt">[⬛](scores/th20_02.txt)</abbr><abbr title="th20_03.txt">[⬛](scores/th20_03.txt)</abbr><abbr title="th20_04.txt">[⬛](scores/th20_04.txt)</abbr><abbr title="th20_05.txt">[⬛](scores/th20_05.txt)</abbr><abbr title="th20_06.txt">[⬛](scores/th20_06.txt)</abbr><abbr title="th20_07.txt">[⬛](scores/th20_07.txt)</abbr><abbr title="th20_08.txt">[⬛](scores/th20_08.txt)</abbr><abbr title="th20_09.txt">[⬛](scores/th20_09.txt)</abbr><abbr title="th20_10.txt">[⬛](scores/th20_10.txt)</abbr><abbr title="th20_11.txt">[⬛](scores/th20_11.txt)</abbr><abbr title="th20_12.txt">[⬛](scores/th20_12.txt)</abbr><abbr title="th20_13.txt">[⬛](scores/th20_13.txt)</abbr><abbr title="th20_14.txt">[⬛](scores/th20_14.txt)</abbr><abbr title="th20_15.txt">[⬛](scores/th20_15.txt)</abbr><abbr title="th20_16.txt">[⬛](scores/th20_16.txt)</abbr><abbr title="th20_17.txt">[⬛](scores/th20_17.txt)</abbr><abbr title="th20_18.txt">[⬛](scores/th20_18.txt)</abbr>

### 规范

#### 曲谱文件

文件/标签命名采用“先到先得”的原则。如果命名时发现了冲突/歧义，请将引起歧义的原有命名和你即将采用的命名一并改成**有标记**的名称。

记谱使用[jianpu-ly](https://github.com/ssb22/jianpu-ly/blob/master/README_zh-Hans.md)语言。原则上，只记**具有特征性的，响度最大**的**线性**（不要有重叠的（当然，有一点重叠的话就分两段记下来就行了））旋律。记谱时，以**小调的一度音为`6,`；大调的一度音为`1`**（就是一般人听到这段声音后凭直觉写出来的样子），以此类推为原则。无需记录重复的旋律，如果完全一样的话。同一文件中，不同的旋律之用`NextScore`分割。

例如，[东方主旋律](https://thbwiki.cc/Theme_of_Eastern_Story)以此规则转写出来是：

`,6 2 3 5 3 2 ,6 2 3 5 3 2 ,6 2 3 5 3 2 ,7 1 ,7 ,5`

以[th01_01.txt](scores/th01_01.txt)（A Sacred Lot）为例，一般的曲谱文件结构应该是这样：

```
%th01_02.txt
MBID=310b3b07-ec9f-3e88-9fd8-529c17478179
title=永遠の巫女
type=work
tag=th01,东方灵异传,东方,东方原曲,ZUN,东方旧作原曲,东方整数作原曲
usertag=th01
alias=永远之巫女,永远的巫女
transcriber=Francium-223
%--
4/4
subtitle=intro
6 - - - 4 - - - 5 - - - 3 - - -
NextScore
subtitle=verse
0. 1q 1q 2q 3 R2{ ,6. 1 2q 3 ,6. 1 2q 3 ,6. 1 2q ,7 } A{ ,7. 1. 2q 3q | ,7. 4 4q 3q 2q }
NextScore
subtitle=verse
R2{ ,7. 1. 2 } A{ ,7 1q ,7 ,6q ,5 ,6. 3. ,6 ,6. 3q ~ 3 - | ,7 1q  2 5q 2 1. ,7. ,6 ,7 1q 2q ~ 2 - }
NextScore
subtitle=verse
R{ 1 - ,7 ,6q ,7q ~ ,7 - ,6 ,5q ,6q ~ ,6 - - - - - ,6 ,7 } R{ 3 - 2 1q 2q ~ 2 - 1 ,7q 1q ~ 1q ,6q ~ ,6 - - - - ,6 ,7 }
NextScore
subtitle=outro
1 - - - 2 - - - 7 - - - 3 - - -
%END

```

|行|解释|
|---|---|
|%th01_02.txt|这个文件的**文件名**为`th01_01.txt`。注意所有曲谱都应是`scores`的一级子文件，且统一以“.txt”结尾。**由脚本自动补充**。|
|MBID=310b3b07-ec9f-3e88-9fd8-529c17478179|这首歌在[MusicBrainz](https://musicbrainz.org/)中唯一且确定的标识符（**MBID**）为`310b3b07-ec9f-3e88-9fd8-529c17478179`。|
|title=永遠の巫女|这首歌的**标题**为`永遠の巫女`。此处应填写其**最早发布版本**的**现时通用名称**，基于**名从主人**原则。|
|type=work|这首歌在[MusicBrainz](https://musicbrainz.org/)中被**标记为**`work`。一般默认是`work`，但是有的旋律不一样的改编曲也被其算作同一`work`下的`recording`。这种情况下应填`recording`。|
|tag=th01,东方灵异传,东方,东方原曲,ZUN,东方旧作原曲,东方整数作原曲|这首歌的**标签**有`th01`和`东方灵异传`、`东方`、`东方原曲`、`ZUN`、`东方旧作原曲`、`东方整数作原曲`。**由脚本根据`usertag`自动生成，所以一般不用动。**根据这些字符串，会自动在`by_tag`中生成快捷方式。|
|usertag=th01|**用户填写的这首歌的标签**。注意这是你要填的，它会决定`tag`的生成。|
|alias=永远之巫女,永远的巫女|这首歌的**别名**有：`永远之巫女`、`永远的巫女`，可以填写多个。包括但不仅限于：可选的**其他拼写**方式、**转写**、**翻译**、在社群中有一定影响力的**别名**。|
|transcriber=Francium-223|**转写者**为[Francium-223](https://github.com/Francium-223/)。|
|%---|**分割元数据和曲谱的线**，注意百分号后至少有两个杠。|
|之后的行|转写的**简谱**。关于语法，更多详情见[此处](https://github.com/ssb22/jianpu-ly/blob/master/README_zh-Hans.md)。|
|%END|文件的**结束标记**。**不出意外的话，由脚本自动补充**。|

以下元数据是可选的，写了之后可以在**jianpu-ly**编译时被渲染出来。

```
subtitle=副标题
subsubtitle=三级标题
instrument=乐器
poet=作词人
composer=作曲家
meter=节拍
arranger=编曲家
tagline=标语
copyright=版权
piece=作品
opus=作品编号
```

除此以外，元数据部分还可以其他注释，例如：

```
%TODO:（如果有的话）
%欢迎补充
```

，会统一被放在文件名的正下方。

#### 元数据（高级）

所有元数据（包括data.json）均由脚本根据曲谱文件里的数据自动生成，因此一般情况下不要乱动。

以[th01_02.json](meta/th01_02.json)为例：

```
{
    "310b3b07-ec9f-3e88-9fd8-529c17478179": {
        "file": "th01_02.txt",
        "type": "work",
        "title": "永遠の巫女",
        "usertag": [
            "th01"
        ],
        "tag": [
            "th01",
            "东方灵异传",
            "东方",
            "东方原曲",
            "ZUN",
            "东方旧作原曲",
            "东方整数作原曲"
        ],
        "alias": [
            "永远之巫女",
            "永远的巫女"
        ],
        "transcriber": [
            "Francium-223"
        ]
    }
}
```

其他键在其各自文件夹中建立索引，如果有一个`"foo": ["bar"]`，索引会建立在一个叫`by_foo`的文件夹。**除`file`、`title`外，其他键对应的值均为列表。**

#### 提示

一般来说，一些标签具有蕴涵关系，可以只写一个标签也能自动生成对应的标签。（见[tag_imply.json](tag_imply.json)和[tag_equal.json](tag_equal.json)。）一般来说，如果有100首含有标签`foo`的歌，其中有99首歌都同时也有标签`bar`，有1首歌没有标签`bar`，那么应该在[tag_imply.json](tag_imply.json)里增加一项

```
"bar":
    {
        "foo": {}
    }
```

，并在曲谱中给那首没有`bar`的歌标注：

`tag=foo,!bar`

### 贡献者

<a href="https://github.com/Francium-223"><img src="https://avatars.githubusercontent.com/u/286506063?s=400&v=4" height="40px" width="40px"></a>

### 鸣谢

[ssb22/jianpu-ly](https://github.com/ssb22/jianpu-ly/blob/master/README_zh-Hans.md)：规范的记谱语言

[MusicBrainz](https://musicbrainz.org/)：为歌曲提供唯一且确定的序号

### 友情链接

[ACGMuse](https://www.acgmuse.com/)

[Justice Eternal（zytx121/je）](https://github.com/zytx121/je)