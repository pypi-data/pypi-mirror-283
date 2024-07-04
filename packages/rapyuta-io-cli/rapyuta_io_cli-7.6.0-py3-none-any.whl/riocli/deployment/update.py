# Copyright 2023 Rapyuta Robotics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
from queue import Queue

import click
from click_help_colors import HelpColorsCommand
from rapyuta_io import Client
from rapyuta_io.clients.deployment import Deployment
from yaspin.api import Yaspin

from riocli.config import new_client
from riocli.constants import Symbols, Colors
from riocli.deployment.util import fetch_deployments
from riocli.deployment.util import print_deployments_for_confirmation
from riocli.utils import tabulate_data
from riocli.utils.execute import apply_func_with_result
from riocli.utils.spinner import with_spinner


@click.command(
    'update',
    cls=HelpColorsCommand,
    help_headers_color=Colors.YELLOW,
    help_options_color=Colors.GREEN,
)
@click.option('--force', '-f', '--silent', is_flag=True, default=False,
              help='Skip confirmation')
@click.option('-a', '--all', 'update_all', is_flag=True, default=False,
              help='Deletes all deployments in the project')
@click.option('--workers', '-w',
              help="number of parallel workers while running update deployment "
                   "command. defaults to 10.", type=int, default=10)
@click.argument('deployment-name-or-regex', type=str, default="")
@with_spinner(text="Updating...")
def update_deployment(
        force: bool,
        workers: int,
        deployment_name_or_regex: str,
        update_all: bool = False,
        spinner: Yaspin = None,
) -> None:
    """
    Updates one more deployments
    """
    client = new_client()
    if not (deployment_name_or_regex or update_all):
        spinner.text = "Nothing to update"
        spinner.green.ok(Symbols.SUCCESS)
        return

    try:
        deployments = fetch_deployments(
            client, deployment_name_or_regex, update_all)
    except Exception as e:
        spinner.text = click.style(
            'Failed to update deployment(s): {}'.format(e), Colors.RED)
        spinner.red.fail(Symbols.ERROR)
        raise SystemExit(1) from e

    if not deployments:
        spinner.text = "Nothing to update"
        spinner.ok(Symbols.SUCCESS)
        return

    with spinner.hidden():
        print_deployments_for_confirmation(deployments)

    spinner.write('')

    if not force:
        with spinner.hidden():
            click.confirm('Do you want to update above deployment(s)?', abort=True)
        spinner.write('')

    try:
        f = functools.partial(_apply_update, client)
        result = apply_func_with_result(
            f=f, items=deployments,
            workers=workers, key=lambda x: x[0]
        )

        data, fg, statuses = [], Colors.GREEN, []
        for name, status in result:
            fg = Colors.GREEN if status else Colors.RED
            icon = Symbols.SUCCESS if status else Symbols.ERROR
            statuses.append(status)
            data.append([
                click.style(name, fg),
                click.style(icon, fg)
            ])

        with spinner.hidden():
            tabulate_data(data, headers=['Name', 'Status'])

        icon = Symbols.SUCCESS if all(statuses) else Symbols.WARNING
        fg = Colors.GREEN if all(statuses) else Colors.YELLOW
        text = "successfully" if all(statuses) else "partially"

        spinner.write('')
        spinner.text = click.style(
            'Deployment(s) updated {}.'.format(text), fg)
        spinner.ok(click.style(icon, fg))
    except Exception as e:
        spinner.text = click.style(
            'Failed to update deployment(s): {}'.format(e), Colors.RED)
        spinner.red.fail(Symbols.ERROR)
        raise SystemExit(1) from e


def get_component_context(component_info) -> dict:
    result = {}

    for component in component_info:
        comp = {}
        executables = []
        exec_metadata = component.get("executableMetaData", []) or []

        for e in exec_metadata:
            # Component will be considered only if any of its executables is
            # docker
            if not (e.get("docker")):
                continue

            executable = {}

            if e.get("docker"):
                executable["docker"] = e["docker"]

            executable["id"] = e.get("id", "")
            executable["name"] = e.get("name", "")
            executables.append(executable)

        if len(executables) > 0:
            result[component["componentID"]] = comp
            comp["component"] = {"executables": executables}
            comp["update_deployment"] = True

    return result


def _apply_update(
        client: Client,
        result: Queue,
        deployment: Deployment,
) -> None:
    try:
        dep = client.get_deployment(deployment['deploymentId'])
        component_context = get_component_context(dep.get("componentInfo", {}))
        payload = {
            "service_id": dep["packageId"],
            "plan_id": dep["planId"],
            "deployment_id": dep["deploymentId"],
            "context": {
                "component_context": component_context
            }
        }
        client.update_deployment(payload)
        result.put((deployment["name"], True))
    except Exception:
        result.put((deployment["name"], False))
