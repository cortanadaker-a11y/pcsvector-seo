"""Minimal fake `streamlit` so the REAL components/bah_calculator.py (main) can render to captured HTML."""
import sys, types
class SS(dict):
    __getattr__ = dict.get
    def __setattr__(self, k, v): self[k] = v
CAP = {'html': [], 'warn': [], 'md': []}
st = types.ModuleType('streamlit')
st.session_state = SS()
class _Ctx:
    def __enter__(self): return self
    def __exit__(self, *a): return False
def columns(spec, **k): return [_Ctx() for _ in range(spec if isinstance(spec, int) else len(spec))]
def selectbox(label, options, index=0, key=None, format_func=None, help=None, disabled=False, **k):
    if key and key in st.session_state: return st.session_state[key]
    return options[index]
def checkbox(label, value=False, key=None, disabled=False, help=None, **k):
    if key and key in st.session_state: return st.session_state[key]
    return value
st.columns = columns; st.selectbox = selectbox; st.checkbox = checkbox
st.markdown = lambda s, **k: CAP['md'].append(s)
st.html = lambda s, **k: CAP['html'].append(s)
st.warning = lambda s, **k: CAP['warn'].append(s)
st.container = lambda **k: _Ctx()
comps = types.ModuleType('streamlit.components'); v1 = types.ModuleType('streamlit.components.v1')
v1.html = lambda *a, **k: None; comps.v1 = v1; st.components = comps
sys.modules['streamlit'] = st; sys.modules['streamlit.components'] = comps; sys.modules['streamlit.components.v1'] = v1
