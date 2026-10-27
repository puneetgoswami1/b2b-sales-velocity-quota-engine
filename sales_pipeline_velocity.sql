-- =====================================================================
-- B2B REVENUE PIPELINE VELOCITY & REP QUOTA ATTAINMENT
-- Author: Puneet Goswami
-- Description: Measures stage conversion rates, sales cycle duration,
--              stalled deal slippage, and individual rep quota pacing.
-- =====================================================================

WITH opportunity_lifecycle AS (
    SELECT 
        deal_id,
        account_name,
        sales_rep_id,
        territory,
        deal_amount_usd,
        created_at,
        closed_at,
        current_stage, -- 'Discovery', 'Demo', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost'
        is_won,
        
        -- Sales cycle duration in days
        DATEDIFF('day', created_at, COALESCE(closed_at, CURRENT_DATE)) AS sales_cycle_days,
        
        -- Deal age indicator for pipeline hygiene
        CASE 
            WHEN closed_at IS NULL AND DATEDIFF('day', created_at, CURRENT_DATE) > 90 THEN 'STALLED_DEAL_SLIPPAGE'
            WHEN closed_at IS NULL AND DATEDIFF('day', created_at, CURRENT_DATE) > 60 THEN 'AGING_PIPELINE'
            ELSE 'HEALTHY_ACTIVE'
        END AS deal_health_status
    FROM revops_dw.fct_crm_opportunities
    WHERE created_at >= CURRENT_DATE - INTERVAL '180 DAYS'
),

rep_pipeline_aggregates AS (
    SELECT 
        sales_rep_id,
        territory,
        COUNT(deal_id) AS total_opportunities_created,
        COUNT(CASE WHEN current_stage IN ('Closed Won', 'Closed Lost') THEN deal_id END) AS total_closed_opportunities,
        SUM(CASE WHEN is_won = 1 THEN 1 ELSE 0 END) AS won_deals_count,
        ROUND(SUM(CASE WHEN is_won = 1 THEN deal_amount_usd ELSE 0 END), 2) AS total_closed_won_revenue_usd,
        ROUND(AVG(CASE WHEN is_won = 1 THEN deal_amount_usd END), 2) AS avg_deal_size_acv_usd,
        ROUND(AVG(CASE WHEN is_won = 1 THEN sales_cycle_days END), 1) AS avg_won_cycle_length_days,
        SUM(CASE WHEN deal_health_status = 'STALLED_DEAL_SLIPPAGE' THEN deal_amount_usd ELSE 0 END) AS stalled_pipeline_usd
    FROM opportunity_lifecycle
    GROUP BY sales_rep_id, territory
),

rep_quota_performance AS (
    SELECT 
        r.sales_rep_id,
        rep.rep_name,
        r.territory,
        rep.quarterly_quota_usd,
        r.total_opportunities_created,
        r.won_deals_count,
        r.total_closed_won_revenue_usd,
        r.avg_deal_size_acv_usd,
        r.avg_won_cycle_length_days,
        r.stalled_pipeline_usd,
        
        -- Win Rate percentage
        ROUND((r.won_deals_count * 100.0) / NULLIF(r.total_closed_opportunities, 0), 2) AS win_rate_pct,
        
        -- Quota Attainment percentage
        ROUND((r.total_closed_won_revenue_usd * 100.0) / NULLIF(rep.quarterly_quota_usd, 0), 2) AS quota_attainment_pct,

        -- Sales Velocity Equation: (Opps * WinRate * ACV) / Cycle Length
        ROUND(
            (r.total_opportunities_created * 
            ((r.won_deals_count * 1.0) / NULLIF(r.total_closed_opportunities, 0)) * 
            COALESCE(r.avg_deal_size_acv_usd, 0)) / 
            NULLIF(r.avg_won_cycle_length_days, 0)
        , 2) AS daily_pipeline_velocity_usd
    FROM rep_pipeline_aggregates r
    JOIN revops_dw.dim_sales_reps rep ON r.sales_rep_id = rep.rep_id
)

SELECT 
    rep_name,
    territory,
    quarterly_quota_usd,
    total_closed_won_revenue_usd,
    quota_attainment_pct,
    win_rate_pct,
    avg_deal_size_acv_usd,
    avg_won_cycle_length_days,
    daily_pipeline_velocity_usd,
    stalled_pipeline_usd,
    
    -- Performance Ranking
    CASE 
        WHEN quota_attainment_pct >= 100.0 THEN 'QUOTA_ACHIEVED_PRESIDENT_CLUB'
        WHEN quota_attainment_pct >= 80.0 THEN 'ON_PACING'
        ELSE 'NEEDS_COACHING_UNDERPERFORMING'
    END AS rep_pacing_tier
FROM rep_quota_performance
ORDER BY daily_pipeline_velocity_usd DESC;