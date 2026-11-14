
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="ASTRA-MED", page_icon="🚀", layout="wide")
st.markdown(r'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Manrope,sans-serif}
.stApp{background:radial-gradient(ellipse at 80% 0%,#1a3155 0%,#0a1222 42%,#070b15 85%);color:#edf4ff}
.block-container{padding-top:1.2rem;max-width:1450px}
section[data-testid="stSidebar"]{background:#0b1425;border-right:1px solid #263954}
.brand{font-size:1.35rem;font-weight:800;letter-spacing:.18em;margin:0 0 1.4rem;color:#f5f9ff}
.brand span{color:#58e1f2}
.hero,.panel,.metric{border:1px solid #2a3d5b;background:linear-gradient(140deg,#152640,#0d1729);border-radius:17px}
.hero{padding:1.3rem 1.5rem;margin-bottom:1rem}
.eyebrow{font-size:.7rem;letter-spacing:.18em;color:#58e1f2;font-weight:700}
.hero h1{font-size:1.8rem;margin:.3rem 0}
.hero p,.muted{color:#a8bad3}
.metric{padding:15px;min-height:112px}
.metric-label{font-size:.72rem;color:#a8bad3;text-transform:uppercase;letter-spacing:.1em}
.metric-value{font-size:1.8rem;font-weight:800;margin:.25rem 0;color:#f5f9ff}
.metric-note{font-size:.75rem}
.panel{padding:16px 18px;margin-bottom:12px}
.stButton>button{background:#12384b;color:white;border:1px solid #58e1f2;border-radius:10px}
.stButton>button:hover{background:#1a4c62;color:white}
.stTextInput input,.stNumberInput input,.stTextArea textarea{background:#0c1729;color:white}
footer{visibility:hidden}
</style>
''', unsafe_allow_html=True)

if "history" not in st.session_state:
    rng=np.random.default_rng(8)
    st.session_state.history=pd.DataFrame({
        "Time":[datetime.now()-timedelta(hours=23-i) for i in range(24)],
        "Heart rate":np.clip(72+rng.normal(0,5,24),55,105).round(),
        "SpO₂":np.clip(98+rng.normal(0,.6,24),94,100).round(1),
        "Temperature":np.clip(36.7+rng.normal(0,.15,24),36,38).round(1),
        "Systolic BP":np.clip(118+rng.normal(0,7,24),95,145).round(),
        "Sleep":np.clip(7+rng.normal(0,.7,24),4,9).round(1)
    })
if "notes" not in st.session_state: st.session_state.notes=[]

st.markdown('<div class="brand"><span>✦</span> ASTRA-MED</div>',unsafe_allow_html=True)
with st.sidebar:
    st.markdown('<p class="eyebrow">MISSION CONSOLE</p>',unsafe_allow_html=True)
    page=st.radio("Navigation",["Overview","Health analytics","Daily check-in","Spaceflight hazards","Health guide"])
    mission=st.selectbox("Mission environment",["Deep-space transit","Lunar surface","Mars habitat","Space station"])
    st.text_input("Crew ID", "CREW-01")
    st.caption("Hackathon prototype • Demo data")
    st.divider()
    st.caption("Not a medical device. Follow mission medical procedures.")

def card(label,value,unit,note,color="#65e5b3"):
    st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value} <span style="font-size:.85rem;color:#a8bad3">{unit}</span></div><div class="metric-note" style="color:{color}">● {note}</div></div>',unsafe_allow_html=True)

def chart(df,key):
    fig=px.area(df,x="Time",y=key)
    fig.update_traces(line_color="#58e1f2",fillcolor="rgba(88,225,242,.12)")
    fig.update_layout(height=320,margin=dict(l=8,r=8,t=20,b=8),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#c5d4e9",xaxis=dict(showgrid=False),yaxis=dict(gridcolor="#263954"))
    return fig

if page=="Overview":
    r=st.session_state.history.iloc[-1]
    st.markdown(f'<div class="hero"><div class="eyebrow">LIVE CREW HEALTH · {mission.upper()}</div><h1>Mission health overview</h1><p>Monitor key indicators, review changes and complete your daily crew wellness routine.</p></div>',unsafe_allow_html=True)
    cols=st.columns(5)
    values=[("Heart rate",int(r["Heart rate"]),"bpm","Latest demo reading"),("Blood oxygen",r["SpO₂"],"%","Latest demo reading"),("Temperature",r["Temperature"],"°C","Latest demo reading"),("Systolic BP",int(r["Systolic BP"]),"mmHg","Latest demo reading"),("Sleep",r["Sleep"],"hrs","Last logged period")]
    for col,v in zip(cols,values):
        with col: card(*v)
    st.write("")
    left,right=st.columns([1.6,1])
    with left:
        st.markdown('<div class="panel"><b>HEART RATE · LAST 24 HOURS</b></div>',unsafe_allow_html=True)
        st.plotly_chart(chart(st.session_state.history,"Heart rate"),use_container_width=True,config={"displayModeBar":False})
    with right:
        st.markdown('<div class="panel"><b>DAILY MISSION CHECKLIST</b><p class="muted">Build a consistent health-monitoring routine.</p></div>',unsafe_allow_html=True)
        for task in ["Log health measurements","Complete sleep and mood check-in","Review hydration and nutrition","Complete assigned exercise"]:
            st.checkbox(task,key="task_"+task)
        st.warning("For severe, sudden or worrying symptoms, contact mission medical support and follow approved emergency procedures.")
    a,b,c=st.columns(3)
    for col,title,desc in [(a,"CARDIOVASCULAR","Heart rate and blood-pressure trends"),(b,"IMMUNE & GENERAL","Temperature, symptoms and fatigue"),(c,"BEHAVIORAL WELLNESS","Sleep, mood, stress and isolation")]:
        with col: st.markdown(f'<div class="panel"><b>{title}</b><p class="muted">{desc}</p></div>',unsafe_allow_html=True)

elif page=="Health analytics":
    st.markdown('<div class="hero"><div class="eyebrow">DATA EXPLORER</div><h1>Health analytics</h1><p>Explore recorded indicators and spot changes over time.</p></div>',unsafe_allow_html=True)
    key=st.selectbox("Select health indicator",["Heart rate","SpO₂","Temperature","Systolic BP","Sleep"])
    st.plotly_chart(chart(st.session_state.history,key),use_container_width=True,config={"displayModeBar":False})
    st.dataframe(st.session_state.history.tail(12).iloc[::-1],use_container_width=True,hide_index=True)

elif page=="Daily check-in":
    st.markdown('<div class="hero"><div class="eyebrow">CREW WELLNESS</div><h1>Daily health check-in</h1><p>Enter readings taken with approved equipment and record how you feel.</p></div>',unsafe_allow_html=True)
    with st.form("checkin"):
        x,y,z=st.columns(3)
        with x:
            hr=st.number_input("Heart rate (bpm)",30,220,72)
            oxygen=st.number_input("Blood oxygen (%)",50.0,100.0,98.0,.1)
        with y:
            temp=st.number_input("Temperature (°C)",30.0,43.0,36.7,.1)
            bp=st.number_input("Systolic BP (mmHg)",60,250,118)
        with z:
            sleep=st.number_input("Sleep hours",0.0,24.0,7.0,.5)
            mood=st.select_slider("Mood",["Very low","Low","Okay","Good","Very good"],value="Good")
        symptoms=st.text_area("Symptoms or notes (optional)")
        save=st.form_submit_button("SAVE CHECK-IN")
    if save:
        row={"Time":datetime.now(),"Heart rate":hr,"SpO₂":oxygen,"Temperature":temp,"Systolic BP":bp,"Sleep":sleep}
        st.session_state.history=pd.concat([st.session_state.history,pd.DataFrame([row])],ignore_index=True).tail(100)
        st.session_state.notes.append({"Time":datetime.now().strftime("%Y-%m-%d %H:%M"),"Mood":mood,"Notes":symptoms})
        st.success("Your check-in has been saved in this session.")
        st.info("This prototype does not diagnose illness. Compare readings with your personal baseline and follow mission medical guidance.")
    if st.session_state.notes: st.dataframe(pd.DataFrame(st.session_state.notes[::-1]),use_container_width=True,hide_index=True)

elif page=="Spaceflight hazards":
    st.markdown('<div class="hero"><div class="eyebrow">SPACEFLIGHT RISK CONTEXT</div><h1>Five hazards of human spaceflight</h1><p>Why monitoring matters during long-duration missions.</p></div>',unsafe_allow_html=True)
    hazards=[("01","Space radiation","Exposure can affect tissues and long-term health. Track mission exposure records and follow shielding guidance."),("02","Isolation & confinement","Limited social contact and confined living may affect sleep, mood and team dynamics."),("03","Distance from Earth","Communication delays and limited supplies make preparation and reliable self-monitoring important."),("04","Gravity fields","Microgravity and gravity transitions can affect bones, muscles, balance and cardiovascular adaptation."),("05","Hostile closed environment","Cabin air, temperature, humidity and other environmental factors can influence crew health.")]
    for i in range(0,5,2):
        cols=st.columns(2)
        for j in range(2):
            if i+j<5:
                n,t,d=hazards[i+j]
                with cols[j]: st.markdown(f'<div class="panel"><div class="eyebrow">HAZARD {n}</div><h3>{t}</h3><p class="muted">{d}</p></div>',unsafe_allow_html=True)

else:
    st.markdown('<div class="hero"><div class="eyebrow">QUICK REFERENCE</div><h1>Health guide</h1><p>Simple explanations for astronaut self-monitoring.</p></div>',unsafe_allow_html=True)
    with st.expander("Heart rate and blood pressure"): st.write("Use approved equipment and the mission team's measurement procedure. Compare with your own baseline; one value alone is not a diagnosis.")
    with st.expander("Blood oxygen and temperature"): st.write("Use calibrated equipment. Repeat unexpected readings according to protocol and report persistent or concerning changes.")
    with st.expander("Sleep, mood and fatigue"): st.write("Record sleep, mood and fatigue consistently. Patterns across days may be more useful than a single check-in.")
    with st.expander("Bone and muscle health"): st.write("Track assigned exercise, mobility assessments, nutrition and mission-provided clinical measurements. Ordinary dashboard readings cannot measure bone density.")
    with st.expander("When should I seek help?"): st.write("Follow mission-specific thresholds and escalation procedures. Contact medical support for severe, sudden or worrying symptoms.")

st.markdown("---")
st.markdown('<p class="muted" style="text-align:center">ASTRA-MED · Advanced Astronaut Health Monitoring & Decision Support · Hackathon prototype · Not a medical device</p>',unsafe_allow_html=True)
