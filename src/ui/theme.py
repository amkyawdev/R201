"""Design tokens for Movie Recap Myanmar.

Single source of truth for colour, spacing, radius, type and motion.
The HTML prototype in /design mirrors these exact values.
"""

# ---------------------------------------------------------------- colour
BG = "#0B0F14"           # deep charcoal base
SURFACE = "#111823"      # raised surface
SURFACE_2 = "#161F2C"    # second elevation
GLASS = "#FFFFFF14"      # frosted glass fill (8% white)
BORDER = "#FFFFFF14"     # 1px luminous hairline
BORDER_STRONG = "#FFFFFF29"

VIOLET = "#7C5CFF"       # electric violet, gradient start
CYAN = "#22D3EE"         # cyan, gradient end
GOLD = "#F5C451"         # warm gold highlight
MAGENTA = "#C084FC"      # bloom mid-stop

TEXT = "#F5F7FA"
TEXT_MUTED = "#9AA4B2"
TEXT_FAINT = "#5C6675"

DANGER = "#FF6B6B"
SUCCESS = "#34D399"

# Gradients (Flet takes a list of colours + stops)
GRAD_PRIMARY = [VIOLET, CYAN]
GRAD_BLOOM = [VIOLET, MAGENTA, CYAN]
GRAD_GOLD = ["#F5C451", "#E8A93B"]

# ---------------------------------------------------------------- spacing (4px grid)
S1, S2, S3, S4, S5, S6, S7, S8 = 4, 8, 12, 16, 20, 24, 32, 40
PAGE_X = 24          # 24px side margins

# ---------------------------------------------------------------- radius
R8, R12, R16, R20, R24, R28 = 8, 12, 16, 20, 24, 28
R_PILL = 999

# ---------------------------------------------------------------- typography
# 28 / 20 / 15 / 12 scale, line-height 1.5
FONT_MM = "Padauk"       # Burmese
FONT_LATIN = "Inter"     # Latin

TYPE_DISPLAY = 28
TYPE_TITLE = 20
TYPE_BODY = 15
TYPE_CAPTION = 12

LH = 1.5

# ---------------------------------------------------------------- motion
# Durations in milliseconds, easings as cubic-bezier control points.
EASE_OUT_QUINT = (0.22, 1.0, 0.36, 1.0)   # signature curve
EASE_IN_OUT = (0.4, 0.0, 0.2, 1.0)

D_FAST = 120
D_TAB = 300
D_SKELETON = 400
D_DIALOG = 240
D_BLOOM = 600
D_BREATHE = 3000

STAGGER_LINE = 60
STAGGER_RIPPLE = 400

# ---------------------------------------------------------------- shadow
SHADOW_SOFT = "0 8px 32px rgba(0,0,0,0.40)"
GLOW_VIOLET = "0 0 24px rgba(124,92,255,0.45)"
GLOW_CYAN = "0 0 24px rgba(34,211,238,0.35)"
GLOW_GOLD = "0 0 20px rgba(245,196,81,0.35)"
