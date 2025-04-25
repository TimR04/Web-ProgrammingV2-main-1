import pandas as pd
import os

def load_iso_mapping(filepath: str) -> dict[str, str]:
    """
    Load ISO3 to country name mapping from a CSV file.

    Args:
        filepath (str): Path to CSV file (semicolon-separated, encoded in latin1).

    Returns:
        dict[str, str]: Mapping of ISO3 codes to country names.
    """
    try:
        # Datei mit Semikolon und latin1-Kodierung lesen
        df = pd.read_csv(filepath, sep=';', encoding='latin1')
        df.columns = df.columns.str.strip()
        return dict(zip(df["ISO3"].str.strip().str.upper(), df["Country"].str.strip()))
    except Exception as e:
        print(f"❌ Error loading ISO code mapping: {e}")
        return {}
