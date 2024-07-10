import os
from glob import glob
from logging import getLogger
from typing import Literal, Tuple
from pathlib import Path
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from accelerate import Accelerator
from datasets import Dataset
from tqdm import tqdm


from .synthesizer import commons
from .synthesizer.models import (
    SynthesizerTrnMs768NSFsid,
    MultiPeriodDiscriminator,
)

from .utils.losses import (
    discriminator_loss,
    feature_loss,
    generator_loss,
    kl_loss,
)
from .utils.mel_processing import mel_spectrogram_torch, spec_to_mel_torch
from .utils.data_utils import TextAudioCollateMultiNSFsid

logger = getLogger(__name__)


class RVCTrainer:
    def __init__(self, checkpoint_dir: str = None, sr: int = 40000):
        self.checkpoint_dir = checkpoint_dir
        self.sr = sr

    def latest_checkpoint(self):
        files_g = glob(os.path.join(self.checkpoint_dir, "G_*.pth"))
        if not files_g:
            return None
        latest_g = max(files_g, key=os.path.getctime)

        files_d = glob(os.path.join(self.checkpoint_dir, "D_*.pth"))
        if not files_d:
            return None
        latest_d = max(files_d, key=os.path.getctime)

        return latest_g, latest_d

    def train(
        self,
        dataset: Dataset,
        resume_from: Tuple[str, str] = None,
        accelerator: Accelerator = None,
        batch_size=1,
        epochs=10,
        lr=0.0001,
        lr_decay=0.999875,
        betas: Tuple[float, float] = (0.8, 0.99),
        eps=1e-9,
        use_spectral_norm=False,
        segment_size=12800,
        filter_length=2048,
        hop_length=400,
        inter_channels=192,
        hidden_channels=192,
        filter_channels=768,
        n_heads=2,
        n_layers=6,
        kernel_size=3,
        p_dropout=0.0,
        resblock: Literal["1", "2"] = "1",
        resblock_kernel_sizes: list[int] = [3, 7, 11],
        resblock_dilation_sizes: list[list[int]] = [[1, 3, 5], [1, 3, 5], [1, 3, 5]],
        upsample_initial_channel=512,
        upsample_rates: list[int] = [10, 10, 2, 2],
        upsample_kernel_sizes: list[int] = [16, 16, 4, 4],
        spk_embed_dim=109,
        gin_channels=256,
        n_mel_channels=125,
        win_length=2048,
        mel_fmin=0.0,
        mel_fmax: float = None,
        c_mel=45,
        c_kl=1.0,
    ):
        if not os.path.exists(self.checkpoint_dir):
            os.makedirs(self.checkpoint_dir)

        if accelerator is None:
            accelerator = Accelerator()

        G = SynthesizerTrnMs768NSFsid(
            spec_channels=filter_length // 2 + 1,
            segment_size=segment_size // hop_length,
            inter_channels=inter_channels,
            hidden_channels=hidden_channels,
            filter_channels=filter_channels,
            n_heads=n_heads,
            n_layers=n_layers,
            kernel_size=kernel_size,
            p_dropout=p_dropout,
            resblock=resblock,
            resblock_kernel_sizes=resblock_kernel_sizes,
            resblock_dilation_sizes=resblock_dilation_sizes,
            upsample_initial_channel=upsample_initial_channel,
            upsample_rates=upsample_rates,
            upsample_kernel_sizes=upsample_kernel_sizes,
            spk_embed_dim=spk_embed_dim,
            gin_channels=gin_channels,
            sr=self.sr,
        )
        D = MultiPeriodDiscriminator(use_spectral_norm=use_spectral_norm)

        optimizer_G = torch.optim.AdamW(
            G.parameters(),
            lr,
            betas=betas,
            eps=eps,
        )
        optimizer_D = torch.optim.AdamW(
            D.parameters(),
            lr,
            betas=betas,
            eps=eps,
        )

        if resume_from is not None:
            g_checkpoint, d_checkpoint = resume_from
            logger.info(f"Resuming from {g_checkpoint} and {d_checkpoint}")
            G.load_state_dict(torch.load(g_checkpoint, map_location=accelerator.device))
            D.load_state_dict(torch.load(d_checkpoint, map_location=accelerator.device))
            finished_epoch = int(Path(g_checkpoint).stem.split("_")[1])
        else:
            finished_epoch = 0

        scheduler_G = torch.optim.lr_scheduler.ExponentialLR(
            optimizer_G, gamma=lr_decay, last_epoch=finished_epoch - 1
        )
        scheduler_D = torch.optim.lr_scheduler.ExponentialLR(
            optimizer_D, gamma=lr_decay, last_epoch=finished_epoch - 1
        )

        dataset = dataset.with_format("torch", device=accelerator.device)
        loader = DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=False,
            collate_fn=TextAudioCollateMultiNSFsid(),
        )

        G, D, optimizer_G, optimizer_D, loader = accelerator.prepare(
            (G, D, optimizer_G, optimizer_D, loader)
        )

        G: torch.Module = G
        D: torch.Module = D

        if accelerator.is_main_process:
            logger.info("Start training")

        G.train()
        D.train()
        with accelerator.autocast():
            prev_loss_gen = -1.0
            prev_loss_fm = -1.0
            prev_loss_mel = -1.0
            prev_loss_kl = -1.0
            prev_loss_disc = -1.0
            prev_loss_gen_all = -1.0
            for epoch in range(epochs):
                if epoch < finished_epoch:
                    continue

                tqdm_loader = tqdm(
                    loader,
                    desc=f"Epoch {epoch+1}/{epochs} (loss_gen: {prev_loss_gen:.4f}, loss_fm: {prev_loss_fm:.4f}, loss_mel: {prev_loss_mel:.4f}, loss_kl: {prev_loss_kl:.4f}, loss_disc: {prev_loss_disc:.4f}, loss_gen_all: {prev_loss_gen_all:.4f})",
                )
                for (
                    phone,
                    phone_lengths,
                    pitch,
                    pitchf,
                    spec,
                    spec_lengths,
                    wave,
                    wave_lengths,
                    sid,
                ) in tqdm_loader:
                    # Generator
                    optimizer_G.zero_grad()
                    (
                        y_hat,
                        ids_slice,
                        x_mask,
                        z_mask,
                        (z, z_p, m_p, logs_p, m_q, logs_q),
                    ) = G(
                        phone,
                        phone_lengths,
                        pitch,
                        pitchf,
                        spec,
                        spec_lengths,
                        sid,
                    )
                    mel = spec_to_mel_torch(
                        spec,
                        filter_length,
                        n_mel_channels,
                        self.sr,
                        mel_fmin,
                        mel_fmax,
                    )
                    y_mel = commons.slice_segments(
                        mel, ids_slice, segment_size // hop_length
                    )
                    y_hat_mel = mel_spectrogram_torch(
                        y_hat.squeeze(1),
                        filter_length,
                        n_mel_channels,
                        self.sr,
                        hop_length,
                        win_length,
                        mel_fmin,
                        mel_fmax,
                    )
                    wave = commons.slice_segments(
                        wave, ids_slice * hop_length, segment_size
                    )

                    # Discriminator
                    optimizer_D.zero_grad()
                    y_d_hat_r, y_d_hat_g, fmap_r, fmap_g = D(wave, y_hat.detach())

                    # Update Discriminator
                    loss_disc, losses_disc_r, losses_disc_g = discriminator_loss(
                        y_d_hat_r, y_d_hat_g
                    )
                    accelerator.backward(loss_disc)
                    optimizer_D.step()

                    # Re-compute discriminator output (since we just got a "better" discriminator)
                    y_d_hat_r, y_d_hat_g, fmap_r, fmap_g = D(wave, y_hat)

                    # Update Generator
                    loss_gen, losses_gen = generator_loss(y_d_hat_g)
                    loss_mel = F.l1_loss(y_mel, y_hat_mel) * c_mel
                    loss_kl = kl_loss(z_p, logs_q, m_p, logs_p, z_mask) * c_kl
                    loss_fm = feature_loss(fmap_r, fmap_g)
                    loss_gen_all = loss_gen + loss_fm + loss_mel + loss_kl
                    accelerator.backward(loss_gen_all)
                    optimizer_G.step()

                    prev_loss_gen = loss_gen.item()
                    prev_loss_fm = loss_fm.item()
                    prev_loss_mel = loss_mel.item()
                    prev_loss_kl = loss_kl.item()
                    prev_loss_disc = loss_disc.item()
                    prev_loss_gen_all = loss_gen_all.item()

                yield (
                    epoch,
                    G,
                    D,
                    optimizer_G,
                    optimizer_D,
                    prev_loss_gen,
                    prev_loss_fm,
                    prev_loss_mel,
                    prev_loss_kl,
                    prev_loss_disc,
                    prev_loss_gen_all,
                )
