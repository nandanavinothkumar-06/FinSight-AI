import streamlit as st


def metric_card(
    title,
    value,
    delta=None,
    help_text=None
):
    """
    Reusable KPI card
    """

    with st.container(border=True):

        st.metric(
            label=title,
            value=value,
            delta=delta,
            help=help_text
        )


def section_header(
    title,
    icon=None
):
    """
    Standardized section header
    """

    if icon:

        st.markdown(
            f"## {icon} {title}"
        )

    else:

        st.markdown(
            f"## {title}"
        )


def insight_card(
    text,
    level="info"
):
    """
    Reusable insight card
    """

    if level == "success":

        st.success(text)

    elif level == "warning":

        st.warning(text)

    elif level == "error":

        st.error(text)

    else:

        st.info(text)


def empty_state(
    message
):
    """
    Standard no-data component
    """

    st.info(
        f"ℹ️ {message}"
    )


def divider():
    """
    Consistent divider
    """

    st.divider()


def status_badge(
    text,
    status="info"
):
    """
    Small status display
    """

    if status == "success":

        st.success(text)

    elif status == "warning":

        st.warning(text)

    elif status == "error":

        st.error(text)

    else:

        st.info(text)