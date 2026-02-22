import numpy as np
import matplotlib.pyplot as plt

# --- helpers ---
def bezier(P0, P1, P2, P3, n=120):
    """Cubic Bezier curve points."""
    t = np.linspace(0, 1, n)
    return ((1-t)**3)[:,None]*P0 + (3*(1-t)**2*t)[:,None]*P1 + (3*(1-t)*t**2)[:,None]*P2 + (t**3)[:,None]*P3

def arc(center, r, a0, a1, n=120):
    """Arc points."""
    a = np.linspace(a0, a1, n)
    x = center[0] + r*np.cos(a)
    y = center[1] + r*np.sin(a)
    return np.c_[x, y]

def line(p0, p1, n=60):
    t = np.linspace(0, 1, n)
    return (1-t)[:,None]*p0 + t[:,None]*p1

def resample_polyline(XY, n=1200):
    """Resample polyline to ~uniform spacing."""
    d = np.sqrt(np.sum(np.diff(XY, axis=0)**2, axis=1))
    s = np.r_[0, np.cumsum(d)]
    s_new = np.linspace(0, s[-1], n)
    x = np.interp(s_new, s, XY[:,0])
    y = np.interp(s_new, s, XY[:,1])
    return np.c_[x, y]

def smooth_closed(XY, window=31):
    """Simple moving-average smoothing for a closed curve."""
    assert window % 2 == 1
    k = window // 2
    pad = np.vstack([XY[-k:], XY, XY[:k]])
    kernel = np.ones(window)/window
    x = np.convolve(pad[:,0], kernel, mode="valid")
    y = np.convolve(pad[:,1], kernel, mode="valid")
    return np.c_[x, y]

# --- build a Monaco-inspired centerline as segments ---
# Start/Finish near "harbor straight"
A = np.array([0.0, 0.0])
B = np.array([6.5, 0.2])  # harbor straight end

# 1) Harbor straight
seg1 = line(A, B, n=90)

# 2) Fast right into tunnel entry (Bezier)
P0 = B
P1 = np.array([7.3, 0.3])
P2 = np.array([8.2, 1.0])
P3 = np.array([8.0, 2.1])
seg2 = bezier(P0, P1, P2, P3, n=120)

# 3) Tunnel (long gentle left arc)
seg3 = arc(center=np.array([6.0, 2.5]), r=2.2, a0=-0.15, a1=2.35, n=180)

# 4) Chicane after tunnel (S-shape using 2 Beziers)
C = seg3[-1]
seg4a = bezier(C, C+np.array([-1.0, 0.2]), C+np.array([-1.3, -0.8]), C+np.array([-2.2, -0.6]), n=80)
D = seg4a[-1]
seg4b = bezier(D, D+np.array([-0.8, 0.5]), D+np.array([-0.2, 1.0]), D+np.array([-1.0, 1.4]), n=80)

# 5) Waterfront sweep (Bezier)
E = seg4b[-1]
seg5 = bezier(E, E+np.array([-1.5, 0.6]), E+np.array([-3.2, 0.2]), np.array([0.9, 2.7]), n=160)

# 6) Tight hairpin (very small radius arc)
F = seg5[-1]
# place hairpin center near F; very tight turn
seg6 = arc(center=F + np.array([0.6, 0.2]), r=0.55, a0=np.deg2rad(205), a1=np.deg2rad(30), n=160)

# 7) Casino rise / uphill kink (Bezier)
G = seg6[-1]
seg7 = bezier(G, G+np.array([0.3, 1.0]), G+np.array([1.8, 1.7]), np.array([2.8, 3.7]), n=140)

# 8) Narrow complex back down (Bezier + line)
H = seg7[-1]
seg8 = bezier(H, H+np.array([1.0, -0.2]), H+np.array([1.3, -1.5]), np.array([2.1, 1.4]), n=160)
I = seg8[-1]
seg9 = bezier(I, I+np.array([-0.1, -1.2]), I+np.array([-2.2, -1.7]), np.array([0.0, 0.0]), n=180)

# Combine, resample, smooth
centerline = np.vstack([seg1, seg2, seg3, seg4a, seg4b, seg5, seg6, seg7, seg8, seg9])
centerline = resample_polyline(centerline, n=1800)
centerline = smooth_closed(centerline, window=41)

# --- compute left/right track edges for a fixed width ---
track_width = 0.55  # adjust for narrower/wider street
dXY = np.gradient(centerline, axis=0)
tangent = dXY / np.linalg.norm(dXY, axis=1, keepdims=True)
normal = np.c_[-tangent[:,1], tangent[:,0]]

left_edge  = centerline + normal*(track_width/2)
right_edge = centerline - normal*(track_width/2)

# --- plot ---
plt.figure(figsize=(9, 7))
plt.plot(left_edge[:,0],  left_edge[:,1],  linewidth=2)
plt.plot(right_edge[:,0], right_edge[:,1], linewidth=2)
plt.plot(centerline[:,0], centerline[:,1], linestyle="--", linewidth=1)

# Start/finish marker
plt.scatter(centerline[0,0], centerline[0,1], s=80)
plt.text(centerline[0,0]+0.1, centerline[0,1]-0.2, "START/FINISH")

plt.gca().set_aspect("equal", adjustable="box")
plt.title("Monaco-inspired Street Circuit (generated)")
plt.axis("off")
plt.show()