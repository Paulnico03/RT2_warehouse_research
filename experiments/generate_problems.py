from pathlib import Path
import random
import csv

OUTPUT_DIR = Path("planning/generated_problems")
METADATA_FILE = Path(
    "data/processed/scenario_metadata.csv"
)
LOCATIONS = ["dock", "aisle-A", "aisle-B", "shipping"]

DISTANCES = {
    ("dock", "aisle-A"): 2,
    ("aisle-A", "dock"): 2,
    ("dock", "aisle-B"): 3,
    ("aisle-B", "dock"): 3,
    ("aisle-A", "shipping"): 2,
    ("shipping", "aisle-A"): 2,
    ("aisle-B", "shipping"): 3,
    ("shipping", "aisle-B"): 3,
}


def generate_problem(
    scenario_id,
    capacity,
    package_locations,
    deadlines,
):
    """
    Generate one PDDL+ warehouse problem.

    package_locations:
        Example: ["aisle-A", "aisle-A", "aisle-B"]

    deadlines:
        Example: [30, 45, 60]
    """

    if len(package_locations) != len(deadlines):
        raise ValueError(
            "package_locations and deadlines must have the same length"
        )

    num_packages = len(package_locations)

    package_names = [
        f"pkg{i + 1}"
        for i in range(num_packages)
    ]

    problem_name = (
        f"warehouse-s{scenario_id:03d}-capacity{capacity}"
    )

    lines = []

    lines.append(f"(define (problem {problem_name})")
    lines.append("    (:domain warehouse-continuous-robot)")
    lines.append("    (:objects")
    lines.append("        robby - robot")
    lines.append(
        "        " + " ".join(package_names) + " - package"
    )
    lines.append(
        "        dock aisle-A aisle-B shipping - location"
    )
    lines.append("    )")
    lines.append("")

    # Initial state
    lines.append("    (:init")

    # Graph topology
    lines.append("        ;; Graph topology")
    for location_a, location_b in DISTANCES:
        lines.append(
            f"        (connected {location_a} {location_b})"
        )

    lines.append("")

    # Distances
    lines.append("        ;; Distances")
    for (location_a, location_b), distance in DISTANCES.items():
        lines.append(
            f"        (= (distance {location_a} "
            f"{location_b}) {distance})"
        )

    lines.append("")

    # Robot state
    lines.append("        ;; Initial robot state")
    lines.append("        (at-robot robby dock)")
    lines.append("        (= (distance-left robby) 0)")
    lines.append("        (= (current-load robby) 0)")
    lines.append(
        f"        (= (max-capacity robby) {capacity})"
    )

    lines.append("")

    # Packages
    lines.append("        ;; Package states and deadlines")

    for package, location, deadline in zip(
        package_names,
        package_locations,
        deadlines,
    ):
        lines.append(
            f"        (at-package {package} {location})"
        )
        lines.append(
            f"        (target-location {package} shipping)"
        )
        lines.append(
            f"        (= (time-remaining {package}) "
            f"{deadline})"
        )
        lines.append("")

    lines.append("    )")
    lines.append("")

    # Goal
    lines.append("    (:goal")
    lines.append("        (and")

    for package in package_names:
        lines.append(
            f"            (delivered {package})"
        )

    lines.append("        )")
    lines.append("    )")
    lines.append(")")

    filename = (
        OUTPUT_DIR
        / f"scenario_{scenario_id:03d}_capacity{capacity}.pddl"
    )

    filename.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    return filename


def generate_scenario(
    scenario_id,
    package_locations,
    deadlines,
):
    """
    Generate the matched capacity-1 and capacity-2 problems
    for one scenario.
    """

    files = []

    for capacity in [1, 2]:
        filename = generate_problem(
            scenario_id=scenario_id,
            capacity=capacity,
            package_locations=package_locations,
            deadlines=deadlines,
        )

        files.append(filename)

    return files


