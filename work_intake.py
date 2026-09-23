"""Fail-closed storage for Discord-originated implementation intakes.

Capturing or approving an intake only persists an auditable record. This module
never starts an executor, creates a branch, or performs a network request.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class IntakePolicy:
    """Allowlisted identities and values accepted by the intake boundary."""

    allowed_reactor_ids: set[int]
    allowed_executors: set[str]
    allowed_targets: set[str]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _event_key(source: dict[str, Any], reaction: dict[str, Any]) -> str:
    """Return a stable key for one Discord reaction event."""
    material = {
        "guild_id": source["guild_id"],
        "channel_id": source["channel_id"],
        "message_id": source["message_id"],
        "user_id": reaction["user_id"],
        "emoji": reaction["emoji"],
    }
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


class WorkIntakeStore:
    """JSON-backed pending-intake store with append-only audit events."""

    def __init__(self, records_path: Path, audit_path: Path):
        self.records_path = records_path
        self.audit_path = audit_path

    def list_records(self) -> list[dict[str, Any]]:
        if not self.records_path.exists():
            return []
        return json.loads(self.records_path.read_text(encoding="utf-8"))

    def capture(
        self,
        prompt: str,
        source: dict[str, Any],
        reaction: dict[str, Any],
        policy: IntakePolicy,
    ) -> tuple[dict[str, Any], bool]:
        """Capture an authorised reaction as a pending, non-executable intake."""
        if reaction["user_id"] not in policy.allowed_reactor_ids:
            raise PermissionError("reactor is not allowlisted")
        if not prompt.strip():
            raise ValueError("prompt is empty")

        key = _event_key(source, reaction)
        records = self.list_records()
        existing = next((record for record in records if record["idempotency_key"] == key), None)
        if existing:
            return existing, False

        timestamp = _utc_now()
        record = {
            "id": f"wi_{key[:16]}",
            "idempotency_key": key,
            "status": "pending_confirmation",
            "created_at": timestamp,
            "updated_at": timestamp,
            "prompt": prompt.strip(),
            "source": source,
            "reaction": reaction,
            "executor": None,
            "target": None,
            "scope": None,
            "approval": None,
        }
        records.append(record)
        self._write_records(records)
        self._append_audit("captured", record["id"], actor_id=reaction["user_id"])
        return record, True

    def approve(
        self,
        intake_id: str,
        approver_id: int,
        executor: str,
        target: str,
        scope: str,
        policy: IntakePolicy,
    ) -> dict[str, Any]:
        """Record a bounded approval only. Execution remains an external step."""
        if approver_id not in policy.allowed_reactor_ids:
            raise PermissionError("approver is not allowlisted")
        if executor not in policy.allowed_executors:
            raise ValueError("executor is not allowlisted")
        if target not in policy.allowed_targets:
            raise ValueError("target is not allowlisted")
        if not scope.strip():
            raise ValueError("scope is empty")

        records = self.list_records()
        record = next((item for item in records if item["id"] == intake_id), None)
        if record is None:
            raise KeyError(f"unknown intake: {intake_id}")
        if record["status"] != "pending_confirmation":
            raise ValueError(f"intake is not pending: {record['status']}")

        timestamp = _utc_now()
        record.update(
            {
                "status": "approved",
                "updated_at": timestamp,
                "executor": executor,
                "target": target,
                "scope": scope.strip(),
                "approval": {"approved_by": approver_id, "approved_at": timestamp},
            }
        )
        self._write_records(records)
        self._append_audit("approved", intake_id, actor_id=approver_id)
        return record

    def _write_records(self, records: list[dict[str, Any]]) -> None:
        self.records_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.records_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.records_path)

    def _append_audit(self, event: str, intake_id: str, actor_id: int) -> None:
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {"at": _utc_now(), "event": event, "intake_id": intake_id, "actor_id": actor_id}
        with self.audit_path.open("a", encoding="utf-8") as audit_file:
            audit_file.write(json.dumps(entry, sort_keys=True) + "\n")
