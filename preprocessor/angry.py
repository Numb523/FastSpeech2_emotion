import os

import librosa
import numpy as np
import soundfile as sf
from tqdm import tqdm

from text import _clean_text


def prepare_align(config):
    in_dir = config["path"]["corpus_path"]
    out_dir = config["path"]["raw_path"]
    sampling_rate = config["preprocessing"]["audio"]["sampling_rate"]
    #max_wav_value = config["preprocessing"]["audio"]["max_wav_value"]
    cleaners = config["preprocessing"]["text"]["text_cleaners"]
    speaker = "Angry"
    with open(os.path.join(in_dir, "metadata.csv"), encoding="utf-8") as f:
        for line in tqdm(f):
            parts = line.strip().split(" | ")
            base_name = parts[0]
            text = parts[1]
            text = _clean_text(text, cleaners)

            wav_path = os.path.join(in_dir, "wavs", "{}".format(base_name))
            if os.path.exists(wav_path):
                os.makedirs(os.path.join(out_dir, speaker), exist_ok=True)
                wav, _ = librosa.load(wav_path, sampling_rate)
                wav = wav / max(abs(wav)) #* max_wav_value
                sf.write(
                    os.path.join(out_dir, speaker, "{}".format(base_name)),
                    wav,
                    sampling_rate,
                    subtype='PCM_16'
                )
                base_name = base_name.strip().split(".")
                with open(
                    os.path.join(out_dir, speaker, "{}.lab".format(base_name[0])),
                    "w",
                ) as f1:
                    f1.write(text)