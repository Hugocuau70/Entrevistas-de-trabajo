import sys, json, pandas as pd
RAW=sys.argv[1]
df=pd.read_csv(f'{RAW}/ce2024/conjunto_de_datos/tr_ce_nac_2024.csv', dtype=str, usecols=['E03','CODIGO','ID_ESTRATO','UE','H001A','M000A'])
df=df[df.E03.fillna('').str.strip().isin(['','00'])] if 'E03' in df else df
df['CODIGO']=df.CODIGO.fillna('').str.strip(); df['ID_ESTRATO']=df.ID_ESTRATO.fillna('').str.strip()
for c in ['UE','H001A','M000A']: df[c]=pd.to_numeric(df[c],errors='coerce')
codes=['5412','5416','5413','5411','5415','5418','5182','5173','5613','5616','4931','4841','3254','6215','6221','3363','3344','311','23','4811','5615','7211','4854','7225']
res={}
for c in codes:
    d=df[df.CODIGO==c]
    tot=d[d.ID_ESTRATO==''] ; s4=d[d.ID_ESTRATO=='4']
    res[c]=dict(ue_total=float(tot.UE.sum()) if len(tot) else None, emp_total=float(tot.H001A.sum()) if len(tot) else None,
                ue_251=float(s4.UE.sum()) if len(s4) else None, emp_251=float(s4.H001A.sum()) if len(s4) else None)
    print(c, res[c])
json.dump(res, open(sys.argv[2],'w'), indent=1)
