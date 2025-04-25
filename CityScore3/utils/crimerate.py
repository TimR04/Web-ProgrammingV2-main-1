import pandas as pd


import pandas as pd

def calculate_safety_score(filepath: str, country_name: str) -> float | None:
    """
    Calculates normalized safety score (0–100) from raw crime index.
    Higher crime index = worse safety.
    """
    try:
        df = pd.read_csv(filepath, sep=';', names=["Country", "CrimeScore"], decimal='.', engine='python')
        df["Country"] = df["Country"].str.strip()
        df["CrimeScore"] = pd.to_numeric(df["CrimeScore"], errors="coerce")

        match = df[df["Country"].str.lower() == country_name.lower()]
        if match.empty:
            return None

        value = match["CrimeScore"].values[0]

        # Dynamische Skala aus Daten ableiten
        min_val = df["CrimeScore"].min()
        max_val = df["CrimeScore"].max()

        # Umkehrung: je höher der CrimeIndex, desto schlechter die Sicherheit
        normalized = (max_val - value) / (max_val - min_val) * 100

        return round(normalized, 2)

    except Exception as e:
        print(f"❌ Error processing crime data file: {e}")
        return None



def get_crime_index(filepath: str, country_name: str) -> float | None:
    """
    Returns the raw crime index for a given country from the CSV file.

    Args:
        filepath (str): Path to the CSV file (semicolon-separated).
        country_name (str): Country name (case-insensitive).

    Returns:
        float | None: Crime index or None if not found.
    """
    try:
        df = pd.read_csv(filepath, sep=';', names=["Country", "CrimeScore"], decimal=',', engine='python')
        df["Country"] = df["Country"].str.strip()

        match = df[df["Country"].str.lower() == country_name.lower()]
        if match.empty:
            return None

        return round(float(match["CrimeScore"].values[0]), 2)

    except Exception as e:
        print(f"❌ Error reading crime data: {e}")
        return None

