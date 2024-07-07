# ruff: noqa
from typing import Dict, List

import torch.cuda
from torch import nn

from pytorch_optimizer.base.types import OPTIMIZER, PARAMETERS, SCHEDULER
from pytorch_optimizer.loss.bi_tempered import BinaryBiTemperedLogisticLoss, BiTemperedLogisticLoss
from pytorch_optimizer.loss.cross_entropy import BCELoss
from pytorch_optimizer.loss.dice import DiceLoss, soft_dice_score
from pytorch_optimizer.loss.f1 import SoftF1Loss
from pytorch_optimizer.loss.focal import BCEFocalLoss, FocalCosineLoss, FocalLoss, FocalTverskyLoss
from pytorch_optimizer.loss.jaccard import JaccardLoss, soft_jaccard_score
from pytorch_optimizer.loss.ldam import LDAMLoss
from pytorch_optimizer.loss.lovasz import LovaszHingeLoss
from pytorch_optimizer.loss.tversky import TverskyLoss
from pytorch_optimizer.lr_scheduler import (
    ConstantLR,
    CosineAnnealingLR,
    CosineAnnealingWarmRestarts,
    CyclicLR,
    MultiplicativeLR,
    MultiStepLR,
    OneCycleLR,
    SchedulerType,
    StepLR,
)
from pytorch_optimizer.lr_scheduler.chebyshev import get_chebyshev_perm_steps, get_chebyshev_schedule
from pytorch_optimizer.lr_scheduler.cosine_anealing import CosineAnnealingWarmupRestarts
from pytorch_optimizer.lr_scheduler.experimental.deberta_v3_lr_scheduler import deberta_v3_large_lr_scheduler
from pytorch_optimizer.lr_scheduler.linear_warmup import CosineScheduler, LinearScheduler, PolyScheduler
from pytorch_optimizer.lr_scheduler.proportion import ProportionScheduler
from pytorch_optimizer.lr_scheduler.rex import REXScheduler
from pytorch_optimizer.lr_scheduler.wsd import get_wsd_schedule
from pytorch_optimizer.optimizer.a2grad import A2Grad
from pytorch_optimizer.optimizer.adabelief import AdaBelief
from pytorch_optimizer.optimizer.adabound import AdaBound
from pytorch_optimizer.optimizer.adadelta import AdaDelta
from pytorch_optimizer.optimizer.adafactor import AdaFactor
from pytorch_optimizer.optimizer.adahessian import AdaHessian
from pytorch_optimizer.optimizer.adai import Adai
from pytorch_optimizer.optimizer.adalite import Adalite
from pytorch_optimizer.optimizer.adam_mini import AdamMini
from pytorch_optimizer.optimizer.adamax import AdaMax
from pytorch_optimizer.optimizer.adamod import AdaMod
from pytorch_optimizer.optimizer.adamp import AdamP
from pytorch_optimizer.optimizer.adams import AdamS
from pytorch_optimizer.optimizer.adamw import StableAdamW
from pytorch_optimizer.optimizer.adan import Adan
from pytorch_optimizer.optimizer.adanorm import AdaNorm
from pytorch_optimizer.optimizer.adapnm import AdaPNM
from pytorch_optimizer.optimizer.adashift import AdaShift
from pytorch_optimizer.optimizer.adasmooth import AdaSmooth
from pytorch_optimizer.optimizer.agc import agc
from pytorch_optimizer.optimizer.aggmo import AggMo
from pytorch_optimizer.optimizer.aida import Aida
from pytorch_optimizer.optimizer.alig import AliG
from pytorch_optimizer.optimizer.amos import Amos
from pytorch_optimizer.optimizer.apollo import Apollo
from pytorch_optimizer.optimizer.avagrad import AvaGrad
from pytorch_optimizer.optimizer.came import CAME
from pytorch_optimizer.optimizer.dadapt import DAdaptAdaGrad, DAdaptAdam, DAdaptAdan, DAdaptLion, DAdaptSGD
from pytorch_optimizer.optimizer.diffgrad import DiffGrad
from pytorch_optimizer.optimizer.fadam import FAdam
from pytorch_optimizer.optimizer.fp16 import DynamicLossScaler, SafeFP16Optimizer
from pytorch_optimizer.optimizer.fromage import Fromage
from pytorch_optimizer.optimizer.galore import GaLore, GaLoreProjector
from pytorch_optimizer.optimizer.gc import centralize_gradient
from pytorch_optimizer.optimizer.gravity import Gravity
from pytorch_optimizer.optimizer.grokfast import GrokFastAdamW, gradfilter_ema, gradfilter_ma
from pytorch_optimizer.optimizer.kate import Kate
from pytorch_optimizer.optimizer.lamb import Lamb
from pytorch_optimizer.optimizer.lars import LARS
from pytorch_optimizer.optimizer.lion import Lion
from pytorch_optimizer.optimizer.lomo import LOMO
from pytorch_optimizer.optimizer.lookahead import Lookahead
from pytorch_optimizer.optimizer.madgrad import MADGRAD
from pytorch_optimizer.optimizer.msvag import MSVAG
from pytorch_optimizer.optimizer.nero import Nero
from pytorch_optimizer.optimizer.novograd import NovoGrad
from pytorch_optimizer.optimizer.padam import PAdam
from pytorch_optimizer.optimizer.pcgrad import PCGrad
from pytorch_optimizer.optimizer.pid import PID
from pytorch_optimizer.optimizer.pnm import PNM
from pytorch_optimizer.optimizer.prodigy import Prodigy
from pytorch_optimizer.optimizer.qhadam import QHAdam
from pytorch_optimizer.optimizer.qhm import QHM
from pytorch_optimizer.optimizer.radam import RAdam
from pytorch_optimizer.optimizer.ranger import Ranger
from pytorch_optimizer.optimizer.ranger21 import Ranger21
from pytorch_optimizer.optimizer.rotograd import RotoGrad
from pytorch_optimizer.optimizer.sam import BSAM, GSAM, SAM, WSAM
from pytorch_optimizer.optimizer.schedulefree import ScheduleFreeAdamW, ScheduleFreeSGD
from pytorch_optimizer.optimizer.sgd import ASGD, SGDW, AccSGD, SignSGD
from pytorch_optimizer.optimizer.sgdp import SGDP
from pytorch_optimizer.optimizer.shampoo import ScalableShampoo, Shampoo
from pytorch_optimizer.optimizer.shampoo_utils import (
    AdaGradGraft,
    BlockPartitioner,
    Graft,
    LayerWiseGrafting,
    PreConditioner,
    PreConditionerType,
    RMSPropGraft,
    SGDGraft,
    SQRTNGraft,
    compute_power_schur_newton,
    compute_power_svd,
    merge_small_dims,
    power_iteration,
)
from pytorch_optimizer.optimizer.sm3 import SM3
from pytorch_optimizer.optimizer.sophia import SophiaH
from pytorch_optimizer.optimizer.srmm import SRMM
from pytorch_optimizer.optimizer.swats import SWATS
from pytorch_optimizer.optimizer.tiger import Tiger
from pytorch_optimizer.optimizer.utils import (
    clip_grad_norm,
    disable_running_stats,
    enable_running_stats,
    get_global_gradient_norm,
    get_optimizer_parameters,
    normalize_gradient,
    reduce_max_except_dim,
    unit_norm,
)
from pytorch_optimizer.optimizer.yogi import Yogi

