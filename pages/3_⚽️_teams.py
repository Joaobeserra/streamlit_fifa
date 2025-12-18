import streamlit as st
import requests

st.set_page_config(
    page_title="Teams",
    page_icon="⚽️",
    layout="wide"
)

df_data = st.session_state["data"]

clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_filtered = df_data[(df_data["Club"] == club)].set_index("Name")

# mostrar logo do clube (baixando via requests para evitar bloqueio de URL externo)
club_logo_url = df_filtered.iloc[0]["Club Logo"]
def _show_image_from_url(url, width=None):
    if not url or str(url) == 'nan':
        return
    try:
        r = requests.get(url, timeout=6)
        if r.status_code == 200 and r.content:
            st.image(r.content, width=width)
            return
    except Exception:
        pass
    try:
        st.image(url, width=width)
    except Exception:
        st.write("(imagem indisponível)")

_show_image_from_url(club_logo_url, width=140)
st.markdown(f"## {club}")

columns = ["Age", "Photo", "Flag", "Overall", 'Value(£)', 'Wage(£)', 'Joined', 
           'Height(cm.)', 'Weight(lbs.)',
           'Contract Valid Until', 'Release Clause(£)']

st.dataframe(df_filtered[columns],
             column_config={
                 "Overall": st.column_config.ProgressColumn(
                     "Overall", format="%d", min_value=0, max_value=100
                 ),
                 "Wage(£)": st.column_config.ProgressColumn("Weekly Wage", format="£%f", 
                                                    min_value=0, max_value=df_filtered["Wage(£)"].max()),
                "Photo": st.column_config.ImageColumn(),
                "Flag": st.column_config.ImageColumn("Country"),
             })