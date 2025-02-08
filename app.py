import streamlit as st
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
    ["📊 Relative Strength", "📂 Short Sell", "ℹ️ เกี่ยวกับ"]
)

if menu == "📊 Relative Strength":
    st.title('Relative Strength Rating ของ William O’Neil')
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