import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols


def general_checks(all_methods_df):
    counts = all_methods_df.groupby("method").count()
    nans = all_methods_df[all_methods_df['SI'].isnull()].groupby('method').count()
    times = all_methods_df.groupby("method")["time"].sum()/60
    return counts, nans, times

def compute_rel_cov(all_methods_df):
    all_methods_df['rel_cov'] = round(all_methods_df['coverage'] / (all_methods_df[['reference_size','mobile_size']].min(axis=1)), 4)


def create_scatter_plot(all_methods_df):
    fig, ax = plt.subplots()
    colors = {'mmligner':'orange', 'theseus':'blue', 'mda':'green', 'pymol':'red', 'matchmaker':'purple'}
    grouped = all_methods_df.groupby('method')
    for key, group in grouped:
        group.plot(ax=ax, kind='scatter', x='rel_cov', y='rmsd', label=key, color=colors[key], s = 15, figsize=(20, 10))
    plt.show()

def create_violine_plot(all_methods_df):
    rmsds = all_methods_df.groupby("method")["rmsd"].apply(list).values
    data_to_plot = [rmsds[0], rmsds[1], rmsds[2], rmsds[3], rmsds[4]]
    positions = (1, 2, 3, 4, 5)
    values = ['matchmaker', 'mda', 'mmligner', 'pymol','theseus'] 
    plt.violinplot(data_to_plot)
    plt.xticks(positions, values)
    plt.show()


def compute_correlation(all_methods_df, coeff="pearson"):
    df = all_methods_df.corr(method=coeff)
    f,ax=plt.subplots(figsize = (9,9))
    sns.heatmap(df,annot= True,linewidths=0.5,fmt = ".3f",ax=ax)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.title(f'{coeff} Correlation for all values')
    plt.show()

    return df

def check_distribution(all_methods_df):
    rmsd = all_methods_df["rmsd"].tolist()
    si = all_methods_df["SI"].tolist()
    mi = all_methods_df["MI"].tolist()
    sas = all_methods_df["SAS"].tolist()
    rmsd_dist_shapiro = stats.shapiro(rmsd)
    si_dist_shapiro = stats.shapiro(si)
    mi_dist_shapiro = stats.shapiro(mi)
    sas_dist_shapiro = stats.shapiro(sas)
    rmsd_dist_kstest = stats.kstest(rmsd, "norm")
    si_dist_kstest = stats.kstest(si, "norm")
    mi_dist_kstest = stats.kstest(mi, "norm")
    sas_dist_kstest = stats.kstest(sas, "norm")
    print(rmsd_dist_shapiro)
    print(si_dist_shapiro)
    print(mi_dist_shapiro)
    print(sas_dist_shapiro)
    print(rmsd_dist_kstest)
    print(si_dist_kstest)
    print(mi_dist_kstest)
    print(sas_dist_kstest)

    sns.displot(all_methods_df, x="rmsd", hue="method", element="step")
    sns.displot(all_methods_df, x="SI", hue="method", element="step")
    sns.displot(all_methods_df, x="MI", hue="method", element="step")
    sns.displot(all_methods_df, x="SAS", hue="method", element="step")
    sns.displot(all_methods_df, x="rel_cov", hue="method", element="step")
    return [rmsd_dist_shapiro, si_dist_shapiro, mi_dist_shapiro, sas_dist_shapiro,
            rmsd_dist_kstest, si_dist_kstest, mi_dist_kstest, sas_dist_kstest]


def compute_anova(all_methods_df):
    rmsd_model = ols('rmsd ~ C(method)', data=all_methods_df).fit()
    rmsd_anova = sm.stats.anova_lm(rmsd_model, typ=2)
    si_model = ols('SI ~ C(method)', data=all_methods_df).fit()
    si_anova = sm.stats.anova_lm(si_model, typ=2)
    mi_model = ols('MI ~ C(method)', data=all_methods_df).fit()
    mi_anova = sm.stats.anova_lm(mi_model, typ=2)
    sas_model = ols('SAS ~ C(method)', data=all_methods_df).fit()
    sas_anova = sm.stats.anova_lm(sas_model, typ=2)
    print("ANOVA results for RMSD:")
    print(rmsd_anova)
    print("\n")
    print("ANOVA results for Similarity Index (SI):")
    print(si_anova)
    print("\n")
    print("ANOVA results for Match Index (MI):")
    print(mi_anova)
    print("\n")
    print("ANOVA results for Structural Alignment Score (SAS):")
    print(sas_anova)
    return [rmsd_anova, si_anova, mi_model, sas_anova]

def compute_kruskal(all_methods_df):
    rmsd_diff = stats.kruskal(*[group["rmsd"].values for name, group in all_methods_df.groupby("method")])
    si_diff = stats.kruskal(*[group["SI"].values for name, group in all_methods_df.groupby("method")])
    mi_diff = stats.kruskal(*[group["MI"].values for name, group in all_methods_df.groupby("method")])
    sas_diff = stats.kruskal(*[group["SAS"].values for name, group in all_methods_df.groupby("method")])
    print("Kruskal Wallis results for RMSD:")
    print(rmsd_diff)
    print("\n")
    print("Kruskal Wallis results for Similarity Index (SI):")
    print(si_diff)
    print("\n")
    print("Kruskal Wallis results for Match Index (MI):")
    print(mi_diff)
    print("\n")
    print("Kruskal Wallis results for Structural Alignment Score (SAS):")
    print(sas_diff)
    return [rmsd_diff, si_diff, mi_diff, sas_diff]

