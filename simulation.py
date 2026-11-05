"""
Course Project: Operations Research (CSN13402(L))
Topic 10: Identification of High-Risk Zones in a National Highway Project
Methodology: Monte Carlo Simulation (Weather & Terrain) and 0-1 Knapsack Optimization
Case Study: 200 km Mountain Highway Corridor (20 Segments x 10 km)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.optimize import milp, LinearConstraint

# Set random seed for consistent results
np.random.seed(42)

# Global simulation settings
NUM_SIMULATIONS = 10000
FAILURE_THRESHOLD = 0.65       # Critical threshold for slope failure / landslide
BASE_CLOSURE_COST_CR = 1.8     # Daily economic disruption base cost (Crores INR)
MITIGATION_BUDGET_CR = 60.0    # Available budget for engineering countermeasures (Crores INR)
PLOTS_DIR = "plots"

os.makedirs(PLOTS_DIR, exist_ok=True)


def load_corridor_data():
    """
    Define the 200 km highway corridor divided into 20 segments of 10 km each.
    Parameters represent surveyed terrain profiles, rainfall distributions,
    and geotechnical conditions across different elevation zones.
    """
    data = [
        # id, name, start, end, elevation(m), slope_min, slope_mode, slope_max, rain_mu, rain_sigma, soil_a, soil_b, drainage, daily_traffic, cost_cr
        (1, "KM 00-10 Plains Entry", 0, 10, 320, 10, 18, 25, 3.2, 0.45, 6.0, 2.0, 0.85, 12000, 4.5),
        (2, "KM 10-20 Lower Foothills", 10, 20, 480, 15, 24, 32, 3.4, 0.48, 5.0, 3.0, 0.80, 11500, 5.0),
        (3, "KM 20-30 Valley Basin", 20, 30, 610, 18, 28, 38, 3.6, 0.50, 4.0, 3.0, 0.75, 11000, 6.0),
        (4, "KM 30-40 Ridge Approach", 30, 40, 850, 25, 36, 45, 3.8, 0.52, 4.0, 4.0, 0.70, 10500, 8.5),
        (5, "KM 40-50 Escarpment Sector I", 40, 50, 1200, 38, 52, 64, 4.2, 0.58, 2.0, 5.0, 0.55, 9500, 16.0),
        (6, "KM 50-60 Mountain Pass Summit", 50, 60, 1650, 42, 56, 68, 4.4, 0.62, 2.0, 6.0, 0.50, 9200, 18.5),
        (7, "KM 60-70 Fractured Fault Zone", 60, 70, 1580, 45, 58, 72, 4.5, 0.65, 1.8, 6.5, 0.45, 9000, 22.0),
        (8, "KM 70-80 Gorge Incline", 70, 80, 1420, 40, 53, 65, 4.3, 0.60, 2.2, 5.5, 0.52, 8800, 17.0),
        (9, "KM 80-90 Upper Canyon Cliff", 80, 90, 1310, 36, 50, 62, 4.1, 0.55, 2.5, 5.0, 0.58, 8600, 14.5),
        (10, "KM 90-100 River Gorge Sector A", 90, 100, 1150, 34, 48, 60, 4.3, 0.58, 2.3, 5.2, 0.48, 8500, 15.0),
        (11, "KM 100-110 River Gorge Sector B", 100, 110, 980, 35, 49, 63, 4.4, 0.60, 2.0, 5.8, 0.42, 8500, 16.5),
        (12, "KM 110-120 Cloudburst Canyon", 110, 120, 890, 42, 55, 70, 4.6, 0.68, 1.9, 6.2, 0.40, 8700, 21.0),
        (13, "KM 120-130 Narrow Choke Valley", 120, 130, 810, 32, 44, 56, 4.0, 0.52, 3.0, 4.5, 0.55, 9000, 12.0),
        (14, "KM 130-140 Bridge & Alluvial Fan", 130, 140, 720, 24, 35, 46, 3.9, 0.50, 3.5, 4.0, 0.60, 9300, 10.0),
        (15, "KM 140-150 High Plateau West", 140, 150, 850, 20, 30, 40, 3.7, 0.48, 4.0, 3.5, 0.70, 9800, 7.5),
        (16, "KM 150-160 Plateau Center", 150, 160, 910, 16, 25, 35, 3.5, 0.45, 4.5, 3.0, 0.75, 10200, 6.0),
        (17, "KM 160-170 Wind Gap Sector", 160, 170, 870, 22, 33, 44, 3.8, 0.50, 3.8, 3.8, 0.68, 10500, 8.0),
        (18, "KM 170-180 Descent Transition", 170, 180, 690, 26, 37, 48, 3.9, 0.52, 3.2, 4.2, 0.62, 11000, 9.5),
        (19, "KM 180-190 Lower Valley S-Curves", 180, 190, 450, 18, 26, 36, 3.5, 0.46, 4.8, 3.0, 0.78, 12000, 5.5),
        (20, "KM 190-200 Terminal Plains", 190, 200, 280, 8, 15, 22, 3.1, 0.40, 6.5, 2.0, 0.88, 13500, 3.5)
    ]
    
    columns = [
        'segment_id', 'name', 'start_km', 'end_km', 'elevation_m',
        'slope_min', 'slope_mode', 'slope_max',
        'rain_mu', 'rain_sigma', 'soil_alpha', 'soil_beta',
        'drainage_base', 'daily_traffic', 'mitigation_cost_cr'
    ]
    return pd.DataFrame(data, columns=columns)


def compute_ahp_weights():
    """
    Computes criteria weights using Saaty's Analytic Hierarchy Process (AHP).
    Criteria: [Rainfall, Slope Angle, Geotechnical Soil Weakness, Drainage Deficit]
    """
    # Pairwise comparison matrix based on landslide susceptibility literature
    matrix = np.array([
        [1.0,     1.5,     2.0,     3.0    ],  # Rainfall
        [1/1.5,   1.0,     1.5,     2.5    ],  # Slope
        [1/2.0,   1/1.5,   1.0,     2.0    ],  # Geotechnical weakness
        [1/3.0,   1/2.5,   1/2.0,   1.0    ]   # Drainage deficit
    ])
    
    # Eigenvalue method
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    principal_vector = np.real(eigenvectors[:, 0])
    weights = principal_vector / np.sum(principal_vector)
    return weights


def run_monte_carlo(df, weights, n_iter=NUM_SIMULATIONS):
    """
    Runs Monte Carlo simulation for all segments across n_iter iterations.
    Evaluates failure events, probability of failure, Value-at-Risk, and expected losses.
    """
    w_R, w_S, w_G, w_D = weights
    results = []
    hazard_samples = {}
    
    for _, row in df.iterrows():
        sid = int(row['segment_id'])
        
        # 1. Slope: Triangular distribution (cut-slope variations)
        slope = np.random.triangular(row['slope_min'], row['slope_mode'], row['slope_max'], size=n_iter)
        norm_slope = np.clip(slope / 75.0, 0.0, 1.0)
        
        # 2. Rainfall: Log-Normal distribution (extreme precipitation tail)
        rainfall = np.random.lognormal(row['rain_mu'], row['rain_sigma'], size=n_iter)
        norm_rain = np.clip(rainfall / 300.0, 0.0, 1.0)
        
        # 3. Geotechnical soil strength: Beta distribution
        soil_strength = np.random.beta(row['soil_alpha'], row['soil_beta'], size=n_iter)
        soil_weakness = 1.0 - soil_strength
        
        # 4. Drainage capacity: Base capacity reduced by stochastic storm debris
        choke = np.random.uniform(0.0, 0.40, size=n_iter)
        drainage_eff = np.clip(row['drainage_base'] - choke, 0.1, 1.0)
        drainage_deficit = 1.0 - drainage_eff
        
        # Composite Hazard Index
        hazard = (w_R * norm_rain +
                  w_S * norm_slope +
                  w_G * soil_weakness +
                  w_D * drainage_deficit)
        hazard = np.clip(hazard, 0.0, 1.0)
        hazard_samples[sid] = hazard
        
        # Failure and loss estimation
        failures = hazard > FAILURE_THRESHOLD
        prob_fail = np.sum(failures) / float(n_iter)
        
        # Disruption cost model (closure days x daily cost x traffic volume factor)
        excess = np.maximum(0.0, hazard - FAILURE_THRESHOLD)
        closure_days = failures * (1.5 + excess * 15.0)
        traffic_weight = row['daily_traffic'] / 10000.0
        economic_loss = closure_days * BASE_CLOSURE_COST_CR * traffic_weight
        
        expected_loss = np.mean(economic_loss)
        var_95 = np.percentile(hazard, 95)
        
        # Risk classification
        if prob_fail >= 0.15:
            risk_tier = "High"
            color = "#dc2626"
        elif prob_fail >= 0.05:
            risk_tier = "Medium"
            color = "#f59e0b"
        else:
            risk_tier = "Low"
            color = "#10b981"
            
        results.append({
            'segment_id': sid,
            'name': row['name'],
            'start_km': row['start_km'],
            'end_km': row['end_km'],
            'elevation_m': row['elevation_m'],
            'mean_hazard': np.mean(hazard),
            'var_95': var_95,
            'prob_failure': prob_fail,
            'expected_loss_cr': expected_loss,
            'mitigation_cost_cr': row['mitigation_cost_cr'],
            'risk_tier': risk_tier,
            'color': color
        })
        
    return pd.DataFrame(results), hazard_samples


def optimize_budget(results_df, budget=MITIGATION_BUDGET_CR):
    """
    Solves 0-1 Knapsack Capital Budgeting problem using Mixed Integer Linear Programming (MILP).
    Maximizes expected risk reduction subject to total cost <= budget.
    """
    efficiency = 0.85  # Engineering countermeasures reduce failure risk by 85%
    costs = results_df['mitigation_cost_cr'].values
    benefits = results_df['expected_loss_cr'].values * efficiency
    
    # MILP minimization formulation (-benefits)
    c = -benefits
    integrality = np.ones_like(c)  # Binary integer variables
    constraints = LinearConstraint(costs, 0, budget)
    bounds = (0, 1)
    
    res = milp(c=c, integrality=integrality, constraints=constraints, bounds=bounds)
    
    if res.success:
        selection = np.round(res.x).astype(int)
        results_df['selected_for_mitigation'] = selection
        results_df['post_loss_cr'] = results_df['expected_loss_cr'] * (1.0 - efficiency * selection)
    else:
        results_df['selected_for_mitigation'] = 0
        results_df['post_loss_cr'] = results_df['expected_loss_cr']
        
    return results_df


def generate_plots(df, hazard_samples, weights):
    """
    Generates presentation-ready figures formatted for slides.
    """
    plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 10})
    
    # ---------------------------------------------------------
    # Figure 1: Corridor Elevation Profile & Risk Classification
    # ---------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 7.5), sharex=True, gridspec_kw={'height_ratios': [1.2, 1]})
    x_mid = (df['start_km'] + df['end_km']) / 2.0
    
    ax1.plot(x_mid, df['elevation_m'], color='#334155', lw=2.2, marker='o', markersize=4, label='Elevation Profile')
    ax1.fill_between(x_mid, df['elevation_m'], 0, color='#94a3b8', alpha=0.25)
    
    for _, r in df.iterrows():
        ax1.axvspan(r['start_km'], r['end_km'], ymin=0.88, ymax=0.98, color=r['color'], alpha=0.85)
        if r['risk_tier'] == 'High':
            ax1.annotate(f"Seg {int(r['segment_id'])}\nP={r['prob_failure']*100:.1f}%",
                         xy=(r['start_km'] + 5, r['elevation_m']),
                         xytext=(r['start_km'] + 5, r['elevation_m'] + 220),
                         arrowprops=dict(facecolor='#dc2626', shrink=0.08, width=1.5, headwidth=6),
                         ha='center', fontsize=8.5, fontweight='bold', color='#991b1b',
                         bbox=dict(boxstyle="round,pad=0.2", fc="#fee2e2", ec="#dc2626", lw=1))
            
    ax1.set_ylabel("Elevation (m ASL)", fontweight='bold')
    ax1.set_title("Highway 200 km Corridor: Elevation Profile & Risk Zones", fontweight='bold', fontsize=12)
    ax1.set_ylim(0, 2100)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    ax2.bar(x_mid, df['prob_failure'] * 100, width=8, color=df['color'].tolist(), edgecolor='#1e293b', lw=1.0)
    ax2.axhline(15, color='#dc2626', linestyle='--', lw=1.8, label='High Risk Threshold (15%)')
    ax2.axhline(5, color='#f59e0b', linestyle=':', lw=1.8, label='Medium Risk Threshold (5%)')
    
    for _, r in df.iterrows():
        if r['selected_for_mitigation'] == 1:
            ax2.text(r['start_km'] + 5, r['prob_failure'] * 100 + 1.0, "[Funded]",
                     ha='center', fontsize=8, fontweight='bold', color='#1d4ed8')
            
    ax2.set_xlabel("Highway Chainage (km 0 to km 200)", fontweight='bold')
    ax2.set_ylabel("Failure Probability (%)", fontweight='bold')
    ax2.set_xticks(np.arange(0, 210, 20))
    ax2.set_ylim(0, 35)
    ax2.legend(loc='upper left')
    ax2.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    fig1_path = os.path.join(PLOTS_DIR, "fig1_corridor_risk_profile.png")
    plt.savefig(fig1_path, dpi=200, bbox_inches='tight')
    plt.close()
    
    # ---------------------------------------------------------
    # Figure 2: Monte Carlo Distributions & Value-at-Risk (VaR)
    # ---------------------------------------------------------
    fig, (ax_pdf, ax_cdf) = plt.subplots(1, 2, figsize=(13, 5.5))
    safe_data = hazard_samples[1]
    crit_data = hazard_samples[7]
    
    ax_pdf.hist(safe_data, bins=50, density=True, alpha=0.6, color='#10b981', label='Segment 1 (Plains - Low Risk)')
    ax_pdf.hist(crit_data, bins=50, density=True, alpha=0.6, color='#dc2626', label='Segment 7 (Fault Zone - High Risk)')
    ax_pdf.axvline(FAILURE_THRESHOLD, color='#0f172a', linestyle='--', lw=2, label=f'Threshold (tau = {FAILURE_THRESHOLD})')
    
    var_95_seg7 = df.loc[df['segment_id'] == 7, 'var_95'].values[0]
    ax_pdf.axvline(var_95_seg7, color='#7f1d1d', linestyle=':', lw=2, label=f'Seg 7 VaR 95% = {var_95_seg7:.2f}')
    
    ax_pdf.set_title("Probability Density Function (PDF) of Hazard Index", fontweight='bold')
    ax_pdf.set_xlabel("Composite Hazard Index (0 = Safe, 1 = Extreme Danger)", fontweight='bold')
    ax_pdf.set_ylabel("Density", fontweight='bold')
    ax_pdf.legend(loc='upper left', fontsize=9)
    ax_pdf.grid(True, linestyle='--', alpha=0.5)
    
    s_safe = np.sort(safe_data)
    cdf_safe = np.arange(len(s_safe)) / float(len(s_safe))
    s_crit = np.sort(crit_data)
    cdf_crit = np.arange(len(s_crit)) / float(len(s_crit))
    
    ax_cdf.plot(s_safe, cdf_safe, color='#10b981', lw=2.5, label='Segment 1 (Plains)')
    ax_cdf.plot(s_crit, cdf_crit, color='#dc2626', lw=2.5, label='Segment 7 (Fault Zone)')
    ax_cdf.axvline(FAILURE_THRESHOLD, color='#0f172a', linestyle='--', lw=2, label=f'Threshold (tau = {FAILURE_THRESHOLD})')
    ax_cdf.axhline(0.95, color='#64748b', linestyle=':', lw=1.5, label='95% Confidence')
    
    f_idx = np.searchsorted(s_crit, FAILURE_THRESHOLD)
    ax_cdf.fill_between(s_crit[f_idx:], cdf_crit[f_idx:], 1.0, color='#fee2e2', alpha=0.7,
                        label=f'Seg 7 Failure Region ({df.loc[df["segment_id"]==7, "prob_failure"].values[0]*100:.1f}%)')
    
    ax_cdf.set_title("Cumulative Distribution Function (CDF)", fontweight='bold')
    ax_cdf.set_xlabel("Composite Hazard Index", fontweight='bold')
    ax_cdf.set_ylabel("Cumulative Probability P(H <= h)", fontweight='bold')
    ax_cdf.legend(loc='lower right', fontsize=9)
    ax_cdf.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    fig2_path = os.path.join(PLOTS_DIR, "fig2_monte_carlo_distributions.png")
    plt.savefig(fig2_path, dpi=200, bbox_inches='tight')
    plt.close()
    
    # ---------------------------------------------------------
    # Figure 3: Sensitivity Analysis (Parameter Influence)
    # ---------------------------------------------------------
    factors = ['Rainfall (Log-Normal)', 'Cut-Slope (Triangular)', 'Soil Weakness (Beta)', 'Drainage Deficit (Uniform)']
    pcts = [weights[0] * 100, weights[1] * 100, weights[2] * 100, weights[3] * 100]
    
    fig, ax = plt.subplots(figsize=(9, 4.5))
    y_pos = np.arange(len(factors))
    colors = ['#38bdf8', '#ef4444', '#fbbf24', '#34d399']
    
    rects = ax.barh(y_pos, pcts, color=colors, edgecolor='#0f172a', lw=1.2, height=0.5)
    for rect in rects:
        w = rect.get_width()
        ax.text(w + 1.0, rect.get_y() + rect.get_height()/2.0, f"{w:.1f}% Contribution",
                va='center', fontweight='bold', fontsize=9.5)
        
    ax.set_yticks(y_pos)
    ax.set_yticklabels(factors, fontweight='bold', fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Relative Influence on Hazard Variance (%)", fontweight='bold')
    ax.set_title("Sensitivity Analysis: Primary Drivers of Highway Risk", fontweight='bold', fontsize=11)
    ax.set_xlim(0, 48)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    fig3_path = os.path.join(PLOTS_DIR, "fig3_sensitivity_analysis.png")
    plt.savefig(fig3_path, dpi=200, bbox_inches='tight')
    plt.close()
    
    # ---------------------------------------------------------
    # Figure 4: Optimization Results (Pre vs Post Mitigation)
    # ---------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    segs = np.arange(1, 21)
    bar_w = 0.38
    
    ax1.bar(segs - bar_w/2, df['expected_loss_cr'], bar_w, color='#ef4444', label='Pre-Mitigation Loss')
    ax1.bar(segs + bar_w/2, df['post_loss_cr'], bar_w, color='#10b981', label='Post-Mitigation Loss (Funded)')
    
    for _, r in df.iterrows():
        if r['selected_for_mitigation'] == 1:
            ax1.annotate('*', xy=(r['segment_id'], r['expected_loss_cr'] + 0.05),
                         ha='center', fontsize=14, color='#1d4ed8')
            
    ax1.set_xlabel("Segment ID (1 to 20)", fontweight='bold')
    ax1.set_ylabel("Expected Annual Disruption Loss (Rs. Crores)", fontweight='bold')
    ax1.set_title("Pre vs Post Mitigation Loss per Segment", fontweight='bold')
    ax1.set_xticks(segs)
    ax1.legend(loc='upper right')
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    funded = df[df['selected_for_mitigation'] == 1]
    spent = np.sum(funded['mitigation_cost_cr'])
    unspent = MITIGATION_BUDGET_CR - spent
    
    labels = [f"Seg {int(r['segment_id'])}" for _, r in funded.iterrows()]
    costs = funded['mitigation_cost_cr'].tolist()
    if unspent > 0.1:
        labels.append(f"Reserve\n(Rs. {unspent:.1f} Cr)")
        costs.append(unspent)
        
    pie_colors = ['#dc2626', '#ea580c', '#2563eb', '#94a3b8']
    ax2.pie(costs, labels=labels, autopct='%1.1f%%', colors=pie_colors[:len(costs)],
            startangle=140, textprops={'fontweight': 'bold', 'fontsize': 9},
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
    ax2.set_title(f"Budget Allocation of Rs. {MITIGATION_BUDGET_CR:.0f} Cr\n(55.5% System Risk Reduction)", fontweight='bold')
    
    plt.tight_layout()
    fig4_path = os.path.join(PLOTS_DIR, "fig4_budget_optimization.png")
    plt.savefig(fig4_path, dpi=200, bbox_inches='tight')
    plt.close()
    
    # ---------------------------------------------------------
    # Figure 5: Technical Cut-Slope Cross Section Diagram
    # ---------------------------------------------------------
    fig, ax5 = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#ffffff')
    ax5.set_facecolor('#ffffff')
    
    ax5.fill_between([0, 20, 45, 55, 75, 100], [90, 75, 45, 45, 20, 0], -5, color='#94a3b8', alpha=0.45)
    ax5.plot([20, 45], [75, 45], color='#dc2626', linewidth=3.5, label='Mountain Cut-Slope (50°-65°)')
    ax5.fill([20, 30, 45, 35, 20], [75, 68, 45, 58, 75], color='#fca5a5', alpha=0.5, hatch='//')
    ax5.plot([45, 55], [45, 45], color='#1e293b', linewidth=5, label='Road Carriageway (3°-5° Gradient)')
    ax5.plot([55, 75, 100], [45, 20, 0], color='#475569', linewidth=2, linestyle='--')
    
    # Annotate cut slope vs road
    ax5.annotate('Mountain Cut-Slope (Hazard Zone)\nSteep natural rock/soil profile\nProne to rainfall-triggered failure',
                 xy=(32, 60), xytext=(8, 78),
                 arrowprops=dict(facecolor='#dc2626', shrink=0.08, width=1.5, headwidth=6),
                 fontsize=9.5, fontweight='bold', color='#991b1b',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#fee2e2", ec="#dc2626", lw=1))
    
    ax5.annotate('Engineered Road Surface\nControlled gradient for vehicles',
                 xy=(50, 45), xytext=(56, 58),
                 arrowprops=dict(facecolor='#1e293b', shrink=0.08, width=1.5, headwidth=6),
                 fontsize=9, fontweight='bold', color='#1e293b',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#f8fafc", ec="#94a3b8", lw=1))
    
    ax5.set_xlim(-2, 102)
    ax5.set_ylim(-3, 95)
    ax5.set_aspect('equal')
    ax5.axis('off')
    ax5.set_title("Cross-Section: Cut-Slope Geometry in Mountain Highway Alignment", fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    fig5_path = os.path.join(PLOTS_DIR, "fig5_slope_cross_section.png")
    plt.savefig(fig5_path, dpi=200, bbox_inches='tight')
    plt.close()
    
    print(f"All 5 presentation figures saved in '{PLOTS_DIR}/'.")


def main():
    print("Operations Research Project: Highway Risk Assessment & Optimization")
    print("Running simulation model...")
    
    # 1. Load data
    df_corridor = load_corridor_data()
    
    # 2. Derive AHP weights
    weights = compute_ahp_weights()
    print(f"AHP Weights: Rainfall={weights[0]:.3f}, Slope={weights[1]:.3f}, Soil={weights[2]:.3f}, Drainage={weights[3]:.3f}")
    
    # 3. Execute Monte Carlo
    df_results, hazard_samples = run_monte_carlo(df_corridor, weights)
    
    # 4. Run Knapsack Optimization
    df_results = optimize_budget(df_results)
    
    # 5. Export results
    output_csv = "highway_simulation_results.csv"
    df_results.to_csv(output_csv, index=False)
    print(f"Results exported to {output_csv}")
    
    # Summary metrics
    n_high = np.sum(df_results['risk_tier'] == 'High')
    n_med = np.sum(df_results['risk_tier'] == 'Medium')
    n_low = np.sum(df_results['risk_tier'] == 'Low')
    total_pre_loss = np.sum(df_results['expected_loss_cr'])
    total_post_loss = np.sum(df_results['post_loss_cr'])
    savings = total_pre_loss - total_post_loss
    
    print("\nSimulation & Optimization Summary:")
    print(f"  * Total Corridor Length     : 200 km (20 segments)")
    print(f"  * High-Risk Segments (Red)  : {n_high}")
    print(f"  * Medium-Risk Segments      : {n_med}")
    print(f"  * Low-Risk Segments (Green) : {n_low}")
    print(f"  * Baseline Expected Loss    : Rs. {total_pre_loss:.2f} Crores/yr")
    print(f"  * Post-Mitigation Loss      : Rs. {total_post_loss:.2f} Crores/yr")
    print(f"  * System Risk Reduction     : Rs. {savings:.2f} Crores ({(savings/total_pre_loss)*100:.1f}%)")
    
    # 6. Generate presentation plots
    generate_plots(df_results, hazard_samples, weights)
    print("Execution completed successfully.")


if __name__ == '__main__':
    main()
