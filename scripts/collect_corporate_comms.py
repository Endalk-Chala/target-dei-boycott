#!/usr/bin/env python3
"""
Corporate Communications Data Collector
Target DEI Boycott Study

This script compiles known Target corporate communications related to the
DEI rollback and boycott. It creates a structured dataset for coding.

Run this to generate the initial corporate communications dataset,
then manually verify and add any missing items.

Author: Endalkachew H. Chala, PhD
Date: April 2026

Requirements: pip install pandas openpyxl
"""

import pandas as pd
from datetime import datetime

# ══════════════════════════════════════════════════════════════
# KNOWN TARGET CORPORATE COMMUNICATIONS
# ══════════════════════════════════════════════════════════════
# These are documented communications from news coverage.
# Sources should be verified and URLs updated during data collection.

communications = [
    {
        'Unit_ID': 1,
        'Date': '2025-01-24',
        'Comm_Type': 1,  # Press Release
        'Spokesperson': 2,  # Kiera Fernandez
        'Source_URL': '',  # Add actual URL
        'Title_Summary': 'Target announces end of DEI initiatives including REACH strategy, '
                         'racial equity commitments, and HRC Corporate Equality Index participation. '
                         'Rebrands Supplier Diversity to Supplier Engagement.',
        'DEI_Framing': 0,  # Not coded yet
        'Boycott_Ack': 0,
        'Community_Stance': 0,
        'Key_Language': '',
        'Coder_Notes': 'CEO Brian Cornell notably absent from announcement. '
                       'Kiera Fernandez (Chief Community Impact & Equity Officer) delivered the news.',
    },
    {
        'Unit_ID': 2,
        'Date': '2025-02-04',
        'Comm_Type': 3,  # Social Media
        'Spokesperson': 5,  # Social Media Team
        'Source_URL': '',
        'Title_Summary': 'Target social media posts during Black History Month — check for '
                         'any BHM-related content and community response in comments.',
        'DEI_Framing': 0,
        'Boycott_Ack': 0,
        'Community_Stance': 0,
        'Key_Language': '',
        'Coder_Notes': 'Context: Boycott launched during Black History Month. '
                       'Top comments on Target Instagram/TikTok/Facebook dominated by boycott supporters.',
    },
    {
        'Unit_ID': 3,
        'Date': '2025-03-05',
        'Comm_Type': 2,  # Earnings Call
        'Spokesperson': 1,  # CEO Brian Cornell
        'Source_URL': '',  # Add earnings call transcript URL
        'Title_Summary': 'Q4 2024 / FY2024 Earnings Call. Reported by Retail Brew as '
                         '"ignoring DEI backlash and boycott." Check transcript for any '
                         'references to community response.',
        'DEI_Framing': 0,
        'Boycott_Ack': 0,
        'Community_Stance': 0,
        'Key_Language': '',
        'Coder_Notes': 'Key question: Did Cornell or any executive address the boycott '
                       'during Q&A? Check analyst questions as well.',
    },
    {
        'Unit_ID': 4,
        'Date': '2025-04-21',
        'Comm_Type': 1,
        'Spokesperson': 4,  # Corporate spokesperson
        'Source_URL': '',
        'Title_Summary': 'Target response to CNN reporting on foot traffic decline and '
                         'boycott impact on minority-owned businesses in stores.',
        'DEI_Framing': 0,
        'Boycott_Ack': 0,
        'Community_Stance': 0,
        'Key_Language': '',
        'Coder_Notes': 'CNN reported traffic dropped after DEI announcement. '
                       'Check for Target statement/response in the article.',
    },
    {
        'Unit_ID': 5,
        'Date': '2025-08-27',
        'Comm_Type': 1,
        'Spokesperson': 4,
        'Source_URL': '',
        'Title_Summary': 'Target response to continued boycott under new CEO (if leadership change occurred). '
                         'Fortune reported boycott organizers said "leadership change doesn\'t mean anything '
                         'without a culture change."',
        'DEI_Framing': 0,
        'Boycott_Ack': 0,
        'Community_Stance': 0,
        'Key_Language': '',
        'Coder_Notes': 'Check if CEO change occurred by this date and how it was framed.',
    },
    {
        'Unit_ID': 6,
        'Date': '2025-10-24',
        'Comm_Type': 1,
        'Spokesperson': 4,
        'Source_URL': '',
        'Title_Summary': 'Target spotlights support for Black founders — Fortune reports Target '
                         'highlighting Black-founded brands after sustained DEI backlash and '
                         'stock selloff.',
        'DEI_Framing': 0,
        'Boycott_Ack': 0,
        'Community_Stance': 0,
        'Key_Language': '',
        'Coder_Notes': 'Potential shift toward conciliatory/restorative stance. '
                       'Compare framing to January 2025 announcement.',
    },
    {
        'Unit_ID': 7,
        'Date': '2026-03-11',
        'Comm_Type': 1,
        'Spokesperson': 4,
        'Source_URL': '',
        'Title_Summary': 'Target response to boycott ending. Axios reported Target said '
                         '"no policies were reversed or reinstated as a result of conversations '
                         'with its leadership."',
        'DEI_Framing': 0,
        'Boycott_Ack': 0,
        'Community_Stance': 0,
        'Key_Language': '',
        'Coder_Notes': 'Critical communication: Target explicitly states no policy changes. '
                       'Analyze tone and framing carefully.',
    },
]

# ══════════════════════════════════════════════════════════════
# ADDITIONAL SOURCES TO COLLECT
# ══════════════════════════════════════════════════════════════

print("="*60)
print("CORPORATE COMMUNICATIONS DATA COLLECTION GUIDE")
print("="*60)

print("""
STEP 1: Verify and complete the pre-populated entries below.
        Each entry needs:
        - Actual Source_URL
        - Key_Language (direct quotes from Target)
        - Coding on all variables (DEI_Framing, Boycott_Ack, Community_Stance)

STEP 2: Search for additional Target communications:
        - Target corporate website (corporate.target.com) press releases
        - Target Pressroom blog posts
        - Target official social media accounts (Instagram, TikTok, Facebook, X)
        - Earnings call transcripts (Q4 2024, Q1-Q3 2025, Q4 2025)
        - Any CEO statements or executive interviews
        - Target website changes (DEI page modifications, Supplier Diversity page)

STEP 3: For each new communication found, add a row to the spreadsheet.

SEARCH QUERIES TO USE:
  - site:corporate.target.com DEI diversity equity
  - Target "official statement" DEI rollback 2025
  - Target earnings call transcript 2025 DEI
  - Brian Cornell Target diversity statement
  - Target press release Black-owned suppliers 2025
  - Target corporate response boycott 2025
""")

# Create DataFrame and save
df = pd.DataFrame(communications)
df['Date'] = pd.to_datetime(df['Date'])

output = 'data/corporate_comms_raw.xlsx'

import os
os.makedirs('data', exist_ok=True)

df.to_excel(output, index=False)
print(f"\nSaved {len(df)} pre-populated entries to: {output}")
print(f"Open this file, verify URLs, add missing communications, then code all variables.")
print(f"\nAfter coding, save as: data/corporate_comms_coded.xlsx")
