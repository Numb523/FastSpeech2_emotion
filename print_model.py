from model import FastSpeech2, ScheduledOptim
from utils.tools import get_configs_of

preprocess_config, model_config, train_config = get_configs_of("AISHELL3")

print(FastSpeech2(preprocess_config, model_config))