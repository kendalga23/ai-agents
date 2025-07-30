#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from coder.crew import Coder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

assignment = ""


def run():
    """
    Run Coder crew.
    """
    inputs = {"assignment": assignment}

    result = Coder().crew().kickoff(inputs=inputs)
    print(result.new)