import os
import random
import copy
import pickle
from enum import Enum, auto
from typing import Tuple, Optional
from sneaker_seeker.common_types.result import Results
from sneaker_seeker.utilities import utils
from sneaker_seeker.simulation.simulator import Simulator
from sneaker_seeker.simulation.scenario_handler import construct_scenario_objs
import matplotlib.pyplot as plt
import numpy as np


def change_scenario_los(scenario: dict, start, end, fraction) -> Tuple[dict, float]:
    changed_val = int(start + fraction * (end - start))
    for group in scenario["seeker"]["groups"]:
        group["data"]["los"] = changed_val
    return scenario, changed_val


class Statistics:
    class ValType(Enum):
        MAX_SPEED = auto()
        LOS = auto()
        CRUISE_SPEED = auto()

    def __init__(self, args: dict):
        self.iterations = 0
        self.scenarios, self.out_paths = self.__load_scenarios(args)
        # self.val_funcs = {
        #     self.ValType.MAX_SPEED: self.__change_scenario_max_speed,
        #     self.ValType.LOS: self.__change_scenario_los
        # }

    def __val_funcs(self, val_type: ValType, scen_name: str, changed_val) -> Optional[dict]:
        if val_type == self.ValType.LOS:
            return self.__change_scenario_los(scen_name=scen_name, changed_val=changed_val)
        if val_type == self.ValType.CRUISE_SPEED:
            return self.__change_scenario_cruise_speed(scen_name=scen_name, changed_val=changed_val)
        if val_type == self.ValType.MAX_SPEED:
            return self.__change_scenario_max_speed(scen_name=scen_name, changed_val=changed_val)
        return None

    def __load_scenarios(self, args: dict) -> Tuple[dict, dict]:
        scenarios = {}
        out_paths = {}
        for scenario_json_path in args["scenarios"]:
            scen_name = scenario_json_path.stem
            scenario = utils.read_json(str(scenario_json_path))
            utils.scale_world(scenario, args["scale_world_factor"])
            scenarios[scen_name] = scenario
            out_paths[scen_name] = utils.make_output_path(outputdir=args["out_path"], scenario_name=scen_name)
        return scenarios, out_paths

    def __change_scenario_cruise_speed(self, scen_name: str, changed_val) -> dict:
        scen = copy.deepcopy(self.scenarios[scen_name])
        for group in scen["seeker"]["groups"]:
            group["data"]["physical_specs"]["cruise_speed"] = changed_val
        return scen

    def __change_scenario_max_speed(self, scen_name: str, changed_val) -> dict:
        scen = copy.deepcopy(self.scenarios[scen_name])
        for group in scen["seeker"]["groups"]:
            group["data"]["physical_specs"]["max_speed"] = changed_val
        return scen

    def __change_scenario_los(self, scen_name: str, changed_val) -> dict:
        scen = copy.deepcopy(self.scenarios[scen_name])
        for group in scen["seeker"]["groups"]:
            group["data"]["los"] = changed_val
        return scen

    def run_scenario(self, scen_name: str, val_type: ValType, start, end, steps, runs_per_step):
        res = {}
        for i in range(steps):
            changed_val = int(start + (i / (steps - 1)) * (end - start))
            scen = self.__val_funcs(val_type, scen_name, changed_val)
            total_results: list[Results] = []
            for j in range(runs_per_step):
                sim = Simulator(self.out_paths[scen_name], **construct_scenario_objs(scen, visualizer_on=False))
                result = sim.run(scen["time_step_ms"], scen["time_goal_ms"], progress_bar_on=False)
                total_results.append(result)
                print(f"{self.iterations = }")
                self.iterations += 1
            res[changed_val] = total_results
        return res


@utils.my_timer
def run_statistics(steps, runs_per_step, debug_input=None, save_to_file_name: str = None) -> dict:
    args = utils.parse_args_to_dict(debug_input)
    stat = {}
    statistics = Statistics(args)
    for scen_name in statistics.scenarios.keys():
        stat[scen_name] = {
            "los": {},
            "max_speed": {},
            "cruise_speed": {}
        }
        stat[scen_name]["los"] = statistics.run_scenario(
            scen_name, Statistics.ValType.LOS, 400, 1500, steps, runs_per_step)
        stat[scen_name]["max_speed"] = statistics.run_scenario(
            scen_name, Statistics.ValType.MAX_SPEED, 40, 100, steps, runs_per_step)
        stat[scen_name]["cruise_speed"] = statistics.run_scenario(
            scen_name, Statistics.ValType.CRUISE_SPEED, 15, 30, steps, runs_per_step)

    if save_to_file_name:
        with open(f'{save_to_file_name}.pickle', 'wb') as file:
            pickle.dump(stat, file)

    return stat


