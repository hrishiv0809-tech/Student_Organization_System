import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.services.scheduler import start_scheduler, shutdown_scheduler
from app.routers import (
    auth_router,
    members_router,
    memberships_router,
    events_router,
    tickets_router,
    checkin_router,
    announcements_router,
    newsletter_router,
    products_router,
    orders_router,
    fundraisers_router,
    tasks_router,
    expenses_router,
    finance_router,
    dashboard_router,
    uploads_router,
    emails_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    start_scheduler()
    yield
    shutdown_scheduler()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
# Copy demo images (used by the seed data) into the upload folder if missing
_seed_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "seed_assets")
if os.path.isdir(_seed_dir):
    import shutil
    for _name in os.listdir(_seed_dir):
        _dst = os.path.join(settings.UPLOAD_DIR, _name)
        if not os.path.exists(_dst):
            shutil.copy2(os.path.join(_seed_dir, _name), _dst)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

api_prefix = settings.API_V1_STR
app.include_router(auth_router, prefix=api_prefix)
app.include_router(members_router, prefix=api_prefix)
app.include_router(memberships_router, prefix=api_prefix)
app.include_router(events_router, prefix=api_prefix)
app.include_router(tickets_router, prefix=api_prefix)
app.include_router(checkin_router, prefix=api_prefix)
app.include_router(announcements_router, prefix=api_prefix)
app.include_router(newsletter_router, prefix=api_prefix)
app.include_router(products_router, prefix=api_prefix)
app.include_router(orders_router, prefix=api_prefix)
app.include_router(fundraisers_router, prefix=api_prefix)
app.include_router(tasks_router, prefix=api_prefix)
app.include_router(expenses_router, prefix=api_prefix)
app.include_router(finance_router, prefix=api_prefix)
app.include_router(dashboard_router, prefix=api_prefix)
app.include_router(uploads_router, prefix=api_prefix)
app.include_router(emails_router, prefix=api_prefix)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}

@app.get("/")
def root_redirect():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API. Docs available at /docs"}
