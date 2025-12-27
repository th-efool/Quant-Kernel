import yaml
from core.CommonTypes import QKApi


TICKER_FILE = "data/APIs/ticker_symbols/india.yaml"


def load_tickers_for_api(api: QKApi, exchange: str):
    with open(TICKER_FILE, "r") as f:
        config = yaml.safe_load(f)

    providers = config["providers"]

    if api == QKApi.yfinance:
        return providers["yfinance"]["symbols"]

    if api == QKApi.upstox:
        return providers["upstox"]["symbols"]

    if api == QKApi.dhan:
        return providers["dhan"]["symbol_security_pairs"]

    raise ValueError(f"Unsupported API: {api}")
