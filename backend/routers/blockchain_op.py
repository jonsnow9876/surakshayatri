from fastapi import APIRouter, HTTPException
import json
from pathlib import Path
from blockchain import compute_block_hash, CHAIN_PATH  # shared hash & path

router = APIRouter()

# ---------- Load Blockchain ----------
def load_chain() -> dict:
    if not CHAIN_PATH.exists():
        return {"chain": []}
    try:
        with open(CHAIN_PATH) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"chain": []}


# ---------- Validate Blockchain ----------
@router.get("/validate")
def validate_chain_endpoint():
    """
    Validate the blockchain. Returns True if valid, else False.
    """
    chain_data = load_chain()
    chain = chain_data.get("chain", [])

    for i, block in enumerate(chain):
        recalculated_hash = compute_block_hash(block)
        if block["hash"] != recalculated_hash:
            raise HTTPException(status_code=400, detail=f"Block {i} has invalid hash")
        if i > 0 and block["prev_hash"] != chain[i-1]["hash"]:
            raise HTTPException(status_code=400, detail=f"Block {i} prev_hash mismatch")

    return {"valid": True}


# ---------- List Blocks ----------
@router.get("/list")
def list_blocks_endpoint():
    """
    Return all blocks in the blockchain.
    """
    chain_data = load_chain()
    return chain_data


# ---------- Get Block by Index ----------
@router.get("/block/{index}")
def get_block(index: int):
    """
    Return a specific block by its index.
    """
    chain_data = load_chain()
    chain = chain_data.get("chain", [])

    if index < 0 or index >= len(chain):
        raise HTTPException(status_code=404, detail="Block not found")

    return chain[index]
