from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import Base, engine
from routers import register, panic, alerts , blockchain_op, tourist_profile
import os

# Ensure tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers (API endpoints)
app.include_router(register.router, prefix="/register", tags=["Tourists"])
app.include_router(tourist_profile.router, prefix="/tourist", tags=["Tourists"])
app.include_router(panic.router, prefix="/panic", tags=["Tourists"])
app.include_router(alerts.router, prefix="/alerts", tags=["Tourists"])
app.include_router(blockchain_op.router, prefix="/blockchain", tags=["Tourists"])
# app.include_router(zones.router, prefix="/zones", tags=["Zones"])

# --- NEW: Serve Frontend ---
# Figure out path to /frontend folder (assuming it sits next to /backend)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Mount frontend as static files (CSS, JS, images)
app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(frontend_path, "js")), name="js")

# Serve index.html as root
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(frontend_path, "register.html"))

# Optional: serve other HTML files by filename (dashboard.html, blockchain.html)
@app.get("/{page_name}")
async def serve_page(page_name: str):
    file_path = os.path.join(frontend_path, page_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "Page not found"}
