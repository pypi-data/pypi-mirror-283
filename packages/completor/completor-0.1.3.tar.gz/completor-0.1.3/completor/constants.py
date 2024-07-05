"""Define custom enumerations and methods."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class Headers:
    """Headers for DataFrames."""

    WATER_CUT = "WCT"
    OPEN = "OPEN"
    RHO = "RHO"
    VISCOSITY = "VIS"
    DEVICE = "DEVICE"
    SF = "SF"  # Saturation functions?
    THERM = "THERM"
    PERFDEPTH = "PERFDEPTH"  # Perforation depth?
    ENDGRID = "ENDGRID"
    VSEG = "VSEG"  # Vertical Segments?
    TUBING_INNER_DIAMETER = "TUBINGID"
    MPMODEL = "MPMODEL"
    PDROPCOMP = "PDROPCOMP"  # Pressure drop completion?
    WBVOLUME = "WBVOLUME"  # Well bore volume?
    ITEM_8 = "ITEM8"
    ITEM_9 = "ITEM9"
    ITEM_10 = "ITEM10"
    ITEM_11 = "ITEM11"
    ITEM_12 = "ITEM12"
    ITEM_13 = "ITEM13"
    ITEM_14 = "ITEM14"
    ITEM_15 = "ITEM15"
    ITEM_16 = "ITEM16"
    ITEM_17 = "ITEM17"
    REGION = "REGION"
    DENSCAL = "DENSCAL"  # Calculated density / Density calculated?
    PRESSURE_TABLE = "PRESSURETABLE"
    CROSS = "CROSS"
    SHUT = "SHUT"
    DR = "DR"
    PHASE = "PHASE"
    BHP_DEPTH = "BHP_DEPTH"  # Bottom hole pressure depth?
    GROUP = "GROUP"
    MARKER = "MARKER"
    SCALING_FACTOR = "SCALINGFACTOR"
    LENGTH = "LENGTH"
    ADDITIONAL_SEGMENT = "AdditionalSegment"
    ORIGINAL_SEGMENT = "OriginalSegment"
    TUBING_SEGMENT_2 = "TUBINGSEGMENT2"
    INFO_TYPE = "INFOTYPE"
    TUBING_OUTLET = "TUBINGOUTLET"
    SAT = "SAT"  # Saturation?
    FLAG = "FLAG"  # This is actually a header, but OPEN, SHUT, and AUTO are its possible values, see manual on COMPDAT.
    DEF = "DEF"
    DIRECTION = "DIR"
    SEG = "SEG"  # Duplicate, ish
    SEG2 = "SEG2"
    OUT = "OUT"
    COMPSEGS_DIRECTION = "COMPSEGS_DIRECTION"
    LATERAL = "LATERAL"
    NUMBER_OF_DEVICES = "NDEVICES"
    I = "I"  # noqa: E741
    J = "J"
    K = "K"
    K2 = "K2"
    STATUS = "STATUS"
    SATURATION_FUNCTION_REGION_NUMBERS = "SATNUM"
    CONNECTION_FACTOR = "CF"  # Transmissibility factor for the connection. If defaulted or set to zero,
    # the connection transmissibility factor is calculated using the remaining items of data in this record. See "The
    # connection transmissibility factor" in the ECLIPSE Technical Description for an account of the methods used in
    # Cartesian and radial geometries. The well bore diameter must be set in item 9.

    DIAMETER = "DIAM"
    FORAMTION_PERMEABILITY_THICKNESS = "KH"  # The product of formation permeability, k, and producing formation
    # thickness, h, in a producing well, referred to as kh.
    SKIN = "SKIN"  # A dimensionless factor calculated to determine the production efficiency of a well by comparing
    # actual conditions with theoretical or ideal conditions. A positive skin value indicates some damage or
    # influences that are impairing well productivity. A negative skin value indicates enhanced productivity,
    # typically resulting from stimulation.
    DFACT = "DFACT"
    COMPDAT_DIRECTION = "COMPDAT_DIRECTION"
    RO = "RO"

    TUB_TVD = "TUB_TVD"  # Same as TUBINGTVD
    TVD = "TVD"
    TUBINGMD = "TUBINGMD"
    TUBINGTVD = "TUBINGTVD"
    SEGMENTTVD = "SEGMENTTVD"
    SEGMENTMD = "SEGMENTMD"
    SEGMENT_DESC = "SEGMENT_DESC"
    SEGMENT = "SEGMENT"
    VISCAL_ICD = "VISCAL_ICD"
    RHOCAL_ICD = "RHOCAL_ICD"
    STRENGTH = "STRENGTH"

    WCT_AICV = "WCT_AICV"
    GHF_AICV = "GHF_AICV"
    RHOCAL_AICV = "RHOCAL_AICV"
    VISCAL_AICV = "VISCAL_AICV"
    ALPHA_MAIN = "ALPHA_MAIN"
    X_MAIN = "X_MAIN"
    Y_MAIN = "Y_MAIN"
    A_MAIN = "A_MAIN"
    B_MAIN = "B_MAIN"
    C_MAIN = "C_MAIN"
    D_MAIN = "D_MAIN"
    E_MAIN = "E_MAIN"
    F_MAIN = "F_MAIN"
    ALPHA_PILOT = "ALPHA_PILOT"
    X_PILOT = "X_PILOT"
    Y_PILOT = "Y_PILOT"
    A_PILOT = "A_PILOT"
    B_PILOT = "B_PILOT"
    C_PILOT = "C_PILOT"
    D_PILOT = "D_PILOT"
    E_PILOT = "E_PILOT"
    F_PILOT = "F_PILOT"

    CV_DAR = "CV_DAR"
    AC_OIL = "AC_OIL"
    AC_GAS = "AC_GAS"
    AC_WATER = "AC_WATER"
    WHF_LCF_DAR = "WHF_LCF_DAR"
    WHF_HCF_DAR = "WHF_HCF_DAR"
    GHF_LCF_DAR = "GHF_LCF_DAR"
    GHF_HCF_DAR = "GHF_HCF_DAR"

    ALPHA = "ALPHA"
    X = "X"
    Y = "Y"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    RHOCAL_AICD = "RHOCAL_AICD"
    VISCAL_AICD = "VISCAL_AICD"

    DEFAULTS = "DEFAULTS"
    AC_MAX = "AC_MAX"

    CV = "CV"
    AC = "AC"
    L = "L"

    BRANCH = "BRANCH"

    TUBINGBRANCH = "TUBINGBRANCH"
    MD = "MD"

    # from `test_completion.py`
    TUB_MD = "TUB_MD"

    # Completion
    START_MEASURED_DEPTH = "STARTMD"
    END_MEASURED_DEPTH = "ENDMD"
    ANNULUS = "ANNULUS"
    ANNULUS_ZONE = "ANNULUS_ZONE"
    VALVES_PER_JOINT = "NVALVEPERJOINT"
    INNER_DIAMETER = "INNER_DIAMETER"
    OUTER_DIAMETER = "OUTER_DIAMETER"
    ROUGHNESS = "ROUGHNESS"
    DEVICE_TYPE = "DEVICETYPE"
    DEVICE_NUMBER = "DEVICENUMBER"
    WELL = "WELL"

    # Well segments
    TUBING_MD = "TUBINGMD"
    TUBING_TVD = "TUBINGTVD"
    SEGMENT_MD = "SEGMENTMD"
    SEGMENT_TVD = "SEGMENTTVD"
    TUBING_SEGMENT = "TUBINGSEGMENT"
    TUBING_SEGMENT2 = "TUBINGSEGMENT2"
    TUBING_BRANCH = "TUBINGBRANCH"
    TUBING_ROUGHNESS = "TUBINGROUGHNESS"

    EMPTY = ""


@dataclass(frozen=True)
class _Keywords:
    """Define keywords used in the schedule file.

    Used as constants, and to check if a given word / string is a keyword.

    Attributes:
        _items: Private helper to iterate through all keywords.
        _members: Private helper to check membership.
        main_keywords: collection of the main keywords: welspecs, compdat, welsegs, and compsegs.
        segments: Set of keywords that are used in a segment.
    """

    WELSPECS = "WELSPECS"
    COMPDAT = "COMPDAT"
    WELSEGS = "WELSEGS"
    COMPSEGS = "COMPSEGS"

    COMPLETION = "COMPLETION"

    WELSEGS_H = "WELSEGS_H"
    WSEGLINK = "WSEGLINK"
    WSEGVALV = "WSEGVALV"
    WSEGAICD = "WSEGAICD"
    WSEGAICV = "WSEGAICV"
    WSEGICV = "WSEGICV"
    WSEGSICD = "WSEGSICD"
    WSEGDAR = "WSEGDAR"

    SCHFILE = "SCHFILE"
    OUTFILE = "OUTFILE"

    main_keywords = [WELSPECS, COMPDAT, WELSEGS, COMPSEGS]

    _items = [WELSPECS, COMPDAT, WELSEGS, COMPSEGS]
    _members = set(_items)

    segments = {WELSEGS, COMPSEGS}

    def __iter__(self):
        return self._items.__iter__()

    def __contains__(self, item):
        return item in self._members


Keywords = _Keywords()


class Method(Enum):
    """An enumeration of legal methods to create wells."""

    CELLS = auto()
    FIX = auto()
    USER = auto()
    WELSEGS = auto()

    def __eq__(self, other: object) -> bool:
        """Implement the equality function to compare enums with their string literal.

        Arguments:
            other: Item to compare with.

        Returns:
            Whether enums are equal.

        Example:
            >>>Method.CELLS == "CELLS"
            >>>True
        """
        if isinstance(other, Enum):
            return self.__class__ == other.__class__ and self.value == other.value and self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        return False
