# Idea Definition — Example (Filled)

This file is a realistic example of a high-quality completed `idea.md`.

## 2. Problem and solution
Problem: Small operations teams lose visibility when support tickets are split across tools.
Solution: A tenant-aware workflow API that unifies ticket ingestion, SLA tracking, and escalation automation.

## 4. Domain model
Entities: Ticket, Customer, SLAWindow, EscalationRule, AssignmentEvent.
Bounded contexts: intake, triage, fulfillment, reporting.

## 12. Initial queue hints (optional)
1) core-api: ticket CRUD + SLA transitions
2) infra: postgres profile + migrations
3) testing: auth + tenancy regression suite

## 16. Open questions
- Should SLA breaches trigger email or webhook first?

## 17. Non-goals
- No AI auto-resolution in v1.
- No external marketplace integrations until v2.
