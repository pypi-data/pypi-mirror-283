import logging
import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

from lisa_on_cuda.utils import session_logger


load_dotenv()
LOGLEVEL = os.getenv('LOGLEVEL', 'INFO').upper()
session_logger.change_logging(LOGLEVEL)
root_folder = Path(globals().get("__file__", "./_")).absolute().parent.parent.parent
env_project_root_folder = Path(os.getenv("PROJECT_ROOT_FOLDER", root_folder))
env_input_css_path = Path(os.getenv("INPUT_CSS_PATH"))


def assert_envs(envs_list):
    for current_env in envs_list:
        try:
            assert current_env is not None and current_env != ""
        except AssertionError as aex:
            logging.error(f"error on assertion for current_env: {current_env}.")
            raise aex


def read_std_out_err(std_out_err, output_type: str, command: list):
    output = std_out_err.split("\n")
    logging.info(f"output type:{output_type} for command:{' '.join(command)}.")
    for line in iter(output):
        logging.info(f"output_content_home stdout:{line.strip()}.")
    logging.info("########")


def run_command(commands_list: list, capture_output: bool = True, text: bool = True, check: bool = True) -> None:
    try:
        output_content_home = subprocess.run(
            commands_list,
            capture_output=capture_output,
            text=text,
            check=check
        )
        read_std_out_err(output_content_home.stdout, "stdout", commands_list)
        read_std_out_err(output_content_home.stderr, "stderr", commands_list)
    except Exception as ex:
        logging.error(f"ex:{ex}.")
        raise ex


def build_frontend(
        project_root_folder: str | Path,
        input_css_path: str | Path,
        output_dist_folder: Path = root_folder / "static" / "dist",
    ) -> None:
    assert_envs([
        str(project_root_folder),
        str(input_css_path)
    ])

    # install deps
    os.chdir(Path(project_root_folder) / "static")
    current_folder = os.getcwd()
    logging.info(f"current_folder:{current_folder}, install pnpm...")
    run_command(["npm", "install", "-g", "npm", "pnpm"])
    logging.info(f"install pnpm dependencies...")
    run_command(["pnpm", "install"])

    # build frontend dist and assert for its correct build
    output_css = str(output_dist_folder / "output.css")
    output_index_html = str(output_dist_folder / "index.html")
    output_dist_folder = str(output_dist_folder)
    logging.info(f"pnpm: build '{output_dist_folder}'...")
    run_command(["pnpm", "build"])
    logging.info(f"pnpm: ls -l {output_index_html}:")
    run_command(["ls", "-l", output_index_html])
    cmd = ["pnpm", "tailwindcss", "-i", str(input_css_path), "-o", output_css]
    logging.info(f"pnpm: {' '.join(cmd)}...")
    run_command(["pnpm", "tailwindcss", "-i", str(input_css_path), "-o", output_css])
    logging.info(f"pnpm: ls -l {output_css}:")
    run_command(["ls", "-l", output_css])
    logging.info(f"end!")


if __name__ == '__main__':
    build_frontend(
        project_root_folder=env_project_root_folder,
        input_css_path=env_input_css_path
    )
