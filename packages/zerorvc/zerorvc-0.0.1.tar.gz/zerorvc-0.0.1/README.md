# ZeroRVC

Run Retrieval-based Voice Conversion training and inference with ease.

## Features

- [x] Dataset Preparation / Upload to Hugging Face Datasets
- [x] Accelerate with Hugging Face Accelerate
- [x] Easy Trainer API
- [ ] Inference API

## Training

```py
import os
from accelerate import Accelerator
from tqdm import tqdm
from zerorvc import RVCTrainer, prepare

HF_TOKEN = os.environ.get("HF_TOKEN")
accelerator = Accelerator()

dataset = prepare(
    "./my-voices", 
    hubert="./models/hubert_base.pt", rmvpe="./models/rmvpe.pt", 
    accelerator=accelerator
)
dataset.push_to_hub("my-rvc-dataset", token=HF_TOKEN)

epochs = 100
trainer = RVCTrainer(checkpoint_dir="./checkpoints")
training = tqdm(
    trainer.train(
        dataset=dataset["train"],
        resume_from=trainer.latest_checkpoint(),
        epochs=epochs, batch_size=8, accelerator=accelerator
    ),
    desc="Training", total=epochs
)
for checkpoint in training:
    training.set_description(
        f"Epoch {checkpoint.epoch}/{epochs} loss: (gen: {checkpoint.loss_gen:.4f}, fm: {checkpoint.loss_fm:.4f}, mel: {checkpoint.loss_mel:.4f}, kl: {checkpoint.loss_kl:.4f}, disc: {checkpoint.loss_disc:.4f})"
    )
    if checkpoint.epoch % 2 == 0:
        checkpoint.save(checkpoint_dir=trainer.checkpoint_dir)
        checkpoint.G.push_to_hub("my-rvc-model", token=HF_TOKEN)
print("Training completed.")
```
