import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import streamlit as st

from sidebar import sidebar_

sidebar_()