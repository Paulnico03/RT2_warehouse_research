from pathlib import Path
import csv
import re
import subprocess


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

DOMAIN = Path(
    "planning/multi_capacity/domain-warehouse-capacity.pddl"
)

PROBLEM_DIR = Path(
    "planning/generated_problems"
)

RAW_OUTPUT_DIR = Path(
    "data/raw/batch_runs"
)

RESULTS_FILE = Path(
    "data/processed/results.csv"
)

METADATA_FILE = Path(
    "data/processed/scenario_metadata.csv"
)

ENHSP_JAR = Path.home() / (
    "enhsp/ENHSP-Public/enhsp-dist/enhsp.jar"
)

TIMEOUT_SECONDS = 120


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def extract_number(pattern, text, cast=float):
    """
    Search a value in ENHSP output.

    Returns None if the field is not present.
    """

    match = re.search(pattern, text, re.MULTILINE)

    if match is None:
        return None

    return cast(match.group(1))


def load_metadata():
    """
    Load scenario metadata indexed by scenario_id.
    """

    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {METADATA_FILE}"
        )

    metadata = {}

    with METADATA_FILE.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        reader = csv.DictReader(csv_file)

        for row in reader:

            scenario_id = int(
                row["scenario_id"]
            )

            metadata[scenario_id] = {
                "seed": int(row["seed"]),
                "num_packages": int(
                    row["num_packages"]
                ),
                "deadline_mode": row[
                    "deadline_mode"
                ],
                "layout_mode": row[
                    "layout_mode"
                ],
                "locations": row["locations"],
                "deadlines": row["deadlines"],
            }

    return metadata


def parse_filename(filename):
    """
    Example:

    scenario_001_capacity2.pddl

    -> scenario = 1
    -> capacity = 2
    """

    match = re.match(
        r"scenario_(\d+)_capacity(\d+)\.pddl",
        filename.name,
    )

    if not match:
        raise ValueError(
            f"Unexpected problem filename: {filename.name}"
        )

    scenario_id = int(match.group(1))
    capacity = int(match.group(2))

    return scenario_id, capacity


def parse_output(text):
    """
    Extract useful metrics from ENHSP output.
    """

    if "Problem Solved" in text:
        status = "solved"

    elif "Problem unsolvable" in text:
        status = "unsolvable"

    else:
        status = "unknown"

    return {
        "status": status,

        "plan_length": extract_number(
            r"^Plan-Length:(\d+)",
            text,
            int,
        ),

        "elapsed_time": extract_number(
            r"^Elapsed Time:\s*([0-9.]+)",
            text,
            float,
        ),

        "metric_search": extract_number(
            r"^Metric \(Search\):([0-9.\-]+)",
            text,
            float,
        ),

        "planning_time_ms": extract_number(
            r"^Planning Time \(msec\):\s*(\d+)",
            text,
            int,
        ),

        "expanded_nodes": extract_number(
            r"^Expanded Nodes:(\d+)",
            text,
            int,
        ),

        "states_evaluated": extract_number(
            r"^States Evaluated:(\d+)",
            text,
            int,
        ),
    }


# ---------------------------------------------------------
# Run one experiment
# ---------------------------------------------------------

def run_problem(problem_file):

    scenario_id, capacity = parse_filename(
        problem_file
    )

    print(
        f"Running scenario {scenario_id:03d} "
        f"with capacity {capacity}..."
    )

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

    timed_out = False

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )

        output = result.stdout + result.stderr

        return_code = result.returncode

    except subprocess.TimeoutExpired as exc:

        timed_out = True

        stdout = exc.stdout or ""
        stderr = exc.stderr or ""

        if isinstance(stdout, bytes):
            stdout = stdout.decode(
                errors="replace"
            )

        if isinstance(stderr, bytes):
            stderr = stderr.decode(
                errors="replace"
            )

        output = stdout + stderr

        return_code = None

    # -----------------------------------------------------
    # Save complete raw planner output
    # -----------------------------------------------------

    RAW_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = RAW_OUTPUT_DIR / (
        f"scenario_{scenario_id:03d}_"
        f"capacity{capacity}.txt"
    )

    output_file.write_text(
        output,
        encoding="utf-8",
    )

    metrics = parse_output(output)

    if timed_out:
        metrics["status"] = "timeout"

    row = {
        "scenario_id": scenario_id,
        "capacity": capacity,
        "problem_file": problem_file.name,
        "status": metrics["status"],
        "timed_out": timed_out,
        "return_code": return_code,
        "plan_length": metrics["plan_length"],
        "makespan": metrics["elapsed_time"],
        "metric_search": metrics["metric_search"],
        "planning_time_ms": metrics["planning_time_ms"],
        "expanded_nodes": metrics["expanded_nodes"],
        "states_evaluated": metrics["states_evaluated"],
    }

    return row


# ---------------------------------------------------------
# Main experiment
# ---------------------------------------------------------

def main():

    if not ENHSP_JAR.exists():
        raise FileNotFoundError(
            f"ENHSP not found at {ENHSP_JAR}"
        )

    if not DOMAIN.exists():
        raise FileNotFoundError(
            f"Domain not found at {DOMAIN}"
        )

    problem_files = sorted(
        PROBLEM_DIR.glob(
            "scenario_*_capacity*.pddl"
        )
    )

    if not problem_files:
        raise RuntimeError(
            "No generated PDDL problems found."
        )

    metadata_by_id = load_metadata()

    results = []

    for problem_file in problem_files:

        row = run_problem(problem_file)

        scenario_id = row["scenario_id"]

        if scenario_id not in metadata_by_id:
            raise RuntimeError(
                f"No metadata found for scenario "
                f"{scenario_id}"
            )

        row.update(
            metadata_by_id[scenario_id]
        )

        results.append(row)

        print(
            f"  -> {row['status']} | "
            f"makespan={row['makespan']} | "
            f"planning={row['planning_time_ms']} ms | "
            f"expanded={row['expanded_nodes']}"
        )

    # -----------------------------------------------------
    # Save CSV
    # -----------------------------------------------------

    RESULTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "scenario_id",
        "capacity",
        "seed",
        "num_packages",
        "deadline_mode",
        "layout_mode",
        "locations",
        "deadlines",
        "problem_file",
        "status",
        "timed_out",
        "return_code",
        "plan_length",
        "makespan",
        "metric_search",
        "planning_time_ms",
        "expanded_nodes",
        "states_evaluated",
    ]

    with RESULTS_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)

    print()
    print(
        f"Finished {len(results)} experiments."
    )

    print(
        f"Results saved to: {RESULTS_FILE}"
    )


if __name__ == "__main__":
    main()
