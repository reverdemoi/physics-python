import matplotlib.colors as mcolors

def generate_color_map(n=100):
    """
    Generate a colormap that transitions smoothly through the colors of the rainbow.
    """
    # Define the colors of the rainbow
    # colors = ["green", "blue", "red"]
    colors = ["#00FFFF", "#1E90FF", "#9370DB"]
    # Create a colormap from these colors
    cmap = mcolors.LinearSegmentedColormap.from_list('rainbow', colors, N=n)
    return cmap

def map_number_to_color(number, cmap, n=100):
    """
    Map a number in the range 1 to n to a color using the provided colormap.
    """
    # Normalize the number to the range 0 to 1
    norm = mcolors.Normalize(vmin=1, vmax=n)
    # Get the color from the colormap
    color = cmap(norm(number))
    return color