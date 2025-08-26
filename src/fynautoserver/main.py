import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fynautoserver.routers.index import router
from fynautoserver.database import init_db

app = FastAPI()

#Router
app.include_router(router, prefix='/api',tags=["tenants"])


# Add CORS middleware **here**
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use "*" if needed during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#db connection eshtablishing
app.add_event_handler("startup",init_db)

def main():
    uvicorn.run("fynautoserver.main:app", host="0.0.0.0", port=8000, reload=True)
 
# For standalone runs (optional)
if __name__ == "__main__":
    main()