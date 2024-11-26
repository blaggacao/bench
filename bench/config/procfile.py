import os
import platform

import click

import bench
from bench.bench import Bench
from bench.utils import which


def setup_procfile(bench_path, yes=False, skip_redis=False, skip_web=False, skip_watch=os.environ.get("CI"), skip_socketio=False, skip_schedule=False):
	config = Bench(bench_path).conf
	procfile_path = os.path.join(bench_path, "Procfile")

	is_mac = platform.system() == "Darwin"
	if not yes and os.path.exists(procfile_path):
		click.confirm(
			"A Procfile already exists and this will overwrite it. Do you want to continue?",
			abort=True,
		)

	procfile = (
		bench.config.env()
		.get_template("Procfile")
		.render(
			node=which("node") or which("nodejs"),
			webserver_port=config.get("webserver_port"),
			skip_redis=skip_redis,
			skip_web=skip_web,
			skip_watch=skip_watch,
			skip_socketio=skip_socketio,
			skip_schedule=skip_schedule,
			workers=config.get("workers", {}),
			is_mac=is_mac,
		)
	)

	with open(procfile_path, "w") as f:
		f.write(procfile)

def main(bench_path, yes, skip_redis, skip_web, skip_watch, skip_socketio, skip_schedule):
	setup_procfile(
		bench_path,
		skip_redis=skip_redis,
		skip_web=skip_web,
		skip_watch=skip_watch,
		skip_socketio=skip_socketio,
		skip_schedule=skip_schedule
	)

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(
		description="Configure the procfile for the bench.",
		usage="""
		python -m bench.config.procfile <bench_path> [options]

		<bench_path> : The path to the bench directory.

		Options:
		--yes            : Automatically answer 'yes' to prompts.
		--skip-redis     : Skip Redis configuration.
		--skip-web       : Skip web server configuration.
		--skip-watch     : Skip watch process configuration.
		--skip-socketio  : Skip Socket.IO configuration.
		--skip-schedule  : Skip schedule configuration.
		"""
	)

	parser.add_argument("bench_path", help="The path to the bench directory.")
	parser.add_argument("--yes", action="store_true", help="Automatically answer 'yes' to prompts.")
	parser.add_argument("--skip-redis", action="store_true", help="Skip Redis configuration.")
	parser.add_argument("--skip-web", action="store_true", help="Skip web server configuration.")
	parser.add_argument("--skip-watch", action="store_true", default=os.environ.get("CI"), help="Skip watch process configuration.")
	parser.add_argument("--skip-socketio", action="store_true", help="Skip Socket.IO configuration.")
	parser.add_argument("--skip-schedule", action="store_true", help="Skip schedule configuration.")

	args = parser.parse_args()

	main(
		args.bench_path,
		args.yes,
		args.skip_redis,
		args.skip_web,
		args.skip_watch,
		args.skip_socketio,
		args.skip_schedule
	)
