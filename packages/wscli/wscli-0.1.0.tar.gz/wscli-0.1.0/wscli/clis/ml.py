from dataclasses import dataclass
from dataclasses import field
from dataclasses import asdict
import json

from typing import List, Dict
from typing import ClassVar

import click
import requests
from wscli.auth import LoginTokens

from wscli.utils import pprint

from wscli.config import WsConfig
from wscli.config import pass_config


from wscli.api_calls import CallConfig
from wscli.api_calls import ApiUrl
from wscli.api_calls import Scheme
from wscli.api_calls import Method
from wscli.api_calls import hit_api

def store_jobs(job_file, jobs: List[Dict]):
    
    with open(job_file, 'a') as fid:
        for job in jobs:
            fid.write(json.dumps(job))


@dataclass(kw_only=True)
class MlConfig:
    domain: str = "localhost"
    scheme: str = "http"
    port: int = 8000
    base_route: str = "ml"
    Key_: ClassVar[str] = "ml"
    job_ids: List[str] = field(default_factory=list)


pass_ml = click.make_pass_decorator(MlConfig, ensure=True)


@click.group()
@click.pass_context
@pass_config
def cli(config: WsConfig, context: click.Context):
    try:
        context.obj = MlConfig(**config.storer.get_key(MlConfig.Key_))
    except TypeError as err:
        click.echo(f"error loading the store key '{MlConfig.Key_}'\n"
                   f"Error:\n    {err}\n"
                   "please use the wscli config commands to fix the issue")
        raise click.Abort()


@cli.command()
@pass_ml
def config_get(ml: MlConfig):
    click.echo(pprint(asdict(ml)))


@cli.command()
@click.option("--domain")
@click.option("--port", type=int)
@click.option("--base-route")
@pass_ml
@pass_config
def config_set(
        config: WsConfig,
        ml: MlConfig,
        domain: str | None = None,
        port: int | None = None,
        base_route: str | None = None):
    if domain:
        ml.domain = domain
    if port:
        ml.port = port
    if base_route:
        ml.base_route = base_route
    config.storer.set_key(key=MlConfig.Key_, data=asdict(ml))
    click.echo(pprint(asdict(ml)))


@cli.command()
@pass_ml
@pass_config
def job_api(config: WsConfig, ml: MlConfig):
    try:
        response = hit_api(
            endpoint="/tasks/api",
            api_url=ApiUrl(
                domain=ml.domain,
                scheme=Scheme(ml.scheme),
                port=ml.port,
                base_route=ml.base_route,
            ),
            call_config=CallConfig(
                token=config.login.access_token,
                method=Method.POST,
                content_type="application/json",
            )
        )
        
        ml.job_ids.append(response["job_id"])
        config.storer.set_key(key=ml.Key_, data=asdict(ml))
    except requests.ConnectionError as err:
        click.echo(f"failed to make api call:\n   {err}")


@cli.command()
@click.option("--job-file", default="wscli-job.json")
@pass_ml
@pass_config
@click.option("--file-url", prompt=True)
def job_http(config: WsConfig, ml: MlConfig, file_url: str, job_file: str):

    try:
        response = hit_api(
            endpoint="tasks/http",
            api_url=ApiUrl(
                domain=ml.domain,
                scheme=Scheme(ml.scheme),
                port=ml.port,
                base_route=ml.base_route,
            ),
            call_config=CallConfig(
                token=config.login.id_token,
                method=Method.POST,
                content_type="application/json",
            ), 
            payload={
                "http_file": {"url":file_url},
                "ml_config": {}

            }
        )
        job_id = response.json()["job_id"]
        store_jobs(job_file, [{"id": job_id}])
        #ml.job_ids.append(response.json()["job_id"])
        #config.storer.set_key(key=ml.Key_, data=asdict(ml))
        print(f"Job {job_id} has been succesfully scheduled")
    except requests.ConnectionError as err:
        click.echo(f"failed to make api call:\n   {err}")


@cli.command
@click.option("--job-id", prompt=True)
@click.option("--user-id", prompt=True)
@pass_config
@pass_ml
def retrieve_results(ml:MlConfig, config: WsConfig,job_id:str, user_id:str,):
        try:
            response = hit_api(
                api_url=ApiUrl(
                    domain=ml.domain,
                    scheme=Scheme(ml.scheme),
                    port=ml.port,
                    base_route=ml.base_route,
                ),call_config=CallConfig(
                    token=config.login.id_token,
                    method=Method.GET,
                    content_type="application/json",
                ),endpoint=f"/results-external/?job_id={job_id}&user_id={user_id}") 
            print(response.json().get("predictions")) 
        
        except requests.ConnectionError as err:
            click.echo(f"failed to make api call:\n   {err}")
    

    
