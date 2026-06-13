import streamlit as st


def load_css():

    st.markdown(
        """
<style>

/* ==========================
   APP BACKGROUND
========================== */

.stApp{
    background:
    linear-gradient(
        180deg,
        #F4F7FB 0%,
        #EEF4FF 100%
    );
}

/* ==========================
   MAIN CONTAINER
========================== */

.main .block-container{
    max-width:1400px;
    padding-top:2rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* ==========================
   BANNER
========================== */
.banner-img img{
    max-height:260px;
    object-fit:contain;
    width:100%;
}

/* ==========================
   SIDEBAR
========================== */

[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E5E7EB;
}

/* ==========================
   HEADERS
========================== */

h1,h2,h3{
    color:#0F172A;
    font-weight:700;
}

/* ==========================
   METRIC CARDS
========================== */

div[data-testid="metric-container"]{

    background:white;

    padding:18px;

    border-radius:16px;

    border-left:5px solid #2563EB;

    box-shadow:
    0px 4px 20px rgba(
        0,
        0,
        0,
        0.08
    );
}

/* ==========================
   METRIC VALUE
========================== */

[data-testid="stMetricValue"]{

    font-size:28px;

    font-weight:700;
}

/* ==========================
   BUTTONS
========================== */

.stButton button{

    background:#2563EB;

    color:white;

    border:none;

    border-radius:10px;

    font-weight:600;
}

.stButton button:hover{

    background:#1D4ED8;
}

/* ==========================
   CONTAINERS
========================== */

[data-testid="stVerticalBlockBorderWrapper"]{

    background:white;

    border-radius:18px;

    padding:10px;

    box-shadow:
    0px 2px 12px rgba(
        0,
        0,
        0,
        0.05
    );
}

/* ==========================
   DATAFRAMES
========================== */

[data-testid="stDataFrame"]{

    border-radius:18px;
}

/* ==========================
   ALERTS
========================== */

.stSuccess,
.stInfo,
.stWarning,
.stError{

    border-radius:12px;
}

</style>
        """,
        unsafe_allow_html=True
    )