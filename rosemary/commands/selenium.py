import click
import os
import subprocess


@click.command('selenium', help="Run Selenium tests for the project or a specific module.")
@click.argument('module_name', required=False)
@click.option('--headless', is_flag=True, help="Run tests in headless mode.")
def selenium(module_name, headless):
    base_path = os.path.join(os.getenv('WORKING_DIR', ''), 'app/modules')

    test_path = base_path
    if module_name:
        test_path = os.path.join(base_path, module_name)
        if not os.path.exists(test_path):
            click.echo(click.style(f"Module '{module_name}' does not exist.", fg='red'))
            return
        click.echo(f"Running Selenium tests for the '{module_name}' module...")
    else:
        click.echo("Running Selenium tests for all modules...")

    test_paths = []
    for root, dirs, files in os.walk(test_path):
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


if __name__ == '__main__':
    selenium()
