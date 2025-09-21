import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

CHAIN_PATH = Path("data/blockchain.json")


# ---------- Shared Hash Function ----------
def compute_block_hash(block: dict) -> str:
    """
    Compute SHA256 hash of a block (excluding the 'hash' field).
    """
    block_copy = {k: block[k] for k in block if k != "hash"}
    block_json = json.dumps(block_copy, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(block_json.encode("utf-8")).hexdigest()


# ---------- Create Genesis Block ----------
def _create_genesis_block() -> dict:
    block_dict = {
        "index": 0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": "genesis",
        "prev_hash": "0"
    }
    block_dict["hash"] = compute_block_hash(block_dict)
    return block_dict


# ---------- Load or Repair Blockchain ----------
def load_chain() -> dict:
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

    if not data or "chain" not in data or len(data["chain"]) == 0:
        data = {"chain": [_create_genesis_block()]}
        CHAIN_PATH.write_text(json.dumps(data, indent=2))
        return data

    # Repair genesis block if hash is invalid
    genesis = data["chain"][0]
    correct_hash = compute_block_hash(genesis)
    if genesis.get("hash") != correct_hash:
        print("[INFO] Fixing genesis block hash")
        data["chain"][0]["hash"] = correct_hash
        CHAIN_PATH.write_text(json.dumps(data, indent=2))

    return data


# ---------- Add New Block ----------
def add_block(data: dict) -> dict:
    chain = load_chain()
    last = chain["chain"][-1]
    block_dict = {
        "index": last["index"] + 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
        "prev_hash": last["hash"]
    }
    block_dict["hash"] = compute_block_hash(block_dict)

    chain["chain"].append(block_dict)
    CHAIN_PATH.write_text(json.dumps(chain, indent=2))
    return block_dict


# ---------- Example Usage ----------
if __name__ == "__main__":
    new_block = add_block({
        "temp_id": "12e3ade1-07ed-4edb-bd3b-e7dee771470b",
        "alert_uuid": "cfbd06ce-df25-4300-bd37-135e84036e50",
        "lat": 0.0,
        "lon": 0.0,
        "message": "1234"
    })
    print("New block added:", new_block)