def calc_lin_reg(mean_values):
    coefficients = np.polyfit(np.arange(len(mean_values)), mean_values, 1)
    poly = np.poly1d(coefficients)
    x_lin_reg = np.arange(len(mean_values))
    y_lin_reg = poly(x_lin_reg)
    return x_lin_reg, y_lin_reg, coefficients


def plot_val_type(val_name: str, titles: dict, data: dict, save_to_file_name: str = None):
    plt.figure(figsize=(20, 11))
    bar_width = 0.35
    ERROR_FACTOR = 0.7
    keys = list(data.keys())
    values = []
    for res in data.values():
        values.append([val.percentage for val in res])
    x_positions = np.arange(len(keys))
    error_values = np.std(values, axis=1) * ERROR_FACTOR  # Calculate the standard deviation as error bars
    # global_min = np.min(values, axis=1)[0]
    mean_values = np.mean(values, axis=1)
    plt.bar(x_positions, mean_values, bar_width, alpha=0.7, label="Mean Collision Percentage")
    plt.errorbar(x_positions, np.mean(values, axis=1), yerr=error_values, fmt='none', capsize=2, color='gray',
                 linewidth=0.5)
    x_lin_reg, y_lin_reg, coef = calc_lin_reg(mean_values)
    plt.plot(x_lin_reg, y_lin_reg, color='red', linestyle='--', linewidth=1.5, label='Linear Regression')
    plt.xlabel(titles["xlabel"])
    plt.ylabel("Collision Success [percentage]")
    plt.title(titles["title"])
    plt.xticks(np.arange(len(keys)), keys)
    plt.legend()
    plt.ylim(50, 100)
    plt.grid(color='gray', linestyle='dashed', alpha=0.3)
    if save_to_file_name:
        plt.savefig(f'{save_to_file_name}_{val_name}.png', dpi=300, bbox_inches='tight')


def plot_statistics(stat: dict, save_to_file_name: str = None):
    scenario_names = list(stat.keys())

    titles = {
        "max_speed": {"xlabel": "Max Drone Speed [m/s]",
                      "title": "Max Drone Speed VS Collision Success" },

        "cruise_speed": {"xlabel": "Max Plane Speed [m/s]",
                         "title": "Max Plane Speed VS Collision Success" },

        "los": {"xlabel": "Line Of Sight [m]",
                "title": "Line Of Sight VS Collision Success"}
    }

    for scen_name in stat.keys():
        for val_name, titles in titles.items():
            plot_val_type(val_name=val_name,
                          titles=titles,
                          data=stat[scen_name][val_name],
                          save_to_file_name=save_to_file_name)


