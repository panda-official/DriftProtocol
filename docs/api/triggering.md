# Triggering

Package: **drift.proto.trigger_service**

[PANDA|Drift Platform](https://driftpythonclient.readthedocs.io/en/latest/docs/panda_drift/#integration) has an
event-driven model. So each service must be triggered by an input package. For services from Data
Acquisition Subsystem it is **TriggerMessage** or *IntervalTriggerMessage*.

## TriggerMessage

TriggerMessage is needed for services which make a "snapshot" of data e.g. an image.

| Name      | Type      | Description          |
|-----------|-----------|----------------------|
| timestamp | Timestamp | Timestamp of trigger |

## IntervalTriggerMessage

IntervalTriggerMessage should be sent when a receiving service takes some data for a time interval.

| Name            | Type      | Description                |
|-----------------|-----------|----------------------------|
| start_timestamp | Timestamp | Start time point of sample |
| stop_timestamp  | Timestamp | Stop time point of sample  |