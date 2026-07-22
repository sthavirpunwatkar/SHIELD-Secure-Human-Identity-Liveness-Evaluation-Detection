# SHIELD - Database Inventory

## SQLite Database: `shield_local.db`

### Table: `verifications`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | TEXT | PRIMARY KEY | Unique identifier (UUID) for the log entry. |
| `session_id` | TEXT | | UUID identifying the overall session from `SessionManager`. |
| `verdict` | TEXT | | Final fused verdict (e.g., 'Live', 'Spoof', 'Low Quality', 'No Face Detected'). |
| `confidence` | REAL | | Final fusion confidence score. |
| `details` | TEXT | | JSON blob representing individual breakdown scores (rppg, behavior, antispoof, etc.) and reasons. |
| `image_url` | TEXT | | Local path / URL mapping to snapshot in `local_storage/snapshots/`. |
| `timestamp` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Database entry creation time. |

## Local Storage

| Path | Purpose |
|------|---------|
| `local_storage/snapshots/` | Stores JPEG snapshots captured during the verification lifecycle for auditing and manual review. |
| `logs/sessions/` | JSONL log files (one per `session_uuid`) tracking per-frame processing latency, verdict, and confidence. |
| `logs/debug_verify.log` | JSONL logs capturing real-time validation data for passive verification. |
