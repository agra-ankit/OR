# Operations Research Project Presentation Guide
**Topic 10: Identification of High-Risk Zones in a National Highway Project**  
*Methodology: Monte Carlo Simulation (Weather & Terrain Data) and 0-1 Knapsack MILP Optimization*

---

## Clean Directory Structure
```text
OR/
├── simulation.py                        # Main simulation and optimization script
├── highway_simulation_results.csv       # Segment-by-segment quantitative output
├── Highway_Risk_Assessment_OR_Project.pptx  # 12-slide ready-to-present PowerPoint deck
├── presentation_guide.md                # Slide-by-slide speaker notes
└── plots/
    ├── fig1_corridor_risk_profile.png   # Slide 7: Elevation & risk zone classification
    ├── fig2_monte_carlo_distributions.png # Slide 8: Monte Carlo PDF, CDF & VaR95
    ├── fig3_sensitivity_analysis.png    # Slide 6: Parameter sensitivity / Tornado chart
    ├── fig4_budget_optimization.png     # Slide 9: 0-1 Knapsack MILP optimization results
    └── fig5_budget_sensitivity_curve.png # Slide 9/10: Pareto frontier / Budget sensitivity curve
```

---

## 13-Slide Structure & Speaker Notes

### Slide 1: Title Slide
* **Title:** Identification of High-Risk Zones in a National Highway Project
* **Sub-title:** An Operations Research Approach to Stochastic Risk Assessment and Capital Budgeting
* **Metadata:** Course: Operations Research (CSN13402(L)) | 200 km Mountain Highway Corridor | 10,000 Monte Carlo Trials

### Slide 2: Problem Statement & Motivation
* **Key Points:**
  * 200 km national highway corridor in rugged terrain prone to recurring monsoon slope failures and washouts.
  * Disasters cause multi-day blockades, freight spoilage, and emergency clearance expenses.
  * **The Core Constraint:** Full-corridor disaster-proofing costs ₹248 Crores, but annual capital safety budget is only **₹60 Crores**.
* **Speaker Note:** *"Traditional planning relies on static averages, which miss rare cloudbursts. Operations Research allows us to quantify risk under uncertainty and optimize budget allocation."*

### Slide 3: Why Operations Research? (Stochastic Modeling)
* **Key Points:**
  * Compares deterministic approach (static averages, misses tail events) vs. probabilistic OR approach (simulates 10,000 storm seasons).
  * Disasters occur during extreme tail events (Central Limit Theorem context).
  * Feeds simulation results directly into integer linear programming for capital budgeting.

### Slide 4: The 4 Hazard Factors & Their Distributions
* **Key Points:**
  1. **Rainfall Intensity ($R$):** Log-Normal distribution $\text{LN}(\mu, \sigma)$ — captures extreme 200mm+ cloudburst tails.
  2. **Cut-Slope Angle ($\theta$):** Triangular distribution $\text{Triangular}(\min, \text{mode}, \max)$ — models spatial variation along 10 km mountain cuts.
  3. **Soil & Rock Strength ($G$):** Beta distribution $\text{Beta}(\alpha, \beta)$ bounded $[0, 1]$ — granite bedrock vs. fractured shale.
  4. **Drainage Deficit ($D$):** Base capacity degraded by stochastic storm debris $\text{Uniform}(0, 0.40)$.

### Slide 5: Monte Carlo Simulation Methodology
* **Key Points:**
  * 6-step architecture: Discretization $\to$ AHP Weighting $\to$ Sampling $\to$ CRI Evaluation $\to$ Threshold Check ($\tau = 0.65$) $\to$ Aggregation.
  * **CRI Governing Equation:**
    $$CRI_i = 0.394 \cdot \tilde{R}_i + 0.285 \cdot \tilde{\theta}_i + 0.205 \cdot (1 - \tilde{G}_i) + 0.116 \cdot (1 - \tilde{D}_i)$$
  * Failure occurs whenever $CRI_i > 0.65$.

### Slide 6: AHP Multi-Criteria Weighting & Sensitivity
* **Embedded Image:** `plots/fig3_sensitivity_analysis.png`
* **Key Points:**
  * Saaty's Pairwise Comparison Matrix evaluated using the principal eigenvector method ($\sum w_i = 1.0$).
  * Weights: Rainfall = **39.4%**, Slope = **28.5%**, Soil Weakness = **20.5%**, Drainage Deficit = **11.6%**.
  * Consistency Ratio: $CR = 0.042 < 0.10$ (Mathematically Consistent).
  * **Tornado Sensitivity Analysis:** Demonstrates that parameter swings in Rainfall ($0.44 \to 0.76$) and Slope ($0.49 \to 0.69$) dominate corridor hazard variability.

