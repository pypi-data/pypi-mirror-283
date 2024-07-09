import logging
import os

import torch

logger = logging.getLogger(__name__)


def load_checkpoint_d(checkpoint_path, combd, sbd, optimizer=None, load_opt=1):
    assert os.path.isfile(checkpoint_path)
    checkpoint_dict = torch.load(checkpoint_path, map_location="cpu")

    ##################
    def go(model, bkey):
        saved_state_dict = checkpoint_dict[bkey]
        if hasattr(model, "module"):
            state_dict = model.module.state_dict()
        else:
            state_dict = model.state_dict()
        new_state_dict = {}
        for k, v in state_dict.items():  # 模型需要的shape
            try:
                new_state_dict[k] = saved_state_dict[k]
                if saved_state_dict[k].shape != state_dict[k].shape:
                    logger.warning(
                        "shape-%s-mismatch. need: %s, get: %s",
                        k,
                        state_dict[k].shape,
                        saved_state_dict[k].shape,
                    )  #
                    raise KeyError
            except:
                # logger.info(traceback.format_exc())
                logger.info("%s is not in the checkpoint", k)  # pretrain缺失的
                new_state_dict[k] = v  # 模型自带的随机值
        if hasattr(model, "module"):
            model.module.load_state_dict(new_state_dict, strict=False)
        else:
            model.load_state_dict(new_state_dict, strict=False)
        return model

    go(combd, "combd")
    model = go(sbd, "sbd")
    #############
    logger.info("Loaded model weights")

    iteration = checkpoint_dict["iteration"]
    learning_rate = checkpoint_dict["learning_rate"]
    if (
        optimizer is not None and load_opt == 1
    ):  ###加载不了，如果是空的的话，重新初始化，可能还会影响lr时间表的更新，因此在train文件最外围catch
        #   try:
        optimizer.load_state_dict(checkpoint_dict["optimizer"])
    #   except:
    #     traceback.print_exc()
    logger.info("Loaded checkpoint '{}' (epoch {})".format(checkpoint_path, iteration))
    return model, optimizer, learning_rate, iteration


def load_checkpoint(checkpoint_path, model, optimizer=None, load_opt=1):
    assert os.path.isfile(checkpoint_path)
    checkpoint_dict = torch.load(checkpoint_path, map_location="cpu")

    saved_state_dict = checkpoint_dict["model"]
    if hasattr(model, "module"):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    new_state_dict = {}
    for k, v in state_dict.items():  # 模型需要的shape
        try:
            new_state_dict[k] = saved_state_dict[k]
            if saved_state_dict[k].shape != state_dict[k].shape:
                logger.warning(
                    "shape-%s-mismatch|need-%s|get-%s",
                    k,
                    state_dict[k].shape,
                    saved_state_dict[k].shape,
                )  #
                raise KeyError
        except:
            # logger.info(traceback.format_exc())
            logger.info("%s is not in the checkpoint", k)  # pretrain缺失的
            new_state_dict[k] = v  # 模型自带的随机值
    if hasattr(model, "module"):
        model.module.load_state_dict(new_state_dict, strict=False)
    else:
        model.load_state_dict(new_state_dict, strict=False)
    logger.info("Loaded model weights")

    iteration = checkpoint_dict["iteration"]
    learning_rate = checkpoint_dict["learning_rate"]
    if (
        optimizer is not None and load_opt == 1
    ):  ###加载不了，如果是空的的话，重新初始化，可能还会影响lr时间表的更新，因此在train文件最外围catch
        #   try:
        optimizer.load_state_dict(checkpoint_dict["optimizer"])
    #   except:
    #     traceback.print_exc()
    logger.info("Loaded checkpoint '{}' (epoch {})".format(checkpoint_path, iteration))
    return model, optimizer, learning_rate, iteration


def save_checkpoint(model, optimizer, learning_rate, iteration, checkpoint_path):
    logger.info(
        "Saving model and optimizer state at epoch {} to {}".format(
            iteration, checkpoint_path
        )
    )
    if hasattr(model, "module"):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    torch.save(
        {
            "model": state_dict,
            "iteration": iteration,
            "optimizer": optimizer.state_dict(),
            "learning_rate": learning_rate,
        },
        checkpoint_path,
    )


def save_checkpoint_d(combd, sbd, optimizer, learning_rate, iteration, checkpoint_path):
    logger.info(
        "Saving model and optimizer state at epoch {} to {}".format(
            iteration, checkpoint_path
        )
    )
    if hasattr(combd, "module"):
        state_dict_combd = combd.module.state_dict()
    else:
        state_dict_combd = combd.state_dict()
    if hasattr(sbd, "module"):
        state_dict_sbd = sbd.module.state_dict()
    else:
        state_dict_sbd = sbd.state_dict()
    torch.save(
        {
            "combd": state_dict_combd,
            "sbd": state_dict_sbd,
            "iteration": iteration,
            "optimizer": optimizer.state_dict(),
            "learning_rate": learning_rate,
        },
        checkpoint_path,
    )
