from collections import OrderedDict
from typing import Any, Iterable, Union

import numpy as np

from bolero.tl.dataset.ray_dataset import (
    RayGenomeChunkDataset,
)
from bolero.tl.dataset.sc_transforms import FilterRegions
from bolero.tl.dataset.transforms import (
    BatchRegionEmbedding,
    CropLastAxisWithJitter,
    ReverseComplement,
)
from bolero.tl.footprint import FootPrintModel
from bolero.utils import validate_config


class BatchFootPrint(FootPrintModel):
    """Apply footprint transformation to the given data batch."""

    def __init__(
        self,
        atac_key: Union[str, list[str]],
        bias_key: str,
        modes: np.ndarray = None,
        clip_min: float = -10,
        clip_max: float = 10,
        return_pval: bool = False,
        smooth_radius: int = None,
        numpy=False,
        device=None,
        tfbs_score_all: bool = False,
        tfbs_score_class1: bool = False,
        nucleosome_score: bool = False,
    ):
        """
        Apply footprint transformation to the given data dictionary.

        Args:
            atac_key (Union[str, List[str]]): Key(s) for the ATAC data in the data dictionary.
            bias_key (str): Key for the bias data in the data dictionary.
            modes (np.ndarray): Modes for the footprint transformation.
            clip_min (float, optional): Minimum value for clipping. Defaults to -10.
            clip_max (float, optional): Maximum value for clipping. Defaults to 10.
            return_pval (bool, optional): Whether to return p-values. Defaults to False.
            smooth_radius (int, optional): Radius for smoothing. Defaults to None.
            numpy (bool, optional): Whether to use numpy. Defaults to True.
            device ([type], optional): Device for the model. Defaults to None.
            tfbs_score_all (bool, optional): Whether to use all TFBS scores. Defaults to False.
            tfbs_score_class1 (bool, optional): Whether to use class 1 TFBS scores. Defaults to False.
            nucleosome_score (bool, optional): Whether to use nucleosome scores. Defaults to False.
        """
        if modes is None:
            modes = np.arange(2, 101, 1)
        else:
            modes = np.array(modes)
        super().__init__(bias_bw_path=None, dispmodels=None, modes=modes, device=device)

        # get the device from the parameters
        self.device = next(self.parameters()).device

        if isinstance(atac_key, str):
            atac_key = [atac_key]
        self.atac_key = atac_key
        self.bias_key = bias_key
        self.clip_min = clip_min
        self.clip_max = clip_max
        self.return_pval = return_pval
        self.smooth_radius = smooth_radius
        self.numpy = numpy
        self.tfbs_score_all = tfbs_score_all
        self.tfbs_score_class1 = tfbs_score_class1
        self.nucleosome_score = nucleosome_score

    def __call__(self, data: dict, modes: np.array = None) -> dict:
        """
        Apply the footprint transformation to the given data.

        Args:
            data (dict): Input data dictionary.

        Returns
        -------
            dict: Transformed data dictionary.
        """
        modes = modes if modes is not None else self.modes
        bias_data = data[self.bias_key]
        # if bias_data has 3 dims, drop the second dim (channels)
        if bias_data.ndim == 3:
            bias_data = bias_data.squeeze(1)

        for atac in self.atac_key:
            try:
                atac_data = data[atac]
                # if atac_data has 3 dims, drop the second dim (channels)
                if atac_data.ndim == 3:
                    atac_data = atac_data.squeeze(1)
            except KeyError:
                continue

            result = self.footprint_from_data(
                atac_data=atac_data,
                bias_data=bias_data,
                clip_min=self.clip_min,
                clip_max=self.clip_max,
                modes=modes,
                return_pval=self.return_pval,
                smooth_radius=self.smooth_radius,
                numpy=self.numpy,
                tfbs_score_all=self.tfbs_score_all,
                tfbs_score_class1=self.tfbs_score_class1,
                nucleosome_score=self.nucleosome_score,
            )
            if isinstance(result, tuple):
                fp, scores = result
            else:
                fp = result
                scores = {}
            data[f"{atac}_footprint"] = fp
            for key, val in scores.items():
                data[f"{atac}_{key}"] = val
        return data


