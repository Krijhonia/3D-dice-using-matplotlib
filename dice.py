import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from matplotlib.patches import Circle
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import colorsys

def create_dice_faces():
    """Create the 6 faces of a dice with their respective dot patterns"""
    
    # Define the 8 vertices of a cube
    vertices = np.array([
        [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # bottom face
        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # top face
    ])
    
    # Define the 6 faces of the cube (each face defined by 4 vertices)
    faces = [
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # front face (1)
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # back face (6)
        [vertices[0], vertices[3], vertices[7], vertices[4]],  # left face (2)
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # right face (5)
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # bottom face (3)
        [vertices[4], vertices[5], vertices[6], vertices[7]]   # top face (4)
    ]
    
    return faces

def get_dot_positions(face_number):
    """Get dot positions for each dice face"""
    positions = {
        1: [(0.5, 0.5)],  # center
        2: [(0.25, 0.25), (0.75, 0.75)],  # diagonal
        3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],  # diagonal + center
        4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],  # corners
        5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],  # corners + center
        6: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.5), (0.75, 0.5), (0.25, 0.75), (0.75, 0.75)]  # 2 columns
    }
    return positions.get(face_number, [])

def project_dots_to_3d_face(dots_2d, face_vertices):
    """Project 2D dot positions onto a 3D face"""
    # Get face vectors
    v1 = face_vertices[1] - face_vertices[0]
    v2 = face_vertices[3] - face_vertices[0]
    
    dots_3d = []
    for x, y in dots_2d:
        # Map 2D coordinates to 3D face
        point_3d = face_vertices[0] + x * v1 + y * v2
        dots_3d.append(point_3d)
    
    return dots_3d

def create_3d_dice():
    """Create and render a beautiful 3D dice"""
    
    # Create figure with dark background - square aspect ratio
    fig = plt.figure(figsize=(10, 10))
    fig.patch.set_facecolor('black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Get dice faces
    faces = create_dice_faces()
    
    # Define colors for each face (slightly different shades of white/cream)
    face_colors = ['#f8f8f8', '#f0f0f0', '#f5f5f5', '#efefef', '#f3f3f3', '#ededed']
    face_numbers = [1, 6, 2, 5, 3, 4]  # corresponding dice numbers for each face
    
    # Create the dice faces
    for i, (face, color, number) in enumerate(zip(faces, face_colors, face_numbers)):
        # Create face
        poly = [[face[j] for j in range(4)]]
        ax.add_collection3d(Poly3DCollection(poly, facecolors=color, 
                                           linewidths=2, edgecolors='#333333', alpha=0.9))
        
        # Add dots to the face
        dots_2d = get_dot_positions(number)
        if dots_2d:
            dots_3d = project_dots_to_3d_face(dots_2d, face)
            
            for dot in dots_3d:
                # Create sphere-like dots
                u = np.linspace(0, 2 * np.pi, 10)
                v = np.linspace(0, np.pi, 10)
                radius = 0.08
                
                x_dot = dot[0] + radius * np.outer(np.cos(u), np.sin(v))
                y_dot = dot[1] + radius * np.outer(np.sin(u), np.sin(v))
                z_dot = dot[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
                
                ax.plot_surface(x_dot, y_dot, z_dot, color='#2c2c2c', alpha=0.8)
    
    # Set equal aspect ratio and clean appearance
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1]) 
    ax.set_zlim([0, 1])        
    
    # Force equal aspect ratio for perfect cube appearance
    ax.set_box_aspect([1,1,1])  # This ensures equal scaling on all axes
    
    # Remove axes and grid for cleaner look
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    
    # Set viewing angle for best perspective
    ax.view_init(elev=20, azim=45)
    
    # Add title
    plt.title('3D Dice', color='white', fontsize=20, fontweight='bold', pad=20)
    
    # Adjust layout
    plt.tight_layout()
    
    return fig, ax

