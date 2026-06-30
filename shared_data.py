import numpy as np

# ============================================================
# RAW DATA FROM SPREADSHEET
# ============================================================
INVERSION_INICIAL = 460834

PVU = {
    "Pino": 14.0, "Cloro": 15.0, "Lavanda": 14.0, "Mar Fresco": 14.0,
    "Lavatraestes": 23.0, "Tipo Zote": 20.0, "Mas Color": 22.0,
    "Mas Color Negro": 22.0, "Suavizante": 15.0, "Suav. Downi": 19.0
}

# Usamos los CVU ORIGINALES (los de las recetas podrían tener dilución en agua no contabilizada)
CVU_ORIG = {
    "Pino": 1.67, "Cloro": 5.0, "Lavanda": 2.9, "Mar Fresco": 2.9,
    "Lavatraestes": 3.68, "Tipo Zote": 8.49, "Mas Color": 10.5,
    "Mas Color Negro": 10.5, "Suavizante": 7.0, "Suav. Downi": 7.0
}

# CVU alternativo basado en recetas (para análisis de sensibilidad)
# NOTA: Las recetas muestran costo de ingredientes para 200L pero podría haber dilución
# que haría que el costo real por litro sea menor. Se deja como referencia.
CVU_RECETA = {
    "Pino": 1091.45/200, "Cloro": 1750.0/200, "Lavanda": 441.145/200,
    "Mar Fresco": 441.145/200, "Lavatraestes": 3174.295/200,
    "Tipo Zote": 1698.545/200, "Mas Color": 2764.9/200,
    "Mas Color Negro": 2764.9/200, "Suavizante": 2042.15/200,
    "Suav. Downi": 1646.95/200
}

SALES_DATA = {
    1: {"litros_dia": 400, "precio": 17.80, "dias": 365},
    2: {"litros_dia": 430, "precio": 18.33, "dias": 365},
    3: {"litros_dia": 462.25, "precio": 18.88, "dias": 365},
    4: {"litros_dia": 496.92, "precio": 19.45, "dias": 365},
    5: {"litros_dia": 534.19, "precio": 20.03, "dias": 365},
}

def get_sales(year):
    d = SALES_DATA[year]
    return d["litros_dia"] * d["precio"] * d["dias"]

def get_volume_liters(year):
    return SALES_DATA[year]["litros_dia"] * 365

# Promedios
PVU_PROM = sum(PVU[p] for p in PVU) / len(PVU)
CVU_PROM = sum(CVU_ORIG[p] for p in CVU_ORIG) / len(CVU_ORIG)

# ============================================================
# FIXED COSTS
# ============================================================
NOMINA = 36220
ARRENDAMIENTO = 8000
SERVICIOS = 9100
PUBLICIDAD = 5500

GA_RATE = 0.08
GA = GA_RATE  # alias for backwards compat
SEGUROS = 5000
MANTENIMIENTO_RATE = 0.015
MANTENIMIENTO = MANTENIMIENTO_RATE  # alias
CONTROL_CALIDAD = 4000
INSUMOS_RATE = 0.01
INSUMOS_OP = INSUMOS_RATE  # alias
DEPRECIACION_MENSUAL = 3150  # 15% anual de $252,000 / 12

# Costos fijos BASE (sin G&A ni variables)
CF_BASE = NOMINA + ARRENDAMIENTO + SERVICIOS + PUBLICIDAD

def get_fixed_costs_monthly(ventas_mensuales):
    return (NOMINA + ARRENDAMIENTO + SERVICIOS + PUBLICIDAD +
            SEGUROS + CONTROL_CALIDAD +
            ventas_mensuales * (GA_RATE + MANTENIMIENTO_RATE + INSUMOS_RATE))

# ============================================================
# BREAK-EVEN CORRECT CALCULATION
# ============================================================
def calc_break_even(anio=1, cvu_dict=None, incluir_adicionales=True):
    ventas = get_sales(anio)
    ventas_m = ventas / 12
    vol_m = get_volume_liters(anio) / 12
    if cvu_dict is None:
        cvu_dict = CVU_ORIG
    cvu_p = sum(cvu_dict[p] for p in cvu_dict) / len(cvu_dict)
    pvu_p = sum(PVU[p] for p in PVU) / len(PVU)
    mc = pvu_p - cvu_p
    cf = get_fixed_costs_monthly(ventas_m) if incluir_adicionales else CF_BASE
    be_u = cf / mc if mc > 0 else float('inf')
    return {
        "pvu_prom": pvu_p, "cvu_prom": cvu_p, "mc_unit": mc,
        "cf_mensual": cf, "be_units": be_u, "be_revenue": be_u * pvu_p,
        "be_pct_capacity": be_u / vol_m * 100,
        "margin_safety": (1 - be_u / vol_m) * 100,
        "volumen_mensual": vol_m
    }

