# docs/operations/scaling.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- Optional per spec §26.12 item 401 -->

> PURPOSE: Scaling playbook: horizontal pod autoscaling, workers, cache. Per spec §26.12 item 401.

## Horizontal Pod Autoscaling

> CONTENT: K8s HPA configuration per deploy/k8s/base/hpa.yaml. Trigger thresholds, scale-up/down delays.

## Worker Scaling

> CONTENT: When to scale workers independently from the API. Worker concurrency settings per broker.

## Caching

> CONTENT: When to add caching: identifying hot read paths, Redis integration, cache invalidation patterns.
