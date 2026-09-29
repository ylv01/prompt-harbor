"""Create a deterministic standalone skill archive without repository/test artifacts."""
import argparse
import hashlib
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]


def package(output):
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    if output.exists():
        raise FileExistsError('Archive exists; choose a new output path')
    source=ROOT/'skills/promptharbor'
    entries=[(p, 'promptharbor/'+p.relative_to(source).as_posix()) for p in source.rglob('*')
             if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for p,name in sorted(entries,key=lambda x:x[1]):
            info=zipfile.ZipInfo(name,(2026,9,29,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes())
    digest=hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix+'.sha256').write_text(digest+'  '+output.name+'\n',encoding='utf-8')
    return digest


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,default=ROOT/'dist/promptharbor-0.2.0.zip')
    print(package(p.parse_args().out))
