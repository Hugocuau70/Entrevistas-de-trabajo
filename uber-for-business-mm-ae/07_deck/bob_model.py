import json
R = [0.20, 0.35, 0.50, 0.60, 0.65, 0.70]          # adoption ramp after go-live
MONTHS = ['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']  # close months; go-live = next month
def h1_mult(ci):  # ci: 0=Dec ... 6=Jun ; months of H1 usage captured per $1 of monthly potential
    live = ci  # Dec close -> Jan live (H1 index 0)
    return sum(R[m - live] for m in range(live, 6)) if live < 6 else 0.0
MULT = [round(h1_mult(i), 2) for i in range(7)]
TIERS = [
  dict(t='Tier 1', inds='Audit & tax, engineering, pharma, consulting, data centers, construction', acc=40, emp=950, pe=240, meet=.85, qual=.75, win=.28, timing={'Dec': .4, 'Jan': .3, 'Feb': .3}, product='Uber Travel + Ride Policies + expense codes', motion='AE-led, BDR-supported; busy-season triggers'),
  dict(t='Tier 2', inds='Food, electronics, advertising, auto parts, warehousing, IT, legal', acc=60, emp=700, pe=130, meet=.50, qual=.60, win=.20, timing={'Feb': .25, 'Mar': .5, 'Apr': .25}, product='Uber Travel + Uber Central', motion='BDR-led sequences; AE from first meeting'),
  dict(t='Tier 3', inds='Telecom, hospitals, labs, staffing, security, trucking', acc=50, emp=500, pe=70, meet=.30, qual=.50, win=.12, timing={'Apr': .5, 'May': .5}, product='Vouchers (rides and Eats)', motion='Automated nurture; builds H2 pipeline'),
]
out = {'mult': dict(zip(MONTHS, MULT)), 'tiers': []}
tot = dict(acc=0, meet=0, opp=0, win=0, pot=0, pipe=0, wonpot=0, h1=0, jun=0)
monthly = [0.0] * 6
for T in TIERS:
    annual = T['emp'] * T['pe']; mo = annual / 12
    meet = T['acc'] * T['meet']; opp = meet * T['qual']; win = opp * T['win']
    h1 = 0; jun = 0
    for m, share in T['timing'].items():
        ci = MONTHS.index(m); w = win * share
        h1 += w * mo * MULT[ci]
        for k in range(ci, 6): monthly[k] += w * mo * R[k - ci]
        if ci <= 5: jun += w * mo * R[5 - ci]
    row = dict(T, annual=annual, meetings=meet, opps=opp, wins=win, portfolio=T['acc'] * annual, pipeline=opp * annual, won=win * annual, h1=h1, jun_runrate=jun)
    out['tiers'].append(row)
    for k, v in [('acc', T['acc']), ('meet', meet), ('opp', opp), ('win', win), ('pot', T['acc'] * annual), ('pipe', opp * annual), ('wonpot', win * annual), ('h1', h1), ('jun', jun)]: tot[k] += v
out['total'] = tot; out['monthly'] = monthly; out['cum'] = [sum(monthly[:i + 1]) for i in range(6)]
print('mult', out['mult'])
for r in out['tiers']: print(r['t'], f"annual/acct {r['annual']/1e3:.0f}K meet {r['meetings']:.0f} opps {r['opps']:.1f} wins {r['wins']:.1f} portfolio {r['portfolio']/1e6:.2f}M pipe {r['pipeline']/1e6:.2f}M won {r['won']/1e6:.2f}M H1 {r['h1']/1e3:.0f}K jun {r['jun_runrate']/1e3:.0f}K")
t = tot; print(f"TOTAL acc {t['acc']} meet {t['meet']:.0f} opps {t['opp']:.1f} wins {t['win']:.1f} blended win {t['win']/t['opp']:.0%} portfolio {t['pot']/1e6:.1f}M pipe {t['pipe']/1e6:.1f}M won {t['wonpot']/1e6:.2f}M H1 {t['h1']/1e3:.0f}K ({t['h1']/350000:.0%}) jun run-rate {t['jun']/1e3:.0f}K/mo")
print('monthly', [round(x/1e3,1) for x in monthly], 'cum', [round(x/1e3) for x in out['cum']])
# SSGT check: SSGT H1 91K vs avg tier1 Dec deal
print('avg T1 Dec deal H1', round(950*240/12*MULT[0]/1e3,1), 'K')
json.dump(out, open('/tmp/claude-0/-home-user-Entrevistas-de-trabajo/88e3197a-7a0a-53b4-a474-d84a37e1b8be/scratchpad/bob.json', 'w'), indent=1, default=str)
