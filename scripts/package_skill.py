"""Package the standalone skill as a ZIP archive."""
import argparse
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]


def package(output):
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    source=ROOT/'skills/promptharbor'
    entries=[(p, 'promptharbor/'+p.relative_to(source).as_posix()) for p in source.rglob('*')
             if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for p,name in sorted(entries,key=lambda x:x[1]):
            z.write(p,name)
    return output


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,default=ROOT/'dist/promptharbor-0.2.1.zip')
    print(package(p.parse_args().out))
