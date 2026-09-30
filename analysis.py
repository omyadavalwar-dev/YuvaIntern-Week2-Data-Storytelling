"""YuvaIntern Week 2: five views of penguin size and sample composition.
Run python analysis.py. The local source snapshot is used without network access.
"""
# %% Load and prepare
from pathlib import Path
import json
import hashlib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parent
for folder in ('charts', 'tables', 'data'):
    (ROOT / folder).mkdir(exist_ok=True)
raw = pd.read_csv(ROOT / 'data/penguins_raw.csv', na_values=['NA'])
measurements = ['bill_length_mm','bill_depth_mm','flipper_length_mm','body_mass_g']
df = raw.copy()
for col in ['species','island','sex']:
    df[col] = df[col].astype('string').str.strip()
df['sex'] = df['sex'].str.lower()
for col in measurements + ['year']:
    df[col] = pd.to_numeric(df[col], errors='raise')
duplicates = int(df.duplicated().sum())
df = df.drop_duplicates().dropna(subset=measurements).copy()
df['sex'] = df['sex'].fillna('Unknown')
assert len(df) == 342 and (df[measurements] > 0).all().all()
assert df.year.between(2007, 2009).all()
df.to_csv(ROOT / 'data/penguins_clean.csv', index=False)
species = ['Adelie','Chinstrap','Gentoo']
colors = dict(zip(species,['#236A93','#C26B27','#28826C']))
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
def save(name):
    plt.tight_layout()
    plt.savefig(ROOT / 'charts' / name, dpi=180, bbox_inches='tight')
    plt.close()

# %% Figure 1 Sample composition heatmap
composition = pd.crosstab(df.species, df.island).reindex(species)
composition.to_csv(ROOT / 'tables/species_island.csv')
fig, ax = plt.subplots(figsize=(8.4,4.2))
im = ax.imshow(composition, cmap='Blues', vmin=0, vmax=125, aspect='auto')
ax.set_xticks(range(3), composition.columns)
ax.set_yticks(range(3), [f'{s} (n={sum(composition.loc[s])})' for s in species])
for i in range(3):
    for j in range(3):
        n = int(composition.iloc[i,j])
        ax.text(j,i,str(n),ha='center',va='center',color='white' if n>70 else 'black',fontsize=15)
ax.set(title='Species and island are linked in this sample',xlabel='Island')
fig.colorbar(im,ax=ax,label='Observed records')
save('01_sample_composition.png')

# %% Figure 2 Cumulative distributions
fig, ax = plt.subplots(figsize=(8.4,4.2))
for s, style in zip(species,['-','--',':']):
    x=np.sort(df.loc[df.species==s,'body_mass_g'])
    ax.step(x,np.arange(1,len(x)+1)/len(x)*100,where='post',color=colors[s],ls=style,lw=2.3,label=f'{s} (n={len(x)})')
ax.axhline(50,color='grey',ls='--',lw=.8)
ax.text(6350,52,'50% of records',ha='right',fontsize=9)
ax.set(xlabel='Body mass (g)',ylabel='Share at or below this mass (%)',ylim=(0,102),title='Gentoo mass distribution is shifted toward heavier birds')
ax.legend(frameon=False,loc='lower right')
save('02_mass_ecdf.png')

# %% Figure 3 Sex within species
known=df[df.sex!='Unknown'].copy()
sex_summary=known.groupby(['species','sex']).body_mass_g.agg(['size','median','mean'])
sex_summary.to_csv(ROOT/'tables/species_sex_mass.csv')
rng=np.random.default_rng(42)
fig,axes=plt.subplots(1,3,figsize=(9.4,4.2),sharey=True)
for ax,s in zip(axes,species):
    groups=[known.loc[(known.species==s)&(known.sex==sex),'body_mass_g'].to_numpy() for sex in ['female','male']]
    bp=ax.boxplot(groups,positions=[0,1],widths=.5,patch_artist=True,showfliers=False)
    for box in bp['boxes']: box.set(facecolor=colors[s],alpha=.35)
    for i,v in enumerate(groups):
        ax.scatter(i+rng.uniform(-.12,.12,len(v)),v,s=9,alpha=.42,color=colors[s])
    ax.set_xticks([0,1],[f'Female\nn={len(groups[0])}',f'Male\nn={len(groups[1])}'])
    ax.set_title(s)
axes[0].set_ylabel('Body mass (g)')
fig.suptitle('Males have higher median mass within each sampled species',y=1.02)
save('03_mass_by_sex.png')

# %% Figure 4 Faceted relationships
fig,axes=plt.subplots(1,3,figsize=(9.4,4.2),sharex=True,sharey=True)
within={}
for ax,s in zip(axes,species):
    g=df[df.species==s]
    r=g.flipper_length_mm.corr(g.body_mass_g); within[s]=float(r)
    ax.scatter(g.flipper_length_mm,g.body_mass_g,s=15,alpha=.6,color=colors[s])
    slope,intercept=np.polyfit(g.flipper_length_mm,g.body_mass_g,1)
    x=np.array([g.flipper_length_mm.min(),g.flipper_length_mm.max()])
    ax.plot(x,slope*x+intercept,color=colors[s],lw=2)
    ax.set(title=f'{s}\nr={r:.3f}, n={len(g)}',xlabel='Flipper length (mm)',xlim=(170,233),ylim=(2500,6500))
axes[0].set_ylabel('Body mass (g)')
fig.suptitle('The flipper and mass association persists within species',y=1.04)
save('04_within_species_relationship.png')

# %% Figure 5 Annual summaries with sample sizes
annual=df.groupby(['species','year']).body_mass_g.agg(['size','median','mean'])
annual.to_csv(ROOT/'tables/annual_mass.csv')
fig,ax=plt.subplots(figsize=(8.4,4.2))
for s,marker in zip(species,['o','^','s']):
    g=annual.loc[s]
    ax.plot(g.index,g['median'],marker=marker,color=colors[s],label=s,lw=2)
    for year,row in g.iterrows():
        offset=14 if s=='Adelie' else -19 if s=='Chinstrap' else 10
        ax.annotate(f'n={int(row["size"])}',(year,row['median']),xytext=(0,offset),textcoords='offset points',ha='center',fontsize=9,color=colors[s])
ax.set(xticks=[2007,2008,2009],xlim=(2006.8,2009.35),ylim=(3200,5600),xlabel='Collection year',ylabel='Median body mass (g)',title='Gentoo remains heavier across the three sampled years')
ax.legend(frameon=False,loc='center right')
save('05_annual_medians.png')

# %% Auditable numerical claims
summary=df.groupby('species').body_mass_g.agg(['size','mean','median','min','max'])
summary.to_csv(ROOT/'tables/species_mass.csv')
audit={'raw_rows':len(raw),'retained_rows':len(df),'duplicates_removed':duplicates,
       'known_sex_rows':len(known),'unknown_sex':int((df.sex=='Unknown').sum()),
       'pooled_r':float(df.flipper_length_mm.corr(df.body_mass_g)), 'within_species_r':within,
       'sha256':hashlib.sha256((ROOT/'data/penguins_raw.csv').read_bytes()).hexdigest(),
       'source_url':'https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv',
       'versions':{'pandas':pd.__version__,'numpy':np.__version__,'matplotlib':matplotlib.__version__}}
(ROOT/'tables/audit.json').write_text(json.dumps(audit,indent=2))
print(summary.round(2).to_string())
print(sex_summary.round(2).to_string())
print(annual.round(2).to_string())
print(json.dumps(audit,indent=2))