def animate_dice_rotation():
    """Create an animated rotating dice"""
    
    fig, ax = create_3d_dice()
    
    def update_view(frame):
        ax.view_init(elev=20, azim=frame)
        return ax,
    
    # For static display, just show one frame
    # In a Jupyter notebook, you could use matplotlib.animation.FuncAnimation
    # to create a rotating animation
    
    plt.show()
    
    return fig

# Enhanced version with better lighting and shadows
def create_metallic_gradient(base_color, steps=10):
    """Create a metallic gradient effect from a base color"""
    rgb = plt.matplotlib.colors.to_rgb(base_color)
    hsv = colorsys.rgb_to_hsv(*rgb)
    
    # Create variations in saturation and value for metallic effect
    colors = []
    for i in range(steps):
        factor = 1.0 - (i / (2 * steps))
        new_hsv = (hsv[0], max(0, hsv[1] - 0.1 * factor), min(1, hsv[2] + 0.1 * factor))
        colors.append(colorsys.hsv_to_rgb(*new_hsv))
    
    return LinearSegmentedColormap.from_list("metallic", colors)

def save_dice_image(fig, filename="dice.png", dpi=300):
    """Save the dice visualization as a high-quality image"""
    fig.savefig(filename, dpi=dpi, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"Image saved as {filename}")

