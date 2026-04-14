#!/usr/bin/env python3
"""
Analysis Script: Target DEI Boycott — TikTok Content Analysis
Brand Covenant Broken: Digital Activism, Corporate Communication,
and Community Accountability in the Target DEI Boycott

Author: Endalkachew H. Chala, PhD
Date: April 2026

Requirements: pip install pandas scipy matplotlib seaborn openpyxl krippendorffs-alpha
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')
plt.rcParams.update({'font.family': 'serif', 'font.size': 11, 'figure.dpi': 300})

# ══════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════

DATA_FILE = 'data/tiktok_coded_data.xlsx'
CORP_FILE = 'data/corporate_comms_coded.xlsx'
OUTPUT_DIR = 'analysis/results'
FIGURE_DIR = 'analysis/figures'

# Variable labels for display
FRAME_LABELS = {
    1: 'Moral/Ethical Betrayal',
    2: 'Economic Power',
    3: 'Historical Continuity',
    4: 'Corporate Hypocrisy',
    5: 'Community Solidarity',
    6: 'Alternative Support',
    7: 'Information/News',
    8: 'Counter-Boycott',
    99: 'Cannot Determine'
}

CREATOR_LABELS = {
    1: 'Consumer', 2: 'Influencer', 3: 'Activist',
    4: 'Faith Leader', 5: 'Business Owner', 6: 'Journalist',
    7: 'Academic', 99: 'Cannot Determine'
}

TONE_LABELS = {
    1: 'Anger/Outrage', 2: 'Disappointment', 3: 'Empowerment/Pride',
    4: 'Humor/Satire', 5: 'Neutral', 6: 'Hope/Optimism', 99: 'Cannot Determine'
}

COMMUNITY_LABELS = {
    0: 'None', 1: 'Black Community', 2: 'Communities of Color',
    3: 'Progressive/Allied', 4: 'Local/Minnesota', 5: 'General Public'
}

MORAL_LABELS = {0: 'None', 1: 'Low', 2: 'Moderate', 3: 'High'}

PERIOD_LABELS = {1: 'Peak Boycott\n(Jan-Apr 2025)', 2: 'Resolution\n(Feb-Mar 2026)'}

COVENANT_LABELS = {0: 'Not Present', 1: 'Implicit', 2: 'Explicit'}

GEO_LABELS = {0: 'No Reference', 1: 'Minnesota/TC', 2: 'Other U.S.', 3: 'National'}


def load_data():
    """Load and prepare datasets."""
    print("Loading data...")
    df = pd.read_excel(DATA_FILE, sheet_name='TikTok_Coding')
    # Drop empty rows
    df = df.dropna(subset=['Video_ID'])
    print(f"  TikTok dataset: {len(df)} videos")

    corp = None
    if os.path.exists(CORP_FILE):
        corp = pd.read_excel(CORP_FILE)
        corp = corp.dropna(subset=['Date'])
        print(f"  Corporate dataset: {len(corp)} communications")

    return df, corp


def descriptive_stats(df):
    """Generate descriptive statistics."""
    print("\n" + "="*60)
    print("DESCRIPTIVE STATISTICS")
    print("="*60)

    # Sample overview
    n = len(df)
    print(f"\nTotal videos coded: {n}")
    print(f"\nBy collection period:")
    period_counts = df['Collection_Period'].value_counts().sort_index()
    for period, count in period_counts.items():
        label = 'Peak Boycott (Jan-Apr 2025)' if period == 1 else 'Resolution (Feb-Mar 2026)'
        print(f"  {label}: {count} ({count/n*100:.1f}%)")

    # Engagement metrics
    print(f"\nEngagement metrics:")
    for metric in ['View_Count', 'Like_Count', 'Comment_Count', 'Share_Count']:
        if metric in df.columns:
            col = pd.to_numeric(df[metric], errors='coerce')
            print(f"  {metric}: M={col.mean():,.0f}, Mdn={col.median():,.0f}, SD={col.std():,.0f}")

    print(f"\nDuration (seconds):")
    dur = pd.to_numeric(df['Duration_Sec'], errors='coerce')
    print(f"  M={dur.mean():.1f}, Mdn={dur.median():.1f}, SD={dur.std():.1f}")

    return period_counts


def frequency_tables(df):
    """Generate frequency tables for all categorical variables."""
    print("\n" + "="*60)
    print("FREQUENCY TABLES")
    print("="*60)

    results = {}
    variables = {
        'Creator_Type': CREATOR_LABELS,
        'Primary_Frame': FRAME_LABELS,
        'Emotional_Tone': TONE_LABELS,
        'Moral_Language': MORAL_LABELS,
        'Brand_Covenant': COVENANT_LABELS,
        'Community_ID': COMMUNITY_LABELS,
        'Geo_Reference': GEO_LABELS,
    }

    for var, labels in variables.items():
        if var not in df.columns:
            continue
        counts = df[var].value_counts().sort_index()
        n = counts.sum()
        print(f"\n{var}:")
        print(f"  {'Code':<6} {'Label':<30} {'n':>5} {'%':>7}")
        print(f"  {'-'*50}")
        for code, count in counts.items():
            label = labels.get(int(code), f'Code {code}') if pd.notna(code) else 'Missing'
            print(f"  {int(code) if pd.notna(code) else 'NA':<6} {label:<30} {count:>5} {count/n*100:>6.1f}%")
        results[var] = counts

    return results


def chi_square_tests(df):
    """Run chi-square tests for key relationships."""
    print("\n" + "="*60)
    print("CHI-SQUARE TESTS")
    print("="*60)

    tests = [
        ('Primary_Frame', 'Collection_Period', 'Framing x Period'),
        ('Emotional_Tone', 'Collection_Period', 'Tone x Period'),
        ('Moral_Language', 'Collection_Period', 'Moral Language x Period'),
        ('Brand_Covenant', 'Collection_Period', 'Brand Covenant x Period'),
        ('Community_ID', 'Collection_Period', 'Community Identity x Period'),
        ('Primary_Frame', 'Creator_Type', 'Framing x Creator Type'),
        ('Emotional_Tone', 'Primary_Frame', 'Tone x Framing'),
        ('Geo_Reference', 'Collection_Period', 'Geographic Reference x Period'),
        ('Primary_Frame', 'Geo_Reference', 'Framing x Geographic Reference'),
        ('Call_to_Action', 'Collection_Period', 'Call to Action x Period'),
    ]

    chi_results = []
    for var1, var2, label in tests:
        if var1 not in df.columns or var2 not in df.columns:
            continue
        ct = pd.crosstab(df[var1], df[var2])
        if ct.shape[0] < 2 or ct.shape[1] < 2:
            continue
        try:
            chi2, p, dof, expected = chi2_contingency(ct)
            n = ct.sum().sum()
            k = min(ct.shape)
            cramers_v = np.sqrt(chi2 / (n * (k - 1))) if n * (k - 1) > 0 else 0
            sig = '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else 'ns'

            print(f"\n{label}:")
            print(f"  chi2({dof}) = {chi2:.2f}, p = {p:.4f} {sig}")
            print(f"  Cramer's V = {cramers_v:.3f}")
            print(f"  N = {n}")

            # Check expected cell count warning
            pct_low = (expected < 5).sum() / expected.size * 100
            if pct_low > 20:
                print(f"  WARNING: {pct_low:.0f}% of expected counts < 5")

            chi_results.append({
                'Test': label,
                'chi2': chi2, 'df': dof, 'p': p,
                'Cramers_V': cramers_v, 'N': n, 'Sig': sig
            })
        except Exception as e:
            print(f"\n{label}: ERROR - {e}")

    return pd.DataFrame(chi_results)


def z_tests_proportions(df):
    """Run z-tests comparing frame proportions across periods."""
    print("\n" + "="*60)
    print("Z-TESTS FOR PROPORTIONS (Peak vs. Resolution)")
    print("="*60)

    peak = df[df['Collection_Period'] == 1]
    resolution = df[df['Collection_Period'] == 2]
    n1, n2 = len(peak), len(resolution)

    if n1 == 0 or n2 == 0:
        print("  Insufficient data for z-tests.")
        return pd.DataFrame()

    z_results = []
    for frame_code, frame_label in FRAME_LABELS.items():
        if frame_code == 99:
            continue
        p1 = (peak['Primary_Frame'] == frame_code).sum() / n1
        p2 = (resolution['Primary_Frame'] == frame_code).sum() / n2
        p_pool = ((peak['Primary_Frame'] == frame_code).sum() + (resolution['Primary_Frame'] == frame_code).sum()) / (n1 + n2)

        if p_pool == 0 or p_pool == 1:
            continue

        se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
        z = (p1 - p2) / se if se > 0 else 0
        p_val = 2 * (1 - stats.norm.cdf(abs(z)))
        sig = '***' if p_val < .001 else '**' if p_val < .01 else '*' if p_val < .05 else 'ns'

        print(f"\n  {frame_label}:")
        print(f"    Peak: {p1:.1%} ({(peak['Primary_Frame'] == frame_code).sum()}/{n1})")
        print(f"    Resolution: {p2:.1%} ({(resolution['Primary_Frame'] == frame_code).sum()}/{n2})")
        print(f"    z = {z:.2f}, p = {p_val:.4f} {sig}")

        z_results.append({
            'Frame': frame_label,
            'Peak_%': p1, 'Resolution_%': p2,
            'z': z, 'p': p_val, 'Sig': sig
        })

    return pd.DataFrame(z_results)


def generate_figures(df):
    """Generate publication-quality figures."""
    print("\n" + "="*60)
    print("GENERATING FIGURES")
    print("="*60)

    os.makedirs(FIGURE_DIR, exist_ok=True)
    colors = ['#1f4e79', '#2e75b6', '#4da3d4', '#7fc4e8', '#b3ddf0', '#d94f4f', '#e8a838', '#6ab04c']

    # Figure 1: Primary Frames Distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    frame_counts = df['Primary_Frame'].value_counts().sort_values(ascending=True)
    frame_labels_mapped = [FRAME_LABELS.get(int(x), f'Code {x}') for x in frame_counts.index]
    bars = ax.barh(frame_labels_mapped, frame_counts.values, color=colors[:len(frame_counts)])
    ax.set_xlabel('Number of Videos')
    ax.set_title('Distribution of Primary Frames in #BoycottTarget TikTok Videos')
    for bar, val in zip(bars, frame_counts.values):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{val} ({val/len(df)*100:.1f}%)', va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(f'{FIGURE_DIR}/fig1_primary_frames.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Saved fig1_primary_frames.png")

    # Figure 2: Frames by Collection Period (grouped bar)
    if df['Collection_Period'].nunique() > 1:
        fig, ax = plt.subplots(figsize=(12, 6))
        ct = pd.crosstab(df['Primary_Frame'], df['Collection_Period'], normalize='columns')
        ct.index = [FRAME_LABELS.get(int(x), f'Code {x}') for x in ct.index]
        ct.columns = [PERIOD_LABELS.get(int(x), f'Period {x}') for x in ct.columns]
        ct.plot(kind='bar', ax=ax, color=['#1f4e79', '#d94f4f'], width=0.7)
        ax.set_ylabel('Proportion')
        ax.set_title('Primary Frames by Boycott Period')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.legend(title='Period')
        plt.tight_layout()
        plt.savefig(f'{FIGURE_DIR}/fig2_frames_by_period.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Saved fig2_frames_by_period.png")

    # Figure 3: Emotional Tone Distribution
    fig, ax = plt.subplots(figsize=(8, 8))
    tone_counts = df['Emotional_Tone'].value_counts()
    tone_labels_mapped = [TONE_LABELS.get(int(x), f'Code {x}') for x in tone_counts.index]
    wedges, texts, autotexts = ax.pie(
        tone_counts.values, labels=tone_labels_mapped,
        autopct='%1.1f%%', colors=colors[:len(tone_counts)],
        textprops={'fontsize': 10}
    )
    ax.set_title('Emotional Tone Distribution')
    plt.tight_layout()
    plt.savefig(f'{FIGURE_DIR}/fig3_emotional_tone.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Saved fig3_emotional_tone.png")

    # Figure 4: Brand Covenant Framing by Period
    if df['Collection_Period'].nunique() > 1:
        fig, ax = plt.subplots(figsize=(8, 5))
        ct = pd.crosstab(df['Brand_Covenant'], df['Collection_Period'], normalize='columns')
        ct.index = [COVENANT_LABELS.get(int(x), f'Code {x}') for x in ct.index]
        ct.columns = [PERIOD_LABELS.get(int(x), f'Period {x}') for x in ct.columns]
        ct.plot(kind='bar', ax=ax, color=['#1f4e79', '#d94f4f'], width=0.6)
        ax.set_ylabel('Proportion')
        ax.set_title('Brand Covenant Framing by Boycott Period')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.legend(title='Period')
        plt.tight_layout()
        plt.savefig(f'{FIGURE_DIR}/fig4_brand_covenant.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Saved fig4_brand_covenant.png")

    # Figure 5: Moral Language Intensity by Period
    if df['Collection_Period'].nunique() > 1:
        fig, ax = plt.subplots(figsize=(8, 5))
        ct = pd.crosstab(df['Moral_Language'], df['Collection_Period'], normalize='columns')
        ct.index = [MORAL_LABELS.get(int(x), f'Code {x}') for x in ct.index]
        ct.columns = [PERIOD_LABELS.get(int(x), f'Period {x}') for x in ct.columns]
        ct.plot(kind='bar', ax=ax, color=['#1f4e79', '#d94f4f'], width=0.6)
        ax.set_ylabel('Proportion')
        ax.set_title('Moral Language Intensity by Boycott Period')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.legend(title='Period')
        plt.tight_layout()
        plt.savefig(f'{FIGURE_DIR}/fig5_moral_language.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Saved fig5_moral_language.png")

    # Figure 6: Geographic References
    fig, ax = plt.subplots(figsize=(8, 5))
    geo_counts = df['Geo_Reference'].value_counts().sort_index()
    geo_labels_mapped = [GEO_LABELS.get(int(x), f'Code {x}') for x in geo_counts.index]
    bars = ax.bar(geo_labels_mapped, geo_counts.values, color='#1f4e79')
    ax.set_ylabel('Number of Videos')
    ax.set_title('Geographic References in Boycott Videos')
    for bar, val in zip(bars, geo_counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                str(val), ha='center', fontsize=10)
    plt.tight_layout()
    plt.savefig(f'{FIGURE_DIR}/fig6_geographic.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Saved fig6_geographic.png")


def export_results(df, chi_results, z_results, freq_results):
    """Export all results to Excel."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = f'{OUTPUT_DIR}/analysis_results.xlsx'

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Descriptive stats
        desc = df[['View_Count', 'Like_Count', 'Comment_Count', 'Share_Count', 'Duration_Sec']].describe()
        desc.to_excel(writer, sheet_name='Descriptive_Stats')

        # Frequency tables
        for var, counts in freq_results.items():
            counts_df = counts.reset_index()
            counts_df.columns = ['Code', 'Count']
            counts_df['Percent'] = counts_df['Count'] / counts_df['Count'].sum() * 100
            counts_df.to_excel(writer, sheet_name=f'Freq_{var[:20]}', index=False)

        # Chi-square results
        if not chi_results.empty:
            chi_results.to_excel(writer, sheet_name='Chi_Square_Tests', index=False)

        # Z-test results
        if not z_results.empty:
            z_results.to_excel(writer, sheet_name='Z_Tests_Proportions', index=False)

        # Crosstabs
        for var1, var2, label in [
            ('Primary_Frame', 'Collection_Period', 'Frame_x_Period'),
            ('Emotional_Tone', 'Collection_Period', 'Tone_x_Period'),
            ('Brand_Covenant', 'Collection_Period', 'Covenant_x_Period'),
        ]:
            if var1 in df.columns and var2 in df.columns:
                ct = pd.crosstab(df[var1], df[var2], margins=True)
                ct.to_excel(writer, sheet_name=f'CT_{label[:25]}')

    print(f"\n  Results exported to {output_file}")


