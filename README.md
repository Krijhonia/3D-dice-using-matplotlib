# 3D Dice Visualization using Matplotlib

A Python project that creates beautiful, customizable 3D dice visualizations using Matplotlib. This project offers multiple visualization styles, metallic effects, and high-quality rendering options.

![3D Dice Example](cool_dice.png)

## Features

- **Multiple Color Schemes:**
  - Classic: Elegant white/gray theme
  - Modern: Fresh green tones
  - Warm: Orange/amber gradients
  - Cool: Sophisticated blue tones

- **Advanced Visual Effects:**
  - Metallic dot rendering
  - Dynamic shadow effects
  - Color-matched glowing titles
  - High-resolution sphere dots
  - Custom gradient shading

- **Customization Options:**
  - Adjustable viewing angles
  - Configurable color schemes
  - High-quality image export
  - Customizable dice dimensions

## Requirements

```bash
matplotlib
numpy
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/3d-dice-matplotlib.git
cd 3d-dice-matplotlib
```

2. Install required packages:
```bash
pip install matplotlib numpy
```

## Usage

### Basic Usage

```python
from dice import create_enhanced_3d_dice

# Create basic dice with default settings
create_enhanced_3d_dice()
```

### Color Schemes

```python
# Classic white theme
create_enhanced_3d_dice(color_scheme='classic')

# Modern green theme
create_enhanced_3d_dice(color_scheme='modern')

# Warm orange theme
create_enhanced_3d_dice(color_scheme='warm')

# Cool blue theme
create_enhanced_3d_dice(color_scheme='cool')
```

### Custom Viewing Angles

```python
# Adjust elevation and azimuth angles
create_enhanced_3d_dice(elev=30, azim=60)
```

### Save to File

```python
# Save as high-quality PNG
create_enhanced_3d_dice(save_path='my_dice.png')
```

## Functions

### `create_enhanced_3d_dice()`

Main function to create the 3D dice visualization.

Parameters:
- `color_scheme` (str): Color scheme ('classic', 'modern', 'warm', 'cool')
- `elev` (float): Elevation angle for viewing
- `azim` (float): Azimuth angle for viewing
- `save_path` (str, optional): Path to save the image

### `create_3d_dice()`

Creates a simpler version of the 3D dice with basic styling.

### `save_dice_image()`

Saves the dice visualization as a high-quality image.

Parameters:
- `fig`: matplotlib figure object
- `filename` (str): Output filename
- `dpi` (int): Resolution (default: 300)

## Examples

```python
# Create and save all color schemes
schemes = ['classic', 'modern', 'warm', 'cool']
for scheme in schemes:
    create_enhanced_3d_dice(
        color_scheme=scheme,
        save_path=f'dice_{scheme}.png'
    )
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with Matplotlib and NumPy
- Inspired by classic dice designs
- Enhanced with modern visualization techniques
