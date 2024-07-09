import pytest
import numpy as np
from myinternshipcalculator2024.calculator import perform_ttest

def test_perform_ttest():
    data1 = np.random.normal(0, 1, 100)
    data2 = np.random.normal(0, 1, 100)
    t_stat, p_value = perform_ttest(data1, data2)
    assert isinstance(t_stat, float)
    assert isinstance(p_value, float)
