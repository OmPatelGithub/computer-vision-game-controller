# Wheel Visualizer Application
The Wheel Visualizer is a Python application that combines computer vision, artificial intelligence, and gaming graphics to create an interactive and immersive experience. This application is designed to visualize the rotation of a virtual wheel on the screen based on the user's hand movements. By leveraging multi-threading and AI libraries like Mediapipe, the application provides real-time feedback, allowing users to control the wheel's rotation using hand gestures.

## Key Features
- Real-time Hand Gesture Recognition: The application utilizes the Mediapipe library to recognize and track hand gestures in real time. This enables users to control the rotation of the virtual wheel by moving their hands.

- Multi-threading: To enhance the responsiveness and interactivity of the application, multi-threading is implemented. Separate threads handle wheel rotation and radius adjustment, ensuring smooth and fluid transitions based on user input.

- Interactive Wheel Visualization: The virtual wheel reacts dynamically to the user's hand movements. As the user moves their hands left or right, the wheel visually rotates in the corresponding direction and angle.

## Demo Video
Wheel Visualizer Demo

## Screenshots
Screenshot 1
Screenshot 2

How to Use
Installation:

Clone this repository to your local machine.
Install the required Python libraries using pip install -r requirements.txt.
Run the Application:

Execute the main Python script: python wheel_visualizer.py.
Interaction:

Stand in front of your camera to allow the application to track your hand gestures.
Move your hands left or right to see the virtual wheel rotate in the corresponding direction and angle.
The application will also display the angle and radius information on the screen.
Requirements
Python 3.6+
OpenCV
Pygame
Mediapipe
Keyboard
Contributions
Contributions to this project are welcome! If you find any issues or have ideas for improvements, please feel free to submit a pull request.

Acknowledgements
This project utilizes the power of the Mediapipe library, developed by Google, for hand gesture recognition.
The Pygame library is used for rendering the graphics and creating an interactive display.
License
This project is licensed under the MIT License.

