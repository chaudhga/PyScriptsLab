import gpt_2_simple as gpt2
import os
import requests
import tensorflow as tf

model_name = "124M"
if not os.path.isdir(os.path.join("models", model_name)):
    print("Downloading {model_name} model...")
    gpt2.download_gpt2(model_name=model_name)
file_name = 'trainingtext.txt'
if not os.path.isfile(file_name):
    print("missing file")

sess = gpt2.start_tf_sess()

gpt2.finetune(sess,
              file_name,
              model_name=model_name,
              steps=500)
