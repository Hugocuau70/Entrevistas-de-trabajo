import sys, json, pandas as pd, numpy as np
RAW = sys.argv[1]; OUT = sys.argv[2]
YEARS = [2022, 2023, 2024, 2025]
def seas(df, val, years):
    # Ratio to centered 2x12 moving average (removes trend/inflation), averaged by month
    df = df.sort_values(['ANIO','MES']).copy()
    df['v'] = pd.to_numeric(df[val], errors='coerce')
    df = df[df.v.notna()]
    ma = df.v.rolling(12).mean()
    df['ma'] = (ma + ma.shift(-1)) / 2
    df['ma'] = df['ma'].shift(-5)
    df['rel'] = df.v / df.ma
    w = df[(df.ANIO >= years[0]) & (df.ANIO <= years[-1]) & df.rel.notna()]
    m = w.groupby('MES').rel.mean().reindex(range(1, 13))
    m = m / m.mean()
    span = f"{w.ANIO.min()}-{w.MES[w.ANIO==w.ANIO.min()].min():02d} to {w.ANIO.max()}-{w.MES[w.ANIO==w.ANIO.max()].max():02d}"
    return m.values * 100, span
def clean(df):
    df.columns = [c.strip() for c in df.columns]
    df['MES'] = df.MES.astype(str).str.strip().astype(int)
    df['ANIO'] = df.ANIO.astype(int)
    df['CODIGO_ACTIVIDAD'] = df.CODIGO_ACTIVIDAD.astype(str).str.strip()
    return df
ems = clean(pd.read_csv(f'{RAW}/conjunto_de_datos_ems_mensual_csv/conjunto_de_datos/tr_ems_nacional_indice_2008_2026.csv', dtype=str))
emim = clean(pd.read_csv(f'{RAW}/emim/conjunto_de_datos/tr_indice_ram_mensual_nac_2007_2025.csv', dtype=str))
emim_s = clean(pd.read_csv(f'{RAW}/emim/conjunto_de_datos/tr_indice_sub_mensual_nac_2007_2025.csv', dtype=str))
enec = clean(pd.read_csv(f'{RAW}/conjunto_de_datos_enec_mensual_csv/conjunto_de_datos/enec_absoluto_nacional_2018_2026.csv', dtype=str))
enec = enec[(enec.CODIGO_ACTIVIDAD == '23') & (enec.NOM_ENT.str.strip() == 'Nacional')]
rows0 = [
 # group, code, name_en, source df, variable, metric label
 ('Professional services','5412','Audit, accounting & tax',ems,'M000','Revenue'),
 ('Professional services','5416','Management consulting',ems,'M000','Revenue'),
 ('Professional services','5413','Engineering & architecture',ems,'M000','Revenue'),
 ('Professional services','5411','Legal services',ems,'M000','Revenue'),
 ('Professional services','5415','IT services & software',ems,'M000','Revenue'),
 ('Professional services','5418','Advertising & agencies',ems,'M000','Revenue'),
 ('Tech & infrastructure','5182','Data processing & hosting',ems,'M000','Revenue'),
 ('Tech & infrastructure','5173','Telecom operators',ems,'M000','Revenue'),
 ('Business support','5613','Staffing & employment services',ems,'M000','Revenue'),
 ('Business support','5616','Security services',ems,'M000','Revenue'),
 ('Logistics','4931','Warehousing',ems,'M000','Revenue'),
 ('Logistics','4841','Freight trucking',ems,'M000','Revenue'),
 ('Healthcare & pharma','3254','Pharmaceutical manufacturing',emim,'IVFV_C','Sales volume'),
 ('Healthcare & pharma','6215','Medical & diagnostic labs',ems,'M000','Revenue'),
 ('Healthcare & pharma','6221','General hospitals',ems,'M000','Revenue'),
 ('Manufacturing','3363','Auto parts',emim,'IVFV_C','Sales volume'),
 ('Manufacturing','3344','Electronic components',emim,'IVFV_C','Sales volume'),
 ('Manufacturing','311','Food manufacturing',emim_s,'IVFV_C','Sales volume'),
 ('Construction','23','Construction (total)',enec,'O110A','Value of output'),
 ('Travel pulse','4811','Scheduled air transport',ems,'M000','Revenue'),
 ('Travel pulse','5615','Travel agencies & reservations',ems,'M000','Revenue'),
 ('Travel pulse','7211','Hotels',ems,'M000','Revenue'),
 ('Travel pulse','4854','Employee & school transport (substitute)',ems,'M000','Revenue'),
 ('Travel pulse','7225','Restaurants & food service (Eats context)',ems,'M000','Revenue'),
]
ALT = {'M000':('H000A','Headcount'), 'IVFV_C':('IHH_T5','Hours worked'), 'O110A':('H001D','Hours worked')}
rows = []
for g, code, name, df, var, metric in rows0:
    rows.append((g, code, name, df, var, metric))
    a = ALT[var]; rows.append((g, code, name, df, a[0], a[1]))
out = []
for g, code, name, df, var, metric in rows:
    d = df[df.CODIGO_ACTIVIDAD == code]
    idx, yrs = seas(d, var, YEARS)
    peak = int(np.nanargmax(idx)); trough = int(np.nanargmin(idx))
    out.append(dict(group=g, code=code, name=name, metric=metric, variable=var,
        source=('INEGI EMIM' if df is emim or df is emim_s else 'INEGI ENEC' if df is enec else 'INEGI EMS'),
        span=yrs, index=[round(float(x),1) for x in idx],
        peak_norm=[round(float(x/np.nanmax(idx)*100)) for x in idx],
        h1_share=round(float(np.nansum(idx[:6])/np.nansum(idx)*100),1),
        peak_month=peak+1, trough_month=trough+1,
        amplitude=round(float(np.nanmax(idx)-np.nanmin(idx)),1)))
json.dump(out, open(OUT,'w'), indent=1)
M='Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
for r in out:
    print(f"{r['name'][:34]:34} {r['source']:10} {r['metric'][:12]:12} H1={r['h1_share']:5}% peak={M[r['peak_month']-1]} low={M[r['trough_month']-1]} amp={r['amplitude']:5} | "+' '.join(f"{x:3d}" for x in r['peak_norm']))
