## 简介

**jianpu-db**是基于[jianpu-ly](https://github.com/ssb22/jianpu-ly/blob/master/README_zh-Hans.md)语法和[MusicBrainz](https://musicbrainz.org/)唯一标识符构建的、面向大语言模型训练及严谨学术研究的高度规范化可读数字音乐简谱旋律数据集。旨在解决大语言模型面对简谱束手无措的痛点、填补网络上以简谱记载的旋律信息量不足、规范度不够的缺口。

本项目正在开发基础架构中，亟待能人异士的加入（无论是开发代码还是转写旋律）……

## 仓库结构

[data.json](data.json)：存储歌曲信息、标签的文件。

[scores](scores/)：存放曲谱的文件夹。

[tag_imply.json](tag_imply.json)：标签间的蕴涵关系，如`东方星莲船`蕴涵`东方原曲`。

[by_title](by_title/)：按标题寻找曲谱（通过软链接）的文件夹。

[by_tag](by_artist/)：按标签寻找曲谱（通过软链接）的文件夹。同一首曲子可以有多个标签。

## 目前进度

（转写完成后，请将对应位置的黑方块“⬛”换成前面的emoji。）

### 东方原曲：

☯️东方灵异传：<abbr title="th01_01.txt">[☯️](scores/th01_01.txt)</abbr><abbr title="th01_02.txt">[⬛](scores/th01_02.txt)</abbr><abbr title="th01_03.txt">[⬛](scores/th01_03.txt)</abbr><abbr title="th01_04.txt">[⬛](scores/th01_04.txt)</abbr><abbr title="th01_05.txt">[⬛](scores/th01_05.txt)</abbr><abbr title="th01_06.txt">[⬛](scores/th01_06.txt)</abbr><abbr title="th01_07.txt">[⬛](scores/th01_07.txt)</abbr><abbr title="th01_08.txt">[⬛](scores/th01_08.txt)</abbr><abbr title="th01_09.txt">[⬛](scores/th01_09.txt)</abbr><abbr title="th01_10.txt">[⬛](scores/th01_10.txt)</abbr><abbr title="th01_11.txt">[⬛](scores/th01_11.txt)</abbr><abbr title="th01_12.txt">[⬛](scores/th01_12.txt)</abbr><abbr title="th01_13.txt">[⬛](scores/th01_13.txt)</abbr><abbr title="th01_14.txt">[⬛](scores/th01_14.txt)</abbr><abbr title="th01_15.txt">[⬛](scores/th01_15.txt)</abbr>

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

🔨弹幕天邪鬼：</abbr><abbr title="th143_01.txt">[⬛](scores/th143_01.txt)</abbr><abbr title="th143_02.txt">[⬛](scores/th143_02.txt)</abbr><abbr title="th143_03.txt">[⬛](scores/th143_03.txt)</abbr><abbr title="th143_04.txt">[⬛](scores/th143_04.txt)</abbr><abbr title="th143_05.txt">[⬛](scores/th143_05.txt)

🃏东方深秘录：</abbr><abbr title="th145_13.txt">[⬛](scores/th145_13.txt)</abbr><abbr title="th145_14.txt">[⬛](scores/th145_14.txt)</abbr><abbr title="th145_15.txt">[⬛](scores/th145_15.txt)</abbr><abbr title="th145_16.txt">[⬛](scores/th145_16.txt)</abbr><abbr title="th145_17.txt">[⬛](scores/th145_17.txt)</abbr><abbr title="th145_18.txt">[⬛](scores/th145_18.txt)</abbr><abbr title="th145_19.txt">[⬛](scores/th145_19.txt)</abbr><abbr title="th145_20.txt">[⬛](scores/th145_20.txt)</abbr><abbr title="th145_21.txt">[⬛](scores/th145_21.txt)</abbr><abbr title="th145_22.txt">[⬛](scores/th145_22.txt)</abbr><abbr title="th145_23.txt">[⬛](scores/th145_23.txt)</abbr><abbr title="th145_24.txt">[⬛](scores/th145_24.txt)</abbr><abbr title="th145_25.txt">[⬛](scores/th145_25.txt)</abbr><abbr title="th145_26.txt">[⬛](scores/th145_26.txt)</abbr><abbr title="th145_27.txt">[⬛](scores/th145_27.txt)</abbr><abbr title="th145_28.txt">[⬛](scores/th145_28.txt)</abbr><abbr title="th145_29.txt">[⬛](scores/th145_29.txt)</abbr><abbr title="th145_30.txt">[⬛](scores/th145_30.txt)</abbr><abbr title="th145PS4_02.txt">[⬛](scores/th145PS4_02.txt)</abbr><abbr title="th145PS4_03.txt">[⬛](scores/th145PS4_03.txt)</abbr><abbr title="th145PS4_04.txt">[⬛](scores/th145PS4_04.txt)</abbr><abbr title="th145PS4_05.txt">[⬛](scores/th145PS4_05.txt)</abbr><abbr title="th145PS4_06.txt">[⬛](scores/th145PS4_06.txt)</abbr><abbr title="th145PS4_07.txt">[⬛](scores/th145PS4_07.txt)</abbr><abbr title="th145PS4_08.txt">[⬛](scores/th145PS4_08.txt)</abbr>

🌕东方绀珠传：<abbr title="th15_01.txt">[⬛](scores/th15_01.txt)</abbr><abbr title="th15_02.txt">[⬛](scores/th15_02.txt)</abbr><abbr title="th15_03.txt">[⬛](scores/th15_03.txt)</abbr><abbr title="th15_04.txt">[⬛](scores/th15_04.txt)</abbr><abbr title="th15_05.txt">[⬛](scores/th15_05.txt)</abbr><abbr title="th15_06.txt">[⬛](scores/th15_06.txt)</abbr><abbr title="th15_07.txt">[⬛](scores/th15_07.txt)</abbr><abbr title="th15_08.txt">[⬛](scores/th15_08.txt)</abbr><abbr title="th15_09.txt">[⬛](scores/th15_09.txt)</abbr><abbr title="th15_10.txt">[⬛](scores/th15_10.txt)</abbr><abbr title="th15_11.txt">[⬛](scores/th15_11.txt)</abbr><abbr title="th15_12.txt">[⬛](scores/th15_12.txt)</abbr><abbr title="th15_13.txt">[⬛](scores/th15_13.txt)</abbr><abbr title="th15_14.txt">[⬛](scores/th15_14.txt)</abbr><abbr title="th15_15.txt">[⬛](scores/th15_15.txt)</abbr><abbr title="th15_16.txt">[⬛](scores/th15_16.txt)</abbr><abbr title="th15_17.txt">[⬛](scores/th15_17.txt)

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

一般的曲谱文件结构应该是这样：

```
%TODO:（如果有的话）
%（该曲谱的文件名）
MBID=这首歌在MusicBrainz中对应的work编号（识别的唯一编码）
title=标题
transcriber=转写者（如果你想写的话）
tag=这首歌的标签，像data.json里那样写（如果你想写的话）
alias=这首歌的别名，像data.json里那样写（如果你想写的话）
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
%---（分割元数据和曲谱的线，至少两个杠）
（你的曲谱）
```

以[th01_01.txt](scores/th01_01.txt)（A Sacred Lot）为例子：

```
%th01_01.txt
MBID=52e3b2d1-80ff-35a7-b11f-f9342c08f22d
title=A Sacred Lot
transcriber=Francium-223
%--
4/4
,6s 3s ,6s 2s 1s ,7s ,6s 3s 2s 1s ,7s ,5s 2s 1s 5s 3s ,6s ,7s 1s ,6s 3s 2s 1s 2s 3s ,6s 2s ,6s 1s ,6s 7s ,6s
NextScore
6 - 7 - 1' - - - 7 - 2' - 1' - - - 7 - 2' ~ q2' ~ s2' d1' d7 | 1' - - - 7 - 2' - 5 - - - 3' - 7' -
NextScore
0 3 6 7 R{ 1' 7 6 2' 1' 7 6 5 6 3' 7 1' 0 3 6 7 1' 7 6 2' 1' 7 6 3 7 1' 2' 3' 0 3 6 7 1' 7 6 3 2' 1' 7 1' 1' 7 2' 3' 0 3' 2' 1' 1' 7 6 3 2' 1' 7 5 6 3 7 1' 0 3 6 7 }
```

MBID、tag、alias等可以不写（当然如果会写最好），提交后由开发者补充。

#### data.json（高级）

因为本数据集记的是旋律，在[MusicBrainz](https://musicbrainz.org/)中的索引应以**work**为单位。如需声明某首歌不属于某一蕴涵的tag（如：属于`ZUN`但不属于`东方原曲`），请在data.json中这样写：

`tag: ["ZUN", "!东方"]`

### 贡献者

<a href="https://github.com/Francium-223"><img src="https://avatars.githubusercontent.com/u/286506063?s=400&v=4" height="40px" width="40px"></a>

### 鸣谢

[ssb22/jianpu-ly](https://github.com/ssb22/jianpu-ly/blob/master/README_zh-Hans.md)：规范的记谱语言

[MusicBrainz](https://musicbrainz.org/)：为歌曲提供唯一且确定的序号

[Touhou Midi Collection](https://github.com/AyHa1810/touhou-midi-collection)：提供东方原曲MIDI

### 友情链接

[ACGMuse](https://www.acgmuse.com/)

[Justice Eternal（zytx121/je）](https://github.com/zytx121/je)