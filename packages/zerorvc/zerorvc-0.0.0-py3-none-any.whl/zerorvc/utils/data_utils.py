from time import time
import logging

import torch
import torch.utils.data

logger = logging.getLogger(__name__)


class TextAudioCollateMultiNSFsid:
    """Zero-pads model inputs and targets"""

    def __init__(self, return_ids=False):
        self.return_ids = return_ids

    def __call__(self, batch):
        """Collate's training batch from normalized text and aduio
        PARAMS
        ------
        batch: [text_normalized, spec_normalized, wav_normalized]
        """
        start_t = time()
        # Right zero-pad all one-hot text sequences to max input length
        _, ids_sorted_decreasing = torch.sort(
            torch.LongTensor([x["spec"].size(1) for x in batch]), dim=0, descending=True
        )

        max_spec_len = max([x["spec"].size(1) for x in batch])
        max_wave_len = max([x["wav_gt"]["array"].size(0) for x in batch])
        spec_lengths = torch.LongTensor(len(batch))
        wave_lengths = torch.LongTensor(len(batch))
        spec_padded = torch.FloatTensor(
            len(batch), batch[0]["spec"].size(0), max_spec_len
        )
        wave_padded = torch.FloatTensor(len(batch), 1, max_wave_len)
        spec_padded.zero_()
        wave_padded.zero_()

        max_phone_len = max([x["hubert_feats"].size(0) for x in batch])
        phone_lengths = torch.LongTensor(len(batch))
        phone_padded = torch.FloatTensor(
            len(batch), max_phone_len, batch[0]["hubert_feats"].shape[1]
        )  # (spec, wav, phone, pitch)
        pitch_padded = torch.LongTensor(len(batch), max_phone_len)
        pitchf_padded = torch.FloatTensor(len(batch), max_phone_len)
        phone_padded.zero_()
        pitch_padded.zero_()
        pitchf_padded.zero_()
        # dv = torch.FloatTensor(len(batch), 256)#gin=256
        sid = torch.LongTensor(len(batch))

        for i in range(len(ids_sorted_decreasing)):
            row = batch[ids_sorted_decreasing[i]]

            spec = row["spec"]
            spec_padded[i, :, : spec.size(1)] = spec
            spec_lengths[i] = spec.size(1)

            wave = row["wav_gt"]["array"]
            wave_padded[i, :, : wave.size(0)] = wave
            wave_lengths[i] = wave.size(0)

            phone = row["hubert_feats"]
            phone_padded[i, : phone.size(0), :] = phone
            phone_lengths[i] = phone.size(0)

            pitch = row["f0"]
            pitch_padded[i, : pitch.size(0)] = pitch
            pitchf = row["f0nsf"]
            pitchf_padded[i, : pitchf.size(0)] = pitchf

            sid[i] = torch.LongTensor([0])

        return (
            phone_padded,
            phone_lengths,
            pitch_padded,
            pitchf_padded,
            spec_padded,
            spec_lengths,
            wave_padded,
            wave_lengths,
            sid,
        )
