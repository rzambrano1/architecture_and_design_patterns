"""
----------------------------------------------------------------------
The module docstring (this section) clearly describe the purpose and 
responsibilities of the script/module.
----------------------------------------------------------------------

Project-wide style guide for Python source files.

This project follows the NumPy/SciPy docstring standard. Compared to the
Google style, this format is less compact but provides clearer structure
and improved readability.

Only include sections that contain meaningful content.
Avoid adding empty sections.

Each module docstring should 
"""

# Boilerplate Modules
# -------------------

import pandas as pd

# Typing Modules
# --------------

from typing import List, Dict, Set, Tuple, Optional, Any, Annotated
from numpy.typing import NDArray

# Optional / project-specific imports may include:
# from matplotlib.figure import Figure
# import torch

# Test Libraries
# --------------

import pytest
import doctest

# ---------------------
# Functions and Methods
# ---------------------

def function_documentation_template(
        string_param: str,
        int_param: int,
        list_param: List[str],
        numpy_arr_param: NDArray,
        pandas_df_param: pd.DataFrame,
        #torch_tensor_param: Annotated[torch.Tensor, "(3, 4, 2)"]
        ) -> Tuple[str, int]:
    """
    One-line summary of what the function does.

    More detailed description here. Explain the purpose and any
    important algorithmic details.

    Parameters:
    -----------

    string_param : str
        Description of the string parameter.
    int_param : int
        Description of the integer parameter.
    list_param : list of str
        List of strings representing X.
    numpy_arr_param : ndarray
        NumPy array containing Y data.
    pandas_df_param : pd.DataFrame
        DataFrame with columns ['col1', 'col2'].
    torch_tensor_param : torch.Tensor, shape (3, 4, 2)
        PyTorch tensor. First dimension represents batches,
        second represents features, third represents channels
    
    Returns:
    --------

    status : str
        Status message ('Ok' or 'Error').
        Default value: None
    code : int
        Status code (0 for success, non-zero for error).
        Default value: 5
    
    Raises:
    -------

    ValueError
        If string_param is empty.
    TypeError
        If int_param is not an integer.

    Warns:
    ------

    See Also
    --------
    related_function : Related functionality.

    Notes
    -----
    This function is thread-safe.

    Examples:
    ---------

    When feasible, examples should be compatible with doctest, for example:
    
    >>> function_documentation_template("test", 5, ["a", "b"],
    ...     np.array([1, 2]), pd.DataFrame(), torch.zeros(3,4,2))
    ('Ok', 0)
    """
    return("Ok", 0)

# Classes and Protocols
# ---------------------

class ClassDocumentationTemplate:
    """
    Brief one-line summary of the class purpose.

    Extended description explaining what the class represents, how it fits
    into the system, and the responsibilities it encapsulates.

    This class demonstrates the preferred documentation style for classes
    in this project.

    Class Attributes:
    ----------------

    CLS_ATTR1 : int
        Description of class attribute 1.
    CLS_ATTR2 : str
        Description of class attribute 2.

    Attributes:
    ----------

    attr1 : str
        Description of instance attribute 1.
    attr2 : int
        Description of instance attribute 2.
    _private_attr : list
        Internal state not intended for external use.

    See Also:
    --------

    RelatedClass : Related abstraction.

    Notes:
    -----

    Any implementation notes, invariants, or design constraints.

    Examples:
    --------

    >>> obj = ClassDocumentationTemplate("value", 3)
    >>> obj.method1()
    'result'
    """

    CLS_ATTR1: int = 10
    CLS_ATTR2: str = "default"

    def __init__(self, param1: str, param2: int = 0):
        """
        Initialize the class instance.

        Parameters:
        ----------

        param1 : str
            Description of param1.
        param2 : int, optional
            Description of param2. Defaults to 0.

        Raises:
        ------

        ValueError
            If param1 is empty.
        """
        if not param1:
            raise ValueError("param1 must be non-empty")

        self.attr1: str = param1
        self.attr2: int = param2
        self._private_attr: list = []

    def method1(self) -> str:
        """
        Brief description of what method1 does.

        More detailed explanation of the logic and intent.

        Returns:
        -------

        str
            Result description.

        Examples:
        --------

        >>> obj = ClassDocumentationTemplate("x")
        >>> obj.method1()
        'result'
        """
        return "result"

    @property
    def computed_property(self) -> float:
        """
        Description of the computed property.

        This property computes X based on Y.

        Returns:
        -------
        
        float
            Computed value.
        """
        return float(self.attr2)
