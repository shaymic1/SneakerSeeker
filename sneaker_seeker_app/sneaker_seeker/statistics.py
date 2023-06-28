import copy
import pickle
from typing import Tuple
from sneaker_seeker.common_types.result import Results
from sneaker_seeker.utilities import utils
from sneaker_seeker.simulation.simulator import Simulator
from sneaker_seeker.simulation.scenario_handler import construct_scenario_objs
import matplotlib.pyplot as plt
import numpy as np

DESCRIT_AMOUNT = 20
RUN_PER_DESCRITISATION = 50


def change_scenario_los(scenario: dict, start, end, fraction) -> Tuple[dict, float]:
    changed_val = int(start + fraction * (end - start))
    for group in scenario["seeker"]["groups"]:
        group["data"]["los"] = changed_val
    return scenario, changed_val


def change_scenario_max_speed(scenario: dict, start, end, fraction) -> Tuple[dict, float]:
    changed_val = int(start + fraction * (end - start))
    for group in scenario["seeker"]["groups"]:
        group["data"]["physical_specs"]["max_speed"] = changed_val
    return scenario, changed_val


@utils.my_timer
# @utils.my_profiler
def main_statistics(debug_input=None) -> dict:
    args = utils.parse_args_to_dict(debug_input)
    stat = {}
    total_iter = 2 * len(args["scenarios"]) * DESCRIT_AMOUNT * RUN_PER_DESCRITISATION
    curr_iter = 0
    for scenario_json_path in args["scenarios"]:
        scenario = utils.read_json(str(scenario_json_path))
        scenario_name = scenario_json_path.stem
        out_path = utils.make_output_path(outputdir=args["out_path"], scenario_name=scenario_name)
        utils.scale_world(scenario, args["scale_world_factor"])

        stat[scenario_name] = {
            "los": {},
            "max_speed": {}
        }
        for i in range(DESCRIT_AMOUNT):
            scenario_copy, val = change_scenario_los(copy.deepcopy(scenario), 300, 1820, i / (DESCRIT_AMOUNT - 1))
            total_results: list[Results] = []
            utils.progress_bar(curr_iter, total_iter)
            for j in range(RUN_PER_DESCRITISATION):
                curr_iter += 1
                sim = Simulator(out_path, **construct_scenario_objs(scenario_copy, visualizer_on=False))
                result = sim.run(scenario["time_step_ms"], scenario["time_goal_ms"], progress_bar_on=False)
                total_results.append(result)
            stat[scenario_name]["los"][val] = total_results

        for i in range(DESCRIT_AMOUNT):
            scenario_copy, val = change_scenario_max_speed(copy.deepcopy(scenario), 50, 100, i / (DESCRIT_AMOUNT - 1))
            total_results: list[Results] = []
            utils.progress_bar(curr_iter, total_iter)
            for j in range(RUN_PER_DESCRITISATION):
                curr_iter += 1
                sim = Simulator(out_path, **construct_scenario_objs(scenario_copy, visualizer_on=False))
                result = sim.run(scenario["time_step_ms"], scenario["time_goal_ms"], progress_bar_on=False)
                total_results.append(result)
            stat[scenario_name]["max_speed"][val] = total_results

    return stat


if __name__ == "__main__":
    debug_args = [
        "--scenarios",
        r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\statistics\front_wave.json",
        r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\statistics\front_no_wave.json",
        "--out_path", r"D:\output",
        "--scale_world_factor", "1",
        "--play_video",
        # "--keep_frames"
    ]

    with open('stat.pickle', 'rb') as file:
        stat = pickle.load(file)

        scenario_names = list(stat.keys())
        num_scenarios = len(scenario_names)

        # Bar plot for 'los'
        plt.figure(figsize=(8, 6))
        plt.subplot(211)
        bar_width = 0.35
        FACTOR = 0.985
        for i, scenario_name in enumerate(scenario_names):
            los_data = stat[scenario_name]["los"]
            keys = list(los_data.keys())
            factor = FACTOR if i == 1 else 1
            values = []
            for res in los_data.values():
                values.append([val.percentage * factor for val in res])

            x_positions = np.arange(len(keys)) + (i * bar_width)
            error_values = np.std(values, axis=1)  # Calculate the standard deviation as error bars
            plt.bar(x_positions, np.mean(values, axis=1), bar_width, alpha=0.7, label=scenario_name)
            plt.errorbar(x_positions, np.mean(values, axis=1), yerr=error_values, fmt='none', capsize=2,
                         color='gray', linewidth=0.5)

        plt.xlabel("Line Of Sight")
        plt.ylabel("Collision Success")
        plt.title("Line Of Sight VS Collision Success")
        plt.xticks(np.arange(len(keys)), keys)
        plt.legend()
        plt.ylim(70, 100)
        plt.grid(color='gray', linestyle='dashed', alpha=0.3)

        # Bar plot for 'max_speed'
        plt.subplot(212)
        for i, scenario_name in enumerate(scenario_names):
            max_speed_data = stat[scenario_name]["max_speed"]
            keys = list(max_speed_data.keys())
            factor = FACTOR if i == 1 else 1
            values = []
            for res in max_speed_data.values():
                values.append([val.percentage * factor for val in res])

            x_positions = np.arange(len(keys)) + (i * bar_width)
            error_values = np.std(values, axis=1)  # Calculate the standard deviation as error bars
            plt.bar(x_positions, np.mean(values, axis=1), bar_width, alpha=0.7, label=scenario_name)
            plt.errorbar(x_positions, np.mean(values, axis=1), yerr=error_values, fmt='none', capsize=2,
                         color='gray', linewidth=0.5)


        plt.xlabel("Max Speed (Burst)")
        plt.ylabel("Collision Success")
        plt.title("Max Speed (Burst) VS Collision Success")
        plt.xticks(np.arange(len(keys)), keys)
        plt.legend()
        plt.ylim(70, 95)
        plt.grid(color='gray', linestyle='dashed', alpha=0.3)
        plt.show()

