from gundi_core.schemas.v1 import EREvent, ERObservation
from .core import SystemEventBaseModel

# Events published by the transformer service


class EventTransformedER(SystemEventBaseModel):
    payload: EREvent


class EventUpdateTransformedER(SystemEventBaseModel):
    payload: EREventUpdate


class ObservationTransformedER(SystemEventBaseModel):
    payload: ERObservation


class ObservationUpdateTransformedER(SystemEventBaseModel):
    payload: ERObservationUpdate

