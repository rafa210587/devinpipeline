import argparse
import asyncio
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config_loader import load_factory_config


@dataclass
class Job:
    name: str
    pipeline: str
    input_path: Path
    output_dir: Path | None
    resume_from: str | None


def _read_json_file(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _resolve_local_path(raw_path: str | Path, base_dir: Path) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return (base_dir / candidate).resolve()


def load_jobs(batch_file: Path) -> list[Job]:
    payload = _read_json_file(batch_file)
    raw_jobs = payload.get("jobs", payload)
    if not isinstance(raw_jobs, list):
        raise ValueError("batch file must contain a list or {'jobs': [...]} ")

    jobs: list[Job] = []
    for i, row in enumerate(raw_jobs, start=1):
        pipeline = str(row.get("pipeline", "full"))
        input_path = Path(str(row["input_path"]))
        output_dir = row.get("output_dir")
        resume_from = row.get("resume_from")
        name = str(row.get("name", f"job_{i:02d}_{pipeline}"))
        jobs.append(
            Job(
                name=name,
                pipeline=pipeline,
                input_path=input_path,
                output_dir=Path(str(output_dir)) if output_dir else None,
                resume_from=str(resume_from) if resume_from else None,
            )
        )
    return jobs


def build_cmd(job: Job, pipeline_script: Path) -> list[str]:
    cmd = [
        sys.executable,
        str(pipeline_script),
        job.pipeline,
        str(job.input_path),
    ]
    if job.output_dir is not None:
        cmd.append(str(job.output_dir))
    if job.pipeline == "resume":
        if not job.resume_from:
            raise ValueError(f"{job.name}: resume job requires resume_from")
        cmd.extend(["--from", job.resume_from])
    return cmd


async def run_one(job: Job, pipeline_script: Path, logs_dir: Path) -> tuple[str, int]:
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / f"{job.name}.log"
    cmd = build_cmd(job, pipeline_script)

    with log_file.open("w", encoding="utf-8") as f:
        f.write("CMD: " + " ".join(cmd) + "\n\n")
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        assert proc.stdout is not None
        async for line in proc.stdout:
            f.write(line.decode(errors="replace"))
        code = await proc.wait()

    return job.name, code


async def run_all(
    jobs: list[Job],
    pipeline_script: Path,
    max_concurrency: int,
    logs_dir: Path,
) -> int:
    sem = asyncio.Semaphore(max_concurrency)
    results: list[tuple[str, int]] = []

    async def wrapped(job: Job) -> None:
        async with sem:
            name, code = await run_one(job, pipeline_script, logs_dir)
            results.append((name, code))

    await asyncio.gather(*(wrapped(job) for job in jobs))

    failed = [(name, code) for (name, code) in results if code != 0]
    print("=== Parallel Run Summary ===")
    for name, code in sorted(results):
        print(f"- {name}: exit={code}")

    if failed:
        print("\nFailures:")
        for name, code in failed:
            print(f"  - {name}: exit={code}")
        return 1

    return 0


def build_parser(
    default_max_concurrency: int,
    default_pipeline_script: Path,
    default_logs_dir: Path,
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Devin pipeline coordinators in parallel."
    )
    parser.add_argument("--batch", type=Path, required=True, help="JSON file with jobs")
    parser.add_argument(
        "--max-concurrency",
        type=int,
        default=default_max_concurrency,
        help="Max parallel jobs",
    )
    parser.add_argument(
        "--pipeline-script",
        type=Path,
        default=default_pipeline_script,
        help="Pipeline script path (defaults from factory_config.json)",
    )
    parser.add_argument(
        "--logs-dir",
        type=Path,
        default=default_logs_dir,
        help="Directory for job logs (defaults from factory_config.json)",
    )
    return parser


def main() -> int:
    package_dir = Path(__file__).resolve().parent
    config = load_factory_config()
    runner_cfg = dict(config.get("parallel_runner", {}))
    storage_cfg = dict(config.get("storage", {}))

    storage_mode = str(storage_cfg.get("mode", "local")).strip().lower()
    raw_repo_path = str(storage_cfg.get("github_repo_path", "")).strip()
    storage_repo_path = Path(raw_repo_path).expanduser().resolve() if raw_repo_path else None
    logs_base_dir = package_dir
    if storage_mode == "github_repo" and storage_repo_path is not None:
        logs_base_dir = storage_repo_path

    default_max_concurrency = int(runner_cfg.get("default_max_concurrency", 2))
    default_pipeline_script = _resolve_local_path(
        runner_cfg.get("pipeline_script", "devin_pipeline_v2.py"), package_dir
    )
    default_logs_dir = _resolve_local_path(
        runner_cfg.get("logs_dir", "factory_runs/_parallel_logs"), logs_base_dir
    )

    args = build_parser(
        default_max_concurrency=default_max_concurrency,
        default_pipeline_script=default_pipeline_script,
        default_logs_dir=default_logs_dir,
    ).parse_args()

    jobs = load_jobs(args.batch)
    if not jobs:
        print("No jobs found in batch file.")
        return 1

    for job in jobs:
        if not job.input_path.exists() and job.pipeline in {"full", "brief"}:
            raise FileNotFoundError(
                f"{job.name}: input_path does not exist: {job.input_path}"
            )

    return asyncio.run(
        run_all(
            jobs=jobs,
            pipeline_script=args.pipeline_script,
            max_concurrency=args.max_concurrency,
            logs_dir=args.logs_dir,
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())

