import joblib
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
import wandb

from bolero.pl.track1d import Track1DExamplePlotter
from bolero.pl.utils import figure_to_array
from bolero.tl.generic.train import GenericTrainer
from bolero.tl.generic.train_helper import (
    CumulativeCounter,
    CumulativePearson,
    batch_pearson_correlation,
)
from bolero.tl.model.track1d.dataset import Track1DDataset
from bolero.tl.model.track1d.model import DialatedCNNTrack1DModel


class Track1DTrainerMixin(GenericTrainer):
    trainer_config = {
        "mode": "REQUIRED",
        "chrom_split": "REQUIRED",
        "output_dir": "REQUIRED",
        "savename": "REQUIRED",
        "wandb_project": "REQUIRED",
        "wandb_job_type": "REQUIRED",
        "wandb_group": None,
        "max_epochs": 100,
        "patience": 10,
        "use_amp": True,
        "use_ema": True,
        "scheduler": False,
        "lr": 0.003,
        "weight_decay": 0.001,
        "accumulate_grad": 1,
        "train_batches": 2000,
        "val_batches": 300,
        "loss_tolerance": 0.0,
        "plot_example_per_epoch": 9,
        # region file
        "region_bed_path": "REQUIRED",
        # loss cov cutoff
        "loss_cov_cutoff": 10,
    }

    prefix: str

    def __init__(self, config):
        super().__init__(config)

        self.model: torch.nn.Module = None

        self._setup_env()
        self._setup_dataset()
        return

    # =============================
    # Model training and validation
    # =============================
    def _setup_model(self):
        raise NotImplementedError

    @torch.no_grad()
    def _model_validation_step(
        self,
        model,
        dataloader,
        val_batches,
    ):
        print_step = max(5, val_batches // 20)
        # if val batches is None, use all batches in the dataset

        size = 0
        val_loss = 0
        single_batch_pearson_counter = CumulativeCounter()
        across_batch_pearson_counter = CumulativePearson()

        example_batches = []  # collect example batches for making images
        for batch_id, batch in enumerate(dataloader):
            y, pred_y = self._model_forward_pass(model, batch)

            # mask is element wise mask based on coverage > cutoff
            loss_ = F.mse_loss(pred_y, y)
            val_loss += loss_.item()

            # ==========
            # Within batch pearson and save for across batch pearson
            # ==========
            # within batch pearson
            corr = batch_pearson_correlation(pred_y, y).detach().cpu()[:, None]
            single_batch_pearson_counter.update(corr)
            # save for across batch pearson
            across_batch_pearson_counter.update(pred_y, y)

            size += 1
            if batch_id < self.plot_example_per_epoch:
                batch["pred_"] = pred_y.detach()
                example_batches.append(batch)

            if ((batch_id + 1) % print_step) == 0:
                desc_str = (
                    f" - (Validation) {self.cur_epoch} [{batch_id}/{val_batches}] "
                    f"Loss: {val_loss/size:.3f}; "
                    f"Within batch Pearson: {single_batch_pearson_counter.mean():.3f}; "
                    f"Across batch Pearson: {across_batch_pearson_counter.corr():.3f}; "
                )
                print(desc_str)

        del dataloader
        self._cleanup_env()

        wandb_images = self._plot_example_images(
            example_batches, target_key=self.prefix, predict_key="pred_"
        )

        # ==========
        # Loss
        # ==========
        val_loss = val_loss / size

        # ==========
        # Within batch pearson
        # ==========
        single_batch_pearson = single_batch_pearson_counter.mean()

        # ==========
        # Across batch pearson
        # ==========
        across_batch_pearson = across_batch_pearson_counter.corr()
        return val_loss, single_batch_pearson, across_batch_pearson, wandb_images

    def _model_forward_pass(self, model, batch):
        raise NotImplementedError

    def _plot_example_images(self, example_batches, target_key, predict_key="pred_"):
        epoch = self.cur_epoch + 1
        wandb_images = []
        for idx, batch in enumerate(example_batches):
            plotter = Track1DExamplePlotter(
                target_key=target_key,
                predict_key=predict_key,
            )
            fig, _ = plotter.plot(
                batch,
                figsize=(6, 8),
                dpi=150,
                top_example=2,
                bottom_example=2,
                plot_channel=0,
            )
            fig_array = figure_to_array(fig)
            fig.savefig(f"{self.savename}.example_{epoch}_{idx}.jpg")
            plt.close(fig)

            wandb_images.append(
                wandb.Image(
                    fig_array,
                    mode="RGB",
                    caption=f"Epoch {epoch} Example {idx}",
                    grouping=epoch,
                    file_type="jpg",  # reduce file size
                )
            )
        return wandb_images

    def _log_save_and_check_stop(self):
        epoch = self.cur_epoch
        train_loss = self.train_loss
        learning_rate = self.cur_lr
        val_loss = self.val_loss
        single_batch_pearson = self.single_batch_pearson
        across_batch_pearson = self.across_batch_pearson
        example_images = self.example_wandb_images

        print(
            f" - (Training) {epoch}; Loss: {train_loss:.3f}; Learning rate {learning_rate}."
        )
        print(f" - (Validation) {epoch} Loss: {val_loss:.3f}")
        print(f"Single Batch Pearson Corr.: {single_batch_pearson:.3f}")
        print(f"Across Batch Pearson Corr.: {across_batch_pearson:.3f}")

        # only clear the early stopping counter if the loss improvement is better than tolerance
        previous_best = self.best_val_loss
        if val_loss < self.best_val_loss - self.loss_tolerance:
            self.early_stopping_counter = 0
        else:
            self.early_stopping_counter += 1
        print(
            f"Previous best loss: {previous_best:.3f}, "
            f"Loss at epoch {epoch}: {val_loss:.3f}; "
            f"Early stopping counter: {self.early_stopping_counter}"
        )
        # save checkpoint if the loss is better
        if val_loss < self.best_val_loss:
            self.best_val_loss = val_loss
            self._save_checkpint(update_best=True)
        else:
            self._save_checkpint(update_best=False)
        if self.wandb_active:
            wandb.log(
                {
                    "train/train_loss": train_loss,
                    "val/val_loss": val_loss,
                    "val/best_val_loss": self.best_val_loss,
                    "val/early_stopping_counter": self.early_stopping_counter,
                    "val/single_batch_pearson": single_batch_pearson,
                    "val/across_batch_pearson": across_batch_pearson,
                    "val_example/example_predictions": example_images,
                }
            )
        flag = self.early_stopping_counter >= self.patience
        return flag

    def _fit(self, max_epochs=None, valid_first=False):
        if max_epochs is None:
            max_epochs = self.max_epochs

        # dataset related
        scaler = self.scaler
        optimizer = self.optimizer
        scheduler = self.scheduler
        ema = self.ema
        self.val_loss = None

        if valid_first:
            print("Perform validation before training.")
            (
                self.val_loss,
                self.single_batch_pearson,
                self.across_batch_pearson,
                wandb_images,
            ) = self._validation_step()
            print(f"Validation loss before training: {self.val_loss:.4f}")
            print(f"Validation Singe Batch pearson: {self.single_batch_pearson:.3f}")
            print(f"Validation Across Batch pearson: {self.across_batch_pearson:.3f}.")
            wandb.log(
                {
                    "val/val_loss": self.val_loss,
                    "val/single_batch_pearson": self.single_batch_pearson,
                    "val/across_batch_pearson": self.across_batch_pearson,
                    "val_example/example_images": wandb_images,
                }
            )

        stop_flag = self.early_stopping_counter >= self.patience
        if self.cur_epoch > 0:
            print(
                f"Resuming training from epoch {self.cur_epoch+1}, with {max_epochs+1} epochs in total."
            )
        while self.cur_epoch < max_epochs and not stop_flag:
            # one can manually create a stop flag file to stop the training
            # path: f"{self.savename}.stop.flag"
            if self._check_stage_flag("stop"):
                print(
                    f"Early stopping flag file found, stopping training at {self.cur_epoch}."
                )
                self.early_stoped = True
                break
            print(
                f"Current epoch: {self.cur_epoch}, max epochs: {max_epochs}, stop flag: {stop_flag}."
            )
            # check early stop
            if self.early_stopping_counter >= self.patience:
                # early stopping counter could be loaded from the checkpoint
                # check before starting the for loop
                print(f"Early stopping at epoch {self.cur_epoch}")
                self.early_stoped = True
                break

            # get train data loader
            dataloader = self.get_train_dataloader(batches=self.train_batches)

            # start train epochs
            moving_avg_loss = 0
            cur_loss = 1e10
            nan_loss = False

            print_steps = max(5, self.train_batches // 50)
            for batch_id, batch in enumerate(dataloader):
                try:
                    auto_cast_context = torch.autocast(
                        device_type=str(self.device).split(":")[0],
                        dtype=torch.bfloat16,
                        enabled=self.use_amp,
                    )
                except RuntimeError:
                    # some GPU, such as T4 does not support bfloat16
                    print("bfloat16 autocast failed, using float16 instead.")
                    auto_cast_context = torch.autocast(
                        device_type=str(self.device).split(":")[0],
                        dtype=torch.float16,
                        enabled=self.use_amp,
                    )
                with auto_cast_context:
                    y, pred_y = self._model_forward_pass(self.model, batch)
                    loss = F.mse_loss(pred_y, y)
                    loss = loss / self.accumulate_grad

                    if np.isnan(loss.item()):
                        nan_loss = True
                        print("Training loss has NaN, skipping epoch.")
                        self._update_state_dict()
                        break

                # ==========
                # Backward
                # ==========
                scaler.scale(loss).backward()
                moving_avg_loss += loss.item()
                # only update optimizer every accumulate_grad steps
                # this is equivalent to updating every step but with larger batch size (batch_size * accumulate_grad)
                # however, with larger batch size, the GPU memory usage will be higher
                if (batch_id + 1) % self.accumulate_grad == 0:
                    scaler.unscale_(
                        optimizer
                    )  # Unscale gradients for clipping without inf/nan gradients affecting the model

                    scaler.step(optimizer)
                    scaler.update()
                    optimizer.zero_grad()

                    if ema:
                        ema.update()

                    if scheduler is not None:
                        scheduler.step()

                if (batch_id + 1) % print_steps == 0:
                    _loss = moving_avg_loss / (batch_id + 1)
                    desc_str = (
                        f" - (Training) {self.cur_epoch} {batch_id} "
                        f"Loss: {_loss:.4f} "
                    )

                    if _loss > (cur_loss + 0.5):
                        batch["cur_loss"] = _loss
                        batch["last_loss"] = cur_loss
                        print(f"Batch {batch_id} loss increased.")
                        joblib.dump(
                            batch,
                            f"{self.savename}.epoch{self.cur_epoch}.batch{batch_id}.joblib",
                        )

                    cur_loss = _loss
                    print(desc_str)

            del dataloader
            self._cleanup_env()
            if nan_loss:
                # epoch break due to nan loss, skip validation
                continue

            self.train_loss = moving_avg_loss / (batch_id + 1)
            self.cur_lr = optimizer.param_groups[0]["lr"]
            (
                self.val_loss,
                self.single_batch_pearson,
                self.across_batch_pearson,
                self.example_wandb_images,
            ) = self._validation_step()

            if np.isnan(self.val_loss):
                print("Validation loss is NaN, skipping epoch.")
                self._update_state_dict()
                continue

            self.cur_epoch += 1
            stop_flag = self._log_save_and_check_stop()
            if stop_flag:
                print(f"Early stopping at epoch {self.cur_epoch}")
                self.early_stoped = True
                break
        self._cleanup_env()
        return

    def _test(self):
        if self.val_loss is None:
            (
                self.val_loss,
                self.single_batch_pearson,
                self.across_batch_pearson,
                _,
            ) = self._validation_step(val_batches=1500)
        (
            self.test_loss,
            self.test_single_batch_pearson,
            self.test_across_batch_pearson,
            wandb_images,
        ) = self._validation_step(testing=True, val_batches=1500)

        wandb.summary["final_valid_loss"] = self.val_loss
        wandb.summary["final_valid_within"] = self.single_batch_pearson
        wandb.summary["final_valid_across"] = self.across_batch_pearson
        wandb.summary["final_test_loss"] = self.test_loss
        wandb.summary["final_test_within"] = self.test_single_batch_pearson
        wandb.summary["final_test_across"] = self.test_across_batch_pearson
        wandb.summary["final_image"] = wandb_images

        # final wandb flag to indicate the run is successfully finished
        wandb.summary["success"] = True
        return

    def train(self):
        """Train function should be implemented in the subclass."""
        raise NotImplementedError


class Track1DBaseTrainer(Track1DTrainerMixin):
    """Train base model on pseudobulk single-cell ATAC data."""

    trainer_config = Track1DTrainerMixin.trainer_config.copy()
    trainer_config.update(
        {
            "mode": "base",
            "lr": 0.003,  # use 0.003 for base init, 0.0003 for fine-tune
            # dataset related files
            "pretrained_model": None,
        }
    )

    dataset_class = Track1DDataset
    model_class = DialatedCNNTrack1DModel

    def __init__(self, config):
        self.prefix = config["prefix"]

        super().__init__(config)
        return

    def _setup_model_from_config(self):
        print("Setting up model from config")
        model = self.model_class.create_from_config(self.config)
        model.to(self.device)
        return model

    def _setup_model_from_pretrain(self):
        # load model from path, set parameter to requires_grad, and model to train
        model_path = self.config["pretrained_model"]
        if model_path is None:
            raise ValueError("Pretrained model path is required.")
        print(f"Setting up model from pretrain model at {model_path}")

        model = torch.load(model_path)
        model.train()
        for param in model.parameters():
            param.requires_grad = True
        return model

    def _setup_model(self):
        mode = self.mode

        if mode == "finetune":
            self.model = self._setup_model_from_pretrain()
        elif mode == "base":
            self.model = self._setup_model_from_config()
        else:
            raise ValueError(
                f"Incorrect mode: {mode}, should be one of ['base', 'finetune']."
            )

        self._set_total_params()
        return

    def _model_forward_pass(self, model: torch.nn.Module, batch: dict):
        prefix = self.prefix

        # ==========
        # X
        # ==========
        X = batch["dna_one_hot"]

        # ==========
        # y_mc_frac
        # ==========
        y = batch[prefix]
        y = torch.log1p(y)

        # ==========
        # Forward
        # ==========
        pred_y = model(X)
        return y, pred_y

    def train(self, valid_first=None) -> None:
        """Train the model."""
        wandb_run = self._setup_wandb()
        if wandb_run is None:
            return

        if valid_first is None:
            if self.mode == "finetune":
                valid_first = True

        with wandb_run:
            self.checkpoint = self._has_last_checkpoint()
            self._setup_model()
            self._setup_fit()
            self._fit(valid_first=valid_first)
            self._test()
            self._cleanup_env()
            wandb.finish()
        return
