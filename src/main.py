from flask import Flask, render_template, jsonify, send_file
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import math

app = Flask(__name__, template_folder='./')

@app.route('/')
def index():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', time=current_time)

@app.route('/get_time/')
def get_time():
    current_time =  datetime.now().strftime('%H:%M:%S.%f')[:-4]
    # Generate an analog clock image
    img = draw_clock(current_time)
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return jsonify({'digital': current_time, 'analog': img})

def draw_clock(time_str):
    # Create a blank image with a white background
    image_size = (400, 400)
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)

    # Calculate the center and radius of the clock face
    center = (image_size[0] // 2, image_size[1] // 2)
    radius = min(center[0], center[1]) - 10

    # Draw the clock face
    draw.ellipse([(center[0] - radius, center[1] - radius),
                  (center[0] + radius, center[1] + radius)], outline="black", width=2)
    
    # Draw clock face markings (optional)
    for i in range(1, 13):
        angle = math.radians(90 - i * 30)
        mark_length = radius * 0.9
        start_point = (center[0] + mark_length * math.cos(angle),
                       center[1] - mark_length * math.sin(angle))
        mark_length = radius * 0.8
        end_point = (center[0] + mark_length * math.cos(angle),
                     center[1] - mark_length * math.sin(angle))
        draw.line([start_point, end_point], fill="black", width=2)

    # Get the current time with millisecond precision
    current_time = datetime.strptime(time_str, '%H:%M:%S.%f')

    # Calculate the angles for the clock hands, including milliseconds
    hour_angle = 90 - (current_time.hour % 12 + current_time.minute / 60) * 30 - current_time.second / 360 * 30
    minute_angle = 90 - current_time.minute * 6 - current_time.second / 60 * 6
    second_angle = 90 - current_time.second * 6 - current_time.microsecond / 1000000 * 6

    # Draw the clock hands
    draw_hand(draw, center, hour_angle, radius * 0.5, width=8, color="black")
    draw_hand(draw, center, minute_angle, radius * 0.7, width=4, color="black")
    draw_hand(draw, center, second_angle, radius * 0.8, width=2, color="red")

    # Save the image to a BytesIO object
    image_buffer = io.BytesIO()
    image.save(image_buffer, format="PNG")
    image_base64 = base64.b64encode(image_buffer.getvalue()).decode('utf-8')

    return image_base64

def draw_hand(draw, center, angle, length, width, color, antialias=True):
    radian_angle = math.radians(angle)
    end_point = (center[0] + length * math.cos(radian_angle),
                 center[1] - length * math.sin(radian_angle))

    # Use antialiasing if specified
    if antialias:
        draw.line([center, end_point], fill=color, width=width, joint="curve")
    else:
        draw.line([center, end_point], fill=color, width=width)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