### Slide 7: Simulation Results — Corridor Risk Profile
* **Embedded Image:** `plots/fig1_corridor_risk_profile.png`
* **Key Points:**
  * 200 km corridor divided into 20 segments (10 km each) across 4 geotechnical zones (Foothills, Fault Escarpment, Gorge Pass, Valley Plateau).
  * **3 High-Risk Red Zones ($P_f \ge 15\%$):** Segment 12 (31.0%), Segment 7 (28.1%), Segment 6 (16.6%).
  * **4 Medium-Risk Yellow Zones ($5\% \le P_f < 15\%$):** Segments 5, 8, 10, 11.
  * **13 Low-Risk Green Zones ($P_f < 5\%$):** Foothills and valley sections.

### Slide 8: Monte Carlo Distributions & Value-at-Risk (VaR)
* **Embedded Image:** `plots/fig2_monte_carlo_distributions.png`
* **Key Points:**
  * Compares safe Segment 1 (plains) vs. critical Segment 7 (fault zone) across 10,000 trials with Kernel Density Estimation (KDE).
  * Segment 7 exhibits an extended tail beyond $\tau = 0.65$, with a 95% Value-at-Risk ($\text{VaR}_{95}$) of **0.82**.
  * In the worst 5% of monsoon storms, hazard reaches catastrophic levels.
  * At threshold $\tau=0.65$, cumulative probability is $71.9\%$, giving exactly $P_f = 28.1\%$.

### Slide 9: 0-1 Knapsack MILP — Budget Optimization
* **Embedded Image:** `plots/fig4_budget_optimization.png`
* **Formulation:**
  $$\max \sum_{i=1}^{20} (0.85 \cdot L_i) \cdot x_i \quad \text{s.t.} \quad \sum_{i=1}^{20} c_i \cdot x_i \le \text{Rs. } 60 \text{ Cr}, \quad x_i \in \{0, 1\}$$
* **Outcome:**
  * Funded: **Segment 12** (₹21.0 Cr), **Segment 7** (₹22.0 Cr), and **Segment 11** (₹16.5 Cr).
  * Total capital deployed: **₹59.50 Crores** (99.17% budget efficiency; ₹0.50 Cr reserve).
  * Baseline expected annual damage reduced from **₹4.89 Crores to ₹2.17 Crores** (**55.5% system risk reduction**).

### Slide 10: Pareto Frontier & Capital Sensitivity Analysis
* **Embedded Image:** `plots/fig5_budget_sensitivity_curve.png`
* **Key Points:**
  * Evaluated across budgets ranging from ₹10 Cr to ₹140 Cr.
  * **Zone I (₹10–₹60 Cr):** Steepest efficiency (+0.92% risk reduction per Crore). Mitigates 100% of critical red hotspots.
  * **Zone II (₹60–₹100 Cr):** Moderate returns (+0.32%/Cr) as secondary yellow zones are absorbed.
  * **Zone III (> ₹100 Cr):** Flat plateau (+0.12%/Cr). Demonstrates severe diminishing marginal returns.
  * **The ₹60 Cr Sweet Spot:** Mathematically justifies the ₹60 Cr budget limit as the optimal economic investment threshold.

### Slide 11: Managerial & Policy Implications
* **Red Zones (Segments 6, 7, 12):** Immediate capital intervention (anchored retaining walls, rock-shed galleries, geo-mesh).
* **Yellow Zones (Segments 5, 8, 10, 11):** Operational monitoring (IoT slope displacement sensors, pre-positioned earthmoving machinery).
* **Green Zones (Remaining 13):** Standard periodic maintenance.

### Slide 12: Conclusion & Future Scope
* **Contributions:** Successfully demonstrated coupling of stochastic simulation with integer linear programming for infrastructure capital budgeting under uncertainty.
* **Future Work:** Real-time IoT sensor telemetry integration and dynamic vehicle rerouting across alternate corridors.

### Slide 13: Thank You & Q&A
* Summary KPI recap: 3 Red Zones identified, ₹59.5 Cr allocated, 55.5% risk reduction. Open for questions.

---

## Live Interactive Demo Guide (Feature 4 for Viva / Questions)
If your professor asks you to demonstrate the code live or test different budget constraints:

1. **Standard Default Run:**
   ```bash
   python simulation.py
   ```
   *Will prompt: `Enter Capital Budget in Crores (or press Enter for default 60.0):`*
   *Simply press Enter or type `60`.*

2. **Command-Line Direct Argument (Instant Demo):**
   ```bash
   # Test with an 80 Crore budget:
   python simulation.py 80

   # Test with a 30 Crore austerity budget:
   python simulation.py 30
   ```
   *Explain to the professor:*
   *"Sir, watch how the 0-1 Knapsack MILP solver dynamically reconfigures the optimal portfolio of segments as the budget changes, adhering strictly to the Pareto Frontier."*
