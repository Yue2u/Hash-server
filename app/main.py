import click
import uvicorn


@click.command()
@click.option("--host", default="0.0.0.0", type=str, help="Host that runs server")
@click.option(
    "--port", default=8000, type=int, help="Port on which your server will be available"
)
@click.option(
    "--proxy-headers",
    is_flag=True,
    default=False,
    help='Use if run under proxy, passes user ip under "X-Forwarded-For" header',
)
@click.option("--reload", is_flag=True, default=False, help="Reload server on changes")
@click.option(
    "--workers",
    default=None,
    type=int,
    required=False,
    help="Number of workers, cannot be used with --reload",
)
def cli(
    host: str, port: int, proxy_headers: bool, reload: bool, workers: int | None = None
):
    args = {
        "host": host,
        "port": port,
        "proxy_headers": proxy_headers,
    }

    if workers:
        reload = False
        args["workers"] = workers
    else:
        args["reload"] = reload

    uvicorn.run("application:fastapi_app", **args)


if __name__ == "__main__":
    cli()
