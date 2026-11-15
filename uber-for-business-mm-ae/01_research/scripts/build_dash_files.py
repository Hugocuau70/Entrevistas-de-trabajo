import sys, json, os, csv
S = sys.argv[1]; OUT = f'{S}/dash_files'
seas = json.load(open(f'{S}/seasonality.json')); cen = json.load(open(f'{S}/census.json'))
code_seas = open(f'{S}/scripts/seasonality.py').read()
code_cen = open(f'{S}/scripts/census.py').read()
code_build = open(__file__).read()
M = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
rows = []
for r in seas:
    kind = 'activity' if r['metric'] in ('Revenue','Sales volume','Value of output') else 'people'
    row = dict(row_id=f"{r['code']}|{kind}", code=r['code'], industry=r['name'], group=r['group'],
               view=kind, metric=r['metric'], source=r['source'], window=r['span'])
    for i, m in enumerate(M): row[m] = r['index'][i]
    row.update(h1_share=r['h1_share'], peak_month=M[r['peak_month']-1].title(), low_month=M[r['trough_month']-1].title(), amplitude=r['amplitude'])
    rows.append(row)
json.dump({'rows': rows, 'meta': [
  {'label': 'Method', 'value': 'Ratio to a centered 2x12 moving average (removes trend and inflation), averaged by calendar month and rescaled so the 12-month mean = 100.'},
  {'label': 'Inputs', 'value': 'INEGI EMS national index 2008-2026 (M000 revenue, H000A headcount); INEGI EMIM branch/subsector index 2007-2025 (IVFV_C sales volume, IHH_T5 hours worked); INEGI ENEC national 2018-2026 (O110A value of output, H001D hours worked).'},
  {'label': 'seasonality.py', 'value': code_seas, 'type': 'code', 'lang': 'python'},
  {'label': 'build_dash_files.py', 'value': code_build, 'type': 'code', 'lang': 'python'}]}, open(f'{OUT}/seasonality.json','w'))
names = {r['code']: (r['name'], r['group']) for r in seas}
crow = []
for code, v in cen.items():
    n, g = names[code]
    crow.append(dict(code=code, industry=n, group=g, establishments_total=v['ue_total'], employees_total=v['emp_total'],
        establishments_251plus=v['ue_251'], employees_251plus=v['emp_251'],
        avg_employees_251plus=round(v['emp_251']/v['ue_251']) if v['ue_251'] else None))
json.dump({'rows': crow, 'meta': [
  {'label': 'Input', 'value': 'INEGI Censos Economicos 2024, national results (tr_ce_nac_2024.csv). Unit = establishment (one office or plant), not company. Stratum 4 = 251 or more employees.'},
  {'label': 'census.py', 'value': code_cen, 'type': 'code', 'lang': 'python'}]}, open(f'{OUT}/census.json','w'))
# Analyst scores (assumptions, 1-5)
SC = {
 '5412': (5,5,5,'Busy season Jan-Apr: shareholder meetings by Apr 30 (LGSM art. 181), annual corporate tax return Mar 31. Auditors work on client sites.'),
 '5416': (5,4,3,'New-year budgets open Q1; consultants work on client sites.'),
 '5413': (4,3,5,'Queretaro data center build-out: CloudHQ first phases due Q2 2027; ODATA and KIO expansions.'),
 '5411': (3,4,2,'Court and transaction calendars; no strong H1 driver.'),
 '5415': (2,4,2,'Hybrid and remote work lowers ride intensity.'),
 '5418': (2,4,3,'Hot Sale (May-Jun) campaign production.'),
 '5182': (3,3,5,'Data center commissioning in Queretaro through 2027.'),
 '5173': (3,2,2,'Mostly enterprise-size operators.'),
 '5613': (3,2,2,'Recruiter and field visits; headcount ramps into Q4.'),
 '5616': (2,2,1,'Shift guards rarely expense rides.'),
 '4931': (2,3,3,'Nearshoring warehouses run night shifts; T-MEC review slows new projects.'),
 '4841': (1,2,1,'Drivers travel in company trucks.'),
 '3254': (5,3,4,'Plan Mexico plant investments; Q1 is the sales peak; field reps visit doctors daily.'),
 '6215': (3,2,2,'Home sample collection and branch visits.'),
 '6221': (2,4,1,'Night-shift staff rides home; flat seasonality.'),
 '3363': (3,3,1,'T-MEC review: new investment down 23% y/y in 1H26.'),
 '3344': (3,3,2,'Plant engineers and supplier visits.'),
 '311':  (3,2,2,'Sales force visits retail chains.'),
 '23':   (3,3,3,'Site visits; value of output peaks in Q4.'),
}
srow = [dict(code=c, industry=names[c][0], group=names[c][1], travel_intensity=a, eats_fit=b, h1_2027_trigger=t, rationale=why) for c,(a,b,t,why) in SC.items()]
json.dump({'rows': srow, 'meta': [{'label': 'How these were made', 'value': 'Analyst judgment on a 1-5 scale, based on the public research in 01_research/context-h1-2027.md. Not measured data: adjust before presenting.'}]}, open(f'{OUT}/scores.json','w'))
# CSV copies for the repo
for name, data in [('seasonality', rows), ('census', crow), ('scores', srow)]:
    with open(f'{OUT}/{name}.csv','w',newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(data[0].keys())); w.writeheader(); w.writerows(data)
print(len(rows), len(crow), len(srow))
