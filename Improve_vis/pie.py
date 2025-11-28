import matplotlib
matplotlib.use('Agg')  # Must be before importing pyplot
import matplotlib.pyplot as plt
import json
from PIL import Image, ImageDraw

color_map = {
    'C1CCCCC1': 'red',
    "O=C(Nc1ccccc1)c1ccccc1": 'blue',
    "c1ccc(-c2ccccc2)cc1": 'grey',
    "c1ccc(COc2ccccc2)cc1": 'brown',
    "c1ccc(Cc2ccccc2)cc1": 'green',
    "c1ccc2[nH]ccc2c1": 'pink',
    "c1ccc2ccccc2c1": 'gold',
    "c1ccc2ncccc2c1": 'yellow',
    "c1ccccc1": "darkblue",
    "c1ccncc1": 'black'
} #One will need to modify the colormap as desired... this is for the data used for this project

def pie(filename):
    with open(filename) as fp:
        mapper = json.load(fp)
    count = 1
    for i in mapper["mapper"]["nodes"]:
        print(count)
        data = i["categorical_cols_summary"]["scaffold"]
        labels = list(data.keys())
        sizes = list(data.values())
        colors = [color_map.get(label, 'white') for label in labels]


        # Create a figure and axis (Square image)
        fig, ax = plt.subplots(figsize=(5,5), dpi=300)  # 1500x1500 pixels
        ax.set_facecolor("none")  # Transparent background

        # Create a centered pie chart
        wedges, _ = ax.pie(sizes, colors=colors, wedgeprops={'edgecolor': 'white'})

        # Ensure the pie chart is centered and perfectly circular
        ax.set_aspect("equal")  
        plt.axis("off")  # Remove axes

        # Adjust layout to remove padding/margins
        #plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  

        # Save the image with tight bounding
        plt.savefig("./shots/pie/pie_chart.png", transparent=True, dpi=600, bbox_inches='tight', pad_inches=0)

        # Open the image
        image = Image.open("./shots/pie/pie_chart.png").convert("RGBA")

        # Define the circle center and radius
        width, height = image.size
        center_x, center_y = width / 2, height / 2  # Correct center based on image dimensions
        radius = min(width, height) // 4 # Make sure radius is half of the shortest dimension

        # Crop to the bounding box of the circle (optional)
        bbox = (center_x - radius, center_y - radius, center_x + radius, center_y + radius)
        result = image.crop(bbox)

        # Save or show the result
        #result.save("./pie/pie_chart" + str(i['id']) + ".png")
        result.save("./shots/pie/pie_chart" + str(count) + ".png")
        count = count + 1