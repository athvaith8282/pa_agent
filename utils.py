import streamlit as st

async def run_async(coro):
    return st.session_state.loop.run_until_complete(coro)