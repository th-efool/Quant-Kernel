import yaml
from core.common_types import QKApi, TickerSource

class TickerLoader:
    def __init__(self, source: TickerSource):
        self.source = source
        self._config = self._load_yaml()

    def _load_yaml(self) -> dict:
        with open(self.source.value, "r") as f:
            return yaml.safe_load(f)

    def for_api(self, api: QKApi, exchange: str = "NSE"):
        providers = self._config.get("providers", {})

        match api:
            case QKApi.yfinance:
                return providers["yfinance"]["symbols"]

            case QKApi.upstox:
                return providers["upstox"]["symbols"]

            case QKApi.dhan:
                return providers["dhan"]["symbol_security_pairs"]

            case _:
                raise ValueError(f"Unsupported API: {api}")

    # --------------------------------------------------
    # DEBUG / INSPECTION
    # --------------------------------------------------

    def debug(self) -> None:
        """
        Print a human-readable overview of the loaded ticker config.
        """

        print("\n[TickerLoader DEBUG]")
        print(f"Source file: {self.source.value}")

        providers = self._config.get("providers", {})
        print(f"Available providers: {list(providers.keys())}")

        for provider, data in providers.items():
            print(f"\nProvider: {provider}")

            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"  {key}: {len(value)} entries")
                    else:
                        print(f"  {key}: {type(value).__name__}")
            else:
                print(f"  Invalid provider format: {type(data)}")

        print("[END DEBUG]\n")




if __name__ == "__main__":
    testLoader = TickerLoader(TickerSource.INDIA)
    testLoader.debug()
    symbols = testLoader.for_api(QKApi.yfinance)
    print("Loaded symbols:", symbols)








