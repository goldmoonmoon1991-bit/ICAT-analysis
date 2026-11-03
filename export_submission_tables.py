"""Export numeric tables for analyses whose original scripts only saved plots.

Uses the supplied input rows and the tests stated in the manuscript/legacy code.
The paired abundance test is exported separately from the legacy ratio test.
Run inside an extracted copy. Existing raw inputs are read without modification.
"""
from pathlib import Path
import argparse
import json
import subprocess
import numpy as np
import pandas as pd


def r_t_test(a,b,paired=False):
    """Use R's original t.test implementation rather than a different engine."""
    av=','.join(str(float(x)) for x in a)
    bv=','.join(str(float(x)) for x in b)
    expr=(f'options(digits=17); t <- t.test(c({av}),c({bv}),'
          f'paired={"TRUE" if paired else "FALSE"}); '
          'cat(unname(t$statistic), t$p.value, sep=",")')
    result=subprocess.check_output(['Rscript','--vanilla','-e',expr],text=True)
    return tuple(map(float,result.strip().split(',')))


def bh_adjust(pvalues):
    p=np.asarray(pvalues,dtype=float)
    order=np.argsort(p)
    q=np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1]
    result=np.empty_like(q)
    result[order]=np.minimum(q,1)
    return result


def main(root):
    out=root/'submission_tables'
    out.mkdir(exist_ok=True)
    f4=root/'Fig4_phenotype_targeting'/'01_raw_data'
    raw=pd.read_csv(f4/'invasion'/'Invasion_dynamic.csv')
    raw=raw.rename(columns={raw.columns[0]:'time_label'})
    raw['time_min']=raw.time_label.str.extract(r'(\d+)').astype(int)
    invasion=raw.drop(columns='time_label').melt(id_vars='time_min',var_name='condition_replicate',value_name='invasion_fraction')
    invasion[['condition','replicate']]=invasion.condition_replicate.str.rsplit('-',n=1,expand=True)
    invasion=invasion.drop(columns='condition_replicate')
    invasion.to_csv(out/'invasion_long.csv',index=False)
    invasion.groupby(['time_min','condition']).invasion_fraction.agg(n='count',mean='mean',sd='std').reset_index().to_csv(out/'invasion_summary.csv',index=False)
    tests=[]
    for time,group in invasion.groupby('time_min'):
        a=group.loc[group.condition=='vehicle','invasion_fraction']
        b=group.loc[group.condition=='IAA','invasion_fraction']
        statistic,pvalue=r_t_test(a,b)
        tests.append([time,len(a),len(b),statistic,pvalue,'two-sided Welch t-test; no multiplicity correction, as stated in legend'])
    pd.DataFrame(tests,columns=['time_min','n_vehicle','n_IAA','t_statistic','p_value','test']).to_csv(out/'invasion_tests.csv',index=False)

    raw=pd.read_csv(f4/'egress'/'ICAT_egress.csv')
    raw['time_s']=np.arange(len(raw))
    egress=raw.melt(id_vars='time_s',var_name='condition_replicate',value_name='egress_percent')
    egress[['condition','replicate']]=egress.condition_replicate.str.rsplit('-',n=1,expand=True)
    egress['condition']=egress.condition.replace({'Etoh':'vehicle','Auxin':'IAA'})
    egress=egress.drop(columns='condition_replicate')
    egress.to_csv(out/'egress_long.csv',index=False)
    egress.groupby(['time_s','condition']).egress_percent.agg(n='count',mean='mean',sd='std').reset_index().to_csv(out/'egress_summary.csv',index=False)
    t50=egress[egress.egress_percent>=50].groupby(['condition','replicate']).time_s.min().rename('first_time_at_least_50_percent_s').reset_index()
    t50.to_csv(out/'egress_t50.csv',index=False)
    a=t50.loc[t50.condition=='vehicle','first_time_at_least_50_percent_s']
    b=t50.loc[t50.condition=='IAA','first_time_at_least_50_percent_s']
    statistic,egress_pvalue=r_t_test(a,b)
    pd.DataFrame([[len(a),len(b),statistic,egress_pvalue,'two-sided Welch t-test; first sampled time >=50%, no interpolation']],columns=['n_vehicle','n_IAA','t_statistic','p_value','test']).to_csv(out/'egress_t50_test.csv',index=False)

    raw=pd.read_csv(root/'Fig5_secretion_mechanism'/'01_raw_data'/'microneme_spatial_restriction'/'total_protein_abundance'/'ARO_MIC2_total_abundance_template.csv')
    tests=[]
    for protein,group in raw.groupby('protein'):
        group=group.sort_values('replicate')
        statistic,pvalue=r_t_test(group.IAA_intensity,group.vehicle_intensity,paired=True)
        tests.append([protein,len(group),statistic,pvalue,'paired two-sided t-test on supplied intensities, IAA vs vehicle'])
    paired=pd.DataFrame(tests,columns=['protein','n_pairs','t_statistic','p_value','test'])
    paired['BH_q_value']=bh_adjust(paired.p_value)
    paired.to_csv(out/'abundance_paired_test_per_legend.csv',index=False)

    mci=pd.read_csv(root/'Fig5_secretion_mechanism'/'04_results'/'tables'/'microneme_spatial_restriction'/'width_ratio'/'ICATkd_MCI_long.csv')
    bins=pd.read_csv(root/'Fig5_secretion_mechanism'/'04_results'/'tables'/'microneme_spatial_restriction'/'position_classes'/'MCI_ClassIII_fraction_by_MCI_bin.csv')
    distance=pd.read_csv(root/'Fig3_ICAT_neighboring'/'04_results'/'tables'/'spatial_relationship'/'Fig3C_MIC2_ICAT_peak_and_2_3_gap_summary.csv')
    physical=distance[distance.metric=='peak_distance_nm_actual'].iloc[0]
    checks={'MCI_cells_by_condition':mci.condition.value_counts().to_dict(),'MCI_total':len(mci),'ClassIII_bins':bins[['mci_bin','n_cells','n_class_III']].to_dict('records'),'Fig3d_distance_nm_mean':physical['mean'],'Fig3d_distance_nm_sd':physical['sd'],'egress_t50_p_value':egress_pvalue,'export_note':'Derived from existing inputs; raw files were not edited. Paired abundance analysis is separate from the preserved legacy ratio statistics.'}
    (out/'numeric_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
    assert len(mci)==153
    assert sorted(mci.condition.value_counts().tolist())==[65,88]
    assert bins.n_class_III.tolist()==[43,28,4]
    assert bins.n_cells.tolist()==[51,51,51]
    assert round(physical['mean'])==33 and round(physical['sd'])==13
    print(json.dumps(checks,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    main(parser.parse_args().root)
