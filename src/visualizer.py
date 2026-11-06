import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from .data_loader import STYLE_COLORS

def build_2d_style_distribution(df):
    """Packaging style distribution and average star rating bar chart."""
    style_agg = df.groupby("Style").agg(
        Count=("Stars", "count"),
        Avg_Stars=("Stars", "mean")
    ).reset_index().sort_values(by="Count", ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=style_agg["Style"],
        y=style_agg["Count"],
        name="Review Volume",
        marker_color=[STYLE_COLORS.get(s, "#38bdf8") for s in style_agg["Style"]],
        opacity=0.85
    ))
    fig.add_trace(go.Scatter(
        x=style_agg["Style"],
        y=style_agg["Avg_Stars"],
        name="Average Stars (1-5)",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="#f59e0b", width=3)
    ))

    fig.update_layout(
        title="Packaging Style Popularity vs. Average Quality Score",
        yaxis=dict(title="Review Count", gridcolor="rgba(255,255,255,0.1)"),
        yaxis2=dict(title="Avg Stars", overlaying="y", side="right", range=[0, 5], showgrid=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        height=380,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def build_flavor_radar(df):
    """Polar radar chart of average ratings across flavor categories."""
    flavors = df.groupby("Flavor_Profile")["Stars"].mean().reset_index()
    fig = go.Figure()

    r = flavors["Stars"].tolist() + [flavors["Stars"].iloc[0]]
    theta = flavors["Flavor_Profile"].tolist() + [flavors["Flavor_Profile"].iloc[0]]

    fig.add_trace(go.Scatterpolar(
        r=r,
        theta=theta,
        fill='toself',
        fillcolor="rgba(244, 63, 94, 0.35)",
        line=dict(color="#f43f5e", width=3),
        name="Flavor Profile Avg Rating"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[2.5, 4.5], gridcolor="rgba(255,255,255,0.15)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.15)")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        height=380,
        margin=dict(l=40, r=40, t=30, b=30)
    )
    return fig

def build_3d_brand_landscape(brand_stats):
    """
    3D Brand Scatter Space:
    X: Review Count (Market Presence)
    Y: Avg Stars (Quality)
    Z: Top 10 Placements (Elite Recognition)
    Color: Avg Stars
    """
    fig = px.scatter_3d(
        brand_stats[brand_stats["review_count"] >= 3],
        x="review_count",
        y="avg_stars",
        z="top_ten_count",
        color="avg_stars",
        size="review_count",
        size_max=30,
        hover_name="Brand",
        hover_data={"country": True, "review_count": True, "avg_stars": ":.2f", "top_ten_count": True},
        color_continuous_scale="Viridis",
        labels={
            "review_count": "Total Variety Reviews",
            "avg_stars": "Average Rating (1-5)",
            "top_ten_count": "Top 10 Global Awards"
        }
    )

    fig.update_layout(
        title="3D Global Ramen Brand Landscape (Volume × Quality × Top 10 Awards)",
        scene=dict(
            xaxis=dict(title="Review Volume", backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title="Average Stars", backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)"),
            zaxis=dict(title="Top 10 Awards", backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)"),
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.3))
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        height=600,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def build_3d_globe_ratings(df):
    """3D Globe plotting average ramen ratings across countries."""
    country_agg = df.groupby("Country").agg(
        Count=("Stars", "count"),
        Avg_Rating=("Stars", "mean")
    ).reset_index()

    fig = px.choropleth(
        country_agg,
        locations="Country",
        locationmode="country names",
        color="Avg_Rating",
        hover_name="Country",
        hover_data={"Count": True, "Avg_Rating": ":.2f"},
        projection="orthographic",
        color_continuous_scale="Plasma",
        title="3D Global Ramen Rating Geography"
    )

    fig.update_geos(
        showcoastlines=True, coastlinecolor="rgba(255,255,255,0.3)",
        showland=True, landcolor="#1e293b",
        showocean=True, oceancolor="#0b132b",
        bgcolor="rgba(0,0,0,0)"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        height=580,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def build_4d_era_animation(df):
    """
    4D Chronological Review Evolution:
    - Dim 1 (X): Review # (Time sequence)
    - Dim 2 (Y): Stars (1-5)
    - Dim 3 (Z): Variety Name Length (Descriptive Flavor Density)
    - Dim 4 (Color): Style
    - Dim 5 (Size): Rating Stars
    - Animation Frame: Review_Era (Chronological Epochs 1 to 6)
    """
    df_anim = df.copy()
    df_anim["Name_Length"] = df_anim["Variety"].str.len()
    df_anim["Review_Era_Str"] = df_anim["Review_Era"].astype(str)

    fig = px.scatter_3d(
        df_anim,
        x="Review #",
        y="Stars",
        z="Name_Length",
        color="Style",
        size="Stars",
        size_max=14,
        animation_frame="Review_Era_Str",
        animation_group="Brand",
        hover_name="Variety",
        hover_data={"Brand": True, "Country": True, "Stars": True, "Style": True},
        color_discrete_map=STYLE_COLORS,
        range_x=[0, 2600],
        range_y=[0, 5.2],
        range_z=[5, 90],
        labels={
            "Review #": "Review Sequence #",
            "Stars": "Star Rating (0-5)",
            "Name_Length": "Flavor Description Length"
        }
    )

    fig.update_layout(
        title="4D Review Epoch Evolution (Dimensions: Chronology × Stars × Flavor Density × Style × Era)",
        scene=dict(
            xaxis=dict(title="Review #", backgroundcolor="#0b132b", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title="Stars", backgroundcolor="#0b132b", gridcolor="rgba(255,255,255,0.1)"),
            zaxis=dict(title="Description Complexity", backgroundcolor="#0b132b", gridcolor="rgba(255,255,255,0.1)"),
            camera=dict(eye=dict(x=1.7, y=1.7, z=1.2))
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        height=620,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig
