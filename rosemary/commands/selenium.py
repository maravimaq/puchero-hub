import click
import os
import subprocess


@click.command('selenium', help="Run Selenium tests for the project.")
@click.option('--headless', is_flag=True, help="Run tests in headless mode.")
def selenium(headless):
    base_path = os.path.join(os.getenv('WORKING_DIR', ''), 'app/modules')

    test_paths = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.startswith('test_selenium') and file.endswith('.py'):
                test_paths.append(os.path.join(root, file))

    if not test_paths:
        click.echo(click.style("No Selenium tests found.", fg='yellow'))
        return

    pytest_cmd = ['pytest', '-v'] + test_paths

    if headless:
        pytest_cmd.extend(['--chrome-headless'])

    click.echo("Running Selenium tests...")
    try:
        subprocess.run(pytest_cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Selenium tests failed: {e}", fg='red'))
        raise SystemExit(1)
