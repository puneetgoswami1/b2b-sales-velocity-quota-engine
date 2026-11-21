# B2B Sales Velocity & Quota Pacing Analytics

A revenue operations (RevOps) pipeline that measures deal stage conversion, flags stalled opportunities, and calculates pipeline velocity across sales reps.

## Problem Context
Looking only at closed-won revenue hides early-stage bottlenecks until late in the quarter. This repository tracks stage-to-stage drop-offs, deal cycle duration, and rep quota attainment to catch pipeline slowdowns early.

## Files
- `sales_pipeline_velocity.sql`: SQL CTE pipeline calculating stage conversion rates, cycle times, stalled deals (>60 days), and rep quota pacing.
- `sales_velocity_engine.py`: Processes 5,000+ CRM opportunity records to compute daily pipeline velocity and attainment tiers.
- `requirements.txt`: Python dependencies.

## How It Works
1. **Pipeline Velocity:** Combines qualified opportunity count, win rate, average contract value (ACV), and average cycle length into daily dollar velocity.
2. **Stage Bottlenecks:** Isolates drop-offs between Proposal and Negotiation where deals stall past 60 days.
3. **Quota Distribution:** Segments reps into pacing tiers against quarterly targets.

## Run Locally

    git clone https://github.com/puneetgoswami1/b2b-sales-velocity-quota-engine.git
    cd b2b-sales-velocity-quota-engine
    pip install -r requirements.txt
    python sales_velocity_engine.py
