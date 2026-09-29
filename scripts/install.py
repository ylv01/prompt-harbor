"""Copy the self-contained skill to a host's skill directory. Never overwrite."""
import argparse
import os
from pathlib import Path
import shutil

SOURCE = Path(__file__).resolve().parents[1] / 'skills/promptharbor'


def install(destination):
    target = Path(destination).expanduser().resolve() / 'promptharbor'
    if target.exists():
        raise FileExistsError(f'{target} already exists; review and remove or rename it before reinstalling.')
    shutil.copytree(SOURCE, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    return target


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--host', choices=['codex','claude'])
    group.add_argument('--dest',type=Path,help='Custom parent skill directory')
    args=parser.parse_args()
    destination=args.dest
    if args.host=='codex':
        destination=Path(os.environ.get('CODEX_HOME',Path.home()/'.codex'))/'skills'
    elif args.host=='claude':
        destination=Path.home()/'.claude/skills'
    try:
        print(install(destination))
    except OSError as exc:
        parser.exit(2,str(exc)+'\n')
