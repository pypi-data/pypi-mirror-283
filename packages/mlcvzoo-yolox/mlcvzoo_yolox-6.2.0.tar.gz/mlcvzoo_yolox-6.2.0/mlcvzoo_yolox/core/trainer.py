# Copyright 2021 Open Logistics Foundation
#
# Licensed under the Open Logistics License 1.0.
# For details on the licensing terms, see the LICENSE file.

"""
Module for defining a custom yolox trainer class
"""

import argparse
import os
from typing import cast

from loguru import logger
from yolox.core.trainer import Trainer
from yolox.utils import all_reduce_norm

from mlcvzoo_yolox.exp.custom_yolox_exp import CustomYOLOXExp


class YoloxTrainer(Trainer):
    """
    Define a custom yolox Trainer class to adapt some of the
    predefined behavior.
    """

    def __init__(self, exp: CustomYOLOXExp, args: argparse.Namespace) -> None:
        Trainer.__init__(self, exp=exp, args=args)

        self.exp = cast(CustomYOLOXExp, self.exp)  # type: ignore

        # Save the original configured evaluation interval for use in the method before_epoch(...)
        self.original_eval_interval = self.exp.eval_interval

        # Overwrite file_name attribute of the yolox Trainer class and use
        # the output_dir that is configured via the yolox experiment.
        # Yolox normally creates an extra subfolder on the basis of the
        # experiment name. This is an unwanted behavior.
        self.file_name = os.path.join(exp.output_dir)

    def after_epoch(self) -> None:
        """
        Define relevant steps that are executed after each training epoch

        IMPORTANT: In the yolox Trainer base class, this method starts
                   an evaluation. We decided to execute the evaluation
                   separately from the training. Therefore, there is
                   currently no evaluation routine during the training.

        Returns:
            None
        """

        if self.epoch % self.exp.checkpoint_interval == 0:
            all_reduce_norm(self.model)
            self.save_ckpt(ckpt_name=f"{self.exp.exp_name}__{self.epoch:04d}")

    def before_epoch(self) -> None:
        """
        This method follows the implementation of its superclass, but has some
        additional / overriding behavior:

        - Don't set self.exp.eval_interval to a hardcoded value, but take the
          one from the experiment configuration
        - Don't log mosaic checkpoints

        Returns:
            None
        """

        logger.info("---> start train epoch{}".format(self.epoch + 1))

        if self.epoch + 1 == self.max_epoch - self.exp.no_aug_epochs or self.no_aug:
            logger.info("--->No mosaic aug now!")
            self.train_loader.close_mosaic()
            logger.info("--->Add additional L1 loss now!")
            if self.is_distributed:
                self.model.module.head.use_l1 = True
            else:
                self.model.head.use_l1 = True

        # Use the original configured evaluation interval
        self.exp.eval_interval = self.original_eval_interval
