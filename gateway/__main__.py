import uvicorn
from gateway.settings import setting

if __name__ == "__main__":
    uvicorn.run(
        "app:app", host=setting.server_host, port=setting.server_port, reload=True
    )