try:
    import bitsandbytes as bnb

    HAS_BNB: bool = True  # pragma: no cover
except ImportError:
    HAS_BNB: bool = False

OPTIMIZER_LIST: List[OPTIMIZER] = [
    AdaBelief,
    AdaBound,
    PID,
    AdamP,
    Adai,
    Adan,
    AdaMod,
    AdaPNM,
    DiffGrad,
    Lamb,
    LARS,
    QHAdam,
    QHM,
    MADGRAD,
    Nero,
    PNM,
    MSVAG,
    RAdam,
    Ranger,
    Ranger21,
    SGDP,
    Shampoo,
    ScalableShampoo,
    DAdaptAdaGrad,
    Fromage,
    AggMo,
    DAdaptAdam,
    DAdaptSGD,
    DAdaptAdan,
    AdamS,
    AdaFactor,
    Apollo,
    SWATS,
    NovoGrad,
    Lion,
    AliG,
    SM3,
    AdaNorm,
    A2Grad,
    AccSGD,
    SGDW,
    Yogi,
    ASGD,
    AdaMax,
    Gravity,
    AdaSmooth,
    SRMM,
    AvaGrad,
    AdaShift,
    AdaDelta,
    Amos,
    AdaHessian,
    SophiaH,
    SignSGD,
    Prodigy,
    PAdam,
    LOMO,
    Tiger,
    CAME,
    DAdaptLion,
    Aida,
    GaLore,
    Adalite,
    BSAM,
    ScheduleFreeSGD,
    ScheduleFreeAdamW,
    FAdam,
    GrokFastAdamW,
    Kate,
    StableAdamW,
    AdamMini,
]
OPTIMIZERS: Dict[str, OPTIMIZER] = {str(optimizer.__name__).lower(): optimizer for optimizer in OPTIMIZER_LIST}

