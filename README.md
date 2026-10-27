# B2B Sales Velocity & Quota Performance Dashboard

An executive revenue operations (RevOps) analytics engine designed to measure deal stage progression, eliminate sales cycle friction, and compute mathematical sales pipeline velocity.

## Overview
Evaluating B2B enterprise sales teams solely on closed revenue fails to capture early pipeline health and conversion bottlenecks. This engine tracks granular CRM deal lifecycle stages, calculates pipeline velocity, and audits sales representative quota attainment to forecast revenue predictability.

## Project Structure
- `sales_pipeline_velocity.sql`: Production SQL CTE pipeline calculating stage conversion ratios, deal cycle duration, stalled pipeline volume, and rep pacing.
- `sales_velocity_engine.py`: Python engine processing 5,000+ opportunity records to compute the classical Sales Velocity equation ($V = \frac{N \times W \times ACV}{T}$) and quota distributions.
- `requirements.txt`: Python package dependencies.

## Key Revenue Metrics
1. **Sales Velocity Formula:**
   $$V = \frac{\text{Opportunities} \times \text{Win Rate} \times \text{Average Deal Size (ACV)}}{\text{Sales Cycle Length (Days)}}$$
   Directly quantifies the daily dollar amount moving through the pipeline.
2. **Pipeline Friction Points:** Isolates stage conversion drop-offs (e.g., Proposal to Negotiation) where deals stall or slip beyond the 60-day threshold.
3. **Quota Pacing Tiers:** Categorizes sales representatives into attainment buckets against quarterly revenue benchmarks.

## How to Run

```bash
# Clone the repository
git clone [https://github.com/puneetgoswami1/b2b-sales-velocity-quota-engine.git](https://github.com/puneetgoswami1/b2b-sales-velocity-quota-engine.git)
cd b2b-sales-velocity-quota-engine

# Install dependencies
pip install -r requirements.txt

# Run sales velocity engine
python sales_velocity_engine.py