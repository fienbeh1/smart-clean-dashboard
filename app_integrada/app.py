import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.stats import spearmanr
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared_data import *

# ── Brand Identity ──────────────────────────────────────────
BRAND = {
    "name": "Smart Clean",
    "tagline": "Análisis Financiero Inteligente",
    "primary": "#64FFDA",
    "primary_light": "#A7FFEB",
    "primary_dark": "#00BFA6",
    "accent": "#FFD700",
    "bg": "#0A192F",
    "card": "#112240",
    "text": "#CCD6F6",
    "muted": "#8892B0",
}

ENFOQUES = {
    "Conservador":    {"icon": "🧮", "color": BRAND["primary"],       "desc": "Corrección de errores y supuestos conservadores"},
    "Mercado":        {"icon": "🏭", "color": BRAND["accent"],        "desc": "Benchmarks de industria de limpieza"},
    "Monte Carlo":    {"icon": "🎲", "color": BRAND["primary_light"], "desc": "Simulación probabilística con Monte Carlo"},
    "Capital Trabajo":{"icon": "💰", "color": "#E65100",             "desc": "Ciclo de conversión de efectivo y WC"},
    "Dashboard":      {"icon": "📊", "color": BRAND["primary_dark"],  "desc": "Dashboard integral y comparativa final"},
}

