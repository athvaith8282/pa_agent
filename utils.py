import time
import json
from functools import wraps
import streamlit as st
import config as cfg

event_runner = st.session_state.loop.run_until_complete    

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """
    Retry decorator to re-execute a function on failure.

    Args:
        max_attempts (int): Number of retry attempts before raising the error.
        delay (float): Delay in seconds between retries.
        exceptions (tuple): Exception types to catch and retry on.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt >= max_attempts:
                        print(f"❌ Failed after {attempt} attempts: {e}")
                        raise
                    print(f"⚠️ Attempt {attempt} failed with error: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                    attempt += 1
        return wrapper
    return decorator

async def get_gmail_token():
    st.warning("⚠️ Please authorize Gmail access")
    # Show authorize button
    # result = st.session_state.oauth2.authorize_button(
    #     name="🔐 Authorize Gmail",
    #     redirect_uri=cfg.REDIRECT_URI,
    #     scope=cfg.SCOPES,
    #     key="gmail_auth",
    #     use_container_width=True,
    #     extras_params={"prompt": "consent", "access_type": "offline"}
    # )
    
    # if result and 'token' in result:
    #     with open(cfg.TOKEN_PATH, 'w') as file:
    #         json.dump(result["token"], file)
    #     st.session_state.gmail_token = result['token']
    #     await st.session_state.graph.rebuild_graph(st.session_state.gmail_token)
    #     st.rerun()