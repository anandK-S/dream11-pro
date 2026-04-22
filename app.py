import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- Optional: Add a custom theme in .streamlit/config.toml ---
# [theme]
# primaryColor = "#00d2d3"
# backgroundColor = "#0a0f1c"
# secondaryBackgroundColor = "#1f2c4a"
# textColor = "#ffffff"

# --- Page Configuration ---
st.set_page_config(
    page_title="IPL Dream11 Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Dummy Data Generation ---
def load_dummy_data():
    data = {
        'Player': ['David Warner', 'Sanju Samson', 'Hardik Pandya', 'Yuzvendra Chahal', 'Ravindra Jadeja',
                   'KL Rahul', 'Virat Kohli', 'Mohammed Siraj', 'Shubman Gill', 'Rishabh Pant'],
        'Role': ['All‑rounder', 'All‑rounder', 'Bowler', 'Bowler', 'All‑rounder',
                 'Batsman', 'Batsman', 'Bowler', 'Batsman', 'Wicketkeeper'],
        'Score': [836.4114, 822.2970, 808.4083, 793.3620, 765.8081, 755.3020,
                  740.1000, 724.1558, 710.2000, 705.7945],
        'Runs': [383, 458, 201, 15, 120, 500, 600, 10, 480, 350],
        'StrikeRate': [135.5, 142.3, 150.2, 50.0, 145.6, 138.9, 140.0, 40.0, 148.5, 155.0],
        'Wickets': [0, 0, 15, 22, 10, 0, 0, 18, 0, 0],
        'Economy': [0.0, 0.0, 8.5, 7.2, 7.8, 0.0, 0.0, 7.5, 0.0, 0.0],
        'Catches': [5, 8, 4, 2, 9, 6, 10, 3, 5, 12]
    }
    df = pd.DataFrame(data)
    df["Label"] = df["Player"] + " | " + df["Role"]
    return df

df = load_dummy_data()

# --- Sidebar Navigation ---
st.sidebar.title("🏏 IPL Dream11 Pro")
st.sidebar.markdown("by **Dream11 Pro**")

st.sidebar.subheader("Match Selection")
team1 = st.sidebar.selectbox(
    "Team 1",
    ["CSK", "KKR", "SRH", "MI", "PBKS", "RR", "DC", "LSG", "GT", "RCB"],
    key="team1"
)
team2 = st.sidebar.selectbox(
    "Team 2",
    ["RCB", "CSK", "KKR", "SRH", "MI", "PBKS", "RR", "DC", "LSG", "GT"],
    key="team2"
)

st.sidebar.subheader("Navigation")
page = st.sidebar.radio(
    "",
    ["Welcome Match Center", "Dashboard", "Visualizations", "Player Comparison", "Team Generator"],
    index=0
)

# --- Helper style markdown ---
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 600; color: #00d2d3; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.2rem; color: #bbf; margin-top: 0.1rem; }
    .metric-card { background: #1f2c4a; border-radius: 8px; padding: 12px; }
</style>
""", unsafe_allow_html=True)

# --- Pages ---
if page == "Welcome Match Center":
    st.markdown('<h1 class="main-title">🏡 Welcome Match Center</h1>', unsafe_allow_html=True)

    # Match Info
    col_info1, col_info2 = st.columns([2, 1])
    with col_info1:
        st.markdown("📍 **Venue:** Neutral Venue")
        st.markdown("🏏 **Pitch:** Balanced")
        st.markdown("☀️ **Weather:** Clear")
        st.markdown("⚡ **Toss:** Team 1 won the toss")

    with col_info2:
        st.markdown("### 🏆 Match Info")
        st.markdown(f"**{team1} vs {team2}**")
        st.markdown("**Format:** T20 | 20 overs each")

    st.divider()

    # Win Probability & Top Picks
    col1, col2 = st.columns([1, 2], gap="medium")
    with col1:
        st.markdown("### 📊 Win Probability")
        fig_pie = px.pie(
            values=[45, 55],
            names=[team1, team2],
            hole=0.4,
            color_discrete_sequence=["#1f77b4", "#00d2d3"],
            labels={team1: f"{team1} 45%", team2: f"{team2} 55%"}
        )
        fig_pie.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=True,
            legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center")
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("### 🏅 Top Fantasy Picks Today")
        top_5 = df[["Player", "Role", "Score"]].nlargest(5, "Score")
        st.dataframe(
            top_5,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Score": st.column_config.NumberColumn("Fantasy Score", format="%.1f")
            }
        )

        st.markdown("### 🤖 AI Squad Suggestions")
        cap = "David Warner"
        vc = "Sanju Samson"
        st.success(f"**Captain:** {cap}")
        st.info(f"**Vice‑Captain:** {vc}")


elif page == "Dashboard":
    st.markdown('<h1 class="main-title">📊 Match Performance Dashboard</h1>', unsafe_allow_html=True)

    # Top Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        top_batsman = df.loc[df["Runs"].idxmax()]
        st.metric(
            label="Top Run Scorer",
            value=top_batsman["Player"],
            delta=f"{int(top_batsman["Runs"])} runs"
        )
    with col2:
        top_bowler = df.loc[df["Wickets"].idxmax()]
        st.metric(
            label="Top Wicket‑Taker",
            value=top_bowler["Player"],
            delta=f"{int(top_bowler["Wickets"])} wickets"
        )
    with col3:
        st.metric(label="Total Players", value=len(df))

    st.divider()

    with st.expander("🔍 View Full Player Stats", expanded=True):
        st.dataframe(
            df[["Label", "Runs", "Wickets", "StrikeRate", "Economy", "Score"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Runs": st.column_config.NumberColumn("Runs", format="%d"),
                "Wickets": st.column_config.NumberColumn("Wickets", format="%d"),
                "StrikeRate": st.column_config.NumberColumn("SR", format="%.1f"),
                "Economy": st.column_config.NumberColumn("Eco", format="%.1f"),
                "Score": st.column_config.NumberColumn("Fantasy Score", format="%.1f"),
            }
        )


elif page == "Visualizations":
    st.markdown('<h1 class="main-title">📈 Match Visualizations</h1>', unsafe_allow_html=True)

    # Top Run Scorers
    st.markdown("### 🏏 Top Run Scorers")
    top_7 = df.nlargest(7, "Runs")
    fig_bar = px.bar(
        top_7,
        x="Player",
        y="Runs",
        color="Role",
        text="Runs",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_bar.update_traces(textposition="inside")
    fig_bar.update_layout(
        template="plotly_dark",
        xaxis_title="Player",
        yaxis_title="Runs",
        margin=dict(t=30, b=0, l=0, r=0)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Bowling Performance Scatter
    st.markdown("### 🎯 Bowling Performance")
    bowlers = df[df["Role"].isin(["Bowler", "All‑rounder"])]
    fig_scatter = px.scatter(
        bowlers,
        x="Wickets",
        y="Economy",
        color="Role",
        size="Score",
        hover_name="Player",
        hover_data=["Runs", "StrikeRate"],
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_scatter.update_layout(
        template="plotly_dark",
        xaxis_title="Wickets",
        yaxis_title="Economy Rate",
        margin=dict(t=30, b=0, l=0, r=0)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


elif page == "Player Comparison":
    st.markdown('<h1 class="main-title">⚔️ Player Comparison Tool</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        player1 = st.selectbox(
            "Select Player 1",
            options=df["Label"].unique(),
            index=0,  # default: David Warner
            format_func=lambda x: x.split(" | ")[0],
        )
    with col2:
        player2 = st.selectbox(
            "Select Player 2",
            options=df["Label"].unique(),
            index=6,  # default: Virat Kohli
            format_func=lambda x: x.split(" | ")[0],
        )

    # Parse selected players
    p1_name = player1.split(" | ")[0]
    p2_name = player2.split(" | ")[0]

    comp_df = df[df["Player"].isin([p1_name, p2_name])].copy()
    labels = [p1_name, p2_name]

    # Summary row
    with st.expander("📊 Overview", expanded=True):
        st.dataframe(
            comp_df[["Player", "Role", "Runs", "Wickets", "StrikeRate", "Economy", "Score"]],
            use_container_width=True,
            hide_index=True
        )

    # Comparison Bar Chart
    fig_comp = go.Figure()
    metrics = ["Runs", "Wickets", "Score"]
    colors = {"Runs": "#a29bfe", "Wickets": "#fdcb6e", "Score": "#e17055"}

    for metric in metrics:
        fig_comp.add_trace(go.Bar(
            x=labels,
            y=comp_df[metric].values,
            name=metric,
            marker_color=colors[metric]
        ))

    fig_comp.update_layout(
        barmode="group",
        template="plotly_dark",
        margin=dict(t=30, b=20, l=40, r=40),
        xaxis_title="Player",
        yaxis_title="Value"
    )
    st.plotly_chart(fig_comp, use_container_width=True)


elif page == "Team Generator":
    st.markdown('<h1 class="main-title">⚙️ AI Dream11 Team Generator</h1>', unsafe_allow_html=True)

    st.markdown("### 🏏 Recommended Dream11 XI")
    team = df.nlargest(11, "Score")
    st.dataframe(
        team[["Label", "Runs", "Wickets", "Score"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Runs": st.column_config.NumberColumn("Runs", format="%d"),
            "Wickets": st.column_config.NumberColumn("Wickets", format="%d"),
            "Score": st.column_config.NumberColumn("Fantasy Score", format="%.1f"),
        }
    )

    # AI Captain / VC
    cap = "David Warner"
    vc = "Sanju Samson"
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🤖 AI Captain")
        st.success(f"**{cap}**")
    with col_b:
        st.markdown("### 🤖 AI Vice‑Captain")
        st.info(f"**{vc}**")

    # Download Button
    st.download_button(
        label="📥 Download Team (CSV)",
        data=team[["Player", "Role", "Runs", "Wickets", "Score"]].to_csv(index=False),
        file_name="dream11_team.csv",
        mime="text/csv",
        use_container_width=True
    )

    # ML‑style bar (Top Predicted Performers)
    st.markdown("### 🤖 ML‑Based Predicted Performers")
    top_8 = df.nlargest(8, "Score")
    fig_ml = px.bar(
        top_8,
        x="Player",
        y="Score",
        color="Role",
        text="Score",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_ml.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig_ml.update_layout(
        template="plotly_dark",
        xaxis_title="Player",
        yaxis_title="Fantasy Score",
        margin=dict(t=30, b=20, l=40, r=40)
    )
    st.plotly_chart(fig_ml, use_container_width=True)