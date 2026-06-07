import csv
import io
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_DIR = Path("data")
DB_PATH = DB_DIR / "tickets.db"


def _get_connection() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_number TEXT NOT NULL UNIQUE,
            text TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            team TEXT NOT NULL,
            summary TEXT NOT NULL,
            confidence TEXT NOT NULL,
            reasoning TEXT NOT NULL,
            model TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def _next_ticket_number(conn: sqlite3.Connection) -> str:
    row = conn.execute("SELECT COUNT(*) as cnt FROM tickets").fetchone()
    next_num = (row["cnt"] if row else 0) + 1
    return f"TCK-{next_num:03d}"


class TicketService:
    @staticmethod
    async def create(
        text: str,
        result: dict[str, str],
        model: str,
    ) -> dict[str, Any]:
        def _sync() -> dict[str, Any]:
            conn = _get_connection()
            now = datetime.now(timezone.utc).isoformat()
            tck = _next_ticket_number(conn)
            cursor = conn.execute(
                """
                INSERT INTO tickets
                    (ticket_number, text, category, priority, team, summary,
                     confidence, reasoning, model, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    tck, text,
                    result["category"], result["priority"],
                    result["team"], result["summary"],
                    result["confidence"], result["reasoning"],
                    model, "Open", now, now,
                ),
            )
            entry_id = cursor.lastrowid
            if entry_id is None:
                raise RuntimeError("Failed to create ticket")
            conn.commit()
            row = conn.execute(
                "SELECT * FROM tickets WHERE id = ?", (entry_id,)
            ).fetchone()
            conn.close()
            return dict(row)

        import anyio
        return await anyio.to_thread.run_sync(_sync)

    @staticmethod
    async def list_tickets(
        limit: int = 50, offset: int = 0
    ) -> tuple[list[dict[str, Any]], int]:
        def _sync() -> tuple[list[dict[str, Any]], int]:
            conn = _get_connection()
            total_row = conn.execute(
                "SELECT COUNT(*) as cnt FROM tickets"
            ).fetchone()
            total = total_row["cnt"] if total_row else 0
            rows = conn.execute(
                "SELECT * FROM tickets ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()
            conn.close()
            return [dict(r) for r in rows], total

        import anyio
        return await anyio.to_thread.run_sync(_sync)

    @staticmethod
    async def get_ticket(ticket_id: int) -> dict[str, Any] | None:
        def _sync() -> dict[str, Any] | None:
            conn = _get_connection()
            row = conn.execute(
                "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
            ).fetchone()
            conn.close()
            return dict(row) if row else None

        import anyio
        return await anyio.to_thread.run_sync(_sync)

    @staticmethod
    async def update_status(ticket_id: int, status: str) -> dict[str, Any] | None:
        def _sync() -> dict[str, Any] | None:
            conn = _get_connection()
            now = datetime.now(timezone.utc).isoformat()
            cursor = conn.execute(
                "UPDATE tickets SET status = ?, updated_at = ? WHERE id = ?",
                (status, now, ticket_id),
            )
            if cursor.rowcount == 0:
                conn.close()
                return None
            conn.commit()
            row = conn.execute(
                "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
            ).fetchone()
            conn.close()
            return dict(row) if row else None

        import anyio
        return await anyio.to_thread.run_sync(_sync)

    @staticmethod
    async def delete_ticket(ticket_id: int) -> bool:
        def _sync() -> bool:
            conn = _get_connection()
            cursor = conn.execute(
                "DELETE FROM tickets WHERE id = ?", (ticket_id,)
            )
            deleted = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return deleted

        import anyio
        return await anyio.to_thread.run_sync(_sync)

    @staticmethod
    async def export_csv() -> str:
        def _sync() -> str:
            conn = _get_connection()
            rows = conn.execute(
                "SELECT * FROM tickets ORDER BY created_at DESC"
            ).fetchall()
            conn.close()

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow([
                "id", "ticket_number", "text", "category", "priority", "team",
                "summary", "confidence", "reasoning", "model", "status",
                "created_at", "updated_at",
            ])
            for row in rows:
                writer.writerow([
                    row["id"], row["ticket_number"], row["text"],
                    row["category"], row["priority"], row["team"],
                    row["summary"], row["confidence"], row["reasoning"],
                    row["model"], row["status"], row["created_at"],
                    row["updated_at"],
                ])
            return output.getvalue()

        import anyio
        return await anyio.to_thread.run_sync(_sync)

    @staticmethod
    async def export_json() -> str:
        def _sync() -> str:
            conn = _get_connection()
            rows = conn.execute(
                "SELECT * FROM tickets ORDER BY created_at DESC"
            ).fetchall()
            conn.close()
            entries = [dict(r) for r in rows]
            return json.dumps(entries, indent=2, ensure_ascii=False)

        import anyio
        return await anyio.to_thread.run_sync(_sync)