def create_enhanced_3d_dice(color_scheme='classic', elev=22, azim=45, save_path=None):
    """Create an enhanced 3D dice with better visual effects
    
    Parameters:
    -----------
    color_scheme : str
        Color scheme for the dice ('classic', 'modern', 'warm', 'cool')
    elev : float
        Elevation angle for viewing
    azim : float
        Azimuth angle for viewing
    save_path : str, optional
        If provided, save the image to this path
    """
    
    # Color scheme definitions
    color_schemes = {
        'classic': {
            'face_colors': ['#ffffff', '#fafafa', '#f7f7f7', '#f4f4f4', '#f1f1f1', '#eeeeee'],
            'edge_color': '#333333',
            'dot_color': '#1a1a1a',
            'background': '#111111'
        },
        'modern': {
            'face_colors': ['#e8f5e9', '#c8e6c9', '#a5d6a7', '#81c784', '#66bb6a', '#4caf50'],
            'edge_color': '#1b5e20',
            'dot_color': '#1b5e20',
            'background': '#081c08'
        },
        'warm': {
            'face_colors': ['#fff3e0', '#ffe0b2', '#ffcc80', '#ffb74d', '#ffa726', '#ff9800'],
            'edge_color': '#e65100',
            'dot_color': '#e65100',
            'background': '#160c00'
        },
        'cool': {
            'face_colors': ['#e3f2fd', '#bbdefb', '#90caf9', '#64b5f6', '#42a5f5', '#2196f3'],
            'edge_color': '#0d47a1',
            'dot_color': '#0d47a1',
            'background': '#050c14'
        }
    }
    
    scheme = color_schemes.get(color_scheme, color_schemes['classic'])
    
    # Create figure with perfect square dimensions and custom background
    fig = plt.figure(figsize=(14, 14))  # Larger square figure for better detail
    fig.patch.set_facecolor(scheme['background'])
    ax = fig.add_subplot(111, projection='3d', computed_zorder=False)
    ax.set_facecolor(scheme['background'])
    
    # Get dice faces
    faces = create_dice_faces()
    face_colors = scheme['face_colors']
    face_numbers = [1, 6, 2, 5, 3, 4]
    
    # Enhanced lighting effects with more dramatic contrast
    lighting_factors = [1.0, 0.9, 0.95, 0.85, 0.92, 0.88]  # refined lighting
    shadow_alphas = [0.15, 0.2, 0.18, 0.22, 0.17, 0.25]  # shadow intensity for each face
    
    for i, (face, base_color, number, light_factor) in enumerate(zip(faces, face_colors, face_numbers, lighting_factors)):
        # Adjust color based on lighting
        from matplotlib.colors import to_rgb
        rgb = to_rgb(base_color)
        adjusted_color = tuple(c * light_factor for c in rgb)
        
        # Create face with enhanced appearance and shadow effect
        poly = [[face[j] for j in range(4)]]
        # Main face
        ax.add_collection3d(Poly3DCollection(poly, facecolors=[adjusted_color], 
                                           linewidths=2.5, edgecolors='#333333', 
                                           alpha=0.98, linestyles='-'))
        # Shadow layer
        shadow_poly = Poly3DCollection(poly, facecolors='black', alpha=shadow_alphas[i])
        ax.add_collection3d(shadow_poly)
        
        # Add enhanced dots with better depth
        dots_2d = get_dot_positions(number)
        if dots_2d:
            dots_3d = project_dots_to_3d_face(dots_2d, face)
            
            for dot in dots_3d:
                # Create more detailed sphere dots with metallic effect
                u = np.linspace(0, 2 * np.pi, 25)  # Higher resolution
                v = np.linspace(0, np.pi, 25)
                radius = 0.062  # Refined dot size
                
                x_dot = dot[0] + radius * np.outer(np.cos(u), np.sin(v))
                y_dot = dot[1] + radius * np.outer(np.sin(u), np.sin(v))
                z_dot = dot[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
                
                # Create metallic gradient for dots
                metallic_cmap = create_metallic_gradient(scheme['dot_color'])
                
                # Add dot with metallic effect
                dot_surface = ax.plot_surface(x_dot, y_dot, z_dot, 
                                           cmap=metallic_cmap,
                                           linewidth=0, 
                                           antialiased=True)
                dot_surface.set_clim(0, 1)  # Set color scale for metallic effect
    
    # Perfect cube proportions with slightly expanded view
    ax.set_xlim([-0.2, 1.2])
    ax.set_ylim([-0.2, 1.2])
    ax.set_zlim([-0.2, 1.2])
    
    # Force perfect cube appearance with precise aspect ratio
    ax.set_box_aspect([1, 1, 1])
    
    # Remove all axes elements for ultra-clean look
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.grid(False)
    
    # Make panes completely invisible
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.pane.fill = False
        axis.pane.set_edgecolor('none')
        axis.pane.set_alpha(0)
        axis.line.set_color('none')
    ax.xaxis.pane.set_alpha(0)
    ax.yaxis.pane.set_alpha(0)
    ax.zaxis.pane.set_alpha(0)
    
    # Set viewing angle based on parameters
    ax.view_init(elev=elev, azim=azim)
    
    # Enhanced title with color-matched glow effect
    title_color = scheme['face_colors'][0]  # Use the brightest face color for title
    title = plt.title('Enhanced 3D Dice', color=title_color, fontsize=28, 
                     fontweight='bold', pad=40, fontfamily='Arial')
    
    # Add a subtle glow to the title that matches the color scheme
    glow_color = scheme['edge_color']
    title.set_path_effects([plt.matplotlib.patheffects.withSimplePatchShadow(
        offset=(2, -2), shadow_rgbFace=glow_color, alpha=0.3)])
    
    plt.tight_layout(pad=2.0)
    
    # Save the image if a path is provided
    if save_path:
        save_dice_image(fig, save_path)
    
    plt.show()
    return fig, ax

# Run the dice creation with different styles
if __name__ == "__main__":
    print("Creating standard 3D dice...")
    create_3d_dice()
    plt.show()
    
    print("\nCreating enhanced 3D dice with different color schemes...")
    
    # Classic style
    print("\nCreating classic style dice...")
    create_enhanced_3d_dice(color_scheme='classic', elev=22, azim=45)
    
    # Modern style
    print("\nCreating modern style dice...")
    create_enhanced_3d_dice(color_scheme='modern', elev=25, azim=40)
    
    # Warm style
    print("\nCreating warm style dice...")
    create_enhanced_3d_dice(color_scheme='warm', elev=20, azim=50)
    
    # Cool style
    print("\nCreating cool style dice...")
    create_enhanced_3d_dice(color_scheme='cool', elev=22, azim=45, save_path='cool_dice.png')
    