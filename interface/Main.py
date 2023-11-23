import pandas as pd
import streamlit as st
import joblib
from supplyModule.CepTreatment import LatLonByCEP



x_numericos = {
    "latitude": 0,
    "longitude": 0,
    "accommodates": 0,
    "bathrooms": 0,
    "bedrooms": 0,
    "beds": 0,
    "extra_people": 0,
    "minimum_nights": 0,
    "ano": 0,
    "mes": 0,
    "len_amenities": 0,
    "host_listings_count": 0,
}

x_tf = {"host_is_superhost": False, "instant_bookable": False}

x_listas = {
    "property_type": [
        "Apartment",
        "Condominium",
        "House",
        "Loft",
        "Others",
        "Serviced apartment",
    ],
    "room_type": ["Entire home/apt", "Private room"],
    "cancellation_policy": ["flexible", "moderate", "strict_14_with_grace_period"],
    "bed_type":["Bed", "Others"]
}
x_listas_aux = {} #Dummies to unique informations

for item in x_listas:
        for option in x_listas[item]:
            x_listas_aux[f"{item}_{option}"] = 0

#Cep input
cep_valor = st.text_input("CEP", placeholder="XXXXX-XXX")
if len(cep_valor) >8:
    try:
        x_numericos["latitude"], x_numericos["longitude"]  = LatLonByCEP(cep_valor)
    except:
        pass

#Numerics inputs
for item in x_numericos:
    if item == "extra_people":
        valor = st.number_input(f"{item}", step=0.01, value=0.0)
        x_numericos[item] = valor
    elif item == "latitude" or item == "longitude":
        pass
    else:
        valor = st.number_input(f"{item}", step=1, value=0)
        x_numericos[item] = valor

#Boolean inputs
for item in x_tf:
    valor = st.selectbox(f"{item}", ("Sim", "Não"))
    if valor == "Sim":
        x_tf[item] = 1
    else:
        x_tf[item] = 0

#Selection inputs
for item in x_listas:
    option = st.selectbox(f"{item}", x_listas[item])
    x_listas_aux[f"{item}_{option}"] = 1

final_dict = {}

bt = st.button("Prever valor do Imóvel")

if bt:

    final_dict.update(x_listas_aux)
    final_dict.update(x_numericos)
    final_dict.update(x_tf)
    answer_df = pd.DataFrame(final_dict, index=[0])
    
    df = pd.read_csv(r'C:\Users\bejr2\OneDrive\Área de Trabalho\Códigos\Phyton\Projeto DataScience\FinalDF_2.csv')
    df = df.drop("Unnamed: 0", axis=1)
    df = df.drop("price", axis=1)
    model_columns = list(df.columns)

    answer_df = answer_df[model_columns]
    print(model_columns)
    print(list(answer_df.columns))

    model = joblib.load(r'C:\Users\bejr2\OneDrive\Área de Trabalho\Códigos\Phyton\Projeto DataScience\FinalModel.joblib')
    preco = model.predict(answer_df)
    st.write(preco[0])