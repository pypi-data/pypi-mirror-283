import numpy as np
import matplotlib.pyplot as plt

def plot_bloch_circles(q, alpha=0.6, color='r'):
    """
    Create three separate 2D circles representing the X, Y, and Z axes of the Bloch sphere,
    with markers for the computational basis states |0> and |1>.
    
    Args:
        alpha (float): The transparency value for the circles (default=0.5).
        color (str): The color of the circles (default='r').
        
    Returns:
        fig, axs: The figure and axes objects containing the three circles.
    """
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))

    x,y,z = q
    
    # X axis circle
    theta = np.linspace(0, 2 * np.pi, 100)
    x_x = np.cos(theta)
    y_x = np.sin(theta)
    axs[0].plot(x_x, y_x, color=color, alpha=alpha)
    axs[0].scatter(y, z, color='k', marker='o')  # |0> marker
    axs[0].set_aspect('equal')
    axs[0].set_title('X Axis')
    axs[0].legend()
    
    # Y axis circle
    x_y = np.cos(theta)
    y_y = np.sin(theta)
    axs[1].plot(x_y, y_y, color=color, alpha=alpha)
    axs[1].scatter(x, z, color='k', marker='o')  # |0> marker
    axs[1].set_aspect('equal')
    axs[1].set_title('Y Axis')
    axs[1].legend()
    
    # Z axis circle
    x_z = np.cos(theta)
    y_z = np.sin(theta)
    axs[2].plot(x_z, y_z, color=color, alpha=alpha)
    axs[2].scatter(x, y, color='k', marker='o')  # |0> marker
    axs[2].set_aspect('equal')
    axs[2].set_title('Z Axis')
    axs[2].legend()
    
    fig.suptitle('Bloch Circles', fontsize=16)
    
    return fig, axs