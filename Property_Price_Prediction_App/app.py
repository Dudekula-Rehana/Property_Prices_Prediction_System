import streamlit as st
from predict import predict_price

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="Property Price Prediction",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

.main{
    background:#f4f7fc;
}

.hero{
    background:linear-gradient(90deg,#1e3a8a,#2563eb);
    padding:30px;
    border-radius:15px;
    color:white;
    text-align:center;
    margin-bottom:25px;
}

.hero h1{
    font-size:42px;
    margin-bottom:10px;
}

.hero p{
    font-size:18px;
}

.result-card{
    background:linear-gradient(90deg,#16a34a,#22c55e);
    color:white;
    padding:25px;
    border-radius:15px;
    text-align:center;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:30px;
}

</style>
""",unsafe_allow_html=True)

# -----------------------------
# HERO SECTION
# -----------------------------

st.markdown("""
<div class='hero'>

<h1>🏠 Property Price Prediction System</h1>

<p>
Estimate residential property prices using
Machine Learning (ElasticNet Regression)
</p>

</div>
""",unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.title("🏠 About")

    st.success("""
### Machine Learning

✔ ElasticNet Regression

✔ 11 Selected Features

✔ Scikit-Learn

✔ Streamlit
""")

    st.info("""
### Developer

Rehana Dudekula

M.Sc Health Informatics

Machine Learning Project
""")

# -----------------------------
# INPUT FORM
# -----------------------------

st.markdown("## 📝 Property Details")

st.write("Fill all property information below.")

with st.form("prediction_form"):

    col1,col2=st.columns(2)

    with col1:

        st.subheader("📍 Location")

        neighborhood=st.selectbox(
            "Neighborhood",
            [
                "CollgCr",
                "Veenker",
                "Crawfor",
                "NoRidge",
                "Mitchel",
                "Somerst",
                "NWAmes",
                "OldTown",
                "BrkSide",
                "Sawyer",
                "NridgHt",
                "NAmes",
                "Edwards",
                "Timber"
            ]
        )

        overall_qual=st.slider(
            "Overall Quality",
            1,
            10,
            5
        )

        overall_cond=st.slider(
            "Overall Condition",
            1,
            10,
            5
        )

        property_size=st.number_input(
            "Lot Area (sq ft)",
            min_value=1000,
            value=8000
        )

        year_built=st.number_input(
            "Year Built",
            min_value=1900,
            max_value=2025,
            value=2000
        )

    with col2:

        st.subheader("🏡 House Details")

        gr_liv_area=st.number_input(
            "Ground Living Area",
            min_value=300,
            value=1500
        )

        first_floor=st.number_input(
            "1st Floor Area",
            min_value=300,
            value=1000
        )

        second_floor=st.number_input(
            "2nd Floor Area",
            min_value=0,
            value=500
        )

        basement=st.number_input(
            "Basement Area",
            min_value=0,
            value=500
        )

        house_age=st.number_input(
            "House Age",
            min_value=0,
            max_value=200,
            value=25
        )

    submit=st.form_submit_button(
        "🚀 Predict Property Price",
        use_container_width=True
    )



    # -------------------------------------------------
# PREDICTION
# -------------------------------------------------

if submit:

    total_sf = first_floor + second_floor + basement

    # Default value since bathrooms are not collected
    total_bath = 2.5

    prediction = predict_price(
        neighborhood,
        overall_qual,
        overall_cond,
        property_size,
        gr_liv_area,
        first_floor,
        second_floor,
        year_built,
        total_sf,
        total_bath,
        house_age
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # PREDICTED PRICE
    # -----------------------------

    st.markdown(
        f"""
        <div class="result-card">
            <h2>💰 Estimated Property Price</h2>
            <h1>₹ {prediction:,.0f}</h1>
            <p>Predicted using ElasticNet Regression Model</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.balloons()

    st.markdown("## 📊 Property Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "⭐ Overall Quality",
            f"{overall_qual}/10"
        )

    with c2:
        st.metric(
            "🏡 House Age",
            f"{house_age} Years"
        )

    with c3:
        st.metric(
            "📐 Total Area",
            f"{total_sf:,} sq.ft"
        )

    st.markdown("---")

    st.markdown("## 🤖 Model Information")

    left, right = st.columns(2)

    with left:

        st.success("""
### Model

✔ ElasticNet Regression

✔ Feature Scaling

✔ OneHot Encoding

✔ Scikit-Learn Pipeline
""")

    with right:

        st.info("""
### Performance

📈 R² Score : **0.89**

📉 RMSE : **0.136**

📊 Features Used : **11**

🚀 Deployment : **Streamlit**
""")

    st.markdown("---")

    st.markdown("### 📍 Input Summary")

    summary1, summary2 = st.columns(2)

    with summary1:

        st.write(f"**Neighborhood:** {neighborhood}")
        st.write(f"**Lot Area:** {property_size:,} sq.ft")
        st.write(f"**Ground Living Area:** {gr_liv_area:,} sq.ft")
        st.write(f"**Year Built:** {year_built}")
        st.write(f"**House Age:** {house_age} Years")

    with summary2:

        st.write(f"**Overall Quality:** {overall_qual}/10")
        st.write(f"**Overall Condition:** {overall_cond}/10")
        st.write(f"**1st Floor Area:** {first_floor:,} sq.ft")
        st.write(f"**2nd Floor Area:** {second_floor:,} sq.ft")
        st.write(f"**Basement Area:** {basement:,} sq.ft")

st.markdown("---")

st.markdown(
    """
<div class="footer">

<h3>🏠 Property Price Prediction System</h3>

<p>
Built using <b>Python</b> • <b>Streamlit</b> • <b>Scikit-Learn</b>
</p>

<p>
Machine Learning Model : <b>ElasticNet Regression</b>
</p>

<hr>

<p>
Developed by <b>Rehana Dudekula</b>
</p>

</div>
""",
    unsafe_allow_html=True
)