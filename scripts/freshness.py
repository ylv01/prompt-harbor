"""Report due evidence/source reviews. Does not fetch pages or renew claims."""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/promptharbor/scripts'))
from harbor import audit, load_data


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--as-of',type=date.fromisoformat,default=date.today())
    p.add_argument('--fail-due',action='store_true')
    args=p.parse_args();data=load_data();report=audit(data,args.as_of)
    report['sources_due']=[{'id':s['id'],'url':s['url']} for s in data['sources']['sources']
                           if (args.as_of-date.fromisoformat(s['checked_on'])).days>s['review_days']]
    report['due']=report['due'] or bool(report['sources_due'])
    print(json.dumps(report,ensure_ascii=True,indent=2))
    raise SystemExit(1 if args.fail_due and report['due'] else 0)
