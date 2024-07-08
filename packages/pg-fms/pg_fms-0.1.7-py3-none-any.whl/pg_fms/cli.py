import click
from .commands import file_operations, file_filtering

@click.group()
@click.version_option(version="0.1.4", prog_name="pg-fms")
def cli():
    click.echo(click.style("PG-FMS: The Purple Geckos File Management System", fg="purple", bold=True))

@cli.command("move-file")
@click.argument("source")
@click.argument("destination")
def move_file_cmd(source, destination):
    file_operations.move_file(source, destination)
    click.echo(f"Moved file from {source} to {destination}")

@cli.command("copy-file")
@click.argument("source")
@click.argument("destination")
def copy_file_cmd(source, destination):
    file_operations.copy_file(source, destination)
    click.echo(f"Copied file from {source} to {destination}")

@cli.command("filter-files")
@click.option("--type", default=None, help="File type to filter by")
@click.option("--size", nargs=2, type=int, help="File size range to filter by")
@click.option(
    "--date-modified",
    type=int,
    help="Number of days since modification to filter by",
)
def filter_files_cmd(file_type, size, date_modified):
    if file_type:
        files = file_filtering.filter_by_type(".", file_type)
    elif size:
        files = file_filtering.filter_by_size(".", size[0], size[1])
    elif date_modified:
        files = file_filtering.filter_by_date_modified(".", date_modified)
    else:
        files = []
    click.echo(f"Filtered files: {files}")

def main():
    cli()

if __name__ == "__main__":
    main()
