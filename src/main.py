import json
import logging
from pathlib import Path

import click
from pydantic import ValidationError

from core.config import RunConfig
from core.manager import RuntimeManager

logger = logging.getLogger(__file__)

@click.command()
@click.option('config', '--config', type=click.Path(), required=True, 
              help="specify the path to the configuration directory")
@click.option('dry', '--dry', is_flag=True, required=False,
              help="Show the fully specified configuration that is being run with without actually running the test")
def main(config, dry):
    """
    entry point for running the actual benchmark with a specific config file  
    """
    conf_path = Path(config)

    with open(conf_path) as f:
        raw = json.load(f)

    try: 
        conf = RunConfig(**raw)
    except ValidationError as e:
        logger.error(f"invalid configuration provided: {e}")
        raise


    
    if not dry:
        manager = RuntimeManager(conf)
        manager.run()
    else: 
        from pprint import pprint
        pprint(conf.model_dump())

if __name__ == "__main__":
    main()

