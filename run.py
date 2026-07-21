import os
import sys
import uvicorn

os.environ["HF_HOME"] = "D:\\montaProjet\\.huggingface"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
