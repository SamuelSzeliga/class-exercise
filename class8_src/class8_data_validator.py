import logging
logger = logging.getLogger(__name__)

def require_columns(df, required_cols):
    """Check that all required columns exist."""

    missing_columns = [col for col in required_cols if col not in df.columns]
    if missing_columns:
        #logger.error(f"{len(missing_columns)} columns missing")
        logger.error(f"Missing columns: {",".join(missing_columns)}")
        raise ValueError(f"{len(missing_columns)} columns missing")
    logger.info(f"All required columns exist")
    return df