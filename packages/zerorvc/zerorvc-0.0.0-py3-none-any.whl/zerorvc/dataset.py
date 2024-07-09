import numpy as np
import torch
import librosa
from accelerate import Accelerator
from datasets import load_dataset, DatasetDict, Audio
from fairseq.checkpoint_utils import load_model_ensemble_and_task
from .preprocess import Preprocessor
from .hubert import HubertFeatureExtractor, HubertModel
from .f0 import F0Extractor, RMVPE


SR_16K = 16000
SR_40K = 40000
N_FFT = 2048
HOP_LENGTH = 400
WIN_LENGTH = 2048


def extract_hubert_features(
    rows, hfe: HubertFeatureExtractor, hubert: str | HubertModel, device: torch.device
):
    if not hfe.is_loaded():
        if isinstance(hubert, str):
            models, _, _ = load_model_ensemble_and_task([hubert])
            model = models[0].to(device)
            hfe.load(model)
        elif isinstance(hubert, HubertModel):
            hfe.load(hubert)
        else:
            raise ValueError("Hubert model not provided")
    feats = []
    for row in rows["wav_16k"]:
        feat = hfe.extract_feature_from(row["array"].astype("float32"))
        feats.append(feat)
    return {"hubert_feats": feats}


def extract_f0_features(
    rows, f0e: F0Extractor, rmvpe: str | RMVPE, device: torch.device
):
    if not f0e.is_loaded():
        if isinstance(rmvpe, str):
            model = RMVPE(4, 1, (2, 2))
            model.load_state_dict(torch.load(rmvpe, map_location=device))
            model.to(device)
            f0e.load(model)
        elif isinstance(rmvpe, RMVPE):
            f0e.load(rmvpe)
        else:
            raise ValueError("RMVPE model not provided")
    f0s = []
    f0nsfs = []
    for row in rows["wav_16k"]:
        f0nsf, f0 = f0e.extract_f0_from(row["array"].astype("float32"))
        f0s.append(f0)
        f0nsfs.append(f0nsf)
    return {"f0": f0s, "f0nsf": f0nsfs}


def feature_postprocess(rows):
    phones = rows["hubert_feats"]
    for i, phone in enumerate(phones):
        phone = np.repeat(phone, 2, axis=0)
        n_num = min(phone.shape[0], 900)
        phone = phone[:n_num, :]
        phones[i] = phone

        if "f0" in rows:
            pitch = rows["f0"][i]
            pitch = pitch[:n_num]
            pitch = np.array(pitch, dtype=np.float32)
            rows["f0"][i] = pitch
        if "f0nsf" in rows:
            pitchf = rows["f0nsf"][i]
            pitchf = pitchf[:n_num]
            rows["f0nsf"][i] = pitchf
    return rows


def calculate_spectrogram(
    rows, n_fft=N_FFT, hop_length=HOP_LENGTH, win_length=WIN_LENGTH
):
    specs = []
    hann_window = np.hanning(win_length)
    pad_amount = int((win_length - hop_length) / 2)
    for row in rows["wav_gt"]:
        stft = librosa.stft(
            np.pad(row["array"], (pad_amount, pad_amount), mode="reflect"),
            n_fft=n_fft,
            hop_length=hop_length,
            win_length=win_length,
            window=hann_window,
            center=False,
        )
        specs.append(np.abs(stft) + 1e-6)

    return {"spec": specs}


def fix_length(rows, hop_length=HOP_LENGTH):
    for i, row in enumerate(rows["spec"]):
        spec = np.array(row)
        phone = np.array(rows["hubert_feats"][i])
        pitch = np.array(rows["f0"][i])
        pitchf = np.array(rows["f0nsf"][i])
        wav_gt = np.array(rows["wav_gt"][i]["array"])

        phone_len = phone.shape[0]
        spec_len = spec.shape[1]
        if phone_len != spec_len:
            len_min = min(phone_len, spec_len)
            phone = phone[:len_min, :]
            pitch = pitch[:len_min]
            pitchf = pitchf[:len_min]
            spec = spec[:, :len_min]
            wav_gt = wav_gt[: len_min * hop_length]
            rows["hubert_feats"][i] = phone
            rows["f0"][i] = pitch
            rows["f0nsf"][i] = pitchf
            rows["spec"][i] = spec
            rows["wav_gt"][i]["array"] = wav_gt
    return rows


def prepare(
    dir: str,
    sr=SR_40K,
    hubert: str | HubertModel = None,
    rmvpe: str | RMVPE = None,
    batch_size=1,
    accelerator: Accelerator = None,
):
    if accelerator is None:
        accelerator = Accelerator()

    ds: DatasetDict = load_dataset("audiofolder", data_dir=dir)
    ds = ds.cast_column("audio", Audio(sampling_rate=sr))

    pp = Preprocessor(sr, 3.0)

    def preprocess(rows):
        wav_gt = []
        wav_16k = []
        for row in rows["audio"]:
            slices = pp.preprocess_audio(row["array"])
            for slice in slices:
                wav_gt.append({"path": "", "array": slice[0], "sampling_rate": sr})
                wav_16k.append({"path": "", "array": slice[1], "sampling_rate": SR_16K})
        return {"wav_gt": wav_gt, "wav_16k": wav_16k}

    ds = ds.map(
        preprocess, batched=True, batch_size=batch_size, remove_columns=["audio"]
    )
    ds = ds.cast_column("wav_gt", Audio(sampling_rate=sr))
    ds = ds.cast_column("wav_16k", Audio(sampling_rate=SR_16K))

    hfe = HubertFeatureExtractor()
    ds = ds.map(
        extract_hubert_features,
        batched=True,
        batch_size=batch_size,
        fn_kwargs={"hfe": hfe, "hubert": hubert, "device": accelerator.device},
    )

    f0e = F0Extractor()
    ds = ds.map(
        extract_f0_features,
        batched=True,
        batch_size=batch_size,
        fn_kwargs={"f0e": f0e, "rmvpe": rmvpe, "device": accelerator.device},
    )

    ds = ds.map(feature_postprocess, batched=True, batch_size=batch_size)
    ds = ds.map(calculate_spectrogram, batched=True, batch_size=batch_size)
    ds = ds.map(fix_length, batched=True, batch_size=batch_size)

    return ds