LR_SCHEDULER_LIST: Dict = {
    SchedulerType.CONSTANT: ConstantLR,
    SchedulerType.STEP: StepLR,
    SchedulerType.MULTI_STEP: MultiStepLR,
    SchedulerType.CYCLIC: CyclicLR,
    SchedulerType.MULTIPLICATIVE: MultiplicativeLR,
    SchedulerType.ONE_CYCLE: OneCycleLR,
    SchedulerType.COSINE: CosineScheduler,
    SchedulerType.POLY: PolyScheduler,
    SchedulerType.LINEAR: LinearScheduler,
    SchedulerType.PROPORTION: ProportionScheduler,
    SchedulerType.COSINE_ANNEALING: CosineAnnealingLR,
    SchedulerType.COSINE_ANNEALING_WITH_WARMUP: CosineAnnealingWarmupRestarts,
    SchedulerType.COSINE_ANNEALING_WITH_WARM_RESTART: CosineAnnealingWarmRestarts,
    SchedulerType.CHEBYSHEV: get_chebyshev_schedule,
    SchedulerType.REX: REXScheduler,
    SchedulerType.WARMUP_STABLE_DECAY: get_wsd_schedule,
}
LR_SCHEDULERS: Dict[str, SCHEDULER] = {
    str(lr_scheduler_name).lower(): lr_scheduler for lr_scheduler_name, lr_scheduler in LR_SCHEDULER_LIST.items()
}

LOSS_FUNCTION_LIST: List = [
    BCELoss,
    BCEFocalLoss,
    FocalLoss,
    SoftF1Loss,
    DiceLoss,
    LDAMLoss,
    FocalCosineLoss,
    JaccardLoss,
    BiTemperedLogisticLoss,
    BinaryBiTemperedLogisticLoss,
    TverskyLoss,
    FocalTverskyLoss,
    LovaszHingeLoss,
]
LOSS_FUNCTIONS: Dict[str, nn.Module] = {
    str(loss_function.__name__).lower(): loss_function for loss_function in LOSS_FUNCTION_LIST
}


def load_bnb_optimizer(optimizer: str) -> OPTIMIZER:  # pragma: no cover
    r"""load bnb optimizer instance."""
    if 'sgd8bit' in optimizer:
        return bnb.optim.SGD8bit
    if 'adam8bit' in optimizer:
        return bnb.optim.Adam8bit
    if 'adamw8bit' in optimizer:
        return bnb.optim.AdamW8bit
    if 'lamb8bit' in optimizer:
        return bnb.optim.LAMB8bit
    if 'lars8bit' in optimizer:
        return bnb.optim.LARS8bit
    if 'lion8bit' in optimizer:
        return bnb.optim.Lion8bit
    if 'adagrad8bit' in optimizer:
        return bnb.optim.Adagrad8bit
    if 'rmsprop8bit' in optimizer:
        return bnb.optim.RMSprop8bit
    raise NotImplementedError(f'[-] not implemented optimizer : {optimizer}')


def load_optimizer(optimizer: str) -> OPTIMIZER:
    optimizer: str = optimizer.lower()

    if optimizer.startswith('bnb'):
        if HAS_BNB and torch.cuda.is_available():
            return load_bnb_optimizer(optimizer)  # pragma: no cover
        raise ImportError(f'[-] bitsandbytes and CUDA required for bnb optimizers : {optimizer}')
    if optimizer not in OPTIMIZERS:
        raise NotImplementedError(f'[-] not implemented optimizer : {optimizer}')

    return OPTIMIZERS[optimizer]


def create_optimizer(
    model: nn.Module,
    optimizer_name: str,
    lr: float = 1e-3,
    weight_decay: float = 0.0,
    wd_ban_list: List[str] = ('bias', 'LayerNorm.bias', 'LayerNorm.weight'),
    use_lookahead: bool = False,
    **kwargs,
):
    r"""Build optimizer.

    :param model: nn.Module. model.
    :param optimizer_name: str. name of optimizer.
    :param lr: float. learning rate.
    :param weight_decay: float. weight decay.
    :param wd_ban_list: List[str]. weight decay ban list by layer.
    :param use_lookahead: bool. use lookahead.
    """
    optimizer_name = optimizer_name.lower()

    parameters = (
        get_optimizer_parameters(model, weight_decay, wd_ban_list) if weight_decay > 0.0 else model.parameters()
    )

    optimizer = load_optimizer(optimizer_name)

    if optimizer_name == 'alig':
        optimizer = optimizer(parameters, max_lr=lr, **kwargs)
    else:
        optimizer = optimizer(parameters, lr=lr, **kwargs)

    if use_lookahead:
        optimizer = Lookahead(
            optimizer,
            k=kwargs['k'] if 'k' in kwargs else 5,
            alpha=kwargs['alpha'] if 'alpha' in kwargs else 0.5,
            pullback_momentum=kwargs['pullback_momentum'] if 'pullback_momentum' in kwargs else 'none',
        )

    return optimizer


def load_lr_scheduler(lr_scheduler: str) -> SCHEDULER:
    lr_scheduler: str = lr_scheduler.lower()

    if lr_scheduler not in LR_SCHEDULERS:
        raise NotImplementedError(f'[-] not implemented lr_scheduler : {lr_scheduler}')

    return LR_SCHEDULERS[lr_scheduler]


def get_supported_optimizers() -> List[OPTIMIZER]:
    return OPTIMIZER_LIST


def get_supported_lr_schedulers() -> List[SCHEDULER]:
    return list(LR_SCHEDULER_LIST.values())


def get_supported_loss_functions() -> List[nn.Module]:
    return LOSS_FUNCTION_LIST
