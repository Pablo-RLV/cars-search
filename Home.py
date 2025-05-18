import streamlit as st
import pandas as pd
import json

with open('data/cars.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
df = pd.DataFrame(data)

st.title("Filtro de Carros")
minimum = df['Price'].min()
maximum = df['Price'].max()
values = st.slider("Selecione a faixa de preço (R$)", minimum, maximum, (minimum, maximum))
brands = df['Name'].unique()
selected_brands = st.multiselect("Selecione as marcas", brands, default=brands)

locations = df['Location'].unique()
selected_locations = st.multiselect("Selecione as localizações", locations, default=locations)

filtered_df = df[
    (df['Price'] >= values[0]) &
    (df['Price'] <= values[1]) &
    (df['Name'].isin(selected_brands)) &
    (df['Location'].isin(selected_locations))
]

cols = st.columns(3)
for idx, row in enumerate(filtered_df.itertuples()):
    col = cols[idx % 3]
    with col:
        with st.container(border=True, height=300):
            st.image(row.Image, use_container_width=True)
            st.markdown(f"**{row.Name} {row.Model}**")
            st.write(f"R${row.Price:,.2f}")
            st.write(f"📍 {row.Location}")