def intercoder_reliability(df):
    """Calculate intercoder reliability if Coder2 data exists."""
    print("\n" + "="*60)
    print("INTERCODER RELIABILITY")
    print("="*60)

    try:
        import krippendorff
    except ImportError:
        print("  Install krippendorff: pip install krippendorff")
        return

    # Check for dual-coded data
    coder_names = df['Coder_Name'].unique()
    if len(coder_names) < 2:
        print("  Only one coder found. Skipping reliability analysis.")
        print("  For ICR: have a second coder code the same videos,")
        print("  then add their data with a different Coder_Name value.")
        return

    # Find overlapping videos
    video_ids = df.groupby('Video_ID')['Coder_Name'].nunique()
    dual_coded = video_ids[video_ids >= 2].index
    print(f"  Dual-coded videos: {len(dual_coded)}")

    reliability_vars = ['Primary_Frame', 'Emotional_Tone', 'Moral_Language',
                        'Brand_Covenant', 'Creator_Type', 'Community_ID', 'Geo_Reference']

    for var in reliability_vars:
        if var not in df.columns:
            continue
        subset = df[df['Video_ID'].isin(dual_coded)][['Video_ID', 'Coder_Name', var]]
        pivot = subset.pivot(index='Video_ID', columns='Coder_Name', values=var)
        if pivot.shape[1] < 2:
            continue
        data = pivot.values.T.astype(float)
        alpha = krippendorff.alpha(reliability_data=data, level_of_measurement='nominal')
        status = 'GOOD' if alpha >= .80 else 'ACCEPTABLE' if alpha >= .667 else 'LOW'
        print(f"  {var}: alpha = {alpha:.3f} [{status}]")


def main():
    """Run full analysis pipeline."""
    print("="*60)
    print("TARGET DEI BOYCOTT — TIKTOK CONTENT ANALYSIS")
    print("="*60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(FIGURE_DIR, exist_ok=True)

    df, corp = load_data()

    # Core analyses
    descriptive_stats(df)
    freq_results = frequency_tables(df)
    chi_results = chi_square_tests(df)
    z_results = z_tests_proportions(df)

    # Figures
    generate_figures(df)

    # Export
    export_results(df, chi_results, z_results, freq_results)

    # ICR
    intercoder_reliability(df)

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)


if __name__ == '__main__':
    main()
