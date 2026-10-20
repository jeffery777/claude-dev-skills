---
id: REQ-001
title: Rate-limit login attempts
status: active
sources:
  - type: chat
    locator: "Fixture user, 2026-10-20"
    quote: "block brute-force login, 5 tries per minute is fine"
non_goals:
  - Global API rate limiting
depends_on: []
refines: []
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Stop brute-force login attempts.

## Acceptance

- The 6th failed attempt within 60 s returns HTTP 429.