def create_random_scenario(
    scenario_id,
    num_packages,
    deadline_mode,
    layout_mode,
    seed,
):
    """
    Create a reproducible warehouse scenario.
    deadline_mode:
        "relaxed"
        "tight"

    layout_mode:
        "clustered"
        "distributed"
    """

    layout_rng = random.Random(seed)

    deadline_rng = random.Random(
        10000 + seed + num_packages * 100
    )

    # -----------------------------------------------------
    # Package locations
    # -----------------------------------------------------

    if layout_mode == "clustered":

        # Alternate the aisle according to the seed
        # so that both aisle-A and aisle-B are represented.
        shared_location = (
            "aisle-A"
            if seed % 2 == 1
            else "aisle-B"
        )

        package_locations = [
            shared_location
            for _ in range(num_packages)
        ]

    elif layout_mode == "distributed":

        if num_packages == 2:

            package_locations = [
                "aisle-A",
                "aisle-B",
            ]

            layout_rng.shuffle(package_locations)

        elif num_packages == 3:

            # Alternate which aisle contains two packages.
            paired_location = (
                "aisle-A"
                if seed % 2 == 1
                else "aisle-B"
            )

            other_location = (
                "aisle-B"
                if paired_location == "aisle-A"
                else "aisle-A"
            )

            package_locations = [
                paired_location,
                paired_location,
                other_location,
            ]

            layout_rng.shuffle(package_locations)

        else:
            raise ValueError(
                "Only 2 or 3 packages are supported."
            )

    else:
        raise ValueError(
            f"Unknown layout mode: {layout_mode}"
        )

    # -----------------------------------------------------
    # Deadlines
    # -----------------------------------------------------

    if deadline_mode == "relaxed":

        if num_packages == 2:
            deadlines = [
                deadline_rng.randint(20, 30)
                for _ in range(num_packages)
            ]
        else:
            deadlines = [
                deadline_rng.randint(25, 40)
                for _ in range(num_packages)
            ]

    elif deadline_mode == "tight":

        if num_packages == 2:
            deadlines = [
                deadline_rng.randint(7, 12)
                for _ in range(num_packages)
            ]
        else:
            deadlines = [
                deadline_rng.randint(11, 16)
                for _ in range(num_packages)
            ]

    else:
        raise ValueError(
            f"Unknown deadline mode: {deadline_mode}"
        )

    return {
        "scenario_id": scenario_id,
        "seed": seed,
        "num_packages": num_packages,
        "deadline_mode": deadline_mode,
        "layout_mode": layout_mode,
        "locations": package_locations,
        "deadlines": deadlines,
    }

def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    scenario_id = 1000
    metadata_rows = []

    for num_packages in [2, 3]:

        for deadline_mode in [
            "relaxed",
            "tight",
        ]:

            for layout_mode in [
                "clustered",
                "distributed",
            ]:

                for seed in range(1, 21):

                    scenario = create_random_scenario(
                        scenario_id=scenario_id,
                        num_packages=num_packages,
                        deadline_mode=deadline_mode,
                        layout_mode=layout_mode,
                        seed=seed,
                    )

                    metadata_rows.append(
                        {
                            "scenario_id": scenario["scenario_id"],
                            "seed": scenario["seed"],
                            "num_packages": scenario["num_packages"],
                            "deadline_mode": scenario["deadline_mode"],
                            "layout_mode": scenario["layout_mode"],
                            "locations": "|".join(
                                scenario["locations"]
                            ),
                            "deadlines": "|".join(
                                str(x)
                                for x in scenario["deadlines"]
                            ),
                        }
                    )

                    generated_files = generate_scenario(
                        scenario_id=scenario["scenario_id"],
                        package_locations=scenario["locations"],
                        deadlines=scenario["deadlines"],
                    )

                    print()
                    print(
                        f"Scenario {scenario_id}"
                        f" | packages={num_packages}"
                        f" | deadline={deadline_mode}"
                        f" | layout={layout_mode}"
                        f" | seed={seed}"
                    )

                    print(
                        f"  locations: "
                        f"{scenario['locations']}"
                    )

                    print(
                        f"  deadlines: "
                        f"{scenario['deadlines']}"
                    )

                    for filename in generated_files:
                        print(
                            f"  Generated: {filename}"
                        )

                    scenario_id += 1

    METADATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with METADATA_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        fieldnames = [
            "scenario_id",
            "seed",
            "num_packages",
            "deadline_mode",
            "layout_mode",
            "locations",
            "deadlines",
        ]

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(metadata_rows)

    print()
    print(
        f"Metadata saved to: {METADATA_FILE}"
    )


if __name__ == "__main__":
    main()
