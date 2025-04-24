from fastapi import FastAPI
from .controllers import product_controller, auth_controller
from .database import engine
from .models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ecommerce API")

# Include routers
app.include_router(product_controller.router)
app.include_router(auth_controller.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)