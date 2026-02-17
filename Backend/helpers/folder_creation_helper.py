from config.folder_config import RAW_UPLOADS_DIR,PUBLISHED_DIR

def get_raw_uploads_root():
    RAW_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    return RAW_UPLOADS_DIR

def get_published_uploads_root():
    PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)
    return PUBLISHED_DIR