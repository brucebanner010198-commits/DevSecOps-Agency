"""Put both the desktop package and the trust-spine package on sys.path."""

import os
import sys

_HERE = os.path.dirname(__file__)
sys.path.insert(0, _HERE)  # `desktop`
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "trust-spine"))  # `trust_spine`
