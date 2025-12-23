import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

import streamlit.web.cli as stcli
import sys

sys.argv = ["streamlit", "run", "gui/app.py"]
sys.exit(stcli.main())
