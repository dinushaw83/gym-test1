"""
Run script for gym-proj3 backend
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8880,
        reload=True
    )