st.set_page_config(page_title=f"{BRAND['name']}", layout="wide")

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
    * {{ font-family: 'Inter', -apple-system, sans-serif !important; }}
    html, body, .stApp, .stAppViewContainer, section[data-testid="stApp"] {{
        background: {BRAND['bg']} !important;
        color: {BRAND['text']} !important;
        font-size: 1.1rem !important;
    }}
    .main .block-container {{
        background: {BRAND['bg']} !important;
        padding-top: 1.5rem !important;
    }}
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: {BRAND['primary']} !important;
        font-weight: 800 !important;
        font-size: 1.6rem !important;
    }}
    h1 {{ font-size: 2rem !important; }}
    p, li, .stMarkdown p, .stMarkdown li {{
        color: {BRAND['text']} !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }}
    .stButton > button {{
        background: {BRAND['primary']} !important;
        color: #0A192F !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.2s !important;
    }}
    .stButton > button:hover {{ background: {BRAND['primary_dark']} !important; color: #0A192F !important; }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 700 !important; color: {BRAND['primary']} !important; font-size: 1.05rem !important; }}
    div[role="tabpanel"] {{ background: transparent !important; }}
    .stMetric {{
        background: {BRAND['card']} !important;
        padding: 1.2rem !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
        border: 1px solid #1E3A5F !important;
    }}
    .stMetric label, .stMetric .metric-label {{
        color: {BRAND['muted']} !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }}
    .stMetric .metric-value {{
        color: {BRAND['primary']} !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
    }}
    .stDataFrame {{ border-radius: 12px; overflow: hidden; }}
    div[data-testid="stDecoration"] {{
        background: linear-gradient(90deg, {BRAND['primary']}, {BRAND['primary_light']}) !important;
    }}
    section[data-testid="stSidebar"] > div:first-child {{
        background: {BRAND['card']} !important;
        border-right: 1px solid #1E3A5F !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown p {{
        color: {BRAND['text']} !important;
        font-weight: 600 !important;
    }}
    .row-widget.stSelectbox label, .row-widget.stNumberInput label, .row-widget.stSlider label {{
        color: {BRAND['primary']} !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }}
    .stSelectbox div[data-baseweb="select"] span, .stNumberInput input, .stSlider div[data-baseweb="slider"] {{
        font-size: 1.05rem !important;
    }}
    div[data-testid="stExpander"] {{
        background: {BRAND['card']} !important;
        border-radius: 12px !important;
        border: 1px solid #1E3A5F !important;
        margin-bottom: 0.5rem !important;
    }}
    div[data-testid="stExpander"] summary {{
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }}
    .stTabs {{
        background: transparent !important;
    }}
    .stAlert {{
        background: {BRAND['card']} !important;
        border: 1px solid #1E3A5F !important;
        border-radius: 12px !important;
        color: {BRAND['text']} !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }}
    .stTable {{
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 12px;
        overflow: hidden;
    }}
    .stTable th {{
        background: {BRAND['primary_dark']} !important;
        color: #0A192F !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }}
    .stTable td {{
        background: {BRAND['card']} !important;
        color: {BRAND['text']} !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }}
    .stCheckbox label, .stRadio label {{
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: {BRAND['text']} !important;
    }}
    .st-br, .st-bv, .st-bw, .st-bx, .st-by, .st-bz {{
        color: {BRAND['text']} !important;
    }}
    hr {{
        border-color: #1E3A5F !important;
        border-width: 2px !important;
    }}
    caption, .stCaption, .stMarkdown caption {{
        color: {BRAND['muted']} !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }}
    .stDataFrame div[data-testid="StyledDataFrameDataCell"] {{
        font-size: 1rem !important;
        font-weight: 600 !important;
    }}
    .stProgress > div > div > div > div {{
        background-color: {BRAND['primary']} !important;
    }}
    div[data-testid="stInfo"] {{
        background: {BRAND['card']} !important;
        border-color: {BRAND['primary_dark']} !important;
    }}
    div[data-testid="stSuccess"] {{
        background: #0B2D26 !important;
        border-color: {BRAND['primary']} !important;
    }}
    div[data-testid="stWarning"] {{
        background: #2D1F0B !important;
        border-color: {BRAND['accent']} !important;
    }}
    div[data-testid="stError"] {{
        background: #2D0B0B !important;
        border-color: #FF5252 !important;
    }}
    .st-bq, .st-br, .st-bs, .st-bt, .st-bu, .st-bv, .st-bw, .st-bx, .st-by, .st-bz,
    .st-c0, .st-c1, .st-c2, .st-c3, .st-c4, .st-c5, .st-c6, .st-c7, .st-c8, .st-c9,
    .st-ca, .st-cb, .st-cc {{
        color: {BRAND['text']} !important;
    }}
    .stSelectbox div[data-baseweb="select"] {{
        background-color: {BRAND['card']} !important;
        border-color: #1E3A5F !important;
    }}
    .stSlider div[data-baseweb="slider"] div {{
        background-color: {BRAND['primary']} !important;
    }}
    div.stMarkdown div[data-testid="stMarkdownContainer"] p {{
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }}
    .st-caption, .stCaption, div[data-testid="stCaption"] {{
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: {BRAND['muted']} !important;
    }}
</style>
""", unsafe_allow_html=True)

if "enfoque" not in st.session_state:
    st.session_state.enfoque = "Conservador"

# ── Brand Header ────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem">
    <div style="background:linear-gradient(135deg,{BRAND['primary']},{BRAND['primary_dark']});
                width:55px;height:55px;border-radius:14px;
                display:flex;align-items:center;justify-content:center;
                font-size:1.6rem;color:#0A192F;font-weight:900;box-shadow:0 2px 12px rgba(100,255,218,0.3)">
        SC
    </div>
    <div>
        <h1 style="margin:0;font-size:2rem;letter-spacing:-0.5px">
            {BRAND['name']}
        </h1>
    </div>
</div>
""", unsafe_allow_html=True)

cols = st.columns(len(ENFOQUES))
for i, (name, meta) in enumerate(ENFOQUES.items()):
    with cols[i]:
        is_sel = st.session_state.enfoque == name
        if st.button(
            f"{meta['icon']} {name}",
            key=f"btn_{name}",
            use_container_width=True,
            type="primary" if is_sel else "secondary",
        ):
            if not is_sel:
                st.session_state.enfoque = name
                st.rerun()
        st.caption(meta["desc"])

st.divider()

# ============================================================
# ENFOQUE 1: CONSERVADOR
# ============================================================
if st.session_state.enfoque == "Conservador":
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Datos Originales vs Corrección", "🎯 Punto de Equilibrio Real",
        "📊 Estados Financieros Corregidos", "💵 Flujo de Efectivo", "📈 Métricas Clave"
    ])

    with tab1:
        st.header("Correcciones Aplicadas")
        st.markdown("""
        | Error | Corrección |
        |---|---|
        | PE inflado ~2x por fórmula errónea | PE = CF / MC correcto |
        | Depreciación tratada como cash outflow | Depreciación solo como gasto contable |
        | Sin G&A, seguros, mantenimiento, QC | Gastos reales de PyME fabril: 13.5% ventas |
        | Sin capital de trabajo | Working capital: 30 días de ventas |
        | Crecimiento 10.7% CAGR | Crecimiento conservador: 5% anual |
        | Interés del préstamo no deducido | Interés ~15.4% anual como gasto operativo |
        | 10 productos con misma demanda | Demanda ponderada por margen |
        """)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Costos Fijos Mensuales")
            v_m = get_sales(1) / 12
            cf = get_fixed_costs_monthly(v_m)
            cf_data = pd.DataFrame({
                "Concepto": ["Arrendamiento", "Servicios", "Publicidad", "Seguros", "Control Calidad",
                             "G&A (8%)", "Mantenimiento (1.5%)", "Insumos (1%)", "**TOTAL**"],
                "Original": ["$8,000", "$9,100", "$5,500", "$0", "$0", "$0", "$0", "$0", "$22,600"],
                "Corregido": [f"$8,000", f"$9,100", f"$5,500", f"$5,000", f"$4,000",
                              f"${v_m*0.08:,.0f}", f"${v_m*0.015:,.0f}", f"${v_m*0.01:,.0f}", f"${cf:,.0f}"]
            })
            st.dataframe(cf_data, use_container_width=True)
        with col2:
            st.subheader("Costos Variables por Litro")
            cvu_df = pd.DataFrame({
                "Producto": list(CVU_ORIG.keys()),
                "CVU Original": [f"${v:.2f}" for v in CVU_ORIG.values()],
                "CVU Real (recetas)": [f"${CVU_ORIG[p]:.2f}" for p in CVU_ORIG],
            })
            st.dataframe(cvu_df, use_container_width=True)

    with tab2:
        st.header("Punto de Equilibrio Real")
        anio = st.selectbox("Año", [1, 2, 3, 4, 5], key="be_anio_cons")
        be = calc_break_even(anio, CVU_ORIG, True)
        ventas = get_sales(anio)
        vol = get_volume_liters(anio)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("PE Correcto (L/mes)", f"{be['be_units']:,.0f}")
        col2.metric("PE Original (L/mes)", f"{be['be_units']*2.09:,.0f}")
        col3.metric("Producción Real (L/mes)", f"{vol/12:,.0f}")
        col4.metric("Margen Seguridad", f"{be['margin_safety']:.1f}%")
        fig = go.Figure()
        meses = list(range(1, 13))
        ing_mensual = ventas / 12
        cf_m = be['cf_mensual']
        cv_m = be['cvu_prom'] * (vol / 12)
        cost_total_m = cf_m + cv_m
        fig.add_trace(go.Scatter(x=meses, y=[ing_mensual]*12, mode='lines+markers',
                                 name='Ingresos', line=dict(color='green', width=3)))
        fig.add_trace(go.Scatter(x=meses, y=[cost_total_m]*12, mode='lines+markers',
                                 name='Costos Totales', line=dict(color='red', width=3)))
        fig.add_trace(go.Scatter(x=meses, y=[cf_m]*12, mode='lines',
                                 name='Costos Fijos', line=dict(color='orange', width=2, dash='dash')))
        fig.add_hline(y=be['be_revenue'], line_dash="dot", line_color="purple",
                      annotation_text=f"PE: ${be['be_revenue']:,.0f}")
        fig.update_layout(title="Punto de Equilibrio Mensual", yaxis_title="$",
                          xaxis_title="Mes", height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Margen de Contribución por Producto (Corregido)")
        mc_data = []
        for p in PVU:
            mc = PVU[p] - CVU_ORIG[p]
            mc_data.append({"Producto": p, "PVU": PVU[p], "CVU Real": CVU_ORIG[p],
                             "MC": mc, "MC%": f"{mc/PVU[p]*100:.1f}%"})
        st.dataframe(pd.DataFrame(mc_data).sort_values("MC", ascending=False), use_container_width=True)

    with tab3:
        st.header("Estado de Resultados Proyectado (5 años)")
        st.markdown("**Crecimiento:** 5% anual | **Incluye:** G&A, seguros, mantenimiento, QC, depreciación")
        years = list(range(1, 6))
        rows = []
        for y in years:
            cf_data = calc_income(y, 0.05, CVU_ORIG, True, True)
            rows.append({
                "Año": y, "Ventas": cf_data["ventas"], "CV": cf_data["cv"],
                "Nómina": cf_data["nomina"], "Renta": cf_data["renta"],
                "Servicios": cf_data["servicios"], "Publicidad": cf_data["publicidad"],
                "G&A": cf_data["ga"], "Seguros": cf_data["seguros"],
                "Mantenimiento": cf_data["mantenimiento"], "QC": cf_data["qc"],
                "Insumos": cf_data["insumos"], "Depreciación": cf_data["depreciacion"],
                "EBITDA": cf_data["ebitda"], "EBIT": cf_data["ebit"]
            })
        df_is = pd.DataFrame(rows)
        fmt = {c: "${:,.0f}" for c in df_is.columns if c != "Año"}
        st.dataframe(df_is.style.format(fmt), use_container_width=True, hide_index=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=years, y=df_is["Ventas"], name="Ventas"))
        fig.add_trace(go.Bar(x=years, y=df_is["EBITDA"], name="EBITDA"))
        fig.add_trace(go.Bar(x=years, y=df_is["EBIT"], name="EBIT"))
        fig.update_layout(title="Ventas vs EBITDA vs EBIT", barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.header("Flujo de Efectivo Libre Corregido")
        st.markdown("**FCFF = EBIT×(1-t) + Depreciación - Capex - ΔWorking Capital**")
        años = list(range(1, 6))
        fcff = []
        working_caps = []
        for y in años:
            cf = calc_income(y, 0.05, CVU_ORIG, True, True)
            tax = cf["ebit"] * 0.30
            depr = cf["depreciacion"]
            capex = 252000 if y == 1 else 0
            wc_prev = get_sales(y-1) / 12 if y > 1 else INVERSION_INICIAL * 0.15
            wc_curr = get_sales(y) / 12
            delta_wc = wc_curr - wc_prev if y > 1 else wc_curr
            fcf = cf["ebit"] - tax + depr - capex - delta_wc
            fcff.append(fcf)
        loan = 400000
        loan_payments = [257434, 250796, 0, 0, 0]
        net_equity = [fcff[i] + (loan if i == 0 else 0) - loan_payments[i] for i in range(5)]
        cf_df = pd.DataFrame({
            "Año": años, "FCFF (Empresa)": fcff,
            "Préstamo": [400000, 0, 0, 0, 0],
            "Pago Préstamo": loan_payments,
            "Flujo Neto al Inversionista": net_equity
        })
        st.dataframe(cf_df.style.format("${:,.0f}"), use_container_width=True, hide_index=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=años, y=fcff, name="FCFF"))
        fig.add_trace(go.Scatter(x=años, y=net_equity, mode='lines+markers',
                                 name="Flujo Neto al Inversionista", line=dict(color='gold', width=3)))
        fig.update_layout(title="Flujo de Caja Libre por Año", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.header("Métricas de Rentabilidad")
        fcf_list = []
        for y in range(1, 6):
            cf = calc_income(y, 0.05, CVU_ORIG, True, True)
            tax = cf["ebit"] * 0.30
            depr = cf["depreciacion"]
            capex = 252000 if y == 1 else 0
            wc = get_sales(y) / 12 if y == 1 else 0
            fcf = cf["ebit"] - tax + depr - capex - wc
            fcf_list.append(fcf)
        investment = INVERSION_INICIAL
        npv_val = calc_npv(fcf_list, investment)
        irr_val = calc_irr(fcf_list, investment)
        payback_meses = calc_payback(fcf_list, investment)
        roi_5y = calc_roi(fcf_list, investment)
        pi = calc_pi(fcf_list, investment)

        col1, col2, col3 = st.columns(3)
        col1.metric("VAN (21% descuento)", f"${npv_val:,.0f}")
        col2.metric("TIR", f"{irr_val*100:.1f}%")
        col3.metric("Payback", f"{payback_meses:.0f} meses" if payback_meses else "N/A")
        col4, col5, col6 = st.columns(3)
        col4.metric("ROI 5 años", f"{roi_5y:.1f}%")
        col5.metric("Índice Rentabilidad", f"{pi:.2f}")
        col6.metric("Inversión Inicial", f"${investment:,.0f}")

        comp = pd.DataFrame({
            "Métrica": ["Margen Operativo Año 1", "PE (L/mes)", "VAN (21%)", "TIR", "Payback", "ROI 5 años"],
            "Original": ["39.8%", "12,054", "$3,890,207", "143.2%", "9 meses", "844%"],
            "Corregido": [f"{cf['ebit']/cf['ventas']*100:.1f}%", f"{be['be_units']:,.0f}",
                          f"${npv_val:,.0f}", f"{irr_val*100:.1f}%",
                          f"{payback_meses:.0f} meses" if payback_meses else "N/A", f"{roi_5y:.1f}%"]
        })
        st.dataframe(comp, use_container_width=True, hide_index=True)
        st.info("**Conclusión:** El proyecto sigue siendo VIABLE pero con indicadores mucho más moderados.")


# ============================================================
# ENFOQUE 2: MERCADO
# ============================================================
elif st.session_state.enfoque == "Mercado":
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Benchmarks de Industria", "💰 Precios y Costos de Mercado",
        "📈 Proyección Realista", "💵 Flujo de Efectivo", "📉 Comparativa Final"
    ])

    with tab1:
        st.header("Comparables de la Industria de Limpieza")
        benchmarks = pd.DataFrame({
            "Métrica": ["Margen Bruto", "Margen EBITDA", "Margen Neto",
                         "Gastos G&A (% Ventas)", "Gastos Ventas (% Ventas)",
                         "Rotación Inventario (días)", "Ciclo Efectivo (días)",
                         "Crecimiento Anual Sector", "Capex / Ventas"],
            "Clorox": ["43%", "18%", "9%", "12%", "10%", "45", "35", "2%", "3%"],
            "Church & Dwight": ["45%", "22%", "12%", "11%", "9%", "50", "38", "4%", "2.5%"],
            "PyME México": ["35-50%", "10-18%", "5-12%", "8-15%", "5-10%", "30-60", "25-45", "3-8%", "2-5%"],
            "Smart Clean (Original)": ["67%", "39.8%", "27.9%", "0%", "2.5%", "0", "0", "10.7%", "9.7%"]
        })
        st.dataframe(benchmarks, use_container_width=True, hide_index=True)
        st.subheader("🔍 Hallazgos Clave")
        st.markdown("""
        - **Margen bruto del 67%** vs industria 43-45% → Costos variables subestimados
        - **Margen EBITDA de 39.8%** vs industria 10-22% → Ausencia de gastos operativos reales
        - **G&A en 0%** vs industria 8-15% → Sin gastos de administración
        - **Sin capital de trabajo** → Toda PyME real requiere 25-45 días de efectivo
        """)
        fig = go.Figure()
        categorias = ["Margen Bruto", "Margen EBITDA", "Margen Neto"]
        fig.add_trace(go.Bar(name="Smart Clean Original", x=categorias, y=[67, 39.8, 27.9], marker_color='royalblue'))
        fig.add_trace(go.Bar(name="Benchmark PyME MX", x=categorias, y=[42, 14, 8], marker_color='lightcoral'))
        fig.add_trace(go.Bar(name="Clorox", x=categorias, y=[43, 18, 9], marker_color='goldenrod'))
        fig.update_layout(title="Comparación de Márgenes", barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("Precios de Venta por Producto vs Competencia")
        st.markdown("Los precios actuales son razonables. El problema principal está en los COSTOS.")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Costos Variables por Producto")
            cvu_df = pd.DataFrame({
                "Producto": list(PVU.keys()),
                "PVU ($/L)": [f"${PVU[p]:.2f}" for p in PVU],
                "CVU Original": [f"${CVU_ORIG[p]:.2f}" for p in CVU_ORIG],
                "CVU Real (Receta)": [f"${CVU_RECETA[p]:.2f}" for p in CVU_RECETA],
                "MC Real": [f"${PVU[p] - CVU_RECETA[p]:.2f}" for p in PVU]
            })
            st.dataframe(cvu_df, use_container_width=True, hide_index=True)
        with col2:
            st.subheader("Margen de Contribución Real")
            fig = go.Figure()
            for p in PVU:
                fig.add_trace(go.Bar(name=p, x=[p], y=[PVU[p] - CVU_RECETA[p]]))
            fig.update_layout(title="MC por Producto ($/L)", height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        st.warning("""
        **Productos con margen bajo:** Lavatraestes (31%), Cloro (42%), Suavizante (32%).
        Necesitan re-precio o reformulación.
        """)

    with tab3:
        st.header("Proyección a 5 Años con Márgenes de Mercado")
        crecimiento_merc = st.slider("Crecimiento anual de ventas (%)", 0, 15, 6, 1, key="crec_merc")
        margen_benchmark = st.selectbox("Benchmark de margen EBITDA",
            ["PyME MX (14%)", "Clorox (18%)", "Church & Dwight (22%)"], key="bench_merc")
        target_ebitda = {"PyME MX (14%)": 0.14, "Clorox (18%)": 0.18, "Church & Dwight (22%)": 0.22}[margen_benchmark]

        years = list(range(1, 6))
        rows = []
        for y in years:
            ventas = get_sales(y) * (1 + crecimiento_merc/100) ** (y-1)
            vol = get_volume_liters(y) * (1 + crecimiento_merc/100) ** (y-1)
            cvu_prom = sum(CVU_ORIG[p] for p in CVU_ORIG) / len(CVU_ORIG)
            cv = cvu_prom * vol
            cf_total = get_fixed_costs_monthly(ventas/12) * 12
            ebitda = ventas - cv - cf_total
            ebitda_target = ventas * target_ebitda
            ajuste = ebitda - ebitda_target
            rows.append({"Año": y, "Ventas": ventas, "CV": cv, "CF_Total": cf_total,
                         "EBITDA": ebitda, "EBITDA_Target": ebitda_target, "Ajuste": ajuste})
        df_proy = pd.DataFrame(rows)
        st.dataframe(df_proy.style.format("${:,.0f}"), use_container_width=True, hide_index=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=df_proy["Ventas"], mode='lines+markers', name="Ventas", line=dict(width=3)))
        fig.add_trace(go.Scatter(x=years, y=df_proy["EBITDA"], mode='lines+markers', name="EBITDA Real", line=dict(width=3)))
        fig.add_trace(go.Scatter(x=years, y=df_proy["EBITDA_Target"], mode='lines',
                                 name=f"EBITDA Target ({margen_benchmark})",
                                 line=dict(dash='dot', color='red', width=2)))
        fig.update_layout(title="Proyección vs Benchmark de Mercado", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.header("Flujo de Efectivo con Estructura de Mercado")
        fcf_list_merc = []
        for y in years:
            ventas = get_sales(y) * (1 + crecimiento_merc/100) ** (y-1)
            vol = get_volume_liters(y) * (1 + crecimiento_merc/100) ** (y-1)
            cvu_prom = sum(CVU_ORIG[p] for p in CVU_ORIG) / len(CVU_ORIG)
            cv = cvu_prom * vol
            cf_total = get_fixed_costs_monthly(ventas/12) * 12
            depr = DEPRECIACION_MENSUAL * 12
            ebit = ventas - cv - cf_total - depr
            tax = ebit * 0.30
            capex = 252000 if y == 1 else 0
            wc = ventas / 12 * 1.2
            delta_wc = wc if y == 1 else wc - (get_sales(y-1) * (1 + crecimiento_merc/100) ** (y-2)) / 12 * 1.2
            fcf = ebit - tax + depr - capex - delta_wc
            fcf_list_merc.append(fcf)
        fcf_df = pd.DataFrame({"Año": years, "FCFF": fcf_list_merc})
        st.dataframe(fcf_df.style.format("${:,.0f}"), use_container_width=True, hide_index=True)
        inv_merc = INVERSION_INICIAL
        npv_merc = calc_npv(fcf_list_merc, inv_merc)
        irr_merc = calc_irr(fcf_list_merc, inv_merc)
        pb_merc = calc_payback(fcf_list_merc, inv_merc)
        roi_merc = calc_roi(fcf_list_merc, inv_merc)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("VAN", f"${npv_merc:,.0f}")
        col2.metric("TIR", f"{irr_merc*100:.1f}%")
        col3.metric("Payback", f"{pb_merc:.0f} meses" if pb_merc else "N/A")
        col4.metric("ROI 5a", f"{roi_merc:.1f}%")
        fig = go.Figure()
        fig.add_trace(go.Bar(x=years, y=fcf_list_merc, marker_color='green',
                             text=[f"${v:,.0f}" for v in fcf_list_merc], textposition='outside'))
        fig.update_layout(title="Flujo de Caja Libre por Año", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.header("Comparativa Final: Original vs Mercado")
        fcf_original = [608864, 614943, 907574, 1037578, 1182082]
        npv_orig = calc_npv(fcf_original, INVERSION_INICIAL)
        irr_orig = calc_irr(fcf_original, INVERSION_INICIAL)
        pb_orig = calc_payback(fcf_original, INVERSION_INICIAL)
        roi_orig = calc_roi(fcf_original, INVERSION_INICIAL)
        comparativa = pd.DataFrame({
            "Métrica": ["VAN (21%)", "TIR", "Payback", "ROI 5a", "Margen EBITDA Año 1"],
            "Original": [f"${npv_orig:,.0f}", f"{irr_orig*100:.1f}%",
                         f"{pb_orig:.0f} meses", f"{roi_orig:.1f}%", "39.8%"],
            "Corregido (Mercado)": [f"${npv_merc:,.0f}", f"{irr_merc*100:.1f}%",
                                    f"{pb_merc:.0f} meses" if pb_merc else "N/A",
                                    f"{roi_merc:.1f}%", f"{target_ebitda*100:.1f}%"],
            "Diferencia": [f"${npv_merc - npv_orig:,.0f}", f"{(irr_merc-irr_orig)*100:.1f}pp",
                           f"{pb_merc - pb_orig:.0f} meses" if pb_merc else "N/A",
                           f"{roi_merc - roi_orig:.1f}pp", f"{target_ebitda*100 - 39.8:.1f}pp"]
        })
        st.dataframe(comparativa, use_container_width=True, hide_index=True)
        st.info("**Conclusión:** El proyecto sigue atractivo pero con indicadores más modestos. La clave: controlar CV y gastos operativos.")


# ============================================================
# ENFOQUE 3: MONTE CARLO
# ============================================================
elif st.session_state.enfoque == "Monte Carlo":
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚙️ Parámetros", "📊 Resultados", "📈 Distribuciones",
        "🎯 Sensibilidad", "✅ Conclusiones"
    ])

    with tab1:
        st.header("Parámetros de la Simulación")
        col1, col2, col3 = st.columns(3)
        with col1:
            n_sim = st.slider("Número de simulaciones", 500, 10000, 3000, 500, key="mc_nsim")
            crec_m = st.slider("Crecimiento anual medio (%)", 2, 15, 6, 1, key="mc_crec_m")
            crec_s = st.slider("Desviación std crecimiento (%)", 1, 8, 3, 1, key="mc_crec_s")
        with col2:
            vc_mult = st.slider("Multiplicador costos variables", 0.8, 1.5, 1.05, 0.05, key="mc_vc_mult")
            vc_std = st.slider("Std dev costos variables (%)", 2, 15, 8, 1, key="mc_vc_std")
            dr_mc = st.slider("Tasa de descuento (%)", 10, 30, 21, 1, key="mc_dr") / 100
        with col3:
            fc_mult = st.slider("Multiplicador costos fijos", 0.8, 1.5, 1.10, 0.05, key="mc_fc_mult")
            d_cxc_mc = st.slider("Días cuentas por cobrar", 0, 60, 30, 5, key="mc_dias")
            tr_mc = st.slider("Tasa impositiva (%)", 20, 35, 30, 1, key="mc_tr") / 100

        ejecutar = st.button("▶️ Ejecutar Simulación Monte Carlo", type="primary", use_container_width=True)

    npv_arr = np.array([])
    irr_arr = np.array([])
    payback_arr = np.array([])
    roi_arr = np.array([])
    be_arr = np.array([])

    if ejecutar or st.session_state.get("mc_resultados"):
        if ejecutar:
            st.session_state["mc_resultados"] = True
            np.random.seed(42)
            npv_res = []; irr_res = []; pb_res = []; roi_res = []; be_res = []
            pbar = st.progress(0)
            stext = st.empty()

            for sim in range(n_sim):
                c = max(0, min(0.20, np.random.normal(crec_m/100, crec_s/100)))
                cv_m = max(0.6, min(1.8, np.random.normal(vc_mult, vc_std/100)))
                cf_m = max(0.8, min(1.5, np.random.normal(fc_mult, 0.05)))
                fcf_l = []; total_cv = 0; total_ventas = 0
                for y in range(1, 6):
                    ventas = get_sales(y) * (1 + c) ** (y-1)
                    vol = get_volume_liters(y) * (1 + c) ** (y-1)
                    cvu_b = sum(CVU_ORIG[p] for p in CVU_ORIG) / len(CVU_ORIG)
                    cv = cvu_b * vol * cv_m
                    total_cv += cv; total_ventas += ventas
                    v_m = ventas / 12
                    cf_mc = get_fixed_costs_monthly(v_m) * 12 * cf_m
                    depr = DEPRECIACION_MENSUAL * 12
                    ebit = ventas - cv - cf_mc - depr
                    tax = max(0, ebit * tr_mc)
                    capex = 252000 if y == 1 else 0
                    wc = ventas / 365 * d_cxc_mc
                    delta_wc = wc if y == 1 else wc - (get_sales(y-1) * (1 + c) ** (y-2)) / 365 * d_cxc_mc
                    fcf_l.append(ebit - tax + depr - capex - delta_wc)
                inv = INVERSION_INICIAL
                npv_res.append(sum(fcf / (1 + dr_mc) ** (i+1) for i, fcf in enumerate(fcf_l)))
                irr_res.append(calc_irr(fcf_l, inv))
                pb = calc_payback(fcf_l, inv)
                pb_res.append(pb if pb else 999)
                roi_res.append(calc_roi(fcf_l, inv))
                vm_p = total_ventas / 5 / 12
                cfm_p = get_fixed_costs_monthly(vm_p) * cf_m
                cvu_p = sum(CVU_ORIG[p] for p in CVU_ORIG) / len(CVU_ORIG) * cv_m
                pvu_p = sum(PVU[p] for p in PVU) / len(PVU)
                be = cfm_p / (pvu_p - cvu_p) if (pvu_p - cvu_p) > 0 else 99999
                be_res.append(be)
                if (sim + 1) % max(1, n_sim // 20) == 0:
                    pbar.progress((sim + 1) / n_sim)
                    stext.text(f"Simulación {sim+1:,} de {n_sim:,}...")
            pbar.progress(1.0)
            stext.text(f"✅ {n_sim:,} simulaciones completadas.")
            st.session_state["mc_npv"] = np.array(npv_res)
            st.session_state["mc_irr"] = np.array(irr_res)
            st.session_state["mc_pb"] = np.array(pb_res)
            st.session_state["mc_roi"] = np.array(roi_res)
            st.session_state["mc_be"] = np.array(be_res)

        npv_arr = st.session_state["mc_npv"]
        irr_arr = st.session_state["mc_irr"]
        payback_arr = st.session_state["mc_pb"]
        roi_arr = st.session_state["mc_roi"]
        be_arr = st.session_state["mc_be"]

        with tab2:
            st.subheader("Resultados Agregados")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("VAN Medio", f"${npv_arr.mean():,.0f}",
                        delta=f"P90: ${np.percentile(npv_arr, 10):,.0f}")
            col2.metric("TIR Media", f"{irr_arr.mean()*100:.1f}%",
                        delta=f"P90: {np.percentile(irr_arr, 10)*100:.1f}%")
            col3.metric("Payback Medio", f"{payback_arr.mean():.0f} meses",
                        delta=f"P90: {np.percentile(payback_arr, 90):.0f} meses")
            col4.metric("ROI Medio 5a", f"{roi_arr.mean():.1f}%",
                        delta=f"P10: {np.percentile(roi_arr, 10):.1f}%")
            st.dataframe(pd.DataFrame({
                "Métrica": ["VAN", "TIR", "Payback", "ROI 5a", "PE (L/mes)"],
                "Media": [f"${npv_arr.mean():,.0f}", f"{irr_arr.mean()*100:.1f}%",
                          f"{payback_arr.mean():.0f} meses", f"{roi_arr.mean():.1f}%", f"{be_arr.mean():,.0f}"],
                "Mediana": [f"${np.median(npv_arr):,.0f}", f"{np.median(irr_arr)*100:.1f}%",
                            f"{np.median(payback_arr):.0f} meses", f"{np.median(roi_arr):.1f}%", f"{np.median(be_arr):,.0f}"],
                "P10 (Optimista)": [f"${np.percentile(npv_arr, 90):,.0f}", f"{np.percentile(irr_arr, 90)*100:.1f}%",
                                    f"{np.percentile(payback_arr, 10):.0f} meses", f"{np.percentile(roi_arr, 90):.1f}%",
                                    f"{np.percentile(be_arr, 10):,.0f}"],
                "P90 (Pesimista)": [f"${np.percentile(npv_arr, 10):,.0f}", f"{np.percentile(irr_arr, 10)*100:.1f}%",
                                    f"{np.percentile(payback_arr, 90):.0f} meses", f"{np.percentile(roi_arr, 10):.1f}%",
                                    f"{np.percentile(be_arr, 90):,.0f}"],
                "Prob. Éxito (VAN>0)": [f"{(npv_arr > 0).mean()*100:.1f}%"] + [""]*4
            }), use_container_width=True, hide_index=True)

        with tab3:
            st.header("Distribuciones de Probabilidad")
            metric = st.selectbox("Seleccionar métrica", ["VAN", "TIR", "Payback", "ROI 5a", "PE Mensual"],
                                  key="mc_dist_metric")
            data_map = {"VAN": npv_arr/1000, "TIR": irr_arr*100, "Payback": payback_arr,
                        "ROI 5a": roi_arr, "PE Mensual": be_arr}
            label_map = {"VAN": "VAN (miles $)", "TIR": "TIR (%)", "Payback": "Payback (meses)",
                         "ROI 5a": "ROI 5 años (%)", "PE Mensual": "Punto de Equilibrio (L/mes)"}
            data = data_map[metric]
            fig = make_subplots(rows=1, cols=2, subplot_titles=[f"Histograma de {metric}", "Box Plot"])
            fig.add_trace(go.Histogram(x=data, nbinsx=50, marker_color='royalblue', name=metric), row=1, col=1)
            fig.add_vline(x=np.median(data), line_dash="dash", line_color="red",
                          annotation_text=f"Mediana: {np.median(data):.1f}", row=1, col=1)
            fig.add_trace(go.Box(y=data, name=metric, marker_color='royalblue', boxmean='sd'), row=1, col=2)
            fig.update_layout(title=f"Distribución de {metric} ({n_sim:,} simulaciones)", height=450, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            stats = pd.DataFrame({
                "Estadístico": ["Media", "Mediana", "Desv. Est.", "P5", "P25", "P75", "P95", "Mín", "Máx"],
                "Valor": [f"{np.mean(data):.2f}", f"{np.median(data):.2f}", f"{np.std(data):.2f}",
                          f"{np.percentile(data, 5):.2f}", f"{np.percentile(data, 25):.2f}",
                          f"{np.percentile(data, 75):.2f}", f"{np.percentile(data, 95):.2f}",
                          f"{np.min(data):.2f}", f"{np.max(data):.2f}"]
            })
            st.dataframe(stats, use_container_width=True, hide_index=True)

        with tab4:
            st.header("Análisis de Sensibilidad")
            st.markdown("Coeficiente de Correlación de Spearman entre cada parámetro y el VAN.")
            np.random.seed(123)
            n_sample = 500
            crecimientos = np.random.normal(crec_m/100, crec_s/100, n_sample)
            cv_mults = np.random.normal(vc_mult, vc_std/100, n_sample)
            cf_mults = np.random.normal(fc_mult, 0.05, n_sample)
            drs = np.random.uniform(0.12, 0.30, n_sample)
            dss = np.random.randint(0, 60, n_sample)
            npvs_mc = []
            for i in range(n_sample):
                c = max(0, min(0.20, crecimientos[i]))
                cv_m = max(0.6, min(1.8, cv_mults[i]))
                cf_m = max(0.8, min(1.5, cf_mults[i]))
                dr = drs[i]; ds = dss[i]
                fcf_l = []
                for y in range(1, 6):
                    ventas = get_sales(y) * (1 + c) ** (y-1)
                    vol = get_volume_liters(y) * (1 + c) ** (y-1)
                    cvu_b = sum(CVU_ORIG[p] for p in CVU_ORIG) / len(CVU_ORIG)
                    cv = cvu_b * vol * cv_m
                    v_m = ventas / 12
                    cf_mc = get_fixed_costs_monthly(v_m) * 12 * cf_m
                    depr = DEPRECIACION_MENSUAL * 12
                    ebit = ventas - cv - cf_mc - depr
                    tax = max(0, ebit * 0.30)
                    capex = 252000 if y == 1 else 0
                    wc = ventas / 365 * ds
                    delta_wc = wc if y == 1 else 0
                    fcf_l.append(ebit - tax + depr - capex - delta_wc)
                npvs_mc.append(sum(fcf / (1 + dr) ** (i+1) for i, fcf in enumerate(fcf_l)))
            npvs_mc = np.array(npvs_mc)
            sens_data = []
            for name, arr in [("Crecimiento", crecimientos), ("Costos Variables", cv_mults),
                              ("Costos Fijos", cf_mults), ("Tasa Descuento", drs), ("Días CxC", dss)]:
                corr, _ = spearmanr(arr, npvs_mc)
                sens_data.append({"Variable": name, "Correlación con VAN": corr})
            sens_df = pd.DataFrame(sens_data)
            st.dataframe(sens_df, use_container_width=True, hide_index=True)
            fig = go.Figure()
            colors = ['green' if r > 0 else 'red' for r in sens_df["Correlación con VAN"]]
            fig.add_trace(go.Bar(x=sens_df["Variable"], y=sens_df["Correlación con VAN"],
                                 marker_color=colors,
                                 text=[f"{r:.3f}" for r in sens_df["Correlación con VAN"]],
                                 textposition='outside'))
            fig.update_layout(title="Sensibilidad: Correlación de Variables con VAN", height=400)
            st.plotly_chart(fig, use_container_width=True)

        with tab5:
            st.header("Conclusiones y Recomendaciones")
            prob_exito = (npv_arr > 0).mean() * 100
            prob_irr_20 = (irr_arr > 0.20).mean() * 100
            prob_pb_24 = (payback_arr < 24).mean() * 100
            col1, col2, col3 = st.columns(3)
            col1.metric("Prob. VAN > 0", f"{prob_exito:.1f}%")
            col2.metric("Prob. TIR > 20%", f"{prob_irr_20:.1f}%")
            col3.metric("Prob. Payback < 24m", f"{prob_pb_24:.1f}%")
            if prob_exito > 80:
                st.success(f"✅ Alta probabilidad de éxito ({prob_exito:.0f}%).")
            elif prob_exito > 50:
                st.warning(f"⚠️ Probabilidad moderada ({prob_exito:.0f}%).")
            else:
                st.error(f"❌ Baja probabilidad ({prob_exito:.0f}%).")
            st.markdown(f"""
            Basado en {n_sim:,} simulaciones:
            1. **Variable más crítica**: Costos variables — la palanca más importante.
            2. **Escenario pesimista (P90)**: VAN de ${np.percentile(npv_arr, 10):,.0f}.
            3. **Capital de trabajo**: Reducir días de cobranza mejora significativamente el flujo.
            4. **Margen de contribución**: {(sum(PVU[p]-CVU_ORIG[p] for p in PVU)/len(PVU))/(sum(PVU[p] for p in PVU)/len(PVU))*100:.0f}% corregido.
            """)


# ============================================================
# ENFOQUE 4: CAPITAL DE TRABAJO
# ============================================================
elif st.session_state.enfoque == "Capital Trabajo":
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔄 Ciclo de Efectivo", "📅 Flujo Mensual Año 1",
        "🏦 Necesidades de Capital", "📊 Escenarios", "📈 Métricas Ajustadas"
    ])

    with tab1:
        st.header("Ciclo de Conversión de Efectivo")
        col1, col2, col3 = st.columns(3)
        with col1:
            d_inv_wc = st.slider("Días de inventario MP", 7, 45, 15, 1, key="wc_d_inv")
        with col2:
            d_cxc_wc = st.slider("Días de cuentas por cobrar", 0, 60, 30, 1, key="wc_d_cxc")
        with col3:
            d_cxp_wc = st.slider("Días de cuentas por pagar", 0, 45, 15, 1, key="wc_d_cxp")
        cce = d_inv_wc + d_cxc_wc - d_cxp_wc
        st.metric("Ciclo de Conversión de Efectivo (CCE)", f"{cce} días",
                  delta="Original: 0 días (no consideraban)")
        st.markdown(f"""
        **Impacto:** Por cada día de CCE se necesitan ${get_sales(1)/365:,.0f}.
        Con CCE de {cce} días: **${get_sales(1)/365*cce:,.0f}** de capital de trabajo requerido.
        """)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=["Inventario", "CxC", "CxC", "CxP", "CCE"],
                             y=[d_inv_wc, d_cxc_wc, 0, -d_cxp_wc, cce],
                             marker_color=['orange', 'red', 'red', 'green', 'blue'],
                             text=[f"{d_inv_wc}d", f"{d_cxc_wc}d", "", f"{d_cxp_wc}d", f"{cce}d"],
                             textposition='outside'))
        fig.update_layout(title="Ciclo de Conversión de Efectivo (días)", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("Flujo de Efectivo Mensual — Año 1 (Corregido)")
        st.markdown("Modelo con ramp-up realista y capital de trabajo.")
        ramp_up = st.slider("Meses hasta capacidad completa", 1, 12, 4, 1, key="wc_ramp")
        pago_contado = st.slider("% de clientes que pagan al contado", 0, 100, 20, 5, key="wc_pago")
        meses = list(range(1, 13))
        ventas_diarias_target = SALES_DATA[1]["litros_dia"]
        precio = SALES_DATA[1]["precio"]
        rows = []; cxc_acum = 0
        efectivo_acum = -INVERSION_INICIAL
        for m in meses:
            factor = min(1.0, m / ramp_up)
            litros_dia = ventas_diarias_target * factor
            dias_mes = 31 if m in [1,3,5,7,8,10,12] else 30 if m in [4,6,9,11] else 28
            ventas_mes = litros_dia * precio * dias_mes
            ventas_cobradas = ventas_mes * pago_contado / 100
            ventas_credito = ventas_mes - ventas_cobradas
            vol_litros = litros_dia * dias_mes
            cvu_prom = sum(CVU_ORIG[p] for p in CVU_ORIG) / len(CVU_ORIG)
            cv_mes = cvu_prom * vol_litros
            v_m = ventas_mes
            cf_mes = get_fixed_costs_monthly(v_m)
            total_egresos = cv_mes + cf_mes
            cobranza_anterior = cxc_acum * 0.5 if m > 1 else 0
            cxc_acum = cxc_acum + ventas_credito - cobranza_anterior if m > 1 else ventas_credito * 0.5
            ingreso_efectivo = ventas_cobradas + cobranza_anterior
            capex = 252000 if m == 1 else 0
            prestamo = 400000 if m == 1 else 0
            pago_prestamo = 257434/12 if m <= 12 else 0
            flujo_mes = ingreso_efectivo - total_egresos - capex + prestamo - pago_prestamo
            efectivo_acum += flujo_mes
            rows.append({"Mes": m, "Litros/día": f"{litros_dia:.0f}", "Ventas": ventas_mes,
                         "Ingreso Efectivo": ingreso_efectivo, "CV": cv_mes,
                         "CF": total_egresos - cv_mes, "Total Egresos": total_egresos,
                         "Flujo Neto": flujo_mes, "Efectivo Acum": efectivo_acum})
        df_mensual = pd.DataFrame(rows)
        fmt_m = {c: "${:,.0f}" for c in df_mensual.columns if c not in ["Mes", "Litros/día"]}
        st.dataframe(df_mensual.style.format(fmt_m), use_container_width=True, hide_index=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=meses, y=df_mensual["Flujo Neto"], name="Flujo Neto Mensual",
                             marker_color=['green' if x > 0 else 'red' for x in df_mensual["Flujo Neto"]]))
        fig.add_trace(go.Scatter(x=meses, y=df_mensual["Efectivo Acum"], mode='lines+markers',
                                 name="Efectivo Acumulado", line=dict(color='gold', width=3)), secondary_y=True)
        fig.add_hline(y=0, line_dash="dot", line_color="gray")
        fig.update_layout(title="Flujo de Efectivo Mensual Año 1", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("Necesidades de Capital de Trabajo por Año")
        years = list(range(1, 6))
        wc_data = []
        for y in years:
            ventas = get_sales(y)
            vol = get_volume_liters(y)
            cvu_prom = sum(CVU_ORIG[p] for p in CVU_ORIG) / len(CVU_ORIG)
            wc_inv = vol / 365 * d_inv_wc * cvu_prom
            wc_cxc = ventas / 365 * d_cxc_wc
            wc_cxp = vol / 365 * d_cxp_wc * cvu_prom
            wc_neto = wc_inv + wc_cxc - wc_cxp
            wc_data.append({"Año": y, "Ventas": ventas, "Inventario": wc_inv,
                            "CxC": wc_cxc, "CxP": wc_cxp, "WC Neto": wc_neto,
                            "ΔWC": wc_neto - wc_data[-1]["WC Neto"] if y > 1 else wc_neto})
        df_wc = pd.DataFrame(wc_data)
        st.dataframe(df_wc.style.format("${:,.0f}"), use_container_width=True, hide_index=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=years, y=df_wc["WC Neto"], name="Capital de Trabajo Neto", marker_color='purple'))
        fig.add_trace(go.Scatter(x=years, y=df_wc["ΔWC"], mode='lines+markers',
                                 name="Inversión Adicional en WC", line=dict(color='orange', width=3)))
        fig.update_layout(title="Evolución del Capital de Trabajo", height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.warning(f"Impacto total: Año 1 ${df_wc['WC Neto'].iloc[0]:,.0f}, Año 5 ${df_wc['WC Neto'].iloc[-1]:,.0f}. "
                   f"El modelo ORIGINAL ignoró TODO esto.")

    with tab4:
        st.header("Escenarios de Capital de Trabajo")
        escenarios = [("Óptimo", 7, 15, 30), ("Normal", 15, 30, 15),
                      ("Pesimista", 30, 45, 7), ("Original (sin WC)", 0, 0, 0)]
        esc_results = []
        for esc_name, d_inv, d_cxc, d_cxp in escenarios:
            fcf_list = []
            for y in range(1, 6):
                ventas = get_sales(y)
                vol = get_volume_liters(y)
                cvu_prom = sum(CVU_ORIG[p] for p in CVU_ORIG) / len(CVU_ORIG)
                cv = cvu_prom * vol
                v_m = ventas / 12
                cf = get_fixed_costs_monthly(v_m) * 12
                depr = DEPRECIACION_MENSUAL * 12
                ebit = ventas - cv - cf - depr
                tax = ebit * 0.30
                capex = 252000 if y == 1 else 0
                wc_inv = vol / 365 * d_inv * cvu_prom
                wc_cxc = ventas / 365 * d_cxc
                wc_cxp = vol / 365 * d_cxp * cvu_prom
                wc_neto_esc = wc_inv + wc_cxc - wc_cxp
                delta_wc = wc_neto_esc if y == 1 else wc_neto_esc - prev_wc
                prev_wc = wc_neto_esc
                fcf_list.append(ebit - tax + depr - capex - delta_wc)
            npv_val = calc_npv(fcf_list, INVERSION_INICIAL)
            irr_val = calc_irr(fcf_list, INVERSION_INICIAL)
            payback = calc_payback(fcf_list, INVERSION_INICIAL)
            roi_val = calc_roi(fcf_list, INVERSION_INICIAL)
            esc_results.append({"Escenario": esc_name, "VAN": npv_val, "TIR": irr_val,
                                "Payback": payback, "ROI": roi_val})
        df_esc = pd.DataFrame(esc_results)
        st.dataframe(df_esc.style.format({"VAN": "${:,.0f}", "TIR": "{:.1%}",
                                           "Payback": "{:.0f} meses", "ROI": "{:.1f}%"}),
                     use_container_width=True, hide_index=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[e["Escenario"] for e in esc_results],
                             y=[e["VAN"] for e in esc_results],
                             marker_color=['green', 'blue', 'orange', 'red'],
                             text=[f"${e['VAN']:,.0f}" for e in esc_results], textposition='outside'))
        fig.update_layout(title="VAN por Escenario de Capital de Trabajo", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.header("Métricas Ajustadas por Capital de Trabajo")
        escenario_wc = st.selectbox("Escenario de WC para métricas finales",
            ["Normal (15-30-15)", "Óptimo (7-15-30)", "Pesimista (30-45-7)"], key="wc_esc_final")
        d_inv_f, d_cxc_f, d_cxp_f = {"Normal (15-30-15)": (15, 30, 15),
                                       "Óptimo (7-15-30)": (7, 15, 30),
                                       "Pesimista (30-45-7)": (30, 45, 7)}[escenario_wc]
        fcf_list = []
        for y in range(1, 6):
            ventas = get_sales(y)
            vol = get_volume_liters(y)
            cvu_prom = sum(CVU_ORIG[p] for p in CVU_ORIG) / len(CVU_ORIG)
            cv = cvu_prom * vol
            v_m = ventas / 12
            cf = get_fixed_costs_monthly(v_m) * 12
            depr = DEPRECIACION_MENSUAL * 12
            ebit = ventas - cv - cf - depr
            tax = ebit * 0.30
            capex = 252000 if y == 1 else 0
            wc_inv = vol / 365 * d_inv_f * cvu_prom
            wc_cxc = ventas / 365 * d_cxc_f
            wc_cxp = vol / 365 * d_cxp_f * cvu_prom
            wc_neto_f = wc_inv + wc_cxc - wc_cxp
            delta_wc = wc_neto_f if y == 1 else wc_neto_f - prev_wc_f
            prev_wc_f = wc_neto_f
            fcf_list.append(ebit - tax + depr - capex - delta_wc)
        investment = INVERSION_INICIAL
        npv_wc = calc_npv(fcf_list, investment)
        irr_wc = calc_irr(fcf_list, investment)
        pb_wc = calc_payback(fcf_list, investment)
        roi_wc = calc_roi(fcf_list, investment)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("VAN (21%)", f"${npv_wc:,.0f}")
        col2.metric("TIR", f"{irr_wc*100:.1f}%")
        col3.metric("Payback", f"{pb_wc:.0f} meses" if pb_wc else "N/A")
        col4.metric("ROI 5a", f"{roi_wc:.1f}%")
        fcf_df = pd.DataFrame({"Año": list(range(1, 6)), "FCFF (sin WC)": [0.0]*5, "FCFF (con WC)": fcf_list})
        for y in range(5):
            raw = calc_income(y+1, 0.05, CVU_ORIG, True, True)
            tax = raw["ebit"] * 0.30
            fcf_sin_wc = raw["ebit"] - tax + raw["depreciacion"] - (252000 if y == 0 else 0)
            fcf_df.loc[y, "FCFF (sin WC)"] = fcf_sin_wc
        fig = go.Figure()
        fig.add_trace(go.Bar(x=list(range(1, 6)), y=fcf_df["FCFF (sin WC)"], name="Sin WC", marker_color='blue'))
        fig.add_trace(go.Bar(x=list(range(1, 6)), y=fcf_df["FCFF (con WC)"], name=f"Con WC ({escenario_wc})",
                             marker_color='orange'))
        fig.update_layout(title="FCFF: Sin Capital de Trabajo vs Con Capital de Trabajo", barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"**Conclusión:** Capital de trabajo realista ({d_inv_f}d inv, {d_cxc_f}d CxC, {d_cxp_f}d CxP): "
                   f"VAN ${npv_wc:,.0f}, TIR {irr_wc*100:.1f}%, Payback {pb_wc:.0f} meses, ROI {roi_wc:.1f}%.")


# ============================================================
# ENFOQUE 5: DASHBOARD INTEGRAL
# ============================================================
elif st.session_state.enfoque == "Dashboard":
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Comparativa Original vs Corregido", "🎯 PE y Costos Reales",
        "📈 Estados Financieros", "💎 VAN / TIR / ROI", "✅ Dashboard Ejecutivo"
    ])

    with tab1:
        st.header("Comparativa Lado a Lado: Original vs Modelo Corregido")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Modelo Original")
            st.markdown("""
            | Concepto | Valor |
            |---|---|
            | Margen Bruto | 67.0% |
            | Margen EBITDA | 39.8% |
            | G&A | 0% |
            | Depreciación | Cash outflow |
            | Capital Trabajo | Ignorado |
            | Crecimiento | 10.7% CAGR |
            | PE | 12,054 L/mes |
            """)
        with col2:
            st.subheader("Modelo Corregido")
            st.markdown(f"""
            | Concepto | Valor |
            |---|---|
            | Margen Bruto | {100 - sum(CVU_ORIG[p] for p in CVU_ORIG)/len(CVU_ORIG)/sum(PVU[p] for p in PVU)*len(PVU)*100:.1f}% |
            | Margen EBITDA | Variable |
            | G&A | 8% ventas |
            | Depreciación | Gasto contable |
            | Capital Trabajo | 15-30-15 días |
            | Crecimiento | Ajustable |
            | PE | ~5,772 L/mes |
            """)
        st.subheader("Gráfico Radar Comparativo")
        categorias = ["Margen Bruto", "Margen Neto", "G&A (inverso)", "PE (inverso)", "TIR", "ROI 5a"]
        orig_norm = [100, 100, 100, 20/143*100, 100, 100]
        corr_norm = [55/67*100, 15/28*100, 92/100*100, 50/143*100, 55/143*100, 250/844*100]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=orig_norm + [orig_norm[0]], theta=categorias + [categorias[0]],
                                      fill='toself', name='Original', line_color='blue'))
        fig.add_trace(go.Scatterpolar(r=corr_norm + [corr_norm[0]], theta=categorias + [categorias[0]],
                                      fill='toself', name='Corregido', line_color='orange'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                          title="Comparativa de Indicadores (normalizado)", height=500)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("Punto de Equilibrio y Costos Reales")
        anio = st.selectbox("Año", [1, 2, 3, 4, 5], key="be_anio_dash")
        incluir_ga = st.checkbox("Incluir gastos reales (G&A, seguros, etc.)", True, key="be_ga_dash")
        be = calc_break_even(anio, CVU_ORIG, incluir_ga)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("PE (L/mes)", f"{be['be_units']:,.0f}")
        col2.metric("PE ($/mes)", f"${be['be_revenue']:,.0f}")
        col3.metric("% Capacidad", f"{be['be_pct_capacity']:.1f}%")
        col4.metric("Margen Seguridad", f"{be['margin_safety']:.1f}%")
        st.subheader("Estructura de Costos Variables por Producto")
        prod_data = []
        for p in PVU:
            mc = PVU[p] - CVU_ORIG[p]
            prod_data.append({"Producto": p, "PVU": f"${PVU[p]:.2f}", "CVU": f"${CVU_ORIG[p]:.2f}",
                              "MC": f"${mc:.2f}", "MC%": f"{mc/PVU[p]*100:.1f}%"})
        st.dataframe(pd.DataFrame(prod_data), use_container_width=True, hide_index=True)
        st.subheader("Composición de Costos Fijos Mensuales")
        v_m = get_sales(anio) / 12
        cf = get_fixed_costs_monthly(v_m)
        cf_items = [("Arrendamiento", ARRENDAMIENTO), ("Servicios", SERVICIOS),
                    ("Publicidad", PUBLICIDAD), ("Seguros", SEGUROS),
                    ("Control Calidad", CONTROL_CALIDAD),
                    ("G&A (8%)", v_m * GA), ("Mantenimiento (1.5%)", v_m * MANTENIMIENTO),
                    ("Insumos (1%)", v_m * INSUMOS_OP)]
        fig = go.Figure(go.Waterfall(
            name="CF", orientation="v",
            measure=["relative"] * len(cf_items) + ["total"],
            x=[item[0] for item in cf_items] + ["Total"],
            y=[item[1] for item in cf_items] + [cf],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        fig.update_layout(title="Composición de Costos Fijos Mensuales", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("Estados Financieros 5 Años")
        crec_dash = st.slider("Crecimiento anual (%)", 0, 15, 5, 1, key="crec_dash_is") / 100
        years = list(range(1, 6))
        rows = []
        for y in years:
            cf = calc_income(y, crec_dash, CVU_ORIG, True, True)
            rows.append({"Concepto": f"Año {y}", "Ventas": cf["ventas"],
                         "Costo Variable": cf["cv"], "Margen Bruto": cf["ventas"] - cf["cv"],
                         "Nómina": cf["nomina"], "Renta": cf["renta"],
                         "Servicios": cf["servicios"], "Publicidad": cf["publicidad"],
                         "G&A": cf["ga"], "Seguros": cf["seguros"],
                         "Mantenimiento": cf["mantenimiento"], "QC": cf["qc"],
                         "Insumos": cf["insumos"], "Depreciación": cf["depreciacion"],
                         "EBITDA": cf["ebitda"], "EBIT": cf["ebit"]})
        df = pd.DataFrame(rows).T
        df.columns = [f"Año {i+1}" for i in range(5)]
        st.dataframe(df.iloc[1:].style.format("${:,.0f}"), use_container_width=True)
        fig = go.Figure()
        for metric, color in [("EBITDA", "green"), ("EBIT", "blue")]:
            vals = [calc_income(y, crec_dash, CVU_ORIG, True, True)[metric.lower()] for y in years]
            pcts = [v / calc_income(y, crec_dash, CVU_ORIG, True, True)["ventas"] * 100 for v, y in zip(vals, years)]
            fig.add_trace(go.Scatter(x=years, y=pcts, mode='lines+markers', name=f"Margen {metric}", line=dict(width=3)))
        fig.update_layout(title="Evolución de Márgenes (%)", yaxis_title="%", xaxis_title="Año", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.header("Cálculo de VAN, TIR, ROI — Con Todos los Ajustes")
        col1, col2, col3 = st.columns(3)
        with col1:
            d_inv_d = st.slider("Días inventario", 0, 45, 15, 1, key="dash_d_inv")
        with col2:
            d_cxc_d = st.slider("Días CxC", 0, 60, 30, 1, key="dash_d_cxc")
        with col3:
            d_cxp_d = st.slider("Días CxP", 0, 45, 15, 1, key="dash_d_cxp")
        tasa_desc_d = st.slider("Tasa de descuento (%)", 10, 30, 21, 1, key="dash_tasa") / 100
        crec_final_d = st.slider("Crecimiento anual (%)", 0, 15, 5, 1, key="dash_crec") / 100

        fcf_list_d = []
        for y in range(1, 6):
            ventas = get_sales(y) * (1 + crec_final_d) ** (y-1)
            vol = get_volume_liters(y) * (1 + crec_final_d) ** (y-1)
            cvu_prom = sum(CVU_ORIG[p] for p in CVU_ORIG) / len(CVU_ORIG)
            cv = cvu_prom * vol
            v_m = ventas / 12
            cf = get_fixed_costs_monthly(v_m) * 12
            depr = DEPRECIACION_MENSUAL * 12
            ebit = ventas - cv - cf - depr
            tax = ebit * 0.30
            capex = 252000 if y == 1 else 0
            wc_inv = vol / 365 * d_inv_d * cvu_prom
            wc_cxc = ventas / 365 * d_cxc_d
            wc_cxp = vol / 365 * d_cxp_d * cvu_prom
            wc_neto_d = wc_inv + wc_cxc - wc_cxp
            delta_wc = wc_neto_d if y == 1 else wc_neto_d - prev_wc_d
            prev_wc_d = wc_neto_d
            fcf_list_d.append(ebit - tax + depr - capex - delta_wc)

        investment_d = INVERSION_INICIAL
        npv_d = calc_npv(fcf_list_d, investment_d, tasa_desc_d)
        irr_d = calc_irr(fcf_list_d, investment_d)
        pb_d = calc_payback(fcf_list_d, investment_d)
        roi_d = calc_roi(fcf_list_d, investment_d)
        pi_d = calc_pi(fcf_list_d, investment_d, tasa_desc_d)

        fcf_orig = [608864, 614943, 907574, 1037578, 1182082]
        npv_orig_d = calc_npv(fcf_orig, 460834, 0.21)
        irr_orig_d = calc_irr(fcf_orig, 460834)
        pb_orig_d = calc_payback(fcf_orig, 460834)
        roi_orig_d = calc_roi(fcf_orig, 460834)

        st.subheader("Flujo de Caja Libre")
        fcf_df_d = pd.DataFrame({"Año": list(range(1, 6)), "FCFF": fcf_list_d})
        st.dataframe(fcf_df_d.style.format("${:,.0f}"), use_container_width=True, hide_index=True)

        st.subheader("Métricas de Rentabilidad")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("VAN", f"${npv_d:,.0f}", delta=f"Original: ${npv_orig_d:,.0f}")
            st.metric("TIR", f"{irr_d*100:.1f}%", delta=f"Original: {irr_orig_d*100:.1f}%")
            st.metric("Payback", f"{pb_d:.0f} meses" if pb_d else "N/A", delta=f"Original: {pb_orig_d:.0f} meses")
        with col2:
            st.metric("ROI 5 años", f"{roi_d:.1f}%", delta=f"Original: {roi_orig_d:.1f}%")
            st.metric("Índice Rentabilidad", f"{pi_d:.2f}", delta="> 1 = viable")
            st.metric("Inversión Inicial", f"${investment_d:,.0f}")

        fig = go.Figure()
        fig.add_trace(go.Bar(x=list(range(1, 6)), y=fcf_list_d, name="FCFF Corregido", marker_color='green'))
        fig.add_trace(go.Bar(x=list(range(1, 6)), y=fcf_orig, name="FCFF Original (inflado)",
                             marker_color='gray', opacity=0.5))
        fig.update_layout(title="Comparación FCFF: Original vs Corregido", barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.header("Dashboard Ejecutivo")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.markdown("### 📈 VAN")
            st.markdown(f"## ${npv_d:,.0f}")
            st.markdown(f"<span style='color: {'green' if npv_d > 0 else 'red'}'>{'✅' if npv_d > 0 else '❌'} {'ACEPTABLE' if npv_d > 0 else 'RECHAZAR'}</span>", unsafe_allow_html=True)
        with kpi2:
            st.markdown("### 📊 TIR")
            st.markdown(f"## {irr_d*100:.1f}%")
            st.markdown(f"<span style='color: {'green' if irr_d > tasa_desc_d else 'red'}'>{'✅' if irr_d > tasa_desc_d else '❌'} {'Supera costo de capital' if irr_d > tasa_desc_d else 'No supera'}</span>", unsafe_allow_html=True)
        with kpi3:
            st.markdown("### ⏱ Payback")
            st.markdown(f"## {pb_d:.0f} meses" if pb_d else "N/A")
            st.markdown(f"<span style='color: {'green' if pb_d and pb_d < 36 else 'orange' if pb_d and pb_d < 60 else 'red'}'>{'✅' if pb_d and pb_d < 36 else '⚠️'} Recuperación {'rápida' if pb_d and pb_d < 36 else 'moderada'}</span>", unsafe_allow_html=True)
        with kpi4:
            st.markdown("### 💰 ROI 5a")
            st.markdown(f"## {roi_d:.1f}%")
            st.markdown(f"<span style='color: {'green' if roi_d > 100 else 'orange' if roi_d > 50 else 'red'}'>{'✅' if roi_d > 100 else '⚠️'} {'Alto retorno' if roi_d > 100 else 'Retorno moderado'}</span>", unsafe_allow_html=True)

        st.subheader("Resumen Ejecutivo")
        st.markdown(f"""
        **SMART CLEAN** — Planta de limpieza industrial, Ahome, Sinaloa.
        | Métrica | Valor | Interpretación |
        |---|---|---|
        | Inversión Inicial | ${investment_d:,.0f} | Mobiliario, equipo, instalación |
        | VAN ({tasa_desc_d*100:.0f}% desc.) | ${npv_d:,.0f} | {"Genera valor" if npv_d > 0 else "Destruye valor"} |
        | TIR | {irr_d*100:.1f}% | {"Excede" if irr_d > tasa_desc_d else "No alcanza"} costo capital {tasa_desc_d*100:.0f}% |
        | Payback | {pb_d:.0f} meses | Recuperación de inversión |
        | ROI 5 años | {roi_d:.1f}% | Retorno total en 5 años |
        | PE (Año 1) | {calc_break_even(1, CVU_ORIG, True)['be_units']:,.0f} L/mes | Punto de equilibrio |
        """)
        st.subheader("Recomendaciones Finales")
        st.markdown("""
        | Prioridad | Acción | Impacto |
        |---|---|---|
        | 🔴 Alta | Negociar precios de materia prima | -15% CV = +$128K EBITDA/año |
        | 🔴 Alta | Política de cobranza: máx 15d contado, 30d crédito | Reduce WC en ~$80K |
        | 🟡 Media | Reformular Lavatraestes (CV más alto) | Mejora margen general |
        | 🟡 Media | Diversificar clientes | Reduce riesgo |
        | 🟢 Baja | Evaluar expansión a consumo masivo | Crecimiento adicional |
        """)
