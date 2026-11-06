import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import load_ramen_data, STYLE_COLORS
from src.visualizer import (
    build_2d_style_distribution,
    build_flavor_radar,
    build_3d_brand_landscape,
    build_3d_globe_ratings,
    build_4d_era_animation
)

st.set_page_config(
    page_title="Global Ramen Ratings Intelligence & 4D Flavor Space",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }
    
    .ramen-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_ramen_data("data/ramen_ratings.csv")

df, brand_stats = get_data()

# Sidebar
st.sidebar.title("🍜 Ramen Intelligence")
st.sidebar.markdown("Exploratory Data Analysis, 3D Brand Morphospaces & 4D Flavor Chronology.")

country_filter = st.sidebar.multiselect("Filter by Country", options=sorted(df["Country"].unique()), default=[])
style_filter = st.sidebar.multiselect("Filter by Style", options=sorted(df["Style"].unique()), default=[])
min_stars = st.sidebar.slider("Minimum Stars", 0.0, 5.0, 0.0, 0.25)

filtered_df = df[df["Stars"] >= min_stars]
if country_filter:
    filtered_df = filtered_df[filtered_df["Country"].isin(country_filter)]
if style_filter:
    filtered_df = filtered_df[filtered_df["Style"].isin(style_filter)]

# Header KPIs
col_title, col_kpis = st.columns([2, 3])
with col_title:
    st.title("Global Ramen Ratings Intelligence")
    st.caption("Sensory flavor mapping, 3D brand positioning landscapes, and chronological 4D review evolution.")

with col_kpis:
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="ramen-card">
            <span style="color: #94a3b8; font-size: 11px;">TOTAL REVIEWS</span>
            <h3 style="margin: 0; color: #38bdf8;">{len(filtered_df):,}</h3>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="ramen-card">
            <span style="color: #94a3b8; font-size: 11px;">BRANDS INDEXED</span>
            <h3 style="margin: 0; color: #10b981;">{filtered_df['Brand'].nunique():,}</h3>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="ramen-card">
            <span style="color: #94a3b8; font-size: 11px;">AVG RATING</span>
            <h3 style="margin: 0; color: #f59e0b;">⭐ {filtered_df['Stars'].mean():.2f}</h3>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="ramen-card">
            <span style="color: #94a3b8; font-size: 11px;">TOP 10 AWARDEES</span>
            <h3 style="margin: 0; color: #f43f5e;">{filtered_df['Is_Top_Ten'].sum()}</h3>
        </div>
        """, unsafe_allow_html=True)

# Tabs
tab_2d, tab_3d, tab_4d, tab_rec = st.tabs([
    "📊 2D Flavor & Style Analytics",
    "🌐 3D Brand Landscape & World Map",
    "⏳ 4D Review Chronology Evolution",
    "🍲 Interactive Ramen Recommender"
])

# TAB 1: 2D
with tab_2d:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(build_2d_style_distribution(filtered_df), use_container_width=True)
    with col2:
        st.plotly_chart(build_flavor_radar(filtered_df), use_container_width=True)
        
    st.markdown("#### Top 10 Most Prolific Ramen Brands")
    top_brands = filtered_df["Brand"].value_counts().head(10).reset_index()
    top_brands.columns = ["Brand", "Total Reviews"]
    top_brand_bar = px.bar(top_brands, x="Brand", y="Total Reviews", color="Total Reviews", color_continuous_scale="Purples")
    top_brand_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(top_brand_bar, use_container_width=True)

# TAB 2: 3D
with tab_3d:
    st.subheader("3D Brand Strategic Landscape (Volume × Quality Score × Top 10 Placements)")
    st.markdown("Compare the market presence and critical reception of global ramen manufacturers.")
    st.plotly_chart(build_3d_brand_landscape(brand_stats), use_container_width=True)
    
    st.divider()
    st.subheader("3D Global Ramen Rating Geography")
    st.plotly_chart(build_3d_globe_ratings(filtered_df), use_container_width=True)

# TAB 3: 4D
with tab_4d:
    st.subheader("4D Spatio-Temporal Review Evolution across Chronological Eras")
    st.markdown("Press the **Play** button below the 3D plot to observe how ramen variety nomenclature and quality standards evolved across 2,500+ reviews.")
    st.plotly_chart(build_4d_era_animation(filtered_df), use_container_width=True)

# TAB 4: RECOMMENDER
with tab_rec:
    st.subheader("🍲 Personalized Flavor & Ramen Discovery Engine")
    st.markdown("Filter by your culinary preferences to find your ideal bowl.")
    
    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        rec_flavor = st.selectbox("Preferred Flavor Profile", ["All"] + sorted(df["Flavor_Profile"].unique().tolist()))
    with rc2:
        rec_style = st.selectbox("Preferred Packaging Style", ["All"] + sorted(df["Style"].unique().tolist()))
    with rc3:
        rec_country = st.selectbox("Preferred Origin Country", ["All"] + sorted(df["Country"].unique().tolist()))
        
    res = df.copy()
    if rec_flavor != "All":
        res = res[res["Flavor_Profile"] == rec_flavor]
    if rec_style != "All":
        res = res[res["Style"] == rec_style]
    if rec_country != "All":
        res = res[res["Country"] == rec_country]
        
    top_picks = res.sort_values(by="Stars", ascending=False).head(10)
    
    st.markdown(f"### Top Curated Matches ({len(top_picks)} Found)")
    for _, row in top_picks.iterrows():
        st.markdown(f"""
        <div class="ramen-card" style="margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #38bdf8;">{row['Brand']} - {row['Variety']}</h4>
                <span style="font-size: 16px; color: #f59e0b; font-weight: bold;">⭐ {row['Stars']} / 5.0</span>
            </div>
            <div style="margin-top: 6px; font-size: 13px; color: #94a3b8;">
                Origin: <b>{row['Country']}</b> | Style: <b>{row['Style']}</b> | Profile: <b>{row['Flavor_Profile']}</b> {f'| 🏆 <b>{row["Top Ten"]}</b>' if row["Is_Top_Ten"] else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
