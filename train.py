"""
BROS
Copyright 2022-present NAVER Corp.
Apache License v2.0
"""

import os

import torch
from pytorch_lightning import Trainer
from lightning_fabric.utilities.seed import seed_everything
from pytorch_lightning.callbacks import ModelCheckpoint

from lightning_modules.bros_bies_module import BROSBIESModule
from lightning_modules.bros_bio_module import BROSBIOModule
from lightning_modules.bros_spade_module import BROSSPADEModule
from lightning_modules.bros_spade_rel_module import BROSSPADERELModule
from lightning_modules.data_modules.bros_data_module import BROSDataModule
from utils import get_callbacks, get_config, get_loggers, get_plugins


def main():
    torch.set_float32_matmul_precision('medium')
    
    checkpoint_callback = ModelCheckpoint(
        save_top_k=5,
        monitor="f1",
        mode="max",
        dirpath="checkpoints/",
        filename="spade-{epoch:02d}-{f1:.2f}",
    )
    cfg = get_config()
    print(cfg)

    os.environ["CUDA_LAUNCH_BLOCKING"] = "1"  # prevent deadlock with tokenizer
    os.environ["TORCH_USE_CUDA_DSA"] = "1"  # prevent deadlock with tokenizer
    os.environ["TOKENIZERS_PARALLELISM"] = "false"  # prevent deadlock with tokenizer
    seed_everything(cfg.seed)

    callbacks = get_callbacks(cfg) #for checkpoints, no longer used
    # plugins = get_plugins(cfg)
    loggers = get_loggers(cfg)

    trainer = Trainer(
        accelerator=cfg.train.accelerator,
        # accelerator="cpu",
        # gpus=torch.cuda.device_count(),
        max_epochs=cfg.train.max_epochs,
        gradient_clip_val=cfg.train.clip_gradient_value,
        gradient_clip_algorithm=cfg.train.clip_gradient_algorithm,
        # callbacks=callbacks,
        callbacks=checkpoint_callback,
        default_root_dir="checkpoints/",
        enable_checkpointing=True,
        # plugins=plugins,
        # strategy="ddp_find_unused_parameters_true",
        sync_batchnorm=True,
        # precision=16 if cfg.train.use_fp16 else 32,
        # terminate_on_nan=False,
        # replace_sampler_ddp=False,
        # move_metrics_to_cpu=False,
        # progress_bar_refresh_rate=0,
        check_val_every_n_epoch=cfg.train.val_interval,
        logger=loggers,
        benchmark=cfg.cudnn_benchmark,
        deterministic=cfg.cudnn_deterministic,
        limit_val_batches=cfg.val.limit_val_batches,
    )

    if cfg.model.head == "bies":
        pl_module = BROSBIESModule(cfg)
    elif cfg.model.head == "bio":
        pl_module = BROSBIOModule(cfg)
    elif cfg.model.head == "spade":
        pl_module = BROSSPADEModule(cfg)
    elif cfg.model.head == "spade_rel":
        pl_module = BROSSPADERELModule(cfg)
    else:
        raise ValueError(f"Not supported head {cfg.model.head}")

    data_module = BROSDataModule(cfg, pl_module.net.tokenizer)

    trainer.fit(pl_module, datamodule=data_module)


if __name__ == "__main__":
    main()
