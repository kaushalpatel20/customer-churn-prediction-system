import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from joblib import load
import shap
import os
import xgboost
import plotly.graph_objects as go
from styles import CSS, FONTS, HEADER_HTML, FOOTER_HTML

# ─── Page Config ───
st.set_page_config(
    page_title="ChurnGuard — Customer Churn Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Inject Fonts + CSS + Header ───
st.markdown(FONTS, unsafe_allow_html=True)
st.markdown(CSS, unsafe_allow_html=True)
st.markdown(HEADER_HTML, unsafe_allow_html=True)

# 1. Define the correct path to the models folder (one level up from 'app')
current_dir = os.path.dirname(__file__)
models_folder = os.path.abspath(os.path.join(current_dir, "..", "models"))

# 2. Load all your models using the correct folder path
logistic_model = load(os.path.join(models_folder, "logistic_model.pkl"))
rf_model       = load(os.path.join(models_folder, "rf_model.pkl"))
xgb_model      = load(os.path.join(models_folder, "xgb_model.pkl"))

print("[OK] All models (Logistic, RF, and XGBoost) loaded successfully!")

# ─── Sidebar ───
with st.sidebar:
    st.markdown("""<div style="display:flex;align-items:center;gap:10px;padding:8px 0 18px 0;">
        <span style="font-size:26px;">📊</span>
        <span style="font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;color:#EAEAF0;">ChurnGuard</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="font-family:'Space Grotesk',sans-serif;font-size:11px;font-weight:700;
        color:#6C63FF;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;">🎛️ Model Selection</div>""",
        unsafe_allow_html=True)
    model_choice = st.radio(
        "Choose model",
        ["Logistic Regression", "Random Forest", "XGBoost"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""<div style="font-family:'Space Grotesk',sans-serif;font-size:11px;font-weight:700;
        color:#6C63FF;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;">📋 Dataset Stats</div>""",
        unsafe_allow_html=True)
    st.markdown("""<div style="background:#1A1D27;border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:14px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
            <span style="color:#8B8FA8;font-size:13px;">Rows</span>
            <span style="color:#EAEAF0;font-family:'JetBrains Mono';font-size:13px;">7,043</span></div>
        <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
            <span style="color:#8B8FA8;font-size:13px;">Features</span>
            <span style="color:#EAEAF0;font-family:'JetBrains Mono';font-size:13px;">21</span></div>
        <div style="display:flex;justify-content:space-between;">
            <span style="color:#8B8FA8;font-size:13px;">Churn Rate</span>
            <span style="color:#FF4C6A;font-family:'JetBrains Mono';font-size:13px;">26.5%</span></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div style="font-family:'Space Grotesk',sans-serif;font-size:11px;font-weight:700;
        color:#6C63FF;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;">⚡ Model Comparison</div>""",
        unsafe_allow_html=True)
    compare_df = pd.DataFrame({
        "Model": ["LR", "RF", "XGB"],
        "AUC": ["0.86", "0.85", "0.85"],
        "F1": ["0.64", "0.65", "0.63"]
    }).set_index("Model")
    st.dataframe(compare_df, use_container_width=True)

tab1, tab2 = st.tabs(["🎯 Predict Customer", "📊 Model Insights"])
preprocessor = rf_model.named_steps["preprocessor"]
rf_classifier = rf_model.named_steps["model"]

with tab1:


    gender = st.selectbox("Gender", ["Male","Female"])
    senior = st.selectbox("Senior Citizen", [0,1])
    partner = st.selectbox("Partner", ["Yes","No"])
    dependents = st.selectbox("Dependents", ["Yes","No"])

    tenure = st.slider("Tenure (months)",0,72)

    phoneservice = st.selectbox("Phone Service", ["Yes","No"])
    multiplelines = st.selectbox("Multiple Lines", ["Yes","No","No phone service"])

    internet = st.selectbox("Internet Service", ["DSL","Fiber optic","No"])

    onlinesecurity = st.selectbox("Online Security", ["Yes","No","No internet service"])
    onlinebackup = st.selectbox("Online Backup", ["Yes","No","No internet service"])
    deviceprotection = st.selectbox("Device Protection", ["Yes","No","No internet service"])
    techsupport = st.selectbox("Tech Support", ["Yes","No","No internet service"])

    streamingtv = st.selectbox("Streaming TV", ["Yes","No","No internet service"])
    streamingmovies = st.selectbox("Streaming Movies", ["Yes","No","No internet service"])

    contract = st.selectbox("Contract", ["Month-to-month","One year","Two year"])
    paperless = st.selectbox("Paperless Billing", ["Yes","No"])

    payment = st.selectbox(
        "Payment Method",
        ["Electronic check","Mailed check","Bank transfer (automatic)","Credit card (automatic)"]
    )

    monthly = st.number_input("Monthly Charges",0.0,200.0)
    total = st.number_input("Total Charges",0.0,10000.0)


    data = pd.DataFrame({
    "gender":[gender],
    "SeniorCitizen":[senior],
    "Partner":[partner],
    "Dependents":[dependents],
    "tenure":[tenure],
    "PhoneService":[phoneservice],
    "MultipleLines":[multiplelines],
    "InternetService":[internet],
    "OnlineSecurity":[onlinesecurity],
    "OnlineBackup":[onlinebackup],
    "DeviceProtection":[deviceprotection],
    "TechSupport":[techsupport],
    "StreamingTV":[streamingtv],
    "StreamingMovies":[streamingmovies],
    "Contract":[contract],
    "PaperlessBilling":[paperless],
    "PaymentMethod":[payment],
    "MonthlyCharges":[monthly],
    "TotalCharges":[total]
    })

    X_transformed = preprocessor.transform(data)
    feature_names = preprocessor.get_feature_names_out()
    X_transformed_df = pd.DataFrame(
        X_transformed,
        columns=feature_names
    )
    explainer = shap.TreeExplainer(rf_classifier)


    if model_choice == "Logistic Regression":
        model = logistic_model
    elif model_choice == "Random Forest":
        model = rf_model
    else:
        model = xgb_model

    if st.button("Predict Churn"):
        with st.spinner("Analyzing customer profile..."):
            prob = model.predict_proba(data)[0][1]

        # ── Determine risk level ──
        if prob > 0.6:
            risk_label, risk_color, risk_desc = "HIGH RISK", "#FF4C6A", "This customer is very likely to churn. Immediate retention action recommended."
        elif prob > 0.3:
            risk_label, risk_color, risk_desc = "MEDIUM RISK", "#FFB547", "This customer shows moderate churn signals. Consider proactive engagement."
        else:
            risk_label, risk_color, risk_desc = "LOW RISK", "#00D9C0", "This customer appears stable. Continue standard service."

        # ── Result card container ──
        st.markdown(f"""<div style="background:#1A1D27;border:1px solid rgba(255,255,255,0.08);
            border-radius:16px;padding:30px;margin:20px 0;text-align:center;
            box-shadow:0 0 25px {risk_color}22;">""", unsafe_allow_html=True)

        # ── Plotly donut gauge ──
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            number={"font": {"family": "JetBrains Mono", "size": 48, "color": "#EAEAF0"}, "suffix": "%", "valueformat": ".1f"},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 0, "tickcolor": "#22263A",
                         "tickfont": {"color": "#8B8FA8", "family": "DM Sans"}},
                "bar": {"color": risk_color, "thickness": 0.25},
                "bgcolor": "#22263A",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30], "color": "rgba(0,217,192,0.08)"},
                    {"range": [30, 60], "color": "rgba(255,181,71,0.08)"},
                    {"range": [60, 100], "color": "rgba(255,76,106,0.08)"},
                ],
                "threshold": {
                    "line": {"color": risk_color, "width": 3},
                    "thickness": 0.8,
                    "value": prob * 100,
                },
            },
        ))
        gauge_fig.update_layout(
            height=280, margin=dict(t=30, b=10, l=40, r=40),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#8B8FA8"),
        )
        st.plotly_chart(gauge_fig, use_container_width=True)

        # ── Risk badge + description ──
        st.markdown(f"""
            <div style="display:flex;flex-direction:column;align-items:center;gap:10px;padding-bottom:8px;">
                <span style="background:{risk_color}22;color:{risk_color};font-family:'Space Grotesk',sans-serif;
                    font-weight:700;font-size:14px;padding:8px 24px;border-radius:20px;
                    border:1px solid {risk_color}44;letter-spacing:1px;">{risk_label}</span>
                <span style="color:#8B8FA8;font-family:'DM Sans',sans-serif;font-size:14px;
                    max-width:400px;">{risk_desc}</span>
                <span style="color:#8B8FA8;font-family:'DM Sans',sans-serif;font-size:12px;
                    margin-top:4px;">Model: <span style="color:#6C63FF;font-family:'JetBrains Mono';">{model_choice}</span></span>
            </div>
        """, unsafe_allow_html=True)

        # ── Styled progress bar ──
        st.markdown(f"""
            <div style="background:#22263A;border-radius:8px;height:8px;margin:0 20px 10px 20px;overflow:hidden;">
                <div style="width:{prob*100:.1f}%;height:100%;background:{risk_color};
                    border-radius:8px;transition:width 0.6s ease;"></div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Balloons for low risk ──
        if prob <= 0.3:
            st.balloons()

        # ── SHAP Explanation (untouched logic) ──
        st.markdown("""<div style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:700;
            color:#EAEAF0;margin:24px 0 12px 0;">🔍 Prediction Explanation (SHAP)</div>""", unsafe_allow_html=True)

        X_transformed = preprocessor.transform(data)

        explainer = shap.Explainer(rf_classifier)
        shap_values = explainer(X_transformed_df)

        fig = plt.figure()

        shap.plots.waterfall(
            shap_values[0, :, 1],
            show=False
        )
        st.pyplot(fig)

with tab2:
    preprocessor = rf_model.named_steps["preprocessor"]
    feature_names = preprocessor.get_feature_names_out()

    rf_classifier = rf_model.named_steps["model"]
    feature_importance = rf_classifier.feature_importances_

    # ── Performance data (original logic preserved) ──
    performance_df = pd.DataFrame({
        "Model": ["Logistic Regression", "Random Forest", "XGBoost"],
        "ROC AUC": [0.86, 0.85, 0.85],
        "F1 Score": [0.64, 0.65, 0.63],
        "Precision": [0.52, 0.56, 0.55],
        "Recall": [0.84, 0.78, 0.75]
    })

    # ── Get metrics for selected model ──
    _perf = performance_df[performance_df["Model"] == model_choice].iloc[0]
    _kpis = [
        ("🎯", "ROC AUC",   f"{_perf['ROC AUC']:.0%}",   "#6C63FF"),
        ("⚡", "Precision",  f"{_perf['Precision']:.0%}",  "#00D9C0"),
        ("🔍", "Recall",     f"{_perf['Recall']:.0%}",     "#FFB547"),
        ("📊", "F1 Score",   f"{_perf['F1 Score']:.0%}",   "#FF4C6A"),
    ]

    # ── KPI Cards Row ──
    kpi_cols = st.columns(4)
    for col, (icon, label, value, color) in zip(kpi_cols, _kpis):
        col.markdown(f"""
        <div class="hover-card" style="text-align:center;padding:22px 12px;">
            <div style="font-size:22px;margin-bottom:6px;">{icon}</div>
            <div style="font-family:'DM Sans',sans-serif;font-size:12px;color:#8B8FA8;
                text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">{label}</div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:32px;font-weight:700;
                color:{color};">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    # ── Feature Importance — Plotly bar chart (replaces matplotlib barh) ──
    feat_imp = pd.DataFrame({
        "feature": feature_names,
        "importance": feature_importance
    }).sort_values("importance", ascending=False)

    top_features = feat_imp.head(15).sort_values("importance", ascending=True)

    _colors = [f"rgba({108 + int(i*8)},{99 + int(i*10)},{255 - int(i*8)},0.85)" for i in range(len(top_features))]
    fi_fig = go.Figure(go.Bar(
        x=top_features["importance"],
        y=top_features["feature"],
        orientation="h",
        marker=dict(color=_colors, line=dict(width=0)),
    ))
    fi_fig.update_layout(
        title=dict(text="Top Factors Driving Churn", font=dict(family="Space Grotesk", size=18, color="#EAEAF0")),
        height=460,
        margin=dict(t=50, b=30, l=10, r=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#8B8FA8"),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False),
        yaxis=dict(showgrid=False),
    )
    st.markdown("""<div class="hover-card" style="padding:16px;">""", unsafe_allow_html=True)
    st.plotly_chart(fi_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    # ── SHAP Section ──
    st.markdown("""<div style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:700;
        color:#EAEAF0;margin-bottom:12px;">🔬 SHAP Analysis</div>""", unsafe_allow_html=True)

    shap_col1, shap_col2 = st.columns(2)

    # Sample data for SHAP (original logic preserved)
    sample_data = pd.concat([data]*50, ignore_index=True)
    sample_data["tenure"] = np.random.randint(0, 72, size=50)
    sample_data["MonthlyCharges"] = np.random.uniform(20, 120, size=50)
    sample_data["TotalCharges"] = np.random.uniform(100, 5000, size=50)

    X_sample_transformed = preprocessor.transform(sample_data)
    feature_names = preprocessor.get_feature_names_out()

    X_sample_df = pd.DataFrame(
        X_sample_transformed,
        columns=feature_names
    )
    explainer = shap.Explainer(rf_classifier)
    shap_values = explainer(X_sample_df)

    with shap_col1:
        st.markdown("""<div class="hover-card" style="padding:16px;">
            <div style="font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:700;
                color:#6C63FF;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">
                Beeswarm Plot</div>""", unsafe_allow_html=True)
        fig = plt.figure(facecolor="#1A1D27")
        ax = fig.gca()
        ax.set_facecolor("#1A1D27")
        shap.plots.beeswarm(shap_values[:, :, 1], max_display=15, show=False)
        for spine in ax.spines.values():
            spine.set_color((1, 1, 1, 0.1))
        ax.tick_params(colors="#8B8FA8")
        ax.xaxis.label.set_color("#8B8FA8")
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    with shap_col2:
        st.markdown("""<div class="hover-card" style="padding:16px;">
            <div style="font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:700;
                color:#6C63FF;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">
                Feature Importance (SHAP)</div>""", unsafe_allow_html=True)
        fig = plt.figure(facecolor="#1A1D27")
        ax = fig.gca()
        ax.set_facecolor("#1A1D27")
        shap.plots.bar(shap_values[:, :, 1], max_display=15, show=False)
        for spine in ax.spines.values():
            spine.set_color((1, 1, 1, 0.1))
        ax.tick_params(colors="#8B8FA8")
        ax.xaxis.label.set_color("#8B8FA8")
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    # ── Model Performance Table ──
    st.markdown("""<div class="hover-card" style="padding:20px;">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:700;
            color:#6C63FF;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;">
            📈 Model Performance Comparison</div>""", unsafe_allow_html=True)
    st.dataframe(
        performance_df.style.format({
            "ROC AUC": "{:.2f}", "F1 Score": "{:.2f}",
            "Precision": "{:.2f}", "Recall": "{:.2f}"
        }).set_properties(**{
            "background-color": "#1A1D27", "color": "#EAEAF0",
            "border": "1px solid rgba(255,255,255,0.06)",
            "font-family": "JetBrains Mono", "font-size": "13px"
        }).highlight_max(
            subset=["ROC AUC", "F1 Score", "Precision", "Recall"],
            color="rgba(108,99,255,0.25)"
        ),
        use_container_width=True, hide_index=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    # ── Business Insights (original content preserved, restyled) ──
    st.markdown("""<div class="hover-card" style="padding:24px;">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:700;
            color:#6C63FF;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;">
            💡 Business Insights</div>""", unsafe_allow_html=True)

    st.markdown("""
**1️⃣ Customer Tenure**
- Customers with shorter tenure are much more likely to churn.
- New customers have a higher probability of leaving compared to long-term subscribers.

**2️⃣ Contract Type**
- Customers on **month-to-month contracts** show the highest churn risk.
- Long-term contracts such as **one-year or two-year agreements significantly reduce churn**.

**3️⃣ Monthly Charges**
- Higher monthly charges correlate with increased churn probability.
- Customers paying more are more likely to switch providers if they perceive better value elsewhere.

**4️⃣ Internet Service Type**
- Customers using **fiber optic internet services** show relatively higher churn rates compared to DSL users.

**5️⃣ Lack of Value-Added Services**
- Customers without services like **online security, tech support, or device protection** are more likely to churn.
""")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    st.markdown("""<div class="hover-card" style="padding:24px;">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:700;
            color:#00D9C0;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;">
            🚀 Business Recommendations</div>""", unsafe_allow_html=True)
    st.markdown("""
• Encourage **long-term contracts** through discounts or loyalty rewards.
• Offer **bundled services (security, tech support)** to increase customer retention.
• Provide **special retention offers for high-charge customers** to reduce churn risk.
• Focus retention campaigns on **new customers with low tenure**.
""")
    st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ──
st.markdown(FOOTER_HTML, unsafe_allow_html=True)