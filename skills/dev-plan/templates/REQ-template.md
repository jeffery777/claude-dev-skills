---
id: REQ-000
title: <short title in the user's terms>
status: proposed            # proposed | active | conflict | done | superseded | dropped
sources:                    # verbatim originals only; never paraphrase here
  - type: chat              # doc | chat | issue | commit | external
    locator: "<where to find it again: file + page or #anchor, date, URL, or commit SHA>"
    quote: "<exact words, unedited>"
non_goals:
  - <what the sources say is out of scope>
depends_on: []              # typed relations: lists of existing REQ ids
refines: []                 #   refines: this REQ narrows or details another
conflicts_with: []          #   conflicts_with: set status: conflict and fill ## Conflicts
superseded_by: []           #   superseded_by: set status: superseded and superseded_reason
superseded_reason: null     # why it was superseded, with a source locator
---

## Need

<Model summary of the sources. Keep it apart from the quotes above and do not
widen it. Mark anything inferred, and keep status: proposed until the user
confirms it.>

## Acceptance

- <An observable, checkable criterion.>

## Conflicts

<Only when status is conflict. List each side with its source locator. Do not
choose between them; the user decides.>

## Notes

<Decisions, their reasons, and [[REQ-xxx-slug]] links.>
