from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class PriceRegion(str, Enum):
    INTERIOR = "interior"
    NEAR_LOW = "near_low"
    NEAR_HIGH = "near_high"
    EXTREME_LOW = "extreme_low"
    EXTREME_HIGH = "extreme_high"


class EventPhase(str, Enum):
    PRE_EVENT = "pre_event"
    LIVE = "live"
    POST_EVENT = "post_event"


class MarketCategory(str, Enum):
    RETAIL_HEAVY = "retail_heavy"
    INFO_HEAVY = "info_heavy"
    MIXED = "mixed"


class DominantProcess(str, Enum):
    CROWD = "crowd"
    AGENT = "agent"
    BOUNDARY = "boundary"
    MIXED = "mixed"
    UNCLEAR = "unclear"


class DecisionType(str, Enum):
    NO_TRADE = "NO_TRADE"
    WATCH = "WATCH"
    FADE = "FADE"
    FOLLOW = "FOLLOW"
    BOUNDARY_FADE = "BOUNDARY_FADE"
    BOUNDARY_FOLLOW = "BOUNDARY_FOLLOW"
    EXIT = "EXIT"
    REDUCE = "REDUCE"


class LifecyclePhase(str, Enum):
    SETUP = "setup"
    ENTRY = "entry"
    VALIDATION = "validation"
    SCALE = "scale"
    EXIT = "exit"
    INVALIDATION = "invalidation"
    CLOSED = "closed"


@dataclass(slots=True)
class MarketState:
    market_id: str
    timestamp: datetime
    mid_price: float
    yes_price: float | None = None
    no_price: float | None = None
    spread: float = 0.0
    depth: float = 0.0
    recent_volume: float = 0.0
    order_flow_imbalance: float = 0.0
    trade_aggression: float = 0.0
    price_change: float = 0.0
    event_phase: EventPhase = EventPhase.PRE_EVENT
    market_category: MarketCategory = MarketCategory.MIXED
    price_region: PriceRegion = PriceRegion.INTERIOR


@dataclass(slots=True)
class WalletState:
    market_id: str
    timestamp: datetime
    wallet_id: str = "aggregate"
    wallet_trade_size: float = 0.0
    wallet_concentration: float = 0.0
    timing_score: float = 0.0
    specialization_score: float = 0.0
    persistence_score: float = 0.0


@dataclass(slots=True)
class SignalState:
    order_flow_imbalance: float
    trade_aggression: float
    liquidity_thinness: float
    price_acceleration: float
    wallet_concentration: float
    persistence: float
    crowd_pressure_score: float
    agent_credibility_score: float
    overreaction_indicator: float


@dataclass(slots=True)
class ProcessState:
    dominant_process: DominantProcess
    crowd_score: float
    agent_score: float
    boundary_score: float
    boundary_active: bool
    explanation: list[str] = field(default_factory=list)


@dataclass(slots=True)
class DecisionState:
    market_id: str
    timestamp: datetime
    decision_type: DecisionType
    reason_codes: list[str]
    intended_horizon: str = "fast"
    edge_level: str = "none"
    strategy_quality_score: float = 0.5


@dataclass(slots=True)
class PortfolioState:
    capital: float
    available_capital: float
    current_exposure: float = 0.0
    event_exposure: float = 0.0
    max_trade_fraction: float = 0.10
    max_total_exposure: float = 0.35
    max_event_exposure: float = 0.20
    strategy_quality_score: float = 0.50


@dataclass(slots=True)
class TradeState:
    trade_id: str
    market_id: str
    timestamp: datetime
    decision_type: DecisionType
    strategy_type: str
    lifecycle_phase: LifecyclePhase
    direction: int
    entry_price: float | None = None
    current_price: float | None = None
    exit_price: float | None = None
    size: float = 0.0
    pnl: float = 0.0
    return_pct: float = 0.0
    bars_held: int = 0
    intended_horizon: str = "fast"
    event_phase: EventPhase = EventPhase.PRE_EVENT
    price_region: PriceRegion = PriceRegion.INTERIOR
    reason_codes: list[str] = field(default_factory=list)
    status: str = "open"

