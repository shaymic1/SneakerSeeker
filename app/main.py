from sneaker_seeker.utils import read_json
from sneaker_seeker.scenario import Scenario
import matplotlib

def main() -> None:
    scenario = Scenario(**read_json("scenarios/scenario01.json"))
    print(scenario)

if __name__ == "__main__":
    main()
