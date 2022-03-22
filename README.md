# 基于FastSpeech2的情感语音合成系统- PyTorch实现

这是基于FastSpeech2[**FastSpeech 2: Fast and High-Quality End-to-End Text to Speech**](https://arxiv.org/abs/2006.04558v1). 的情感语音合成系统 
这个实现是基于 [ming024的FastSpeech2](https://github.com/ming024/FastSpeech2) 


![](./img/model.png)

# 更新
- 2022/3/22: 未实现情感化语音，但是修复原作者FastSpeech2使用AISHELL3训练模型合成中文时无法跳过阿拉伯数字的问题

# 音频样本
 

# 快速开始

## 依赖项
安装python依赖项
```
pip install -r requirements.txt
```

## 推理

下载 [预训练模型](https://drive.google.com/drive/folders/1DOhZGlTLMbbAAFZmZGDdc77kz1PloS7F?usp=sharing) 并放置到文件夹``output/ckpt/LJSpeech/``,  ``output/ckpt/AISHELL3``, or ``output/ckpt/LibriTTS/``.

对于英语单人TTS（LJSpeech），运行
```
python synthesize.py --text "YOUR_DESIRED_TEXT" --restore_step 900000 --mode single --dataset LJSpeech
```

对于普通话多语者TTS（AISHELL3），运行
```
python synthesize.py --text "大家好" --speaker_id SPEAKER_ID --restore_step 600000 --mode single --dataset AISHELL3
```

对于英语多语者TTS（LibriTTS），运行
```
python3 synthesize.py --text "YOUR_DESIRED_TEXT"  --speaker_id SPEAKER_ID --restore_step 800000 --mode single --dataset LibriTTS
```

生成的话语将被放入 ``output/result/``。



## 批量推理
支持批量推理，请运行

```
python synthesize.py --source preprocessed_data/LJSpeech/val.txt --restore_step 900000 --mode batch 
```
要合成的所有话语 ``preprocessed_data/LJSpeech/val.txt``

## 可控性
可以通过指定所需的音调/能量/持续时间比率来控制合成话语的音调/音量/说话速率。例如，可以将语速提高 20 %，将音量降低 20 %。

```
python synthesize.py --text "YOUR_DESIRED_TEXT" --restore_step 900000 --mode single --dataset LJSpeech --duration_control 0.8 --energy_control 0.8
```

# 训练

## 数据集

支持的数据集：

- [LJSpeech](https://keithito.com/LJ-Speech-Dataset/): 一个单说话人英语数据集，由 13100 个女性说话者的短音频片段组成，这些音频片段来自 7 个非小说类书籍，总共大约 24 小时。
- [AISHELL-3](http://www.aishelltech.com/aishell_3): 一个普通话 TTS 数据集，有 218 位男性和女性说话者，总共大约 85 小时。
- [LibriTTS](https://research.google/tools/datasets/libri-tts/): 一个多说话者英语数据集，包含 2456 位说话者 585 小时的演讲。

下面我们以 LJSpeech 为例：

## 预处理
 
首先运行:
```
python prepare_align.py --dataset LJSpeech
```
然后进行对齐：

如论文中所述, [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/en/latest/) (MFA) 用于获得话语和音素序列之间的对齐。
[这里](https://drive.google.com/drive/folders/1DBRkALpPd6FL9gjHMmMEdHODmkgNIIK4?usp=sharing) 提供了支持的数据集的对齐方式。
您必须将文件解压缩为 ``preprocessed_data/LJSpeech/TextGrid/``。

之后，运行预处理脚本：
```
python preprocess.py config/LJSpeech/preprocess.yaml
```

或者，您可以自己对齐语料库。
下载官方 MFA 包并运行：
```
./montreal-forced-aligner/bin/mfa_align raw_data/LJSpeech/ lexicon/librispeech-lexicon.txt english preprocessed_data/LJSpeech
```
或者
```
./montreal-forced-aligner/bin/mfa_train_and_align raw_data/LJSpeech/ lexicon/librispeech-lexicon.txt preprocessed_data/LJSpeech
```

对齐语料库后，运行预处理脚本:
```
python preprocess.py config/LJSpeech/preprocess.yaml
```

## 训练

训练模型：
```
python train.py --dataset LJSpeech
```

# TensorBoard

使用：
```
tensorboard --logdir output/log/LJSpeech
```

在您的本地主机上服务 TensorBoard。
显示了损失曲线、合成的梅尔谱图和音频：

![](./img/tensorboard_loss.png)
![](./img/tensorboard_spec.png)
![](./img/tensorboard_audio.png)

# 实现问题



# 参考
- [FastSpeech 2: Fast and High-Quality End-to-End Text to Speech](https://arxiv.org/abs/2006.04558), Y. Ren, *et al*.
- [xcmyz's FastSpeech implementation](https://github.com/xcmyz/FastSpeech)
- [TensorSpeech's FastSpeech 2 implementation](https://github.com/TensorSpeech/TensorflowTTS)
- [rishikksh20's FastSpeech 2 implementation](https://github.com/rishikksh20/FastSpeech2)

# 引文
```
@INPROCEEDINGS{chien2021investigating,
  author={Chien, Chung-Ming and Lin, Jheng-Hao and Huang, Chien-yu and Hsu, Po-chun and Lee, Hung-yi},
  booktitle={ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)}, 
  title={Investigating on Incorporating Pretrained and Learnable Speaker Representations for Multi-Speaker Multi-Style Text-to-Speech}, 
  year={2021},
  volume={},
  number={},
  pages={8588-8592},
  doi={10.1109/ICASSP39728.2021.9413880}}
```
