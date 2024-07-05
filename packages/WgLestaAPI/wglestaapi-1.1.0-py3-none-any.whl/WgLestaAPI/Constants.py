"""
Constants for running the WgLestaAPI library
"""

CIS_PREFIX = "cis-"
"""The prefix is necessary to unify short game names for Lesta Games
"""

class APIHOLDERS(object):
    """API Owners"""
    WG      = "wargaming.net"
    LESTA   = "lesta.ru"


class TYPEREQUESTS(object):
    """Request types available for API"""
    GET     = "GET"
    POST    = "POST"

    ALL     = (GET, POST)


class REGION(object):
    """List of regions available for API"""
    RU      = "ru"
    SU      = "su"
    EU      = "eu"
    NA      = "com"
    ASIA    = "asia"
    WGCB    = "com"
    
    CIS     = (RU, SU)                      # Только СНГ
    ALL_CIS = (RU, SU, EU, NA, ASIA, WGCB)  # Включая СНГ
    ALL     = (EU, NA, ASIA, WGCB)          # Не включая СНГ


class GAMENAMES(object):
    """Names of Wargaming.net and Lesta Games games to perform API methods"""
    class SHORTNAMES(object):
        """Short names"""
        WOT         = "wot"     # World of Tanks
        """World of Tanks
        """
        WOTB        = "wotb"    # World of Tanks Blitz
        """World of Tanks Blitz
        """
        WOTC        = "wotx"    # World of Tanks Console
        """World of Tanks Console
        """
        WOWS        = "wows"    # World of Warships
        """World of Warships
        """
        WOWP        = "wowp"    # World of Warplanes
        """World of Warplanes
        """
        WG          = "wgn"     # Wargaming.net
        """Wargaming.net
        """
        # CIS
        TANKI       = CIS_PREFIX + "wot"    # Мир танков
        """Мир танков
        
        (only `SU` region)
        """
        KORABLI     = CIS_PREFIX + "wows"   # Мир кораблей
        """Мир кораблей
        
        (only `SU` region)
        """
        TANKSBLITZ  = CIS_PREFIX + "wotb"   # Tanks Blitz
        """Tanks Blitz
        
        (only `RU` region)
        """

        # All short names
        ALL = (WOT, WOTB, WOTC, WOWS, WOWP, WG, TANKI, KORABLI, TANKSBLITZ)

    class LONGNAMES(object):
        """Long names"""
        WOT         = "worldoftanks"        # World of Tanks
        """World of Tanks
        """
        WOTB        = "wotblitz"            # World of Tanks Blitz
        """World of Tanks Blitz
        """
        WOTC        = "worldoftanks"        # World of Tanks Console
        """World of Tanks Console
        """
        WOWS        = "worldofwarships"     # World of Warships
        """World of Warships
        """
        WOWP        = "worldofwarplanes"    # World of Warplanes
        """World of Warplanes
        """
        WG          = "worldoftanks"        # Wargaming.net
        """Wargaming.net
        """
        # CIS
        TANKI       = "tanki"               # Мир танков
        """Мир танков
        
        (only `SU` region)
        """
        KORABLI     = "korabli"             # Мир кораблей
        """Мир кораблей
        
        (only `SU` region)
        """
        TANKSBLITZ  = "tanksblitz"          # Tanks Blitz
        """Tanks Blitz
        
        (only `RU` region)
        """

        # All long names
        ALL = (WOT, WOTB, WOTC, WOWS, WOWP, WG, TANKI, KORABLI, TANKSBLITZ)

class METHODEXECUTION(object):
    ASYNC = "async"
    """Asynchronous API request
    """
    SYNC = "sync"
    """Synchronous API request
    """
    

SELECTOR = {
    # CIS
    GAMENAMES.SHORTNAMES.TANKI: {
        "api_prefix": "api",
        "game_longname": GAMENAMES.LONGNAMES.TANKI,
        "region": [REGION.SU]
    },
    GAMENAMES.SHORTNAMES.TANKSBLITZ: {
        "api_prefix": "papi",
        "game_longname": GAMENAMES.LONGNAMES.TANKSBLITZ,
        "region": [REGION.RU]
    },
    GAMENAMES.SHORTNAMES.KORABLI: {
        "api_prefix": "api",
        "game_longname": GAMENAMES.LONGNAMES.KORABLI,
        "region": [REGION.SU]
    },
    
    # ALL
    GAMENAMES.SHORTNAMES.WOT: {
        "api_prefix": "api",
        "game_longname": GAMENAMES.LONGNAMES.WOT,
        "region": [REGION.EU, REGION.NA, REGION.ASIA]
    },
    GAMENAMES.SHORTNAMES.WOTB: {
        "api_prefix": "api",
        "game_longname": GAMENAMES.LONGNAMES.WOTB,
        "region": [REGION.EU, REGION.NA, REGION.ASIA]
    },
    GAMENAMES.SHORTNAMES.WOTC: {
        "api_prefix": "api-modernarmor",
        "game_longname": GAMENAMES.LONGNAMES.WOTC,
        "region": [REGION.WGCB]
    },
    GAMENAMES.SHORTNAMES.WOWS: {
        "api_prefix": "api",
        "game_longname": GAMENAMES.LONGNAMES.WOWS,
        "region": [REGION.EU, REGION.NA, REGION.ASIA]
    },
    GAMENAMES.SHORTNAMES.WOWP: {
        "api_prefix": "api",
        "game_longname": GAMENAMES.LONGNAMES.WOWP,
        "region": [REGION.EU, REGION.NA]
    },
    GAMENAMES.SHORTNAMES.WG: {
        "api_prefix": "api",
        "game_longname": GAMENAMES.LONGNAMES.WG,
        "region": [REGION.EU, REGION.NA, REGION.ASIA]
    },
    
}