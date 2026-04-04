#!/usr/bin/env python3

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


OUTPUT_DIR = Path("hil/generated")


def main() -> int:
    with open("selected_block.json", "r", encoding="utf-8") as f:
        selected = json.load(f).get("selected")

    if not selected:
        print("No selected block. Skipping artifact rendering.")
        return 0

    block = selected["block"]
    config = selected["config"]

    tx_template_path = Path(config["tx_template"])
    rx_template_path = Path(config["rx_template"])
    scenario_template_path = Path(config["scenario_template"])

    env = Environment(
        loader=FileSystemLoader("."),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    tx_template = env.get_template(tx_template_path.as_posix())
    rx_template = env.get_template(rx_template_path.as_posix())
    scenario_template = env.get_template(scenario_template_path.as_posix())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    tx_output = OUTPUT_DIR / "tx.py"
    rx_output = OUTPUT_DIR / "rx.py"
    scenario_output = OUTPUT_DIR / "scenario.yaml"
    iteration_output = OUTPUT_DIR / "iteration_plan.json"
    metadata_output = OUTPUT_DIR / "run_metadata.json"

    tx_output.write_text(
        tx_template.render(block=block, config=config),
        encoding="utf-8",
    )
    rx_output.write_text(
        rx_template.render(block=block, config=config),
        encoding="utf-8",
    )
    scenario_output.write_text(
        scenario_template.render(block=block, config=config),
        encoding="utf-8",
    )

    iteration_plan = {
        "block": block,
        "sample_rate": config["parameters"]["sample_rate"],
        "center_freq": config["parameters"]["center_freq"],
        "waveform": config["parameters"]["waveform"],
        "tx_gain": config["parameters"]["tx_gain"],
        "rx_gain": config["parameters"]["rx_gain"],
        "iterations": config["parameters"]["iterations"],
        "metrics": config["metrics"],
    }

    iteration_output.write_text(
        json.dumps(iteration_plan, indent=2),
        encoding="utf-8",
    )

    metadata_output.write_text(
        json.dumps(
            {
                "block": block,
                "tx_node": config["parameters"]["tx_node"],
                "rx_node": config["parameters"]["rx_node"],
                "container_image": config["parameters"]["container_image"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Rendered artifacts for block: {block}")
    print(f"Generated: {tx_output}")
    print(f"Generated: {rx_output}")
    print(f"Generated: {scenario_output}")
    print(f"Generated: {iteration_output}")
    print(f"Generated: {metadata_output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())