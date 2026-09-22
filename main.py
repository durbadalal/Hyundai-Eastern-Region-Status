import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Hyundai Eastern Region - Dealer Sales & Service Network",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; padding-bottom: 2.5rem; }
    .stMetric { background-color: #f8f9fa; padding: 12px; border-radius: 8px; border: 1px solid #dee2e6; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# MOCK DATA GENERATION - EASTERN REGION DEALERSHIPS
# ==============================================================================
@st.cache_data
def generate_eastern_region_data():
    np.random.seed(101)
    n_records = 800
    
    region_structure = {
        "West Bengal": {
            "Mukesh Hyundai": ["EM Bypass", "VIP Road", "Rajarhat"],
            "Spring Hyundai": ["Behala", "Maheshtala"],
            "Bengal Hyundai": ["Alipore", "Howrah"],
            "Saini Hyundai": ["Chinar Park", "Gariahat", "Siliguri"]
        },
        "Odisha": {
            "Utkal Hyundai": ["Bhubaneswar Main", "Cuttack Road"],
            "Bhubaneshwar Hyundai": ["Patia", "Puri Highway"]
        },
        "Bihar": {
            "Patna Hyundai": ["Boring Road", "Kankarbagh"],
            "Grand Hyundai": ["Muzaffarpur", "Gaya"]
        },
        "Jharkhand": {
            "Ranchi Hyundai": ["Main Road Ranchi", "Bariatu"],
            "Capitol Hyundai": ["Jamshedpur", "Dhanbad"]
        },
        "Assam": {
            "Saraighat Hyundai": ["Guwahati GS Road", "Dispur"],
            "Brahmaputra Hyundai": ["Dibrugarh", "Jorhat"]
        }
    }
    
    models = ["Creta", "Venue", "i20", "Exter", "Verna", "Alcazar", "Tucson"]
    service_types = ["Periodic Maintenance", "Free Service 1/2/3", "Accidental Bodywork", "Pre-Monsoon Checkup"]
    
    records = []
    for _ in range(n_records):
        state = np.random.choice(list(region_structure.keys()))
        dealer = np.random.choice(list(region_structure[state].keys()))
        branch = np.random.choice(region_structure[state][dealer])
        model = np.random.choice(models, p=[0.35, 0.25, 0.15, 0.12, 0.08, 0.03, 0.02])
        
        sales_rev = np.random.randint(650000, 2200000)
        service_rev = np.random.randint(3000, 28000)
        csat = np.random.choice([3, 4, 5], p=[0.08, 0.22, 0.70])
        
        records.append({
            "State": state,
            "Dealership": dealer,
            "Branch_Location": branch,
            "Car_Model": model,
            "Sales_Revenue": sales_rev,
            "Service_Revenue": service_rev,
            "Service_Type": np.random.choice(service_types),
            "CSAT_Rating": csat,
            "Month": np.random.choice(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"])
        })
        
    return pd.DataFrame(records)

# ==============================================================================
# CAMPAIGN GENERATOR (WITH ROBUST FALLBACK)
# ==============================================================================
def generate_regional_ai_copy(state, dealer, branch, model, campaign_type, api_key):
    if api_key and api_key.strip():
        try:
            import openai
            client = openai.OpenAI(api_key=api_key.strip())
            prompt = f"""
            You are the Regional Marketing Director for Hyundai Motor India (Eastern Region).
            Create a localized marketing message or service reminder targeted at Hyundai customers in {state}.
            
            Parameters:
            - Target State: {state}
            - Dealership & Branch: {dealer} ({branch})
            - Car Model: Hyundai {model}
            - Objective: {campaign_type}
            
            Formatting Requirements:
            1. **WhatsApp / SMS Teaser Header**
            2. **Message Content** (Include appropriate regional references)
            3. **Call To Action (CTA)**
            """
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception:
            pass  # Fallback code executes smoothly if API key fails or quota exceeds

    # Standard Fallback Template
    return f"""
### 🚗 Exclusive Regional Offer from {dealer} ({branch})

**Dear Valued Customer,**

Greetings from **{dealer} ({branch}, {state})**! 

We are excited to bring you a special promotional event for the **Hyundai {model}** for our customers across **{state}**.

* **Campaign Focus:** {campaign_type}
* **Exclusive Dealership Privilege:** Complimentary 50-Point Safety Checkup & Special Exchange Bonus.
* **Special Event Note:** Tailored seasonal perks available for a limited period at our {branch} outlet.

**Call To Action (CTA):**
📲 Visit {dealer} ({branch}) today or book your test drive / service slot instantly via the **Hyundai Care App**.
*Contact Showroom Desk: +91 98300 XXXXX*
"""

# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/44/Hyundai_Motor_Company_logo.svg", width=150)
    st.title("Eastern Region Portal")
    st.markdown("---")
    
    df_raw = generate_eastern_region_data()
    
    st.subheader("1. Filter Region & Dealers")
    selected_states = st.multiselect(
        "Select State(s):",
        options=df_raw["State"].unique().tolist(),
        default=df_raw["State"].unique().tolist()
    )
    
    filtered_df = df_raw[df_raw["State"].isin(selected_states)]
    
    dealer_options = filtered_df["Dealership"].unique().tolist()
    selected_dealers = st.multiselect(
        "Filter Dealership(s):",
        options=dealer_options,
        default=dealer_options
    )
    
    filtered_df = filtered_df[filtered_df["Dealership"].isin(selected_dealers)]
    
    st.markdown("---")
    st.subheader("2. AI Settings")
    openai_api_key = st.text_input("OpenAI API Key (Optional)", type="password", help="Enter key for live AI generation. If blank, standard regional template will be generated.")
    
    st.caption("Hyundai Motor India - Eastern Regional Office")

# ==============================================================================
# MAIN BODY
# ==============================================================================
st.title("🚗 Hyundai Eastern Region - Dealership Sales & Service Tracker")
st.markdown("Unified portal monitoring dealer network performance, car model trends, service revenue, and regional marketing.")

tab1, tab2, tab3 = st.tabs(["📊 Regional Overview", "🛠️ Service Network Analysis", "🤖 Regional AI Outreach"])

# ------------------------------------------------------------------------------
# TAB 1: REGIONAL OVERVIEW
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("Eastern Zone Performance Summary")
    
    c1, c2, c3, c4 = st.columns(4)
    tot_sales = filtered_df["Sales_Revenue"].sum()
    tot_service = filtered_df["Service_Revenue"].sum()
    top_dealer = filtered_df.groupby("Dealership")["Sales_Revenue"].sum().idxmax() if not filtered_df.empty else "N/A"
    avg_csat = filtered_df["CSAT_Rating"].mean() if not filtered_df.empty else 0.0
    
    c1.metric("Total Sales Revenue", f"₹{tot_sales/1e7:.2f} Cr")
    c2.metric("Total Service Revenue", f"₹{tot_service/1e5:.2f} Lakhs")
    c3.metric("Top Dealership", top_dealer)
    c4.metric("Avg CSAT Rating", f"{avg_csat:.2f} / 5.0")
    
    st.markdown("---")
    
    r1_col1, r1_col2 = st.columns(2)
    
    with r1_col1:
        st.markdown("**Sales Revenue by State**")
        state_sales = filtered_df.groupby("State")["Sales_Revenue"].sum().reset_index()
        fig_state = px.bar(
            state_sales, x="State", y="Sales_Revenue", color="State",
            labels={"Sales_Revenue": "Revenue (INR)"},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_state, use_container_width=True)
        
    with r1_col2:
        st.markdown("**Vehicle Model Demand Breakdown**")
        model_sales = filtered_df.groupby("Car_Model")["Sales_Revenue"].sum().reset_index()
        fig_model = px.pie(
            model_sales, names="Car_Model", values="Sales_Revenue", hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_model, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 2: SERVICE NETWORK ANALYSIS
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("Dealer Service Efficiency & Metrics")
    
    sc1, sc2 = st.columns(2)
    
    with sc1:
        st.markdown("**Service Revenue by Dealership**")
        dealer_service = filtered_df.groupby("Dealership")["Service_Revenue"].sum().reset_index().sort_values(by="Service_Revenue", ascending=False)
        fig_dealer_serv = px.bar(
            dealer_service, x="Service_Revenue", y="Dealership", orientation='h',
            color="Dealership", color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_dealer_serv, use_container_width=True)
        
    with sc2:
        st.markdown("**Service Type Revenue Distribution**")
        serv_type_df = filtered_df.groupby("Service_Type")["Service_Revenue"].sum().reset_index()
        fig_serv_type = px.pie(
            serv_type_df, names="Service_Type", values="Service_Revenue",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig_serv_type, use_container_width=True)
        
    st.markdown("**Detailed Dealer Records**")
    st.dataframe(
        filtered_df[['State', 'Dealership', 'Branch_Location', 'Car_Model', 'Sales_Revenue', 'Service_Revenue', 'CSAT_Rating']],
        use_container_width=True,
        hide_index=True
    )

# ------------------------------------------------------------------------------
# TAB 3: REGIONAL AI OUTREACH
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("Eastern Region AI Campaign Generator")
    st.markdown("Create state-specific sales offers, festival campaign copy, or automated service reminders.")
    
    col_in, col_out = st.columns([1, 1.2])
    
    with col_in:
        sel_state = st.selectbox("Select Target State:", filtered_df["State"].unique())
        avail_dealers = filtered_df[filtered_df["State"] == sel_state]["Dealership"].unique()
        sel_dealer = st.selectbox("Select Dealership:", avail_dealers)
        avail_branches = filtered_df[(filtered_df["State"] == sel_state) & (filtered_df["Dealership"] == sel_dealer)]["Branch_Location"].unique()
        sel_branch = st.selectbox("Select Branch:", avail_branches)
        sel_model = st.selectbox("Target Vehicle:", filtered_df["Car_Model"].unique())
        
        campaign_type = st.selectbox(
            "Campaign / Communication Purpose:",
            [
                "Festive Season Special Offer (Durga Puja / Chhath / Bihu)",
                "Pre-Monsoon Free Inspection & Service Camp",
                "Exchange Bonus & Upgrade Drive to Creta/Alcazar",
                "Periodic Maintenance Renewal WhatsApp Reminder"
            ]
        )
        
        generate_btn = st.button("🚀 Generate Regional Marketing Copy", type="primary", use_container_width=True)
        
    with col_out:
        if generate_btn:
            with st.spinner("Generating regional copy..."):
                output = generate_regional_ai_copy(
                    sel_state, sel_dealer, sel_branch, sel_model, campaign_type, openai_api_key
                )
                st.markdown("### Generated Communication")
                st.success(output)
        else:
            st.info("👈 Select options on the left and click **Generate Regional Marketing Copy**.")