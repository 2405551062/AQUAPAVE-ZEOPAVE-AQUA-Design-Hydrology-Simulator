import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── Konfigurasi Halaman ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AQUAPAVE | Optimasi Desain",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Kustom ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .hero-banner {
    background: linear-gradient(135deg, #0a3d6b 0%, #1565C0 50%, #0288d1 100%);
    border-radius: 16px;
    padding: 40px 36px 32px;
    margin-bottom: 24px;
    color: white;
    position: relative;
    overflow: hidden;
  }
  .hero-banner::before {
    content: "💧";
    font-size: 160px;
    position: absolute;
    right: -20px; top: -20px;
    opacity: 0.08;
  }
  .hero-title { font-size: 2.6rem; font-weight: 700; margin: 0; letter-spacing: -1px; }
  .hero-sub   { font-size: 1.05rem; margin: 6px 0 0; opacity: 0.85; }
  .hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    margin-top: 14px;
    letter-spacing: 0.5px;
  }

  .kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin-bottom: 24px; }
  .kpi-card {
    background: white;
    border-radius: 12px;
    padding: 20px 18px 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border-top: 4px solid;
    text-align: center;
  }
  .kpi-card.biru   { border-color: #1565C0; }
  .kpi-card.teal   { border-color: #00897B; }
  .kpi-card.hijau  { border-color: #388E3C; }
  .kpi-card.oranye { border-color: #E65100; }
  .kpi-value { font-size: 1.8rem; font-weight: 700; color: #1a1a2e; line-height: 1; }
  .kpi-label { font-size: 0.78rem; color: #666; margin-top: 6px; }
  .kpi-icon  { font-size: 1.4rem; margin-bottom: 6px; }

  .section-head {
    font-size: 1.1rem; font-weight: 700;
    color: #0a3d6b;
    border-left: 4px solid #1565C0;
    padding-left: 12px;
    margin: 18px 0 14px;
  }
  .result-box2 {
    background: #141414;
    border-radius: 10px;
    padding: 18px 20px;
    border: 1px solid #141414;
    margin: 10px 0;
  }
  .result-box {
    background: linear-gradient(135deg,#E3F2FD,#E8F5E9);
    border-radius: 10px;
    padding: 18px 20px;
    border: 1px solid #BBDEFB;
    margin: 10px 0;
  }
  .result-box-dark {
    background: #1e2a3a;
    border-radius: 10px;
    padding: 18px 20px;
    border: 1px solid #2c3e50;
    margin: 10px 0;
    color: #ecf0f1;
  }
  .result-value { font-size: 2rem; font-weight: 700; color: #1565C0; }
  .result-label { font-size: 0.82rem; color: #555; }

  .badge-lulus { background:#E8F5E9; color:#2E7D32; border-radius:8px; padding:6px 14px; font-weight:600; font-size:0.9rem; }
  .badge-gagal { background:#FFEBEE; color:#C62828; border-radius:8px; padding:6px 14px; font-weight:600; font-size:0.9rem; }
  .badge-warn  { background:#FFF3E0; color:#E65100; border-radius:8px; padding:6px 14px; font-weight:600; font-size:0.9rem; }

  div[data-baseweb="tab-list"] { gap: 6px; }
  div[data-baseweb="tab"] { border-radius: 8px 8px 0 0; }

  .footer {
    text-align:center; color:#999; font-size:0.78rem;
    border-top:1px solid #eee; margin-top:40px; padding-top:16px;
  }
</style>
""", unsafe_allow_html=True)


# ─── Bilah Sisi ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("Asset/LogoUNUD.png", width=80)
    st.markdown("### ⚙️ Parameter Global")

    area_m2 = st.number_input(
        "Luas Area Perkerasan (m²)", 10.0, 10000.0, 1000.0, step=50.0
    )
    intensitas_hujan = st.slider(
        "Intensitas Hujan (mm/jam)", 10, 100, 50,
        help="Intensitas hujan rancangan untuk simulasi"
    )
    target_fc = st.selectbox(
        "Kelas Kuat Tekan Target",
        ["f'c 10 MPa", "f'c 12,5 MPa", "f'c 15 MPa", "f'c 17,5 MPa", "f'c 20 MPa"]
    )
    target_fc_val = float(target_fc.replace(",", ".").split()[1])

    st.divider()
    st.markdown("**📖 Tentang AQUAPAVE**")
    st.caption(
        "Platform optimasi digital untuk perkerasan berpori ZEOPAVE-AQUA. "
        "Dikembangkan oleh Teknik Sipil dan Teknologi Informasi, Universitas Udayana — Badung Festival Inovasi 2026."
    )
    st.caption(
        "Tim Peneliti: I Dewa Made Ari Praja Nugraha · "
        "Nyoman Gede Adi Mahardika · Ida Bagus Widnyana Manuaba"
    )


# ─── Banner Utama ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-title">💧 AQUAPAVE</div>
  <div class="hero-sub">
    Platform Optimasi Desain ZEOPAVE-AQUA —
    Perkerasan Berpori dengan Sistem Retensi Air untuk Mitigasi Banjir
  </div>
  <span class="hero-badge">🏆 Badung Festival Inovasi 2026 · Universitas Udayana</span>
</div>
""", unsafe_allow_html=True)

# Kartu KPI
st.markdown("""
<div class="kpi-grid">
  <div class="kpi-card biru">
    <div class="kpi-icon">🌊</div>
    <div class="kpi-value">39,7%</div>
    <div class="kpi-label">Retensi Air (Rata-rata Lab)</div>
  </div>
  <div class="kpi-card teal">
    <div class="kpi-icon">⚡</div>
    <div class="kpi-value">15,00 MPa</div>
    <div class="kpi-label">Kuat Tekan (Ekuivalen 28 Hari)</div>
  </div>
  <div class="kpi-card hijau">
    <div class="kpi-icon">♻️</div>
    <div class="kpi-value">85%</div>
    <div class="kpi-label">Potensi Optimasi Material</div>
  </div>
  <div class="kpi-card oranye">
    <div class="kpi-icon">🌿</div>
    <div class="kpi-value">≤15%</div>
    <div class="kpi-label">Substitusi Lumpur IPAL</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Tab ─────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🧮 Kalkulator Mix Design",
    "💧 Permeabilitas",
    "🏗️ Kuat Tekan",
    "🌊 Retensi Air",
    "🌿 Emisi CO₂",
    "📊 Dasbor Perbandingan",
    "💰 Efisiensi Biaya",
])


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — KALKULATOR MIX DESIGN
# ════════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown(
        '<div class="section-head">Optimizer Mix Design — ZEOPAVE-AQUA</div>',
        unsafe_allow_html=True
    )
    st.caption(
        "Rancang campuran beton optimal menggunakan substitusi lumpur IPAL, zeolit, dan hebel (AAC). "
        "Berdasarkan rasio pengikat:agregat = 1:3 (SNI 1974:2011)."
    )

    k1, k2 = st.columns([1, 1])

    with k1:
        st.markdown("**Komponen Pengikat (per 1 kg pengikat)**")
        ipal_pct   = st.slider(
            "Substitusi Lumpur IPAL (%)", 0, 25, 15,
            help="Menggantikan semen OPC. Optimal penelitian: 10–15%"
        )
        semen_pct  = 100 - ipal_pct

        st.markdown("**Komponen Agregat (per 3 kg agregat)**")
        sirtu_pct  = st.slider("Batu Sirtu (kasar 4–12,5 mm) %", 50, 100, 80)
        hebel_pct  = st.slider("Hebel AAC %", 0, 30, 15)
        zeolit_pct = 100 - sirtu_pct - hebel_pct
        if zeolit_pct < 0:
            st.warning("⚠️ Persentase Sirtu + Hebel melebihi 100%. Sesuaikan slider.")
            zeolit_pct = 0

        rasio_ab = st.slider("Faktor Air-Pengikat (f.a.b)", 0.30, 0.55, 0.40, 0.01)
        vol_batch = st.number_input("Volume Adukan (m³)", 0.1, 100.0, 1.0, 0.1)

    with k2:
        berat_satuan = 1850.0  # kg/m³ beton berpori tipikal
        massa_total  = berat_satuan * vol_batch

        massa_pengikat = massa_total / (1 + 3 + rasio_ab)
        massa_agregat  = 3 * massa_pengikat
        massa_air      = rasio_ab * massa_pengikat

        semen_kg  = massa_pengikat * (semen_pct  / 100)
        ipal_kg   = massa_pengikat * (ipal_pct   / 100)
        sirtu_kg  = massa_agregat  * (sirtu_pct  / 100)
        hebel_kg  = massa_agregat  * (hebel_pct  / 100)
        zeolit_kg = massa_agregat  * (zeolit_pct / 100)

        st.markdown("**📦 Hasil Mix Design**")
        tabel_mix = pd.DataFrame({
            "Material":        ["Semen OPC", "Lumpur IPAL", "Batu Sirtu", "Hebel AAC", "Zeolit", "Air"],
            "Massa (kg)":      [round(semen_kg,1), round(ipal_kg,1), round(sirtu_kg,1),
                                round(hebel_kg,1), round(zeolit_kg,1), round(massa_air,1)],
            "Proporsi (%)":    [
                round(semen_kg/massa_total*100,1),  round(ipal_kg/massa_total*100,1),
                round(sirtu_kg/massa_total*100,1),  round(hebel_kg/massa_total*100,1),
                round(zeolit_kg/massa_total*100,1), round(massa_air/massa_total*100,1),
            ],
        })
        st.dataframe(tabel_mix, width='stretch', hide_index=True)

        fig_pie = go.Figure(go.Pie(
            labels=tabel_mix["Material"],
            values=tabel_mix["Massa (kg)"],
            hole=0.42,
            marker_colors=["#1565C0","#00897B","#E65100","#7B1FA2","#F9A825","#0288D1"],
        ))
        fig_pie.update_layout(
            title="Komposisi Campuran",
            height=300, margin=dict(t=40,b=10,l=10,r=10),
            showlegend=True, legend=dict(font_size=11),
        )
        st.plotly_chart(fig_pie, width='stretch')

    st.divider()
    st.markdown("**Estimasi Porositas & Kemudahan Pengerjaan**")
    k3, k4, k5 = st.columns(3)

    porositas_dasar = 21.5
    efek_ipal    = -0.10 * ipal_pct
    efek_hebel   = +0.08 * hebel_pct
    efek_fab     = -5.0  * (rasio_ab - 0.40)
    porositas_est = np.clip(porositas_dasar + efek_ipal + efek_hebel + efek_fab, 12, 30)

    perm_est = 0.012 * (porositas_est ** 2.1) / 1000

    faktor_ipal = 1.0 if ipal_pct <= 15 else 1.0 - 0.04*(ipal_pct-15)
    fc_est = (20.5 - 0.35 * porositas_est) * faktor_ipal

    with k3:
        warna_p = "#1565C0" if 18 <= porositas_est <= 25 else "#E65100"
        st.markdown(f"""
        <div class="result-box">
          <div style="color:{warna_p}" class="result-value">{porositas_est:.1f}%</div>
          <div class="result-label">Estimasi Porositas<br><small>Target: 18–25%</small></div>
        </div>""", unsafe_allow_html=True)

    with k4:
        warna_k = "#00897B" if perm_est >= 0.45 else "#E65100"
        st.markdown(f"""
        <div class="result-box">
          <div style="color:{warna_k}" class="result-value">{perm_est:.3f}<span style="font-size:1rem"> cm/dtk</span></div>
          <div class="result-label">Estimasi Permeabilitas<br><small>Target: ≥ 0,45 cm/dtk</small></div>
        </div>""", unsafe_allow_html=True)

    with k5:
        warna_f = "#388E3C" if fc_est >= target_fc_val else "#C62828"
        status  = "✅ MEMENUHI" if fc_est >= target_fc_val else "❌ DI BAWAH TARGET"
        st.markdown(f"""
        <div class="result-box">
          <div style="color:{warna_f}" class="result-value">{fc_est:.1f}<span style="font-size:1rem"> MPa</span></div>
          <div class="result-label">Estimasi f'c (28 hari)<br><small>{status} vs {target_fc_val} MPa</small></div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — PERMEABILITAS
# ════════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown(
        '<div class="section-head">Permeabilitas — Metode Constant Head (SNI 2435:2008)</div>',
        unsafe_allow_html=True
    )
    st.caption("Hitung koefisien permeabilitas k dari pengukuran laboratorium menggunakan rumus Q·L / (A·h·t).")

    p1, p2 = st.columns(2)
    with p1:
        st.markdown("**Dimensi Benda Uji**")
        diam_mm = st.number_input("Diameter Benda Uji (mm)", 50.0, 300.0, 150.0)
        L_cm    = st.number_input("Panjang Benda Uji L (cm)", 5.0, 50.0, 15.0)
        h_cm    = st.number_input("Tinggi Muka Air Konstan h (cm)", 1.0, 100.0, 30.0)

        st.markdown("**Data Pengujian**")
        n_uji = st.number_input("Jumlah Pengujian", 1, 10, 3)
        Q_vals, t_vals = [], []
        for i in range(int(n_uji)):
            col_a, col_b = st.columns(2)
            with col_a:
                Q_vals.append(st.number_input(
                    f"Q{i+1} (cm³)", 0.0, 10000.0,
                    [320.0, 355.0, 340.0][i] if i < 3 else 330.0, key=f"Q{i}"
                ))
            with col_b:
                t_vals.append(st.number_input(
                    f"t{i+1} (dtk)", 1.0, 3600.0,
                    [60.0, 60.0, 60.0][i] if i < 3 else 60.0, key=f"t{i}"
                ))

    with p2:
        A_cm2  = np.pi * (diam_mm / 10 / 2) ** 2
        k_vals, baris = [], []
        for i in range(int(n_uji)):
            k_i = (Q_vals[i] * L_cm) / (A_cm2 * h_cm * t_vals[i])
            k_vals.append(k_i)
            baris.append({
                "Pengujian": f"Uji {i+1}",
                "Q (cm³)": Q_vals[i],
                "t (dtk)": t_vals[i],
                "k (cm/dtk)": round(k_i, 4),
            })

        k_rerata = np.mean(k_vals)
        k_std    = np.std(k_vals) if len(k_vals) > 1 else 0

        st.markdown(f"**Luas Penampang Benda Uji:** {A_cm2:.2f} cm²")
        st.dataframe(pd.DataFrame(baris), width='stretch', hide_index=True)

        badge_k = "badge-lulus" if k_rerata >= 0.45 else "badge-gagal"
        label_k = (
            "✅ MEMENUHI — Melampaui standar minimum beton berpori"
            if k_rerata >= 0.45
            else "❌ DI BAWAH — Standar minimum beton berpori: 0,45 cm/dtk"
        )
        st.markdown(f"""
        <div class="result-box" style="text-align:center">
          <div class="result-value">{k_rerata:.4f} cm/dtk</div>
          <div class="result-label">Permeabilitas Rerata (k) — Std Dev: ±{k_std:.4f}</div>
          <br><span class="{badge_k}">{label_k}</span>
        </div>""", unsafe_allow_html=True)

        referensi = {
            "Beton Konvensional": 0.001,
            "Min. Beton Berpori": 0.45,
            "Target ZEOPAVE-AQUA": 0.60,
            "Campuran Anda": k_rerata,
        }
        fig_k = go.Figure(go.Bar(
            x=list(referensi.keys()), y=list(referensi.values()),
            marker_color=["#EF5350","#FB8C00","#1565C0","#00897B"],
            text=[f"{v:.3f}" for v in referensi.values()],
            textposition="outside",
        ))
        fig_k.update_layout(
            title="Perbandingan Nilai k (cm/dtk)",
            height=320, yaxis_title="k (cm/dtk)",
            margin=dict(t=40,b=10,l=10,r=10),
        )
        st.plotly_chart(fig_k, width='stretch')


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — KUAT TEKAN
# ════════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown(
        '<div class="section-head">Kuat Tekan Beton — SNI 1974:2011</div>',
        unsafe_allow_html=True
    )
    st.caption("Hitung f'c dari beban uji silinder dan konversi ke kuat tekan ekuivalen 28 hari.")

    FAKTOR_UMUR = {7: 0.65, 14: 0.879, 21: 0.95, 28: 1.00, 56: 1.09, 90: 1.15}

    t1, t2 = st.columns(2)
    with t1:
        umur_uji  = st.selectbox("Umur Pengujian (hari)", [7, 14, 21, 28, 56, 90], index=1)
        diam_spec = st.number_input("Diameter Silinder (mm)", 100.0, 200.0, 150.0)
        n_benda   = st.number_input("Jumlah Benda Uji", 1, 10, 3)

        beban_kN, bobot_kg = [], []
        for i in range(int(n_benda)):
            ca, cb = st.columns(2)
            default_P = [235.2, 233.4, 230.4]
            default_W = [6.45, 6.80, 7.10]
            with ca:
                beban_kN.append(st.number_input(
                    f"Beban P{i+1} (kN)", 0.0, 2000.0,
                    default_P[i] if i < 3 else 230.0, key=f"P{i}"
                ))
            with cb:
                bobot_kg.append(st.number_input(
                    f"Berat W{i+1} (kg)", 0.0, 30.0,
                    default_W[i] if i < 3 else 6.5, key=f"W{i}"
                ))

    with t2:
        A_m2    = np.pi * (diam_spec / 1000 / 2) ** 2
        faktor  = FAKTOR_UMUR.get(umur_uji, 1.0)

        baris_fc, fc28_list = [], []
        for i in range(int(n_benda)):
            fc_umur = (beban_kN[i] * 1000) / (A_m2 * 1e6)
            fc28    = fc_umur / faktor
            fc28_list.append(fc28)
            baris_fc.append({
                "Benda Uji":                    f"BU-{i+1}",
                "Berat (kg)":                   bobot_kg[i],
                "Beban (kN)":                   beban_kN[i],
                f"f'c @ {umur_uji} hari (MPa)": round(fc_umur, 2),
                "f'c @ 28 hari (MPa)":          round(fc28, 2),
                "Luas (m²)":                    round(A_m2, 6),
            })

        fc28_rerata = np.mean(fc28_list)
        fc28_std    = np.std(fc28_list) if len(fc28_list) > 1 else 0

        st.dataframe(pd.DataFrame(baris_fc), width='stretch', hide_index=True)

        lulus_kuat = fc28_rerata >= target_fc_val
        badge_s    = "badge-lulus" if lulus_kuat else "badge-gagal"
        label_s    = (
            f"✅ MEMENUHI target f'c {target_fc_val} MPa"
            if lulus_kuat
            else f"❌ DI BAWAH target f'c {target_fc_val} MPa"
        )
        st.markdown(f"""
        <div class="result-box" style="text-align:center">
          <div class="result-value">{fc28_rerata:.2f} MPa</div>
          <div class="result-label">Rerata f'c ekuivalen @ 28 hari — Std Dev: ±{fc28_std:.2f} MPa</div>
          <br><span class="{badge_s}">{label_s}</span>
        </div>""", unsafe_allow_html=True)

        umur_plot = [7, 14, 21, 28, 56, 90]
        fc_prog   = [fc28_rerata * FAKTOR_UMUR[u] for u in umur_plot]
        fig_prog  = go.Figure()
        fig_prog.add_trace(go.Scatter(
            x=umur_plot, y=fc_prog, mode="lines+markers",
            name="Campuran Anda", line=dict(color="#1565C0", width=3),
            marker=dict(size=8, color="#1565C0"),
        ))
        fig_prog.add_hline(
            y=target_fc_val, line_dash="dash", line_color="#E65100",
            annotation_text=f"Target f'c = {target_fc_val} MPa",
        )
        fig_prog.update_layout(
            title="Perkembangan Kuat Tekan terhadap Umur",
            height=300, xaxis_title="Umur (hari)", yaxis_title="f'c (MPa)",
            margin=dict(t=40,b=10,l=10,r=10),
        )
        st.plotly_chart(fig_prog, width='stretch')

        st.markdown("**Faktor Konversi Umur (SNI)**")
        st.dataframe(
            pd.DataFrame({
                "Umur (hari)":       list(FAKTOR_UMUR.keys()),
                "Faktor Konversi":   list(FAKTOR_UMUR.values()),
            }),
            width='stretch', hide_index=True,
        )


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — RETENSI AIR
# ════════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown(
        '<div class="section-head">Simulator Sistem Retensi Air — ZEOPAVE-AQUA</div>',
        unsafe_allow_html=True
    )
    st.caption(
        "Simulasikan kemampuan ZEOPAVE-AQUA dalam mengurangi limpasan permukaan "
        "dan menyimpan air hujan untuk lokasi Anda."
    )

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("**Parameter Lokasi**")
        retensi_pct    = st.slider(
            "Tingkat Retensi (%)", 20.0, 60.0, 39.7, 0.1,
            help="Rata-rata lab: 39,7% (rentang 35–55%)"
        )
        kedalaman_mm   = st.number_input("Kedalaman Struktural Perkerasan (mm)", 100, 600, 300)
        tebal_zeolit   = st.slider("Tebal Lapisan Hebel–Zeolit (mm)", 50, 300, 150)
        koef_limpasan  = st.slider(
            "Koefisien Limpasan Sebelum ZEOPAVE (C)", 0.5, 0.95, 0.85,
            help="Perkotaan kedap air tipikal: 0,85–0,95"
        )
        durasi_jam     = st.number_input("Durasi Hujan (jam)", 0.25, 24.0, 1.0, 0.25)

    with r2:
        vol_hujan_m3       = (intensitas_hujan / 1000) * area_m2 * durasi_jam
        limpasan_konv      = vol_hujan_m3 * koef_limpasan
        vol_tersimpan      = vol_hujan_m3 * (retensi_pct / 100)
        limpasan_zeopave   = vol_hujan_m3 - vol_tersimpan
        reduksi_limpasan   = (limpasan_konv - limpasan_zeopave) / limpasan_konv * 100
        kapasitas_m3       = area_m2 * (tebal_zeolit / 1000) * 0.25

        st.markdown("**💧 Hasil Analisis Hidrologi**")
        st.markdown(f"""
        <div class="result-box2">
          <table style="width:100%;border-collapse:collapse">
            <tr><td>🌧️ Total Volume Hujan</td>
                <td style="text-align:right;font-weight:600">{vol_hujan_m3:.1f} m³</td></tr>
            <tr><td>🏗️ Limpasan Perkerasan Konvensional</td>
                <td style="text-align:right;font-weight:600;color:#C62828">{limpasan_konv:.1f} m³</td></tr>
            <tr><td>✅ Limpasan ZEOPAVE-AQUA</td>
                <td style="text-align:right;font-weight:600;color:#1565C0">{limpasan_zeopave:.1f} m³</td></tr>
            <tr><td>🌿 Volume Air Tersimpan</td>
                <td style="text-align:right;font-weight:600;color:#388E3C">{vol_tersimpan:.1f} m³</td></tr>
            <tr><td>📉 Reduksi Limpasan</td>
                <td style="text-align:right;font-weight:600;color:#00897B">{reduksi_limpasan:.1f}%</td></tr>
            <tr><td>🪨 Kapasitas Simpan Lapisan Zeolit</td>
                <td style="text-align:right;font-weight:600">{kapasitas_m3:.1f} m³</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        kapasitas_liter_jam = kapasitas_m3 * 1000 / durasi_jam
        st.markdown(f"""<div style="margin-top:10px">
        <span class="badge-lulus">💧 Kapasitas sistem: {kapasitas_liter_jam:,.0f} L/jam untuk {area_m2:.0f} m²</span>
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("**Kinerja Retensi vs Intensitas Hujan**")
    intensitas_range = np.arange(10, 110, 10)
    retensi_range    = np.clip(retensi_pct - 0.08 * (intensitas_range - intensitas_hujan), 25, 55)

    fig_ret = go.Figure()
    fig_ret.add_trace(go.Scatter(
        x=intensitas_range, y=retensi_range, mode="lines+markers", fill="tozeroy",
        name="Tingkat Retensi (%)", line=dict(color="#00897B", width=2.5),
        fillcolor="rgba(0,137,123,0.15)",
    ))
    fig_ret.add_vline(
        x=intensitas_hujan, line_dash="dash", line_color="#E65100",
        annotation_text=f"Rancangan: {intensitas_hujan} mm/jam",
    )
    fig_ret.update_layout(
        title="Tingkat Retensi vs Intensitas Hujan",
        xaxis_title="Intensitas Hujan (mm/jam)", yaxis_title="Tingkat Retensi (%)",
        height=300, margin=dict(t=40,b=10,l=10,r=10), yaxis_range=[0, 65],
    )
    st.plotly_chart(fig_ret, width='stretch')

    st.markdown("**Diagram Aliran Air (Sankey)**")
    fig_sankey = go.Figure(go.Sankey(
        node=dict(
            label=[
                "Curah Hujan",
                "Infiltrasi (ZEOPAVE)",
                "Simpanan Zeolit",
                "Perkolasi Alami",
                "Luapan ke Drainase",
                "Limpasan Konvensional",
            ],
            color=["#42A5F5","#26A69A","#66BB6A","#AB47BC","#FFA726","#EF5350"],
            pad=15, thickness=20,
        ),
        link=dict(
            source=[0, 0, 1, 1, 1],
            target=[1, 5, 2, 3, 4],
            value=[
                vol_tersimpan, limpasan_zeopave,
                min(vol_tersimpan * 0.55, kapasitas_m3),
                vol_tersimpan * 0.30,
                max(0, vol_tersimpan - kapasitas_m3 - vol_tersimpan * 0.30),
            ],
            color=[
                "rgba(38,166,154,0.4)","rgba(239,83,80,0.3)",
                "rgba(102,187,106,0.4)","rgba(171,71,188,0.3)","rgba(255,167,38,0.3)",
            ],
        ),
    ))
    fig_sankey.update_layout(
        title="Aliran Air Melalui Sistem ZEOPAVE-AQUA (m³)",
        height=340, margin=dict(t=40,b=10,l=10,r=10),
    )
    st.plotly_chart(fig_sankey, width='stretch')


# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — EMISI CO₂ & EFISIENSI MATERIAL
# ════════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown(
        '<div class="section-head">Emisi CO₂ & Efisiensi Material</div>',
        unsafe_allow_html=True
    )
    st.caption(
        "Kuantifikasi manfaat lingkungan dari substitusi lumpur IPAL "
        "dan optimasi material melalui platform AQUAPAVE."
    )

    e1, e2 = st.columns(2)
    with e1:
        st.markdown("**Parameter Emisi**")
        co2_opc   = st.number_input(
            "CO₂ per ton Semen OPC (ton CO₂/ton)", 0.7, 1.0, 0.85, 0.01,
            help="Tipikal: 0,8–0,9 ton CO₂/ton semen"
        )
        co2_ipal  = st.number_input(
            "CO₂ per ton Lumpur IPAL (ton CO₂/ton)", 0.0, 0.3, 0.05, 0.01,
            help="Lumpur IPAL memiliki karbon tertanam sangat kecil"
        )
        ipal_sub_pct     = st.slider("Substitusi IPAL (%)", 0, 25, 15)
        total_pengikat_t = st.number_input("Total Pengikat yang Dibutuhkan (ton)", 1.0, 1000.0, 10.0)
        hemat_uji_lab    = st.slider("Pengurangan Uji Lab oleh AQUAPAVE (%)", 50, 95, 85)

    with e2:
        co2_konv    = total_pengikat_t * co2_opc
        opc_terpakai = total_pengikat_t * (1 - ipal_sub_pct / 100)
        ipal_terpakai= total_pengikat_t * (ipal_sub_pct / 100)
        co2_zeopave = opc_terpakai * co2_opc + ipal_terpakai * co2_ipal
        co2_hemat   = co2_konv - co2_zeopave
        pct_reduksi_co2 = co2_hemat / co2_konv * 100

        uji_manual    = 20
        uji_aquapave  = uji_manual * (1 - hemat_uji_lab / 100)
        material_hemat_kg = (uji_manual - uji_aquapave) * 0.05 * 1850

        st.markdown(f"""
        <div class="result-box2">
          <table style="width:100%;border-collapse:collapse">
            <tr><th style="text-align:left;color:#FFF">Indikator</th>
                <th style="text-align:right;color:#FFF">Nilai</th></tr>
            <tr><td>🏭 CO₂ — Konvensional (100% OPC)</td>
                <td style="text-align:right;color:#C62828;font-weight:700">{co2_konv:.2f} ton CO₂</td></tr>
            <tr><td>✅ CO₂ — ZEOPAVE-AQUA</td>
                <td style="text-align:right;color:#388E3C;font-weight:700">{co2_zeopave:.2f} ton CO₂</td></tr>
            <tr><td>♻️ Reduksi Emisi CO₂</td>
                <td style="text-align:right;color:#00897B;font-weight:700">{co2_hemat:.2f} ton ({pct_reduksi_co2:.1f}%)</td></tr>
            <tr><td>🪣 Lumpur IPAL Dialihkan dari TPA</td>
                <td style="text-align:right;font-weight:700">{ipal_terpakai:.2f} ton</td></tr>
            <tr><td>🧪 Pengurangan Uji Lab (AQUAPAVE)</td>
                <td style="text-align:right;font-weight:700">{hemat_uji_lab}%</td></tr>
            <tr><td>⚖️ Material Dihemat (batch percobaan)</td>
                <td style="text-align:right;font-weight:700">{material_hemat_kg:,.0f} kg</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    e3, e4 = st.columns(2)

    with e3:
        fig_co2 = go.Figure(go.Bar(
            x=["Konvensional\n(100% OPC)", f"ZEOPAVE-AQUA\n({ipal_sub_pct}% IPAL)"],
            y=[co2_konv, co2_zeopave],
            marker_color=["#EF5350","#66BB6A"],
            text=[f"{co2_konv:.2f} t", f"{co2_zeopave:.2f} t"],
            textposition="outside",
        ))
        fig_co2.update_layout(
            title=f"Perbandingan Emisi CO₂<br><sup>Reduksi: {pct_reduksi_co2:.1f}%</sup>",
            height=320, yaxis_title="CO₂ (ton)",
            margin=dict(t=50,b=10,l=10,r=10),
        )
        st.plotly_chart(fig_co2, width='stretch')

    with e4:
        sdgs = {
            "SDG 9\nIndustri &\nInfrastruktur": 85,
            "SDG 11\nKota\nBerkelanjutan":       75,
            "SDG 12\nKonsumsi\nBertanggung Jawab": 70,
            "SDG 13\nPenanganan\nIklim":         65,
        }
        fig_sdg = go.Figure(go.Bar(
            x=list(sdgs.keys()), y=list(sdgs.values()),
            marker_color=["#FF6D00","#1976D2","#6A1B9A","#2E7D32"],
            text=[f"{v}%" for v in sdgs.values()], textposition="outside",
        ))
        fig_sdg.update_layout(
            title="Keselarasan SDGs — ZEOPAVE-AQUA",
            height=320, yaxis_range=[0, 100], yaxis_title="Keselarasan (%)",
            margin=dict(t=50,b=10,l=10,r=10),
        )
        st.plotly_chart(fig_sdg, width='stretch')

    st.markdown("**Tren Reduksi CO₂ vs % Substitusi IPAL**")
    rentang_ipal = np.arange(0, 26, 1)
    co2_tren = [
        total_pengikat_t * ((1 - p/100) * co2_opc + (p/100) * co2_ipal)
        for p in rentang_ipal
    ]
    fig_tren = go.Figure()
    fig_tren.add_trace(go.Scatter(
        x=rentang_ipal, y=co2_tren, mode="lines",
        fill="tozeroy", fillcolor="rgba(102,187,106,0.15)",
        line=dict(color="#388E3C", width=2.5),
    ))
    fig_tren.add_vline(
        x=ipal_sub_pct, line_dash="dash", line_color="#E65100",
        annotation_text=f"Saat ini: {ipal_sub_pct}%",
    )
    fig_tren.update_layout(
        title="Total Emisi CO₂ vs Substitusi IPAL",
        xaxis_title="Substitusi Lumpur IPAL (%)", yaxis_title="CO₂ (ton)",
        height=280, margin=dict(t=40,b=10,l=10,r=10),
    )
    st.plotly_chart(fig_tren, width='stretch')


# ════════════════════════════════════════════════════════════════════════════════
# TAB 6 — DASBOR PERBANDINGAN
# ════════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown(
        '<div class="section-head">Dasbor Perbandingan Kinerja</div>',
        unsafe_allow_html=True
    )
    st.caption(
        "ZEOPAVE-AQUA vs Perkerasan Konvensional Kedap Air — "
        "perbandingan teknis dan lingkungan secara komprehensif."
    )

    kategori = [
        "Permeabilitas", "Retensi Air", "Efisiensi CO₂",
        "Porositas", "Kuat Tekan Struktural", "Pemanfaatan IPAL",
    ]
    skor_zeopave = [95, 80, 75, 85, 65, 90]
    skor_konv    = [5,  0,  20,  5, 85,  0]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=skor_zeopave + [skor_zeopave[0]], theta=kategori + [kategori[0]],
        fill="toself", name="ZEOPAVE-AQUA",
        line=dict(color="#1565C0", width=2.5),
        fillcolor="rgba(21,101,192,0.2)",
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=skor_konv + [skor_konv[0]], theta=kategori + [kategori[0]],
        fill="toself", name="Perkerasan Konvensional",
        line=dict(color="#EF5350", width=2.5),
        fillcolor="rgba(239,83,80,0.1)",
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True, height=420,
        title="Radar Kinerja Multi-Kriteria",
        margin=dict(t=50,b=20,l=20,r=20),
    )
    st.plotly_chart(fig_radar, width='stretch')

    st.markdown("**Tabel Perbandingan Rinci**")
    data_banding = {
        "Parameter": [
            "Permeabilitas", "Porositas", "Kuat Tekan (28 hari)",
            "Retensi Air", "Reduksi Limpasan", "CO₂ per ton pengikat",
            "Pemanfaatan Lumpur IPAL", "Optimasi Material", "Kapasitas Mitigasi Banjir",
        ],
        "Perkerasan Konvensional": [
            "< 0,01 cm/dtk", "< 5%", "20–30 MPa",
            "~0%", "~0%", "0,85 ton CO₂",
            "Tidak ada", "Standar (manual)", "Tidak ada",
        ],
        "ZEOPAVE-AQUA": [
            "0,45–0,75 cm/dtk ✅", "18–25% ✅", "15,00 MPa (lab) ✅",
            "39,7% rata-rata ✅", "35–55% ✅", "~0,72 ton CO₂ (sub 15%) ✅",
            "Substitusi 10–15% ✅", "Hingga 85% (AQUAPAVE) ✅",
            "20.000 L/jam per 1.000 m² ✅",
        ],
        "Referensi Standar": [
            "ACI 522 ≥ 0,14 cm/dtk", "ACI 522: 15–25%",
            "SNI — min 10 MPa (lalu lintas ringan)",
            "Target penelitian: 35–55%", "Target penelitian: 35–55%",
            "Scrivener et al. 2018", "Chen et al. 2021",
            "Target penelitian: ≥85%", "Prototipe lab 2026",
        ],
    }
    st.dataframe(pd.DataFrame(data_banding), width='stretch', hide_index=True)

    st.divider()
    st.markdown("**Ringkasan Dampak untuk Lokasi Anda**")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        air_tersimpan_m3 = (intensitas_hujan/1000) * area_m2 * 1 * 0.397
        st.metric(
            "Air Tersimpan (hujan 1 jam)",
            f"{air_tersimpan_m3:.0f} m³",
            delta=f"+{air_tersimpan_m3/((intensitas_hujan/1000)*area_m2)*100:.0f}% vs 0%",
        )
    with m2:
        ipal_total_t = 0.8 * area_m2 / 100
        st.metric("Lumpur IPAL Termanfaatkan", f"{ipal_total_t:.1f} ton", delta="↓ dari TPA")
    with m3:
        co2_manfaat = ipal_total_t * (co2_opc - co2_ipal)
        st.metric("CO₂ Terhindarkan", f"{co2_manfaat:.2f} ton", delta="↓ emisi")
    with m4:
        st.metric("Optimasi Material", "85%", delta="↑ via AQUAPAVE")


# ════════════════════════════════════════════════════════════════════════════════
# TAB 7 — EFISIENSI BIAYA
# ════════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown(
        '<div class="section-head">💰 Estimasi Biaya Pembuatan ZEOPAVE-AQUA</div>',
        unsafe_allow_html=True
    )
    st.caption(
        "Estimasi biaya material berdasarkan harga satuan aktual dari pengujian laboratorium 2026. "
        "Sesuaikan volume dan harga untuk kebutuhan proyek Anda."
    )

    MATERIAL_DEFAULT = [
        {"no": 1, "nama": "Air",                "vol": 0.2, "satuan": "kg", "harga": 4_000},
        {"no": 2, "nama": "Semen",              "vol": 0.6, "satuan": "kg", "harga": 1_500},
        {"no": 3, "nama": "Kerikil",            "vol": 3.0, "satuan": "kg", "harga": 2_000},
        {"no": 4, "nama": "Limbah Lumpur IPAL", "vol": 0.4, "satuan": "kg", "harga": 0},
        {"no": 5, "nama": "Hebel",              "vol": 6.0, "satuan": "kg", "harga": 20_000},
        {"no": 6, "nama": "Zeolit",             "vol": 1.0, "satuan": "kg", "harga": 10_000},
    ]
    UNIT_PER_M2 = 14.75  # 1 m² ≈ 14,75 unit ZEOPAVE-AQUA

    st.markdown("---")
    st.markdown("#### 📋 Input Harga Satuan & Volume Material (per 1 unit ZEOPAVE-AQUA)")

    kepala = st.columns([0.5, 2.5, 1.2, 1.2, 1.8, 1.8])
    for h, judul in zip(kepala, ["No", "Material", "Volume (kg)", "Satuan", "Harga Satuan (Rp)", "Jumlah (Rp)"]):
        h.markdown(f"**{judul}**")

    baris_biaya = []
    for m in MATERIAL_DEFAULT:
        c0, c1, c2, c3, c4, c5 = st.columns([0.5, 2.5, 1.2, 1.2, 1.8, 1.8])
        with c0:
            st.markdown(f"**{m['no']}**")
        with c1:
            nama = st.text_input(
                f"Nama {m['no']}", m["nama"],
                key=f"nama_{m['no']}", label_visibility="collapsed"
            )
        with c2:
            vol = st.number_input(
                f"Volume {m['no']}", value=m["vol"], min_value=0.0, step=0.05,
                key=f"vol_{m['no']}", label_visibility="collapsed"
            )
        with c3:
            satuan = st.text_input(
                f"Satuan {m['no']}", m["satuan"],
                key=f"satuan_{m['no']}", label_visibility="collapsed"
            )
        with c4:
            harga = st.number_input(
                f"Harga {m['no']}", value=float(m["harga"]), min_value=0.0,
                step=500.0, key=f"harga_{m['no']}", label_visibility="collapsed",
                format="%.0f"
            )
        subtotal = vol * harga
        with c5:
            st.markdown(
                f"<div style='padding-top:8px;font-weight:600'>Rp {subtotal:,.0f}</div>",
                unsafe_allow_html=True,
            )
        baris_biaya.append({"nama": nama, "vol": vol, "satuan": satuan, "harga": harga, "subtotal": subtotal})

    st.markdown("---")
    with st.expander("➕ Tambah Material Lain"):
        ex_col = st.columns([2.5, 1.2, 1.8])
        with ex_col[0]: ex_nama  = st.text_input("Nama Material", "Admixture")
        with ex_col[1]: ex_vol   = st.number_input("Volume (kg)", 0.0, 100.0, 0.0, step=0.1)
        with ex_col[2]: ex_harga = st.number_input("Harga Satuan (Rp)", 0.0, 1_000_000.0, 0.0, step=500.0)
        if ex_vol > 0:
            baris_biaya.append({
                "nama": ex_nama, "vol": ex_vol, "satuan": "kg",
                "harga": ex_harga, "subtotal": ex_vol * ex_harga,
            })

    total_per_unit = sum(b["subtotal"] for b in baris_biaya)
    total_per_m2   = total_per_unit * UNIT_PER_M2

    st.markdown("---")
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1B5E20,#388E3C);border-radius:12px;
                padding:22px 28px;color:white;margin-bottom:18px">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div>
          <div style="font-size:0.85rem;opacity:0.8">💵 Total Biaya per 1 Unit ZEOPAVE-AQUA</div>
          <div style="font-size:2rem;font-weight:700;margin-top:4px">Rp {total_per_unit:,.2f}</div>
        </div>
        <div>
          <div style="font-size:0.85rem;opacity:0.8">📐 Total Biaya per 1 m²</div>
          <div style="font-size:2rem;font-weight:700;margin-top:4px">Rp {total_per_m2:,.2f}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🏗️ Estimasi Biaya Proyek")
    bc1, bc2, bc3 = st.columns(3)
    with bc1:
        luas_proyek = st.number_input(
            "Luas Area Proyek (m²)", 10.0, 100_000.0, float(area_m2), step=50.0
        )
    with bc2:
        overhead_pct = st.slider("Overhead & Upah Kerja (%)", 0, 60, 20)
    with bc3:
        ppn_pct = st.slider("PPN (%)", 0, 15, 11)

    biaya_material  = total_per_m2 * luas_proyek
    biaya_overhead  = biaya_material * (overhead_pct / 100)
    subtotal_biaya  = biaya_material + biaya_overhead
    biaya_ppn       = subtotal_biaya * (ppn_pct / 100)
    total_proyek    = subtotal_biaya + biaya_ppn

    harga_konv_m2 = st.number_input(
        "Harga Perkerasan Konvensional / Aspal (Rp/m²) — Pembanding",
        100_000.0, 5_000_000.0, 450_000.0, step=10_000.0
    )
    total_konv    = harga_konv_m2 * luas_proyek
    selisih_rp    = total_proyek - total_konv
    selisih_pct   = (selisih_rp / total_konv * 100) if total_konv > 0 else 0

    tabel_biaya = pd.DataFrame({
        "Komponen Biaya": [
            "Biaya Material",
            f"Overhead & Upah Kerja ({overhead_pct}%)",
            "Sub-Total",
            f"PPN ({ppn_pct}%)",
            "TOTAL PROYEK",
        ],
        "Jumlah (Rp)": [
            f"Rp {biaya_material:,.0f}",
            f"Rp {biaya_overhead:,.0f}",
            f"Rp {subtotal_biaya:,.0f}",
            f"Rp {biaya_ppn:,.0f}",
            f"Rp {total_proyek:,.0f}",
        ],
    })
    st.dataframe(tabel_biaya, width='stretch', hide_index=True)

    badge_biaya = "badge-warn" if selisih_pct > 0 else "badge-lulus"
    label_biaya = (
        f"⬆️ +{selisih_pct:.1f}% lebih mahal dari perkerasan konvensional"
        if selisih_pct > 0
        else f"✅ {abs(selisih_pct):.1f}% lebih murah dari perkerasan konvensional"
    )
    st.markdown(f"""
    <div style="margin:12px 0">
      <span class="{badge_biaya}">{label_biaya}</span>&nbsp;&nbsp;
      <span style="color:#555;font-size:0.88rem">
        (Konvensional: Rp {total_konv:,.0f} | ZEOPAVE-AQUA: Rp {total_proyek:,.0f})
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    gc1, gc2 = st.columns(2)

    with gc1:
        label_pie = [b["nama"] for b in baris_biaya if b["subtotal"] > 0]
        nilai_pie  = [b["subtotal"] for b in baris_biaya if b["subtotal"] > 0]
        fig_pie_b = go.Figure(go.Pie(
            labels=label_pie, values=nilai_pie, hole=0.42,
            marker_colors=["#42A5F5","#1565C0","#E65100","#00897B","#7B1FA2","#F9A825"],
            textinfo="label+percent",
        ))
        fig_pie_b.update_layout(
            title="Komposisi Biaya Material per Unit",
            height=340, margin=dict(t=50,b=10,l=10,r=10),
            showlegend=False,
        )
        st.plotly_chart(fig_pie_b, width='stretch')

    with gc2:
        fig_wf = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative","relative","total","relative","total"],
            x=["Material", f"Overhead\n{overhead_pct}%", "Sub-Total", f"PPN\n{ppn_pct}%", "Total Proyek"],
            y=[biaya_material, biaya_overhead, 0, biaya_ppn, 0],
            connector=dict(line=dict(color="#ccc")),
            increasing=dict(marker_color="#1565C0"),
            totals=dict(marker_color="#00897B"),
            text=[
                f"Rp {biaya_material/1e6:.1f}M",
                f"Rp {biaya_overhead/1e6:.1f}M",
                f"Rp {subtotal_biaya/1e6:.1f}M",
                f"Rp {biaya_ppn/1e6:.1f}M",
                f"Rp {total_proyek/1e6:.1f}M",
            ],
            textposition="outside",
        ))
        fig_wf.update_layout(
            title=f"Rincian Biaya Proyek {luas_proyek:.0f} m²",
            height=340, yaxis_title="Biaya (Rp)",
            margin=dict(t=50,b=10,l=10,r=10),
        )
        st.plotly_chart(fig_wf, width='stretch')

    st.markdown("#### ♻️ Keuntungan Biaya dari Limbah IPAL (Gratis)")
    baris_ipal  = next((b for b in baris_biaya if "ipal" in b["nama"].lower()), None)
    baris_semen = next((b for b in baris_biaya if "semen" in b["nama"].lower()), None)
    vol_ipal    = baris_ipal["vol"]   if baris_ipal  else 0.4
    harga_semen = baris_semen["harga"] if baris_semen else 1_500

    hemat_per_unit  = vol_ipal * harga_semen
    hemat_proyek    = hemat_per_unit * UNIT_PER_M2 * luas_proyek
    total_ipal_kg   = vol_ipal * UNIT_PER_M2 * luas_proyek

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.metric("Penghematan per Unit (vs semen)", f"Rp {hemat_per_unit:,.0f}", delta="IPAL = Rp 0 (gratis!)")
    with sc2:
        st.metric(f"Penghematan Proyek {luas_proyek:.0f} m²", f"Rp {hemat_proyek:,.0f}", delta="↓ biaya material")
    with sc3:
        st.metric("Total IPAL Termanfaatkan", f"{total_ipal_kg:,.1f} kg", delta="↑ limbah → infrastruktur")

    st.markdown("#### 📈 Sensitivitas Biaya vs % Substitusi IPAL")
    total_pengikat_unit = vol_ipal + (baris_semen["vol"] if baris_semen else 0.6)
    biaya_non_pengikat  = total_per_unit - (harga_semen * (baris_semen["vol"] if baris_semen else 0.6))

    pct_range   = np.arange(0, 26, 1)
    biaya_range = []
    for p in pct_range:
        semen_sini = total_pengikat_unit * (1 - p/100)
        biaya_range.append((biaya_non_pengikat + semen_sini * harga_semen) * UNIT_PER_M2)

    fig_sens = go.Figure()
    fig_sens.add_trace(go.Scatter(
        x=pct_range, y=biaya_range, mode="lines",
        fill="tozeroy", fillcolor="rgba(21,101,192,0.12)",
        line=dict(color="#1565C0", width=2.5), name="Biaya per m²",
    ))
    fig_sens.add_vline(
        x=vol_ipal / total_pengikat_unit * 100, line_dash="dash", line_color="#E65100",
        annotation_text=f"Komposisi aktual ({vol_ipal/total_pengikat_unit*100:.0f}% IPAL)",
    )
    fig_sens.update_layout(
        title="Estimasi Biaya Material per m² vs % Substitusi IPAL",
        xaxis_title="% Substitusi IPAL (dari total pengikat)",
        yaxis_title="Biaya Material per m² (Rp)",
        height=300, margin=dict(t=50,b=10,l=10,r=10),
    )
    fig_sens.update_yaxes(tickformat=",")
    st.plotly_chart(fig_sens, width='stretch')

    st.caption(
        "⚠️ Catatan: Estimasi menggunakan harga referensi aktual dari pengujian laboratorium 2026. "
        "Harga pasar dapat bervariasi tergantung lokasi, kuantitas pembelian, dan kondisi pasar setempat."
    )


# ─── Footer ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <b>AQUAPAVE</b> — Platform Optimasi Desain Digital untuk Perkerasan Berpori ZEOPAVE-AQUA<br>
  Fakultas Teknik, Universitas Udayana · Badung Festival Inovasi 2026<br>
  Mendukung SDG 9 · SDG 11 · SDG 12 · SDG 13
</div>
""", unsafe_allow_html=True)