class scPrinterDataset(RayGenomeChunkDataset):
    """Singel cell dataset for scPrinter model."""

    default_config = {
        "dataset_path": "REQUIRED",
        "genome": "REQUIRED",
        "batch_size": 64,
        "dna_window": 1840,
        "signal_window": 1000,
        "max_jitter": 128,
        "clip_min": -10,
        "clip_max": 10,
        "n_pseudobulks": 30,
        "cov_filter_name": "REQUIRED",
        "min_cov": 10,
        "max_cov": 100000,
        "low_cov_ratio": 0.1,
        "reverse_complement": True,
        "shuffle_files": False,
        "read_parquet_kwargs": None,
    }

    @classmethod
    def get_default_config(cls) -> dict:
        """
        Get the default configuration.
        """
        return cls.default_config

    @classmethod
    def create_from_config(
        cls,
        config: dict,
    ) -> "scPrinterDataset":
        """
        Create a scPrinterDataset object from the configuration.
        """
        # remove additional keys in the configuration
        config = {k: v for k, v in config.items() if k in cls.default_config}
        validate_config(config, cls.default_config)
        print(f"Create scPrinterDataset with config: {config}")
        return cls(**config)

    def __init__(
        self,
        dataset_path: str,
        genome,
        batch_size: int = 64,
        dna_window: int = 1840,
        signal_window: int = 1000,
        max_jitter: int = 128,
        clip_min: float = -10,
        clip_max: float = 10,
        n_pseudobulks: int = 10,
        min_cov: int = 10,
        max_cov: int = 100000,
        low_cov_ratio: float = 0.1,
        cov_filter_name: str = None,
        reverse_complement: bool = True,
        shuffle_files=False,
        read_parquet_kwargs=None,
    ):
        super().__init__(
            dataset_path=dataset_path,
            genome=genome,
            shuffle_files=shuffle_files,
            read_parquet_kwargs=read_parquet_kwargs,
        )
        self.batch_size = batch_size

        # region properties
        self.dna_window = dna_window
        self.signal_window = signal_window
        self.max_jitter = max_jitter
        self.min_counts = min_cov
        self.max_counts = max_cov
        self.reverse_complement = reverse_complement
        self.clip_min = clip_min
        self.clip_max = clip_max
        self.n_pseudobulks = n_pseudobulks
        self.min_cov = min_cov
        self.max_cov = max_cov
        self.low_cov_ratio = low_cov_ratio
        self.cov_filter_name = cov_filter_name

        self.bias_column = "tn5_bias"

        self.region_embedding = None
        self.name_to_pseudobulker = OrderedDict()
        return

    def __repr__(self) -> str:
        _str = (
            f"scPrinterDataset\n"
            f"Dataset directory: {self.dataset_path}\n"
            f"DNA window: {self.dna_window}, Signal window: {self.signal_window},\n"
            f"Max jitter: {self.max_jitter}, Batch size: {self.batch_size},\n"
        )
        return _str

    def _get_region_cropper(self, dataset) -> None:
        """
        Crop the regions in the working dataset.

        Returns
        -------
        None
        """
        if self._dataset_mode != "train":
            max_jitter = 0
        else:
            max_jitter = self.max_jitter

        signal_columns = self.signal_columns
        key_list = [self.dna_column] + signal_columns
        length_list = [self.dna_window] + [self.signal_window] * len(signal_columns)

        _cropper = CropLastAxisWithJitter(
            key=key_list,
            final_length=length_list,
            max_jitter=max_jitter,
        )

        def _cropper_squeeze(data):
            data = _cropper(data)
            for sig_col in signal_columns:
                # also reduce single channel signals to 1D
                _data = data[sig_col]
                if _data.ndim == 3 and _data.shape[1] == 1:
                    data[sig_col] = data[sig_col].squeeze(1)
            return data

        dataset = dataset.map_batches(_cropper_squeeze)
        return dataset

    def _get_reverse_complement_region(self, dataset) -> None:
        """
        Reverse complement the DNA sequences by 50% probability.

        Returns
        -------
        None
        """
        _rc = ReverseComplement(
            dna_key=self.dna_column,
            signal_key=self.signal_columns,
        )
        dataset = dataset.map_batches(_rc)
        return dataset

    def add_region_embedding(self, embedding):
        """Add a predefined region embedding to the dataset."""
        self.region_embedding = embedding
        return

    def _get_add_region_embedding(self, dataset):
        fn = BatchRegionEmbedding
        fn_constructor_kwargs = {
            "embedding": self.region_embedding,
            "region_key": "region",
        }
        dataset = dataset.map_batches(
            fn=fn,
            fn_constructor_kwargs=fn_constructor_kwargs,
            concurrency=1,
        )
        return dataset

    def add_pseudobulker(self, name: str, cls, pseudobulker_kwargs: dict):
        """
        Add a pseudobulker to the dataset.

        Parameters
        ----------
        name : str
            The name of the pseudobulker, will be used as pseudobulk prefix in final dict.
        cls : Pseudobulker class
            The pseudobulker class that can be used to generate pseudobulks.
        pseudobulker_kwargs : dict
            The keyword arguments to pass to the pseudobulker class constructor.
        """
        if "barcode_order" not in pseudobulker_kwargs:
            pseudobulker_kwargs["barcode_order"] = self.barcode_order
        generator = cls.create_from_config(**pseudobulker_kwargs)
        self.name_to_pseudobulker[name] = generator
        return

    def get_footprinter(
        self,
        prefix: str,
    ) -> BatchFootPrint:
        """
        Get the footprint for a specific region and sample.
        """
        atac_keys = [f"{prefix}:bulk_data"]

        fn = BatchFootPrint
        fn_constructor_kwargs = {
            "atac_key": atac_keys,
            "bias_key": self.bias_column,
            "clip_min": self.clip_min,
            "clip_max": self.clip_max,
            "return_pval": False,
            "smooth_radius": None,
            "numpy": False,
            "device": None,
        }

        footprinter = fn(**fn_constructor_kwargs)
        return footprinter

    def _filter_bed_regions(
        self,
        dataset,
        cov_filter_key,
        min_cov,
        max_cov,
        low_cov_ratio,
        batch_size,
        concurrency,
    ):
        fn = FilterRegions
        fn_constructor_kwargs = {
            "cov_filter_key": cov_filter_key,
            "min_cov": min_cov,
            "max_cov": max_cov,
            "low_cov_ratio": low_cov_ratio,
        }
        dataset = dataset.map_batches(
            fn=fn,
            fn_constructor_kwargs=fn_constructor_kwargs,
            concurrency=concurrency,
            batch_size=batch_size,
        )
        return dataset

    def get_processed_dataset(
        self,
        chroms: list[str],
        region_bed_path: str,
        return_cells: bool = False,
        return_regions: bool = False,
    ) -> None:
        """
        Process the dataset and return the processed dataset.

        Parameters
        ----------
        - chroms (list): List of chromosomes to include in the dataset.
        - region_bed_path (str): Path to the BED file containing the regions.
        - return_cells (bool): Whether to return the cells in the dataset. Default is False.
        - return_regions (bool): Whether to return the regions in the dataset. Default is False.

        Returns
        -------
        - work_ds (Dataset): The processed dataset.

        """
        standard_length = (
            max(self.dna_window, self.signal_window) + self.max_jitter * 2 + 200
        )
        standard_length = int(standard_length)
        region_bed = self.standard_region_length(region_bed_path, standard_length)

        work_ds = super()._get_processed_dataset(
            chroms=chroms,
            region_bed=region_bed,
            name_to_pseudobulker=self.name_to_pseudobulker,
            bypass_keys=[self.bias_column],
            n_pseudobulks=self.n_pseudobulks,
            return_rows=return_cells,
            inplace=False,
            region_action_keys=[self.bias_column],
        )

        min_cov = self.min_cov
        max_cov = self.max_cov
        low_cov_ratio = self.low_cov_ratio
        cov_filter_name = self.cov_filter_name
        # filter coverage
        if cov_filter_name is not None:
            cov_filter_key = f"{cov_filter_name}:bulk_data"
            assert (
                cov_filter_key in self.signal_columns
            ), f"cov_filter_key {cov_filter_key} not in {self.signal_columns}"
            work_ds = self._filter_bed_regions(
                dataset=work_ds,
                cov_filter_key=cov_filter_key,
                min_cov=min_cov,
                max_cov=max_cov,
                low_cov_ratio=low_cov_ratio,
                batch_size=512,
                concurrency=1,
            )

        # add dna one hot
        work_ds = self._get_dna_one_hot(
            dataset=work_ds,
            concurrency=1,
        )

        work_ds = self._get_region_cropper(work_ds)

        if self.reverse_complement and self._dataset_mode == "train":
            work_ds = self._get_reverse_complement_region(work_ds)

        if self.region_embedding is not None:
            work_ds = self._get_add_region_embedding(work_ds)

        # remove region column
        if not return_regions:
            work_ds = work_ds.drop_columns(["region"])
        return work_ds

    def get_dataloader(
        self,
        chroms,
        region_bed_path,
        as_torch=True,
        return_regions=False,
        return_cells=False,
        n_batches=None,
        **dataloader_kwargs,
    ) -> Iterable[dict[str, Any]]:
        """
        Get the dataloader.

        Parameters
        ----------
        local_shuffle_buffer_size : int, optional
            The size of the local shuffle buffer, by default 10000.
        randomize_block_order : bool, optional
            Whether to randomize the block order, by default False.
        as_torch : bool, optional
            Whether to return a PyTorch dataloader, by default True.
        device : str, optional
            The device to use, by default None.
        return_cells : bool, optional
            Whether to return the cell ids, by default False.
        **dataloader_kwargs
            Additional keyword arguments pass to ray.data.Dataset.iter_batches.

        Returns
        -------
        DataLoader
            The dataloader.
        """
        shuffle_rows = int(500 * (self.n_pseudobulks + 1))
        shuffle_rows = min(shuffle_rows, 5000)

        # dataset_kwargs will be passed to self.get_processed_dataset method
        dataset_kwargs = {
            "chroms": chroms,
            "region_bed_path": region_bed_path,
            "return_cells": return_cells,
            "return_regions": return_regions,
        }
        data_iter_kwargs = dataloader_kwargs

        loader = self._get_dataloader_with_wrapper(
            dataset_kwargs=dataset_kwargs,
            data_iter_kwargs=data_iter_kwargs,
            as_torch=as_torch,
            shuffle_rows=shuffle_rows,
            n_batches=n_batches,
            batch_size=self.batch_size,
        )
        return loader
