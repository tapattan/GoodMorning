import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import datetime
import pandas as pd 

def get_weekdays_in_year(year):
    
    today = datetime.date.today()
    
    # หากเป็นปีปัจจุบัน ให้ใช้วันนี้เป็นขอบเขตสูงสุด
    if year == today.year:
        last_day = today
    else:
        last_day = datetime.date(year, 12, 31)  # ใช้วันสิ้นปี
    
    weeks_data = {}

    # วนลูปตั้งแต่วันที่ 1 มกราคมถึงวันที่ last_day
    current_day = datetime.date(year, 1, 1)
    while current_day <= last_day:
        iso_year, iso_week, iso_weekday = current_day.isocalendar()
        
        # เก็บเฉพาะวันจันทร์-ศุกร์
        if iso_weekday in range(0, 6):  # 1 = จันทร์, 5 = ศุกร์
            if iso_week not in weeks_data:
                weeks_data[iso_week] = []
            weeks_data[iso_week].append(current_day)
        
        current_day += datetime.timedelta(days=1)
    
    return weeks_data


st.set_page_config(page_title="CSV Viewer", layout="wide")

st.sidebar.title("📌 เมนูหลัก")
menu = st.sidebar.radio(
    "เลือกเมนู",
    ["📊 Relative Strength", "📂 Short Sell", "🎃 Market Breadth" ,"ℹ️ เกี่ยวกับ"]
)

if menu == "📊 Relative Strength":
    st.title('Relative Strength Rating ของ William O’Neil ภายใน SET50')
    st.subheader('รายสัปดาห์')

    year_selected = st.selectbox("เลือกปี", [2025,2024])

    weeks_data = get_weekdays_in_year(year_selected)

    week_selected = st.selectbox("เลือกสัปดาห์", list(weeks_data.keys()))

    st.write(f"คุณเลือก: ปี {year_selected}, สัปดาห์ที่ {week_selected}")
    #st.write("วันจันทร์ - ศุกร์ ในสัปดาห์นี้:", 
    #         [d.strftime('%Y-%m-%d') for d in weeks_data[week_selected]])

    df = pd.read_csv(f'rs_datasources/{year_selected}-week{week_selected}.csv')

    # แสดงตารางข้อมูล
    N = week_selected
    s1 = weeks_data[N][0].strftime('%Y-%m-%d')
    s2 = weeks_data[N][-1].strftime('%Y-%m-%d')
    st.write(f"Relative Strength Rating {s1}-{s2}")
    #st.dataframe(df[['no','symbol','return']])  # ใช้ dataframe เพื่อแสดงข้อมูลแบบ scroll ได้
    rp = df[['no','symbol','return']]
    rp = rp.set_index('no')
    st.dataframe(rp, use_container_width=True)

if menu == '📂 Short Sell':
   st.title('เร็วๆ นี้ ')

if menu == 'ℹ️ เกี่ยวกับ':
   st.title('เครื่องมือวิเคราะห์การลงทุน')
   st.write("""
    พบ bug แจ้งไอเดียต่างๆ ได้
    """) 
   
if menu == "🎃 Market Breadth":
   st.title('Market Breadth ผลตอบแทนใน SET50')
   st.subheader('รายสัปดาห์')
   # สร้างกราฟแท่งด้วย Plotly
   year_selected = st.selectbox("เลือกปี", [2025,2024])

   df = pd.read_csv(f'rs_datasources/MarketBreadth{year_selected}.csv')
   #fig = px.bar(df, x="week", y="MarketBreadth", title="📊 MarketBreadth SET50")

   # แสดงกราฟใน Streamlit
   #st.plotly_chart(fig, use_container_width=True) 
   # คำนวณค่า Cumulative Sum
   df["SumMarketBreadth"] = df["MarketBreadth"].cumsum()

   # สร้างกราฟด้วย Plotly
   fig = go.Figure()

   # กราฟแท่ง
   fig.add_trace(go.Bar(
        x=df["week"], 
        y=df["MarketBreadth"], 
        name="MarketBreadth",
        marker_color="blue",
        opacity=0.7
    ))

   # กราฟเส้น Cumulative Sum
   fig.add_trace(go.Scatter(
        x=df["week"], 
        y=df["SumMarketBreadth"], 
        name="ค่าสะสม (Cumsum)", 
        mode="lines+markers",
        line=dict(color="red", width=2),
        yaxis="y2"
    ))

   # ตั้งค่าแกน Y ให้รองรับสองแกน
   fig.update_layout(
        title="📊 กราฟแท่ง + กราฟเส้น Cumulative Sum",
        #xaxis=dict(title="หมวดหมู่"),
        yaxis=dict(title="ค่าปกติ", side="left"),
        yaxis2=dict(title="ค่าสะสม", overlaying="y", side="right"),
        legend=dict(x=0.01, y=0.99),
        template="plotly_white"
    )

   # แสดงกราฟใน Streamlit
   st.plotly_chart(fig, use_container_width=True)