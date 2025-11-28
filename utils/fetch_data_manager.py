# utils/fetch_data_manager.py
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_multiple_data(_tasks, max_workers=None):
    """
    Fetch multiple data sources concurrently.
    `_tasks` won't be hashed by Streamlit cache.

    Args:
        _tasks (dict): {"label": (callable, arg1, ...)}
    """
    results = {}

    with ThreadPoolExecutor(max_workers=max_workers or len(_tasks)) as executor:
        future_to_name = {
            executor.submit(func, *args): name
            for name, (func, *args) in _tasks.items()
        }

        for future in as_completed(future_to_name):
            name = future_to_name[future]
            try:
                results[name] = future.result()
            except Exception as e:
                traceback_str = traceback.format_exc()
                st.warning(f"⚠️ Error fetching {name}: {e}")
                results[name] = {"error": str(e), "traceback": traceback_str}

    return results
