"""
Streamlit 債券定價與分析工具（含因子影響方向表）
新增標籤頁：📊 因子影響方向表（行列互換版）
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 頁面配置
st.set_page_config(page_title="債券定價教學與分析工具", layout="wide")

st.title("📘 債券定價教學與分析工具")
st.markdown("左側調整債券引數，右側計算結果。下方標籤頁提供各因子的詳細解釋與互動圖表。")

# ------------------------------
# 輔助函式（與原相同）
def bond_price(face_value, coupon_rate, ytm, years_to_maturity, freq=2):
    periods = int(years_to_maturity * freq)
    if periods == 0:
        return face_value
    coupon_payment = face_value * coupon_rate / freq
    ytm_per_period = ytm / freq
    price = 0.0
    for t in range(1, periods + 1):
        price += coupon_payment / (1 + ytm_per_period) ** t
    price += face_value / (1 + ytm_per_period) ** periods
    return price

def macaulay_duration(face_value, coupon_rate, ytm, years_to_maturity, freq=2):
    periods = int(years_to_maturity * freq)
    if periods == 0:
        return 0.0
    coupon_payment = face_value * coupon_rate / freq
    ytm_per_period = ytm / freq
    price = bond_price(face_value, coupon_rate, ytm, years_to_maturity, freq)
    weighted_sum = 0.0
    for t in range(1, periods + 1):
        cash_flow = coupon_payment if t < periods else coupon_payment + face_value
        pv_cf = cash_flow / (1 + ytm_per_period) ** t
        weighted_sum += pv_cf * (t / freq)
    return weighted_sum / price if price > 0 else 0.0

def modified_duration(macaulay_dur, ytm, freq=2):
    ytm_per_period = ytm / freq
    return macaulay_dur / (1 + ytm_per_period)

def bond_convexity(face_value, coupon_rate, ytm, years_to_maturity, freq=2):
    periods = int(years_to_maturity * freq)
    if periods == 0:
        return 0.0
    coupon_payment = face_value * coupon_rate / freq
    ytm_per_period = ytm / freq
    price = bond_price(face_value, coupon_rate, ytm, years_to_maturity, freq)
    convexity = 0.0
    for t in range(1, periods + 1):
        cash_flow = coupon_payment if t < periods else coupon_payment + face_value
        pv_cf = cash_flow / (1 + ytm_per_period) ** t
        convexity += pv_cf * (t / freq) * ((t / freq) + 1)
    convexity = convexity / (price * (1 + ytm_per_period) ** 2)
    return convexity

# ------------------------------
# 側邊欄：引數輸入
st.sidebar.header("⚙️ 債券引數（演示示例）")
col1, col2 = st.sidebar.columns(2)
face_value = col1.number_input("面值 (元)", value=100.0, min_value=10.0, step=10.0)
coupon_rate = col2.number_input("票面利率 (%)", value=5.0, min_value=0.0, step=0.5) / 100.0

col3, col4 = st.sidebar.columns(2)
ytm = col3.number_input("到期收益率 (%)", value=4.5, min_value=0.0, step=0.25) / 100.0
years_to_maturity = col4.number_input("剩餘期限 (年)", value=10.0, min_value=0.5, max_value=50.0, step=0.5)

freq_options = {1: "1（每年一次）", 2: "2（每半年一次）", 4: "4（每季一次）", 12: "12（每月一次）"}
freq = st.sidebar.selectbox("每年付息次數", options=list(freq_options.keys()), format_func=lambda x: freq_options[x])

# 核心計算結果
price = bond_price(face_value, coupon_rate, ytm, years_to_maturity, freq)
mac_dur = macaulay_duration(face_value, coupon_rate, ytm, years_to_maturity, freq)
mod_dur = modified_duration(mac_dur, ytm, freq)
conv = bond_convexity(face_value, coupon_rate, ytm, years_to_maturity, freq)

# 顯示關鍵指標卡片
st.header("📊 當前債券關鍵指標")
colA, colB, colC, colD = st.columns(4)
colA.metric("債券價格 (元)", f"{price:,.2f}")
colB.metric("麥考利久期 (年)", f"{mac_dur:.3f}")
colC.metric("修正久期 (年)", f"{mod_dur:.3f}")
colD.metric("凸性", f"{conv:.3f}")

# ------------------------------
# 標籤頁區域
st.header("📚 債券定價因子詳解")
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💰 價格與四大因子",
    "🎫 票面利率 (Coupon)",
    "📉 到期收益率 (YTM)",
    "⏳ 剩餘期限 (N)",
    "📏 久期 (Duration)",
    "🔄 凸性 (Convexity)",
    "📊 因子影響方向表"   # 新增標籤頁
])

# ---------- Tab 1~6 內容與原相同（略，可複用之前程式碼）----------
# 為簡潔，此處僅展示 Tab7 的新表格。實際使用時請複製之前的 Tab1~6 程式碼。
# 以下是佔位說明（實際執行時需包含完整內容）：
with tab1:
    st.subheader("債券價格由哪些因素決定？")
    st.latex(r"P = \sum_{t=1}^{n} \frac{C}{(1+r)^t} + \frac{F}{(1+r)^n}")
    st.markdown("...（詳細說明請見完整版）...")
with tab2:
    st.subheader("票面利率 (Coupon Rate) 如何影響價格？")
    st.markdown("...（圖表與例子）...")
with tab3:
    st.subheader("到期收益率 (YTM) 與價格的反向關係")
    st.markdown("...（Price-Yield曲線）...")
with tab4:
    st.subheader("剩餘期限 (N) 如何影響價格與利率敏感性？")
    st.markdown("...（期限與久期關係）...")
with tab5:
    st.subheader("久期 (Duration) 的定義與計算方法")
    st.markdown("...（久期公式與因子影響）...")
with tab6:
    st.subheader("凸性 (Convexity) — 價格的彎曲程度")
    st.markdown("...（凸性修正圖示）...")

# ---------- Tab 7: 因子影響方向表（行列互換版）----------
with tab7:
    st.subheader("📊 債券價格、久期、凸性受各因子影響的方向")
    st.markdown("**行 = 自變數（Yield, N, Coupon）** | **列 = 因變數（Price, Duration, Convexity）**")
    
    # 建立表格資料（方向符號 + 特殊說明）
    table_data = {
        "因子 \\ 指標": ["到期收益率 (Yield)", "剩餘期限 (N)", "票面利率 (Coupon)"],
        "債券價格 (Price)": ["−", "± (注1)", "+"],
        "久期 (Duration)": ["−", "+", "−"],
        "凸性 (Convexity)": ["−", "+", "−"]
    }
    df_direction = pd.DataFrame(table_data)
    
    # 使用 Streamlit 的 dataframe 顯示，並高亮
    st.dataframe(df_direction, use_container_width=True, hide_index=True)
    
    st.markdown("""
    **注1：剩餘期限 (N) 對價格的影響方向取決於債券處於折價還是溢價狀態**  
    - 若 **Coupon > YTM**（溢價債） → N ↑ → Price ↑（正相關）  
    - 若 **Coupon < YTM**（折價債） → N ↑ → Price ↓（負相關）  
    - 若 **Coupon = YTM**（平價債） → N 變化不影響 Price

    **其他符號解釋：**  
    - **+** ：正相關（因子增加，指標增加）  
    - **−** ：負相關（因子增加，指標減少）  
    - **±** ：方向隨折溢價條件變化

    ---
    ### 當前債券狀態驗證
    """)
    
    # 動態展示當前債券的折溢價狀態，並驗證表格方向
    if coupon_rate > ytm:
        premium_status = "溢價債券 (Coupon > YTM)"
        n_effect = "正相關（N ↑ → Price ↑）"
    elif coupon_rate < ytm:
        premium_status = "折價債券 (Coupon < YTM)"
        n_effect = "負相關（N ↑ → Price ↓）"
    else:
        premium_status = "平價債券 (Coupon = YTM)"
        n_effect = "無影響（Price 恆等於面值）"
    
    st.info(f"""
    **當前債券狀態**：{premium_status}  
    - 票面利率 {coupon_rate*100:.2f}%  vs  到期收益率 {ytm*100:.2f}%  
    - 因此，**剩餘期限 N 對價格的影響方向為：{n_effect}**。
    """)
    
    # 額外給出一個簡單數值例子
    st.subheader("🔍 數值驗證例子（使用當前引數）")
    st.markdown(f"""
    - **YTM 變化**：YTM 從 {ytm*100:.2f}% 升至 {ytm*100+1:.2f}% → 價格從 {price:.2f} 降至 {bond_price(face_value, coupon_rate, ytm+0.01, years_to_maturity, freq):.2f} 元（**負相關** ✅）  
    - **N 變化**：將期限從 {years_to_maturity} 年改為 {years_to_maturity+5} 年 → 價格變為 {bond_price(face_value, coupon_rate, ytm, years_to_maturity+5, freq):.2f} 元（驗證上述 {n_effect}）  
    - **Coupon 變化**：票息從 {coupon_rate*100:.2f}% 升至 {coupon_rate*100+1:.2f}% → 價格升至 {bond_price(face_value, coupon_rate+0.01, ytm, years_to_maturity, freq):.2f} 元（**正相關** ✅）
    """)

# 底部現金流明細（可選）
with st.expander("📋 檢視詳細現金流與現值"):
    periods = int(years_to_maturity * freq)
    if periods > 0 and periods <= 100:
        coupon_pmt = face_value * coupon_rate / freq
        ytm_per_period = ytm / freq
        cf_data = []
        for t in range(1, periods+1):
            cf = coupon_pmt if t < periods else coupon_pmt + face_value
            pv = cf / (1 + ytm_per_period)**t
            cf_data.append({"期數": t, "現金流(元)": f"{cf:.2f}", "現值(元)": f"{pv:.2f}"})
        st.dataframe(pd.DataFrame(cf_data), use_container_width=True)
    else:
        st.write("期限太短，無法顯示明細。")