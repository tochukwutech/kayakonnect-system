class PricingEngine:
    def __init__(self):
        # Base flat rate (₦)
        self.base_fare = 500.00

        # Load size multipliers
        self.load_multipliers = {
            "small":  1.0,
            "medium": 1.5,
            "large":  2.2
        }

        # Urgency multipliers
        # Mapped from UI labels (low/normal/high) to Sean's pricing_engine values
        self.urgency_multipliers = {
            "low":    1.0,   # slight
            "normal": 1.3,   # fair
            "high":   1.8    # high
        }

        # Cost per simulated kilometre (₦)
        self.cost_per_km = 150.00

    def _calculate_distance(self, location: str, destination: str) -> float:
        loc  = location.strip().lower()
        dest = destination.strip().lower()

        if loc == dest:
            return 2.0

        simulated_distance = max(5.0, float((len(loc) + len(dest)) % 25))
        return simulated_distance

    def calculate_price(self, load_size: str, urgency_level: str,
                        location: str, destination: str) -> float:
        load    = load_size.strip().lower()
        urgency = urgency_level.strip().lower()

        load_mult    = self.load_multipliers.get(load, 1.0)
        urgency_mult = self.urgency_multipliers.get(urgency, 1.0)

        distance      = self._calculate_distance(location, destination)
        distance_cost = distance * self.cost_per_km

        total = (self.base_fare + distance_cost) * load_mult * urgency_mult
        return round(total, 2)

    def suggest_price(self, load_size: str, urgency_level: str,
                      location: str, destination: str) -> dict:
        recommended = self.calculate_price(
            load_size, urgency_level, location, destination
        )
        return {
            "status": "success",
            "parameters_received": {
                "load_size":     load_size,
                "urgency_level": urgency_level,
                "pickup":        location,
                "destination":   destination
            },
            "recommended_price": recommended
        }


## test code to check if engine is working as expected
if __name__ == "__main__":
    print("=" * 50)
    print("    KAYAKONNECT PRICING ENGINE - TEST RUN    ")
    print("=" * 50)

    engine = PricingEngine()

    print("\n[Test 1] Small, Normal urgency — Ikeja to Lekki")
    r1 = engine.suggest_price("small", "normal", "Ikeja", "Lekki")
    print(f"  → ₦{r1['recommended_price']}")

    print("\n[Test 2] Large, High urgency — Surulere to Yaba")
    r2 = engine.suggest_price("large", "high", "Surulere", "Yaba")
    print(f"  → ₦{r2['recommended_price']}")

    print("\n[Test 3] Medium, Low urgency — Abuja to Wuse 2")
    r3 = engine.suggest_price("medium", "low", "Abuja", "Wuse 2")
    print(f"  → ₦{r3['recommended_price']}")

    print("\n" + "=" * 50)