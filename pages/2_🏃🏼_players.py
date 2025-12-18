import streamlit as st
import requests

st.set_page_config(
    page_title="Players",
    page_icon="🏃🏼",
    layout="wide"
)
df_data = st.session_state["data"]


clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_players = df_data[(df_data["Club"] == club)]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

player_stats = df_data[df_data["Name"] == player].iloc[0]

cols_header = st.columns([1, 1, 6])
# mostrar foto do jogador, logo do clube (se existirem) e nome do jogador
player_photo = player_stats.get("Photo") if hasattr(player_stats, 'get') else player_stats["Photo"]
club_logo = player_stats.get("Club Logo") if hasattr(player_stats, 'get') else player_stats["Club Logo"]

def _show_image_from_url(col, url, width=None):
    if not url or str(url) == 'nan':
        col.empty()
        return
    try:
        r = requests.get(url, timeout=6)
        if r.status_code == 200 and r.content:
            col.image(r.content, width=width)
            return
    except Exception:
        pass
    # fallback: let Streamlit try to load the URL in the frontend
    try:
        col.image(url, width=width)
    except Exception:
        col.empty()

_show_image_from_url(cols_header[0], player_photo, width=180)
_show_image_from_url(cols_header[1], club_logo, width=100)

cols_header[2].title(player_stats["Name"])
cols_header[2].markdown(f"**Clube:** {player_stats['Club']}")
cols_header[2].markdown(f"**Posição:** {player_stats['Position']}")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height(cm.)'] / 100}")
col3.markdown(f"**Peso:** {player_stats['Weight(lbs.)']*0.453:.2f}")
st.divider()

st.subheader(f"Overall {player_stats['Overall']}")
st.progress(int(player_stats["Overall"]))

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Valor de mercado", value=f"£ {player_stats['Value(£)']:,}")
col2.metric(label="Remuneração semanal", value=f"£ {player_stats['Wage(£)']:,}")
col3.metric(label="Cláusula de rescisão", value=f"£ {player_stats['Release Clause(£)']:,}")