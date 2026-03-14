from typing import List, Dict


class RankingEngine:

    def rank(
        self,
        snapshot: Dict[str, dict],
        metric: str = "price",
        limit: int = 5
    ) -> List[dict]:

        results = []

        for symbol, item in snapshot.items():

            value = item.get(metric)

            if value is None:
                continue

            results.append({
                "symbol": symbol,
                metric: value
            })

        results.sort(
            key=lambda x: x[metric],
            reverse=True
        )

        return results[:limit]