import os
from typing import Optional, Dict

import streamlit as st
from openai import OpenAI
from weather import get_weather
from season import find_season


TITRE = "RECETTE IMAGINE LOCAL ET DE SAISON"


def meteo_msg(city: Optional[str] = None) -> Dict[str, str]:
    weather = get_weather(city=city)
    return {'role': 'user', 'content': f'recette avec une météo {weather}'}


def season_msg(city: Optional[str] = None) -> Dict[str, str]:
    season = find_season(city)
    return {'role': 'user', 'content': f'recette de  {season}'}


def region_msg(city: Optional[str] = None) -> Dict[str, str]:
    return {'role': 'user', 'content': f'authentique et  originale de la region {city}'}


def main():
    st.title(TITRE)

    # Set OpenAI API key from Streamlit secrets
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Donnez-moi un nom de ville pour votre recette"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Supposez que vous avez déjà les messages dans une liste appelée 'messages'
        messages = st.session_state.messages

        # Création d'une liste de dictionnaires de messages au format requis pour OpenAI
        messages_list = [{"role": m["role"], "content": m["content"]} for m in messages]
        messages_list.append(meteo_msg(city=prompt))
        messages_list.append(season_msg(city=prompt))
        messages_list.append(region_msg(city=prompt))

        # Appel à OpenAI pour générer une réponse
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages_list,
            stream=True,
        )

        # Affichage de la réponse
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == '__main__':
    main()
