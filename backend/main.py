from fastapi import FastAPI
from database import Base, engine
from routers import register, panic, alerts

# Ensure tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(register.router, prefix="/register", tags=["Tourists"])
app.include_router(panic.router, prefix="/panic", tags=["Tourists"])
app.include_router(alerts.router, prefix="/alerts", tags=["Tourists"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "Suraksha Yatri Backend is running"}
