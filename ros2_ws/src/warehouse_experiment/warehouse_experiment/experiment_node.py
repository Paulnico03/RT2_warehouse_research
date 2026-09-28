import json
import re
import subprocess
from pathlib import Path

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


PROJECT_ROOT = Path.home() / "RT2_warehouse_research"

DOMAIN = (
    PROJECT_ROOT
    / "planning"
    / "multi_capacity"
    / "domain-warehouse-capacity.pddl"
)

PROBLEM_DIR = (
    PROJECT_ROOT
    / "planning"
    / "generated_problems"
)

ENHSP_JAR = (
    Path.home()
    / "enhsp"
    / "ENHSP-Public"
    / "enhsp-dist"
    / "enhsp.jar"
)

TIMEOUT_SECONDS = 120


def extract_int(pattern, text):
    match = re.search(
        pattern,
        text,
        re.MULTILINE,
    )

    if match is None:
        return None

    return int(match.group(1))


def extract_float(pattern, text):
    match = re.search(
        pattern,
        text,
        re.MULTILINE,
    )

    if match is None:
        return None

    return float(match.group(1))


def parse_output(output):
    if "Problem Solved" in output:
        status = "solved"
    elif "Problem unsolvable" in output:
        status = "unsolvable"
    else:
        status = "unknown"

    plan_length = extract_int(
        r"Plan-Length:\s*(\d+)",
        output,
    )

    makespan = extract_float(
        r"^Elapsed Time:\s*([0-9.]+)",
        output,
    )

    planning_time = extract_int(
        r"Planning Time \(msec\):\s*(-?\d+)",
        output,
    )

    # ENHSP occasionally reported invalid negative
    # timing values in the final experiment.
    if (
        planning_time is not None
        and planning_time < 0
    ):
        planning_time = None

    expanded_nodes = extract_int(
        r"^Expanded Nodes:\s*(\d+)",
        output,
    )

    states_evaluated = extract_int(
        r"^States Evaluated:\s*(\d+)",
        output,
    )

    return {
        "status": status,
        "plan_length": plan_length,
        "makespan": makespan,
        "planning_time_ms": planning_time,
        "expanded_nodes": expanded_nodes,
        "states_evaluated": states_evaluated,
    }


class WarehouseExperimentNode(Node):

    def __init__(self):
        super().__init__(
            "warehouse_experiment_node"
        )

        self.result_publisher = (
            self.create_publisher(
                String,
                "/warehouse_experiment/result",
                10,
            )
        )

        self.request_subscription = (
            self.create_subscription(
                String,
                "/warehouse_experiment/request",
                self.request_callback,
                10,
            )
        )

        self.get_logger().info(
            "Warehouse experiment node ready."
        )

        self.get_logger().info(
            "Waiting for JSON requests on "
            "/warehouse_experiment/request"
        )

    def publish_result(self, data):
        message = String()
        message.data = json.dumps(data)

        self.result_publisher.publish(
            message
        )

    def request_callback(self, message):
        try:
            request = json.loads(
                message.data
            )

            scenario_id = int(
                request["scenario_id"]
            )

            capacity = int(
                request["capacity"]
            )

        except (
            KeyError,
            ValueError,
            TypeError,
            json.JSONDecodeError,
        ) as exc:
            self.publish_result(
                {
                    "status": "error",
                    "error": (
                        "Invalid request: "
                        f"{exc}"
                    ),
                }
            )
            return

        if capacity not in (1, 2):
            self.publish_result(
                {
                    "scenario_id": scenario_id,
                    "capacity": capacity,
                    "status": "error",
                    "error": (
                        "Capacity must be 1 or 2."
                    ),
                }
            )
            return

        problem_file = (
            PROBLEM_DIR
            / (
                f"scenario_{scenario_id}"
                f"_capacity{capacity}.pddl"
            )
        )

        if not DOMAIN.exists():
            self.publish_result(
                {
                    "scenario_id": scenario_id,
                    "capacity": capacity,
                    "status": "error",
                    "error": (
                        f"Domain not found: "
                        f"{DOMAIN}"
                    ),
                }
            )
            return

        if not ENHSP_JAR.exists():
            self.publish_result(
                {
                    "scenario_id": scenario_id,
                    "capacity": capacity,
                    "status": "error",
                    "error": (
                        f"ENHSP not found: "
                        f"{ENHSP_JAR}"
                    ),
                }
            )
            return

        if not problem_file.exists():
            self.publish_result(
                {
                    "scenario_id": scenario_id,
                    "capacity": capacity,
                    "status": "error",
                    "error": (
                        f"Problem not found: "
                        f"{problem_file}"
                    ),
                }
            )
            return

        command = [
            "java",
            "-jar",
            str(ENHSP_JAR),
            "-o",
            str(DOMAIN),
            "-f",
            str(problem_file),
            "-planner",
            "opt-hrmax",
        ]

        self.get_logger().info(
            f"Running scenario {scenario_id}, "
            f"capacity {capacity}..."
        )

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )

            output = (
                result.stdout
                + result.stderr
            )

            metrics = parse_output(
                output
            )

            response = {
                "scenario_id": scenario_id,
                "capacity": capacity,
                "problem_file": (
                    problem_file.name
                ),
                "timed_out": False,
                "return_code": (
                    result.returncode
                ),
                **metrics,
            }

        except subprocess.TimeoutExpired:
            response = {
                "scenario_id": scenario_id,
                "capacity": capacity,
                "problem_file": (
                    problem_file.name
                ),
                "status": "timeout",
                "timed_out": True,
                "return_code": None,
                "plan_length": None,
                "makespan": None,
                "planning_time_ms": None,
                "expanded_nodes": None,
                "states_evaluated": None,
            }

        self.publish_result(
            response
        )

        self.get_logger().info(
            "Result published: "
            f"{response['status']}"
        )


def main(args=None):
    rclpy.init(args=args)

    node = WarehouseExperimentNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
