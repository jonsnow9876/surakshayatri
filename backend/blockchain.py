import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

CHAIN_PATH = Path("data/blockchain.json")


# ---------- Helper: SHA256 ----------
def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ---------- Helper: Create Genesis Block ----------
def _create_genesis_block() -> dict:
    genesis_block = {
        "index": 0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": "genesis",
        "prev_hash": "0",
        "hash": _sha256("0")
    }
    return genesis_block


# ---------- Load Blockchain ----------
def load_chain() -> dict:
    """
    Load blockchain from file, create genesis block if missing, empty, or invalid.
    """
    if not CHAIN_PATH.exists():
        CHAIN_PATH.parent.mkdir(parents=True, exist_ok=True)
        chain = {"chain": [_create_genesis_block()]}
        CHAIN_PATH.write_text(json.dumps(chain, indent=2))
        return chain

    try:
        content = CHAIN_PATH.read_text()
        data = json.loads(content) if content.strip() else None
    except json.JSONDecodeError:
        data = None

    # If file is empty, invalid, or chain key is missing/empty
    if not data or "chain" not in data or len(data["chain"]) == 0:
        data = {"chain": [_create_genesis_block()]}
        CHAIN_PATH.write_text(json.dumps(data, indent=2))

    return data


# ---------- Add New Block ----------
def add_block(data: dict) -> dict:
    """
    Add a new block to the blockchain.
    Required keys in data: temp_id, alert_uuid, lat, lon
    Optional: message
    """
    chain = load_chain()
    last = chain["chain"][-1]
    index = last["index"] + 1
    timestamp = datetime.now(timezone.utc).isoformat()
    prev_hash = last["hash"]

    payload_dict = {
        "index": index,
        "timestamp": timestamp,
        "data": data,
        "prev_hash": prev_hash
    }

    payload_json = json.dumps(payload_dict, sort_keys=True)
    block_hash = _sha256(payload_json)

    new_block = {
        **payload_dict,
        "hash": block_hash
    }

    chain["chain"].append(new_block)
    CHAIN_PATH.write_text(json.dumps(chain, indent=2))

    return new_block
