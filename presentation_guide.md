# Operations Research Project Presentation Guide
**Topic 10: Identification of High-Risk Zones in a National Highway Project**  
*Methodology: Monte Carlo Simulation (Weather & Terrain Data) and 0-1 Knapsack MILP Optimization*

---

## Directory Structure
```text
OR/
├── simulation.py                   # Main simulation and optimization script
├── highway_simulation_results.csv  # Detailed segment-by-segment quantitative results
├── plots/
│   ├── fig1_corridor_risk_profile.png        # Slide 7: Corridor elevation and risk profile
│   ├── fig2_monte_carlo_distributions.png    # Slide 8: Monte Carlo PDF, CDF, and VaR
│   ├── fig3_sensitivity_analysis.png         # Slide 9: Sensitivity / Tornado analysis
│   ├── fig4_budget_optimization.png          # Slide 10: Knapsack optimization results
│   └── fig5_slope_cross_section.png          # Slide 4: Cut-slope vs road gradient
└── presentation_guide.md                     # Slide-by-slide speaker notes
```

---

## Recommended Slide Structure & Speaker Notes

### Slide 1: Title Slide
* **Title:** Identification of High-Risk Zones in a National Highway Corridor Using Monte Carlo Simulation
* **Sub-title:** An Operations Research Approach to Stochastic Risk Assessment and Capital Budgeting
* **Team Details:** Course Code: CSN13402(L)

### Slide 2: Problem Statement & Motivation
* **Key Points:**
  * National highways in mountainous terrain are highly vulnerable to slope failures, landslides, and flash washouts during monsoon seasons.
  * Disasters cause multi-day closures, heavy freight disruption, and emergency response costs.
  * **The Challenge:** Finite maintenance budgets cannot protect an entire 200 km corridor simultaneously; highway authorities need a quantitative method to identify the most hazardous zones.
* **Speaker Note:** *"Traditional civil planning relies on deterministic averages, but structural failures occur during extreme weather tails. Operations Research allows us to model these uncertainties probabilistically."*

### Slide 3: Why Operations Research? (Stochastic Modeling)
* **Key Points:**
  * Deterministic assumptions fail because rainfall, soil saturation, and rock strength are uncertain.
  * Monte Carlo simulation allows evaluation of 10,000 alternate monsoon scenarios.
  * Combines probabilistic risk assessment with 0-1 Knapsack Mixed Integer Linear Programming (MILP) for optimal budget allocation.

### Slide 4: Highway Geometry & The "Cut-Slope" Concept
* **Insert Image:** `plots/fig5_slope_cross_section.png`
* **Key Points:**
  * Clarifies the difference between road gradient ($3^\circ-5^\circ$, engineered for vehicles) and the adjacent mountain cut-slope ($45^\circ-65^\circ$).
  * The steep cut-slope towers above the road and is the primary source of slope failure under saturation.

### Slide 5: Mathematical Formulation
* **Parameters & Distributions:**
  * **Rainfall ($R$):** Log-Normal distribution $\text{LN}(\mu, \sigma)$ to capture extreme cloudburst events.
  * **Slope Angle ($\theta$):** Triangular distribution $\text{Triangular}(\min, \text{mode}, \max)$.
  * **Geotechnical Strength ($G$):** Beta distribution $\text{Beta}(\alpha, \beta)$ bounded $[0, 1]$.
  * **Drainage Deficit ($D$):** Stochastic clogging from storm debris.
* **Composite Hazard Index ($CRI$):**
  $$CRI_i = w_R \cdot \tilde{R}_i + w_S \cdot \tilde{\theta}_i + w_G \cdot (1 - \tilde{G}_i) + w_D \cdot (1 - \tilde{D}_i)$$
  Failure occurs when $CRI_i > 0.65$.

### Slide 6: Multi-Criteria Weighting via AHP
* **Key Points:**
  * Analytic Hierarchy Process (Saaty's AHP) pairwise comparison matrix used to establish consistent weights.
  * Derived weights:
    * Rainfall Intensity ($w_R$): **39.4%**
    * Slope Steepness ($w_S$): **28.5%**
    * Geotechnical Weakness ($w_G$): **20.5%**
    * Drainage Deficit ($w_D$): **11.6%**

### Slide 7: Simulation Results — Corridor Risk Heatmap
* **Insert Image:** `plots/fig1_corridor_risk_profile.png`
* **Key Points:**
  * 200 km corridor categorized into 20 segments (10 km each).
  * **High Risk (Red Zone, $P_f \ge 15\%$):** Segments 6, 7, and 12 (Mountain Pass Summit and Cloudburst Canyon).
  * **Medium Risk (Yellow Zone, $5\% \le P_f < 15\%$):** Segments 5, 8, 10, 11.
  * **Low Risk (Green Zone, $P_f < 5\%$):** 13 segments in foothills and plateaus.

### Slide 8: Monte Carlo Dynamics & Value-at-Risk (VaR)
* **Insert Image:** `plots/fig2_monte_carlo_distributions.png`
* **Key Points:**
  * Compares low-risk plains (Segment 1) vs high-risk fault zone (Segment 7).
  * Segment 7 shows an extended tail with a 95% Value-at-Risk ($\text{VaR}_{95}$) of **0.82**, yielding a **28.1%** probability of exceeding the failure threshold.

### Slide 9: Sensitivity Analysis
* **Insert Image:** `plots/fig3_sensitivity_analysis.png`
* **Key Points:**
  * Quantifies relative influence of stochastic parameters on overall system variance.
  * Rainfall intensity and slope steepness account for **67.9%** of composite hazard uncertainty.

### Slide 10: Capital Budgeting Optimization (0-1 Knapsack MILP)
* **Insert Image:** `plots/fig4_budget_optimization.png`
* **Formulation:**
  $$\max \sum_{i=1}^{20} (\Delta \text{Risk}_i) \cdot x_i \quad \text{s.t.} \quad \sum_{i=1}^{20} c_i x_i \le \text{Rs. } 60 \text{ Cr}, \quad x_i \in \{0, 1\}$$
* **Outcome:**
  * Funded projects: **Segment 12** (Rs. 21.0 Cr), **Segment 7** (Rs. 22.0 Cr), and **Segment 11** (Rs. 16.5 Cr).
  * Total expenditure: **Rs. 59.50 Crores**.
  * Baseline expected annual loss reduced from **Rs. 4.89 Crores to Rs. 2.17 Crores** (**55.5% system risk reduction**).

### Slide 11: Managerial & Practical Implications
* **Targeted Mitigation:** Move away from uniform corridor spending; focus capital investments where expected risk reduction per rupee is maximized.
* **Operational Readiness:** Medium-risk zones (Yellow) can be equipped with IoT early-warning sensors and prepositioned earthmoving machinery instead of costly structural overhauls.

### Slide 12: Conclusion & Future Scope
* **Summary:** Successfully demonstrated the integration of Monte Carlo stochastic simulation with mixed-integer linear programming for infrastructure resilience.
* **Future Work:** Dynamic real-time weather forecasting integration and vehicle rerouting optimization across alternate arterial networks.
