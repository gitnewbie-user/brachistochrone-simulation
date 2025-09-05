import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.optimize import fsolve

g = 9.81  


a = float(input("Enter horizontal distance a: "))
b = float(input("Enter vertical drop b: "))

# ---------- Solve for θ1 ----------
def condition(theta):
    return (a/b) - ((theta - np.sin(theta)) / (1 - np.cos(theta)))

theta1 = fsolve(condition, np.pi)[0]  
R = b / (1 - np.cos(theta1))          

print(f"θ1 ≈ {theta1:.4f}, R ≈ {R:.4f}")

def cycloid_x(theta): return R * (theta - np.sin(theta))
def cycloid_y(theta): return -R * (1 - np.cos(theta))

def line_x(s): return a * s
def line_y(s): return -b * s

T_cycloid = np.sqrt(R / g) * theta1

alpha = np.arctan2(b, a)
L = np.sqrt(a**2 + b**2)
acc = g * np.sin(alpha)
T_line = np.sqrt(2 * L / acc)

print(f"Time (Cycloid): {T_cycloid:.4f} s")
print(f"Time (Line): {T_line:.4f} s")


fig = plt.figure(figsize=(12, 8))


ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
ax1.set_aspect('equal')
ax1.set_xlim(-0.2, a + 0.2)
ax1.set_ylim(-b - 0.2, 0.2)
ax1.set_title("Brachistochrone Problem Simulation")


ax2 = plt.subplot2grid((3, 1), (2, 0))
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')  


theta_vals = np.linspace(0, theta1, 500)
ax1.plot(cycloid_x(theta_vals), cycloid_y(theta_vals), 'b-', linewidth=2, label="Brachistochrone (Cycloid)")
ax1.plot([0, a], [0, -b], 'r-', linewidth=2, label="Straight Line")


mid_theta = theta1 / 2
mid_x_cyc = cycloid_x(mid_theta)
mid_y_cyc = cycloid_y(mid_theta)
ax1.text(mid_x_cyc, mid_y_cyc - 0.5, 'Cycloid Path', fontsize=10, color='blue', 
        ha='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

mid_x_line = a / 2
mid_y_line = -b / 2
ax1.text(mid_x_line + 0.5, mid_y_line, 'Straight Line', fontsize=10, color='red',
        ha='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

ax1.legend()

# Balls
ball_cycloid, = ax1.plot([], [], 'bo', markersize=10, label="Cycloid Ball")
ball_line, = ax1.plot([], [], 'ro', markersize=10, label="Line Ball")

# Timers in separate subplot - fix positioning
timer_cycloid = ax2.text(0.05, 0.65, '', fontsize=14, color='blue', 
                        bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
timer_line = ax2.text(0.05, 0.15, '', fontsize=14, color='red',
                     bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcoral", alpha=0.8))

# Add title for timer section
ax2.text(0.05, 0.90, 'Timer:', fontsize=16, weight='bold')

# We synchronize the animation duration with the slower path
T_max = max(T_cycloid, T_line)
fps = 60
frames = int(T_max * fps) + 60  # Add extra frames to see final times

def animate(frame):
    t_real = frame / fps   # real time in seconds

    # --- Straight line position ---
    if t_real <= T_line:
        s = 0.5 * acc * t_real**2     # distance travelled along slope
        frac = min(s / L, 1)          # fraction of slope covered
        xL, yL = line_x(frac), line_y(frac)
        timer_line.set_text(f'Straight Line: {t_real:.2f}s')
    else:
        xL, yL = a, -b
        timer_line.set_text(f'Straight Line: {T_line:.2f}s (FINISHED)')

    # --- Cycloid position ---
    if t_real <= T_cycloid:
        theta_now = t_real * np.sqrt(g / R)
        xC, yC = cycloid_x(theta_now), cycloid_y(theta_now)
        timer_cycloid.set_text(f'Cycloid: {t_real:.2f}s')
    else:
        xC, yC = a, -b
        timer_cycloid.set_text(f'Cycloid: {T_cycloid:.2f}s (FINISHED)')

    # Update ball positions
    ball_line.set_data([xL], [yL])
    ball_cycloid.set_data([xC], [yC])
    
    return ball_line, ball_cycloid, timer_line, timer_cycloid

ani = animation.FuncAnimation(fig, animate, frames=frames, interval=1000/fps, blit=True)
plt.tight_layout()
plt.show()