# ============================================================
# INCOME STATEMENT
# ============================================================
def calc_income(anio, growth=0.05, cvu_dict=None, incluir_adicionales=True, *args):
    ventas = get_sales(anio) * (1 + growth) ** (anio - 1)
    vol = get_volume_liters(anio) * (1 + growth) ** (anio - 1)
    if cvu_dict is None:
        cvu_dict = CVU_ORIG
    cvu_p = sum(cvu_dict[p] for p in cvu_dict) / len(cvu_dict)
    cv = cvu_p * vol
    n = NOMINA * 12 * (1 + growth) ** (anio - 1)
    r = ARRENDAMIENTO * 12 * (1 + growth) ** (anio - 1)
    s = SERVICIOS * 12 * (1 + growth) ** (anio - 1)
    pb = PUBLICIDAD * 12 * (1 + growth) ** (anio - 1)
    if incluir_adicionales:
        ga = ventas * GA_RATE * (1 + growth) ** (anio - 1)
        seg = SEGUROS * 12 * (1 + growth) ** (anio - 1)
        mant = ventas * MANTENIMIENTO_RATE * (1 + growth) ** (anio - 1)
        qc = CONTROL_CALIDAD * 12 * (1 + growth) ** (anio - 1)
        ins = ventas * INSUMOS_RATE * (1 + growth) ** (anio - 1)
        depr = DEPRECIACION_MENSUAL * 12
    else:
        ga = seg = mant = qc = ins = depr = 0
    total_cf = n + r + s + pb + ga + seg + mant + qc + ins
    total = cv + total_cf
    ebitda = ventas - total
    ebit = ebitda - depr
    return {"ventas": ventas, "cv": cv, "nomina": n, "renta": r,
            "servicios": s, "publicidad": pb, "ga": ga, "seguros": seg,
            "mantenimiento": mant, "qc": qc, "insumos": ins, "depreciacion": depr,
            "total_cf": total_cf, "total_costos": total, "ebitda": ebitda, "ebit": ebit}

# ============================================================
# CASH FLOW & METRICS
# ============================================================
def calc_fcff(anio, growth=0.05, cvu_dict=None, incluir_adicionales=True,
              d_inv=15, d_cxc=30, d_cxp=15, tasa=0.30):
    inc = calc_income(anio, growth, cvu_dict, incluir_adicionales)
    ebit = inc["ebit"]
    tax = max(0, ebit * tasa)
    depr = inc["depreciacion"]
    capex = 252000 if anio == 1 else 0
    ventas = inc["ventas"]
    vol = get_volume_liters(anio) * (1 + growth) ** (anio - 1)
    cvu_p = sum((cvu_dict or CVU_ORIG)[p] for p in (cvu_dict or CVU_ORIG)) / len(cvu_dict or CVU_ORIG)
    wc_inv = vol / 365 * d_inv * cvu_p
    wc_cxc = ventas / 365 * d_cxc
    wc_cxp = vol / 365 * d_cxp * cvu_p
    wc = wc_inv + wc_cxc - wc_cxp
    if anio == 1:
        delta_wc = wc
    else:
        prev_vol = get_volume_liters(anio-1) * (1 + growth) ** (anio-2)
        prev_vtas = get_sales(anio-1) * (1 + growth) ** (anio-2)
        prev_wc = prev_vol/365*d_inv*cvu_p + prev_vtas/365*d_cxc - prev_vol/365*d_cxp*cvu_p
        delta_wc = wc - prev_wc
    fcf = ebit - tax + depr - capex - delta_wc
    return {"fcf": fcf, "ebit": ebit, "tax": tax, "depr": depr,
            "capex": capex, "delta_wc": delta_wc, "wc_neto": wc}

def get_fcff_series(growth=0.05, cvu_dict=None, incluir_adicionales=True,
                    d_inv=15, d_cxc=30, d_cxp=15, tasa=0.30):
    return [calc_fcff(y, growth, cvu_dict, incluir_adicionales, d_inv, d_cxc, d_cxp, tasa)["fcf"]
            for y in range(1, 6)]

def calc_npv(cashflows, investment, discount_rate=0.21):
    pv = sum(cf / (1 + discount_rate) ** (i+1) for i, cf in enumerate(cashflows))
    return pv - investment

def calc_pv(cashflows, discount_rate=0.21):
    return sum(cf / (1 + discount_rate) ** (i+1) for i, cf in enumerate(cashflows))

def calc_irr(cashflows, investment):
    cf_all = [-investment] + list(cashflows)
    rate = 0.3
    for _ in range(500):
        f = sum(cf / (1 + rate) ** i for i, cf in enumerate(cf_all))
        if abs(f) < 1e-8:
            return rate
        df = sum(-i * cf / (1 + rate) ** (i+1) for i, cf in enumerate(cf_all))
        if abs(df) < 1e-12:
            break
        rate = rate - f / df
        if rate < -0.5:
            rate = -0.5
        if rate > 10:
            rate = 10
    lo, hi = -0.49, 5.0
    for _ in range(100):
        mid = (lo + hi) / 2
        f = sum(cf / (1 + mid) ** i for i, cf in enumerate(cf_all))
        if abs(f) < 1e-8:
            return mid
        if f > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def calc_payback(cashflows, investment):
    cum = -investment
    for i, cf in enumerate(cashflows):
        cum += cf
        if cum >= 0:
            prev = cum - cf
            return (i + (-prev) / cf) * 12
    return None

def calc_roi(cashflows, investment):
    return (sum(cashflows) - investment) / investment * 100

def calc_pi(cashflows, investment, dr=0.21):
    pv = sum(cf / (1 + dr) ** (i+1) for i, cf in enumerate(cashflows))
    return pv / investment
