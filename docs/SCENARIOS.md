
# Imaginary Case Scenarios

## 1) Canary rollback on rising 5xx
- Input: Rollout event during canary; `http_5xx_rate` > 2% for 3m.
- Action: Request approval, then rollback deployment to previous revision; notify Slack.
- Safety: Tagged as `risky`, `prod-only` so approvals kick in by policy.

## 2) CPU burst and error rate spike in staging
- Input: CPU > 90% for 5m OR error spike.
- Action: Scale deployment +1 replica (non-prod only) and notify Slack.
- Safety: Cooldown 10m to avoid thrash.

## 3) CrashLoopBackOff remediation
- Input: K8s event with reason=CrashLoopBackOff, count ≥ 3.
- Action: Restart pod; open ticket via HTTP POST.
- Safety: Cooldown 5m to avoid loops; ticket links to audit trail.
