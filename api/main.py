from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import articles, search, sources

app = FastAPI(
    title="GovWatch India API",
    description="Real-time Indian government news aggregator API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your Vercel domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router)
app.include_router(search.router)
app.include_router(sources.router)


@app.get("/")
async def root():
    return {
        "name": "GovWatch India API",
        "version": "0.1.0",
        "status": "running",
        "endpoints": ["/articles", "/search", "/sources"]
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
