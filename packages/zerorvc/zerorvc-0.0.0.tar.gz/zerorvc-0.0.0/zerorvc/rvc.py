import os
from glob import glob
from logging import getLogger

logger = getLogger(__name__)


class RVC:
    def __init__(self, model: str, index: str):
        self.model = model
        self.index = index

    def from_pretrained(dir: str):
        model = os.path.join(dir, "model.pth")
        if not os.path.exists(model):
            raise Exception(f"model.pth not found in {dir}")

        index = glob(os.path.join(dir, "added_*.index"))
        if index:
            index = index[0]
        else:
            index = None

        rvc = RVC(model, index)
        return rvc
