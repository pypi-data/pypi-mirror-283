from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ModelSettings:
    model: str
    api_key: str
    hyperparams: Optional[dict[str, Any]]
    system_prompt: Optional[str]
    json_mode: Optional[bool] = False

@dataclass
class AgentConfig:
    architecture: Any
    model_settings: ModelSettings
    state: str
    system_prompt: str
    role: str

@dataclass
class AppConfig:
    agent: AgentConfig

@dataclass
class EvaluatorConfig:
    state: dict[str, Any]
    params: Optional[dict[str, Any]]
    model_settings: Optional[ModelSettings]
    target: Optional[Any]
    in_range: Optional[str]
    
@dataclass
class SyntheticUserSettings:
    personas: dict[str, Any]
    scenarios: dict[str, Any]
    model_settings: ModelSettings
    shuffle_seed: Optional[int]

@dataclass
class SimulationConfig:
    agent: AgentConfig
    synthetic_user: SyntheticUserSettings

@dataclass
class AIEvalConfig:
    app: AppConfig
    evaluators: dict[str, EvaluatorConfig]
    simulations: SimulationConfig
