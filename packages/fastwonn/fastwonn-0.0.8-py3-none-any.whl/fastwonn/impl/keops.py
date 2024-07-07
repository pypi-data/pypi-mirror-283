#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────────────
from typing import List

import pykeops.torch as tkeops
import torch
from torch import Tensor

# ──────────────────────────────────────────────────────────────────────────────

__all__: List[str] = ["_cdist_topk_keops"]

# ──────────────────────────────────────────────────────────────────────────────


def _cdist_topk_keops(x: Tensor, k: int = 2, x_distances: bool = False) -> Tensor:
    if x_distances:
        raise NotImplementedError(
            "KeOps implementation does not support distance matrices. Use the 'torch' implementation instead."
        )

    xts: int = x.shape[1]
    xi: tkeops.LazyTensor = tkeops.Vi(0, xts)
    xj: tkeops.LazyTensor = tkeops.Vj(1, xts)
    dij = ((xi - xj) ** 2).sum(-1)
    return dij.Kmin(k + 1, dim=1)(x, x)