def compute_mannwhitneyu(all_methods_df):
    theseus_df = all_methods_df[all_methods_df["method"] == "theseus"]
    pymol_df = all_methods_df[all_methods_df["method"] == "pymol"]
    matchmaker_df = all_methods_df[all_methods_df["method"] == "matchmaker"]
    mmligner_df = all_methods_df[all_methods_df["method"] == "mmligner"]
    mda_df = all_methods_df[all_methods_df["method"] == "mda"]
    dfs = {"theseus": theseus_df, "pymol": pymol_df, "mmaker": matchmaker_df, "mmligner": mmligner_df, "mda": mda_df}
    keys = [*dfs]
    metrics = ["rmsd", "SI", "MI", "SAS"]
    significants = []
    non_significants = []
    for metric in metrics:
        for key1 in keys:
            for key2 in keys[keys.index(key1)+1:]:
                res = stats.mannwhitneyu(dfs[key1]["rmsd"], dfs[key2]["rmsd"])
                if res[1] < 0.05:
                    significants.append([metric, key1, key2, res])
                elif res[1] >= 0.05:
                    non_significants.append([metric, key1, key2, res])

    print("All significant results:")
    for entry in significants:
        print(f"Result for {entry[0]} with {entry[1]} and {entry[2]}:")
        print(entry[3])
    print("\n***********************************\n")
    print("All non significant results:")
    for entry in non_significants:
        print(f"Result for {entry[0]} with {entry[1]} and {entry[2]}:")
        print(entry[3])

    return significants, non_significants

def count_best_results(all_methods_df):
    strucs = all_methods_df['reference_id'].append(all_methods_df['mobile_id']).unique().tolist()
    names=["reference_id", "mobile_id", "method", "rmsd", 
                           "coverage", "reference_size", "mobile_size", "time", 
                           "SI", "MI", "SAS", "ref_name", "ref_group", "ref_species", 
                           "ref_chain", "mob_name", "mob_group", "mob_species", "mob_chain"]
    SI_df = pd.DataFrame(columns=names)
    MI_df = pd.DataFrame(columns=names)
    SAS_df = pd.DataFrame(columns=names)
    SI_wo_mmligner_df = pd.DataFrame(columns=names)
    MI_wo_mmligner_df = pd.DataFrame(columns=names)
    SAS_wo_mmligner_df = pd.DataFrame(columns=names)
    wo_mmligner_df = all_methods_df[all_methods_df["method"] != "mmligner"]
    for structure in strucs:
        for mobile in strucs[strucs.index(structure) + 1:]:
            temp_df = all_methods_df[(all_methods_df["reference_id"] == structure) & (all_methods_df["mobile_id"] == mobile)]
            SI_df = SI_df.append(temp_df.loc[temp_df['SI'] == temp_df['SI'].min()])
            MI_df = MI_df.append(temp_df.loc[temp_df['MI'] == temp_df['MI'].min()])
            SAS_df = SAS_df.append(temp_df.loc[temp_df['SAS'] == temp_df['SAS'].min()])

            temp_wo_mmligner_df = wo_mmligner_df[(wo_mmligner_df["reference_id"] == structure) & (wo_mmligner_df["mobile_id"] == mobile)]
            SI_wo_mmligner_df = SI_wo_mmligner_df.append(temp_wo_mmligner_df.loc[temp_wo_mmligner_df['SI'] == temp_wo_mmligner_df['SI'].min()])
            MI_wo_mmligner_df = MI_wo_mmligner_df.append(temp_wo_mmligner_df.loc[temp_wo_mmligner_df['MI'] == temp_wo_mmligner_df['MI'].min()])
            SAS_wo_mmligner_df = SAS_wo_mmligner_df.append(temp_wo_mmligner_df.loc[temp_wo_mmligner_df['SAS'] == temp_wo_mmligner_df['SAS'].min()])
    print("Counts of best values for the Similarity Index (SI):")
    print(SI_df["method"].value_counts())
    print("\n")
    print("Counts of best values for the Match Index (MI):")
    print(MI_df["method"].value_counts())
    print("\n")
    print("Counts of best values for the Structural Alignment Score (SAS):")
    print(SAS_df["method"].value_counts())
    print("\n")

    print("Counts of best values for the Similarity Index (SI) without MMLigner:")
    print(SI_wo_mmligner_df["method"].value_counts())
    print("\n")
    print("Counts of best values for the Match Index (MI) without MMLigner:")
    print(MI_wo_mmligner_df["method"].value_counts())
    print("\n")
    print("Counts of best values for the Structural Alignment Score (SAS) without MMLigner:")
    print(SAS_wo_mmligner_df["method"].value_counts())
    return [SI_df, MI_df, SAS_df, SI_wo_mmligner_df, MI_wo_mmligner_df, SAS_wo_mmligner_df]
    