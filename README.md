# Brand Covenant Broken: Digital Activism, Corporate Communication, and Community Accountability in the Target DEI Boycott

**Author:** Endalkachew H. Chala, PhD

**Status:** Data collection phase

## Study Overview

A mixed-methods case study examining how Target's January 2025 DEI rollback triggered a platform-mediated community response on TikTok, and what this reveals about corporate brand responsibility, digital counterpublics, and community accountability in a polarized environment. The study foregrounds the Minnesota context — Target's headquarters in Minneapolis and the local organizing that shaped the boycott.

## Repository Structure

```
target-dei-boycott/
├── README.md
├── codebook/
│   ├── Target_DEI_Boycott_Codebook.docx    # Full codebook with variable definitions
│   └── Target_DEI_Boycott_Coding_Sheet.xlsx # Excel template (3 sheets: TikTok, Corporate, Code Reference)
├── data/
│   ├── tiktok_coded_data.xlsx               # Coded TikTok dataset (after collection)
│   ├── corporate_comms_raw.xlsx             # Pre-populated corporate communications
│   └── corporate_comms_coded.xlsx           # Coded corporate dataset (after collection)
├── analysis/
│   ├── target_dei_analysis.py               # Main analysis script (descriptive, chi-square, z-tests, figures)
│   ├── results/                             # Analysis output (auto-generated)
│   │   └── analysis_results.xlsx
│   └── figures/                             # Publication-quality figures (auto-generated)
│       ├── fig1_primary_frames.png
│       ├── fig2_frames_by_period.png
│       ├── fig3_emotional_tone.png
│       ├── fig4_brand_covenant.png
│       ├── fig5_moral_language.png
│       └── fig6_geographic.png
├── scripts/
│   └── collect_corporate_comms.py           # Corporate communications collector
└── paper/
    └── manuscript.docx                      # Paper manuscript (after analysis)
```

## Method

### TikTok Content Analysis
- **Sample:** 250-300 TikTok videos from #BoycottTarget, #TargetBoycott, #TargetFailsDEI
- **Periods:** Peak Boycott (Jan-Apr 2025) and Resolution (Feb-Mar 2026)
- **Variables:** 24 coded variables across 5 categories (identification, creator, framing, action, platform)
- **Key variables:** Primary frame, brand covenant framing, moral language intensity, geographic reference, community identity construction

### Corporate Communications Analysis
- **Sample:** All identifiable Target official communications regarding the DEI rollback
- **Sources:** Press releases, earnings calls, social media, executive statements
- **Variables:** Communication type, spokesperson, DEI framing, boycott acknowledgment, community engagement stance

### Analysis
- Descriptive statistics and frequency distributions
- Chi-square tests for independence (framing x period, framing x creator type, etc.)
- Z-tests for proportions comparing peak vs. resolution periods
- Cramer's V for effect sizes
- Intercoder reliability: Krippendorff's alpha (target: alpha >= .80)

## Requirements

```bash
pip install pandas scipy matplotlib seaborn openpyxl krippendorff
```

## Running the Analysis

```bash
# After data collection and coding is complete:
python analysis/target_dei_analysis.py
```

## Data Collection Workflow

1. **TikTok data:** Search hashtags on TikTok, record video metadata in coding sheet, watch and code each video
2. **Corporate data:** Run `scripts/collect_corporate_comms.py` to generate starter dataset, then verify and expand
3. **Intercoder reliability:** Have second coder independently code 10%+ of sample
4. **Analysis:** Run `target_dei_analysis.py` after coding is complete

## Timeline

| Phase | Target Date |
|-------|-------------|
| Data collection begins | April 13, 2026 |
| TikTok coding complete | May 4, 2026 |
| Corporate coding complete | May 4, 2026 |
| ICR testing | May 7, 2026 |
| Analysis | May 10, 2026 |
| Draft manuscript | May 25, 2026 |
| Submit to journal | June 2026 |

## License

This research data and code are shared for academic purposes.

## Contact

Endalkachew H. Chala, PhD
endalk2006@gmail.com