# # Bar plot for 'los'
# plt.figure(figsize=(20, 11))
# # plt.subplot(211)
# bar_width = 0.35
# ERROR_FACTOR = 0.7
# global_min = 0
# for i, scenario_name in enumerate(scenario_names):
#     los_data = stat[scenario_name]["los"]
#     keys = list(los_data.keys())
#     values = []
#     for res in los_data.values():
#         values.append([val.percentage for val in res])
#
#     x_positions = np.arange(len(keys)) + (i * bar_width)
#     error_values = np.std(values, axis=1) * ERROR_FACTOR  # Calculate the standard deviation as error bars
#     global_min = np.min(values, axis=1)[0]
#     mean_values = np.mean(values, axis=1)
#     plt.bar(x_positions, mean_values, bar_width, alpha=0.7, label="Mean Collision Percentage")
#     plt.errorbar(x_positions, np.mean(values, axis=1), yerr=error_values, fmt='none', capsize=2,
#                  color='gray', linewidth=0.5)
#     x_lin_reg, y_lin_reg, coef = calc_lin_reg(mean_values)
#     plt.plot(x_lin_reg, y_lin_reg, color='red', linestyle='--', linewidth=1.5, label='Linear Regression')
#
# plt.xlabel(titles["xlabel"])
# plt.ylabel(titles["ylabel"])
# plt.title(titles["title"])
# plt.xticks(np.arange(len(keys)), keys)
# plt.legend()
# plt.ylim(50, 100)
# plt.grid(color='gray', linestyle='dashed', alpha=0.3)
# if save_to_file_name:
#     plt.savefig(f'{save_to_file_name}_{val_name}.png', dpi=300, bbox_inches='tight')
#
# # Bar plot for 'max_speed'
# plt.figure(figsize=(20, 11))
# # plt.subplot(212)
# for i, scenario_name in enumerate(scenario_names):
#     max_speed_data = stat[scenario_name]["max_speed"]
#     keys = list(max_speed_data.keys())
#     # factor = (FACTOR * random.uniform(0.97, 1)) if i == 1 else 1
#     values = []
#     for res in max_speed_data.values():
#         values.append([val.percentage for val in res])
#
#     x_positions = np.arange(len(keys)) + (i * bar_width)
#     error_values = np.std(values, axis=1) * ERROR_FACTOR  # Calculate the standard deviation as error bars
#     global_min = np.min(values, axis=1)[0]
#     mean_values = np.mean(values, axis=1)
#     plt.bar(x_positions, mean_values, bar_width, alpha=0.7, label="Mean Collision Percentage")
#     plt.errorbar(x_positions, np.mean(values, axis=1), yerr=error_values, fmt='none', capsize=2,
#                  color='gray', linewidth=0.5)
#     x_lin_reg, y_lin_reg, coef = calc_lin_reg(mean_values)
#     plt.plot(x_lin_reg, y_lin_reg, color='red', linestyle='--', linewidth=1.5, label='Linear Regression')
#
# plt.xlabel("Max Speed (Burst)")
# plt.ylabel("Collision Success")
# plt.title("Max Speed (Burst) VS Collision Success")
# plt.xticks(np.arange(len(keys)), keys)
# plt.legend()
# plt.ylim(50, 100)
# plt.grid(color='gray', linestyle='dashed', alpha=0.3)
# if save_to_file_name:
#     plt.savefig(f'{save_to_file_name}_MaxSpeed.png', dpi=300, bbox_inches='tight')
# plt.show()
#
# plt.figure(figsize=(20, 11))
# # plt.subplot(212)
# for i, scenario_name in enumerate(scenario_names):
#     data = stat[scenario_name]["cruise_speed"]
#     keys = list(data.keys())
#     # factor = (FACTOR * random.uniform(0.97, 1)) if i == 1 else 1
#     values = []
#     for res in data.values():
#         values.append([val.percentage for val in res])
#
#     x_positions = np.arange(len(keys)) + (i * bar_width)
#     error_values = np.std(values, axis=1) * ERROR_FACTOR  # Calculate the standard deviation as error bars
#     global_min = np.min(values, axis=1)[0]
#     mean_values = np.mean(values, axis=1)
#     plt.bar(x_positions, mean_values, bar_width, alpha=0.7, label="Mean Collision Percentage")
#     plt.errorbar(x_positions, np.mean(values, axis=1), yerr=error_values, fmt='none', capsize=2,
#                  color='gray', linewidth=0.5)
#     x_lin_reg, y_lin_reg, coef = calc_lin_reg(mean_values)
#     plt.plot(x_lin_reg, y_lin_reg, color='red', linestyle='--', linewidth=1.5, label='Linear Regression')
#
# plt.xlabel("Max Speed (Burst)")
# plt.ylabel("Collision Success")
# plt.title("Max Speed (Burst) VS Collision Success")
# plt.xticks(np.arange(len(keys)), keys)
# plt.legend()
# plt.ylim(50, 100)
# plt.grid(color='gray', linestyle='dashed', alpha=0.3)
# if save_to_file_name:
#     plt.savefig(f'{save_to_file_name}_MaxSpeed.png', dpi=300, bbox_inches='tight')
# plt.show()

if __name__ == "__main__":
    user_name = os.getenv("USERNAME")
    drive_name = "OneDrive" if user_name == "shali" else "OneDrive - Rafael"

    debug_args = [
        "--scenarios",
        fr"C:\Users\{user_name}\{drive_name}\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\debug.json",
        # r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\new_scenarios\line_no_wave.json",
        "--out_path", r"D:\output",
        "--scale_world_factor", "1",
    ]
    steps = 20
    runs_per_step = 1000
    fname = f"circles{steps}X{runs_per_step}"
    # result = run_statistics(steps, runs_per_step, debug_input=debug_args, save_to_file_name=fname)
    with open(f'{fname}.pickle', 'rb') as file:
        stat = pickle.load(file)
    print(stat)

    plot_statistics(stat, save_to_file_name=fname)
