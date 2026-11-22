"""EEE213 numerical problem #4: ideal single-diode solar-cell maximum power.

Reproduces Newton iterations, derivative check, independent maximization,
plots and machine-readable results. Stated parameters are illustrative assumptions,
not manufacturer specifications. Run: python code/numerical.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / 'figures'
FIGURES.mkdir(exist_ok=True)

# Defined SI constants and stated model assumptions
KB = 1.380649e-23  # J/K, exact SI constant
Q = 1.602176634e-19  # C, exact SI constant
T = 298.15  # K, assumed
N = 1.30  # diode ideality factor (unitless), assumed
IPH = 5.00  # A, photocurrent, assumed
I0 = 1.00e-10  # A, diode saturation current, assumed
A = N * KB * T / Q  # V, n times thermal voltage
VOC = A * math.log1p(IPH / I0)  # V


def current(v: float) -> float:
    """Ideal single-diode output current, in amperes."""
    return IPH - I0 * math.expm1(v / A)


def power(v: float) -> float:
    """Terminal power in watts (V * A)."""
    return v * current(v)


def f(v: float) -> float:
    """dP/dV in amperes: root gives stationary power point."""
    u = v / A
    return IPH + I0 - I0 * math.exp(u) * (1.0 + u)


def df(v: float) -> float:
    """d^2P/dV^2 in A/V; analytic derivative of f."""
    u = v / A
    return -(I0 / A) * math.exp(u) * (2.0 + u)


def newton(v0: float = 0.70, tol_v: float = 1e-12,
           tol_f: float = 1e-10, max_iter: int = 50):
    """Newton iteration, requiring both step size and residual tolerances."""
    v = v0
    rows = []
    for iteration in range(max_iter):
        residual = f(v)
        derivative = df(v)
        if derivative == 0 or not math.isfinite(derivative):
            raise ArithmeticError('Zero or non-finite derivative')
        step = -residual / derivative
        new_v = v + step
        rows.append({'iteration':iteration, 'v_v':v, 'f_a':residual,
                     'derivative_a_per_v':derivative, 'step_v':step})
        if not math.isfinite(new_v) or not (0.0 <= new_v <= VOC):
            raise ArithmeticError(f'Newton update outside physical interval: {new_v}')
        v = new_v
        if abs(step) < tol_v and abs(f(v)) < tol_f:
            return v, rows
    raise RuntimeError('Newton iteration did not converge')


def golden_section_maximum(a: float, b: float, tol: float = 1e-12):
    """Independent derivative-free search; uses direct P(V), not Newton/f/df."""
    ratio = (math.sqrt(5.0) - 1.0) / 2.0
    c, d = b - ratio * (b - a), a + ratio * (b - a)
    for _ in range(200):
        if b - a < tol:
            break
        if power(c) > power(d):
            b, d = d, c
            c = b - ratio * (b - a)
        else:
            a, c = c, d
            d = a + ratio * (b - a)
    return (a + b) / 2.0


def main():
    vmp, iters = newton()
    imp = current(vmp)
    pmp = power(vmp)
    vgold = golden_section_maximum(0.0, VOC)
    pgold = power(vgold)

    # Independently scan power curve at uniform voltage steps, not by solving f=0.
    vv = np.linspace(0, VOC, 200001)
    ii = IPH - I0 * np.expm1(vv / A)
    pp = vv * ii
    ix = int(np.argmax(pp))
    vgrid = float(vv[ix]); pgrid = float(pp[ix])

    check_v = 0.65
    h = 1.0e-6  # V
    derivative_fd = (f(check_v + h) - f(check_v - h)) / (2 * h)
    derivative_an = df(check_v)
    fd_abs_diff = abs(derivative_an - derivative_fd)

    if not (0 < vmp < VOC and imp > 0 and df(vmp) < 0):
        raise AssertionError('Maximum-power physical checks failed')
    if abs(vmp - vgold) > 1e-7:
        raise AssertionError('Independent golden-section check failed')
    if abs(vmp - vgrid) > (VOC / 200000) + 1e-10:
        raise AssertionError('Power-grid check failed')
    if fd_abs_diff > 1e-4:
        raise AssertionError('Finite-difference derivative check failed')

    print('NUMERICAL PROBLEM #4: SOLAR-CELL MAXIMUM POWER POINT')
    print('MODEL: ideal illuminated single diode, Rs=0 ohm, Rsh=infinity; constant T/irradiance')
    print('PARAMETERS: Iph=5.00 A, I0=1.00e-10 A, n=1.30, T=298.15 K (stated assumptions)')
    print(f'thermal_voltage kB*T/q = {KB*T/Q:.9f} V; a=n*VT = {A:.9f} V')
    print(f'open_circuit_voltage Voc = {VOC:.9f} V')
    print('NEWTON ITERATIONS:')
    print('iter | voltage(V) | residual dP/dV (A) | f\'(V) (A/V) | delta V (V)')
    for row in iters:
        print(f" {row['iteration']:2d}  | {row['v_v']:.10f} | {row['f_a']:+.9e} | {row['derivative_a_per_v']:+.9e} | {row['step_v']:+.9e}")
    print(f'Vmp (Newton) = {vmp:.10f} V')
    print(f'Imp = {imp:.10f} A')
    print(f'Pmp = {pmp:.10f} W')
    print(f'final_residual_abs = {abs(f(vmp)):.9e} A')
    print(f'curvature at MPP, d2P/dV2 = {df(vmp):+.8f} A/V (negative: local maximum)')
    print(f'INDEPENDENT golden-section (power-only) Vmp = {vgold:.10f} V, Pmp = {pgold:.10f} W')
    print(f'INDEPENDENT dense grid Vmp = {vgrid:.10f} V, Pmp = {pgrid:.10f} W')
    print(f'voltage agreement golden vs Newton = {abs(vgold-vmp):.9e} V')
    print(f'voltage agreement grid vs Newton = {abs(vgrid-vmp):.9e} V')
    print(f'finite-difference derivative at {check_v:.2f} V: analytic = {derivative_an:.9e} A/V; finite-difference = {derivative_fd:.9e} A/V; absolute difference = {fd_abs_diff:.9e} A/V')
    print(f'endpoint check P(0)={power(0):.3e} W, P(Voc)={power(VOC):.3e} W')
    print(f'SOFTWARE Python {sys.version.split()[0]}, NumPy {np.__version__}, Matplotlib {matplotlib.__version__}')

    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.6))
    axs[0].plot(vv, ii, lw=2.3, color='#24637a')
    axs[0].scatter([vmp], [imp], color='#eb8d3f', s=66, zorder=5)
    axs[0].annotate(f'MPP: ({vmp:.3f} V, {imp:.3f} A)',
                    (vmp,imp), xytext=(-132,-62),textcoords='offset points',
                    arrowprops={'arrowstyle':'->','color':'#6b7280'}, fontsize=10)
    axs[0].set(xlabel='Terminal voltage V (V)', ylabel='Terminal current I (A)', title='I–V curve')
    axs[0].grid(alpha=0.2)
    axs[1].plot(vv, pp, lw=2.3, color='#3469bd')
    axs[1].scatter([vmp], [pmp], color='#eb8d3f', s=66, zorder=5)
    axs[1].annotate(f'Maximum {pmp:.3f} W', (vmp,pmp), xytext=(-132,-62),
                    textcoords='offset points',arrowprops={'arrowstyle':'->','color':'#6b7280'},fontsize=10)
    axs[1].set(xlabel='Terminal voltage V (V)',ylabel='Power P (W)', title='P–V curve')
    axs[1].grid(alpha=0.2)
    fig.suptitle('Ideal solar-cell maximum power point — assumed parameters', fontsize=13)
    fig.tight_layout()
    fig.savefig(FIGURES / 'solar_cell_iv_pv.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.7, 3.6))
    steps = [abs(r['step_v']) for r in iters]
    ax.semilogy(range(len(steps)), steps, marker='o', lw=2, color='#315bba')
    ax.set(xlabel='Newton iteration',ylabel='Absolute Newton step |ΔV| (V)',title='Newton convergence at solar-cell MPP')
    ax.grid(alpha=0.18)
    fig.tight_layout()
    fig.savefig(FIGURES / 'solar_cell_newton_convergence.png', dpi=200,bbox_inches='tight',facecolor='white')
    plt.close(fig)

    obj = {
        'problem_number':4, 'model':'ideal_single_diode', 'parameter_source':'stated_assumptions',
        'Iph_A':IPH,'I0_A':I0,'n_dimensionless':N,'T_K':T,'n_kBT_over_q_V':A,
        'Voc_V':VOC, 'Vmp_newton_V':vmp,'Imp_A':imp,'Pmp_W':pmp,
        'final_residual_A':f(vmp),'second_derivative_A_per_V':df(vmp),
        'golden_section_Vmp_V':vgold,'power_grid_Vmp_V':vgrid,
        'absolute_agreement_golden_V':abs(vmp-vgold),'absolute_agreement_grid_V':abs(vmp-vgrid),
        'fd_derivative_at_V':check_v,'fd_derivative_analytical_A_per_V':derivative_an,
        'fd_derivative_central_A_per_V':derivative_fd,'fd_derivative_absolute_difference_A_per_V':fd_abs_diff,
        'iterations':iters,
        'figures':['figures/solar_cell_iv_pv.png','figures/solar_cell_newton_convergence.png'],
    }
    (ROOT / 'numerical_results.json').write_text(json.dumps(obj, indent=2),encoding='utf-8')

if __name__ == '__main__':
    main()
