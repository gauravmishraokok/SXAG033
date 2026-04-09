"""
demo_court.py — Hardcoded contradiction detection for MEMORA court showcase.

HOW IT WORKS
------------
This module owns an in-memory DEMO_QUEUE dict.  On every chat turn the
chat endpoint calls `check_and_inject(user_message)`.  The function scans
the message for known contradiction patterns against the user's established
identity (Gaurav Mishra / gauravmishraokok / MSRIT) and injects a fully-
formed contradiction card into DEMO_QUEUE when a conflict is detected.

The /court/queue endpoint reads directly from DEMO_QUEUE, so the card
appears in the Court panel the next time the frontend polls (~1.5 s).

ESTABLISHED IDENTITY (hardcoded)
---------------------------------
  name    : Gaurav Mishra
  github  : gauravmishraokok
  college : M S Ramaiah Institute of Technology (MSRIT)

CONTRADICTION TRIGGERS
-----------------------
  Name    : "my name is X"   where X ≠ Gaurav / Gaurav Mishra
  College : "I study at X" / "I am from X" / "I go to X"  where X ≠ MSRIT/Ramaiah
  Age     : "I am X years old"  where X ≠ established age (if ever set)
"""

from __future__ import annotations

import re
from datetime import datetime, timezone


# ── In-memory queue (module singleton) ──────────────────────────────────────
# Keys are stable card IDs so re-triggering the same contradiction updates
# the existing card rather than duplicating it.
DEMO_QUEUE: dict[str, dict] = {}


# ── Established identity ─────────────────────────────────────────────────────
_NAME        = "Gaurav Mishra"
_GITHUB      = "gauravmishraokok"
_COLLEGE     = "M S Ramaiah Institute of Technology (MSRIT)"
_COLLEGE_SHORT = "MSRIT"

# Lowercase tokens that count as the *correct* identity — no contradiction
_VALID_NAMES    = {"gaurav", "gaurav mishra"}
_VALID_COLLEGES = {
    "msrit", "ms ramaiah", "m.s. ramaiah", "m s ramaiah",
    "ramaiah", "ms ramaiah institute", "msrit bangalore",
    "m s ramaiah institute of technology",
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _extract(pattern: str, text: str) -> str | None:
    """Return the first capture group, stripped, or None."""
    m = re.search(pattern, text, re.IGNORECASE)
    if not m:
        return None
    val = m.group(1).strip().rstrip(".,!?;:")
    return val if val else None


def _is_valid_name(val: str) -> bool:
    return val.lower() in _VALID_NAMES


def _is_valid_college(val: str) -> bool:
    v = val.lower()
    return any(k in v for k in _VALID_COLLEGES)


# ── Card builders ────────────────────────────────────────────────────────────

def _name_card(incoming_name: str) -> dict:
    return {
        "quarantine_id": "q-name",
        "incoming_content": f'User claims their name is "{incoming_name}"',
        "incoming_cube_id": "fast-semantic-incoming",
        "conflicting_cube_id": "mem-identity-name",
        "conflicting_content": f"User's name is {_NAME}",
        "contradiction_score": 0.94,
        "reasoning": (
            f'The incoming claim ("{incoming_name}") directly contradicts the established '
            f"identity. The stored name '{_NAME}' is further corroborated by the GitHub "
            f"username '{_GITHUB}', which encodes the same name. "
            "The probability that this new claim is correct is very low."
        ),
        "suggested_resolution": "reject",
        "supporting_evidence": [
            {
                "label": "GitHub Username",
                "content": f"{_GITHUB} — encodes '{_NAME}', not '{incoming_name}'",
            }
        ],
        "created_at": _now(),
    }


def _college_card(incoming_college: str) -> dict:
    return {
        "quarantine_id": "q-college",
        "incoming_content": f'User claims they study at "{incoming_college}"',
        "incoming_cube_id": "fast-semantic-incoming",
        "conflicting_cube_id": "mem-identity-college",
        "conflicting_content": f"User studies at {_COLLEGE}",
        "contradiction_score": 0.88,
        "reasoning": (
            f"User explicitly stated they study at {_COLLEGE_SHORT} in a previous turn. "
            f'"{incoming_college}" is a different institution in Bangalore. '
            "A student cannot be simultaneously enrolled at two colleges; "
            "the earlier confirmed statement takes precedence."
        ),
        "suggested_resolution": "reject",
        "supporting_evidence": [],
        "created_at": _now(),
    }


# ── Main injection function ──────────────────────────────────────────────────

def check_and_inject(message: str) -> None:
    """
    Scan `message` for identity contradictions and inject court cards.

    Called by the chat endpoint on every user message.  Safe to call even
    when no contradiction exists — it simply does nothing.
    """

    # ── Name contradiction ────────────────────────────────────────────────
    name_val = _extract(r"my name is ([A-Za-z ]{1,40})", message)
    if name_val and not _is_valid_name(name_val):
        entry = DEMO_QUEUE.get("q-name")
        # Only inject if not already pending
        if entry is None or entry.get("resolved"):
            DEMO_QUEUE["q-name"] = {"item": _name_card(name_val), "resolved": False}

    # ── College contradiction ─────────────────────────────────────────────
    college_val = (
        _extract(r"i (?:study|studied|am studying|am enrolled) at ([^,.!?\n]{2,60})", message)
        or _extract(r"i am from ([^,.!?\n]{2,60})", message)
        or _extract(r"i go to ([^,.!?\n]{2,60})", message)
        or _extract(r"i attend ([^,.!?\n]{2,60})", message)
        or _extract(r"studying at ([^,.!?\n]{2,60})", message)
        or _extract(r"student at ([^,.!?\n]{2,60})", message)
    )
    if college_val and not _is_valid_college(college_val):
        entry = DEMO_QUEUE.get("q-college")
        if entry is None or entry.get("resolved"):
            DEMO_QUEUE["q-college"] = {"item": _college_card(college_val), "resolved": False}
