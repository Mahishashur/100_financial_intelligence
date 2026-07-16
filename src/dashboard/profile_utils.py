import streamlit as st


def company_selector(company_df):

    company = st.selectbox(

        "🔍 Select Company",

        sorted(company_df["id"].tolist())

    )

    return company

def company_selector(company_df):

    return st.selectbox(

        "🔍 Select Company",

        sorted(company_df["id"])

    )


def company_card(company, sector):

    st.title(company["company_name"])

    st.markdown(
        f"🌐 **Website:** {company['website']}"
    )

    col1, col2 = st.columns(2)

    col1.info(
        f"**Sector**\n\n{sector['broad_sector']}"
    )

    col2.info(
        f"**Sub Sector**\n\n{sector['sub_sector']}"
    )

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "ROE %",
        company["roe_percentage"]
    )

    c2.metric(
        "ROCE %",
        company["roce_percentage"]
    )

    c3.metric(
        "Book Value",
        company["book_value"]
    )

    c4, c5 = st.columns(2)

    c4.metric(
        "Face Value",
        company["face_value"]
    )

    c5.metric(
        "Index Weight %",
        sector["index_weight_pct"]
    )

    st.markdown("---")

    st.subheader("About Company")

    st.write(company["about_company"])