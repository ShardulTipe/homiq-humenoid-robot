import cv2
import numpy as np
import random
import time


# Robot movement control functions
def move_forward():
    print("Moving forward")


def stop():
    print("Stopping")


def turn_left():
    print("Turning left")


def turn_right():
    print("Turning right")


# Define actions
ACTIONS = ["move_forward", "turn_left", "turn_right"]
ACTION_FUNCTIONS = {
    "move_forward": move_forward,
    "turn_left": turn_left,
    "turn_right": turn_right
}

# Parameters for Q-learning
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON = 0.1  # Exploration rate

# Initialize Q-table (for simplicity, using basic states like "obstacle detected" or "clear path")
Q_table = {
    "clear_path": {action: 0 for action in ACTIONS},
    "obstacle_in_front": {action: 0 for action in ACTIONS}
}

# Parameters for obstacle detection
OBSTACLE_THRESHOLD_AREA = 3000  # Adjust based on trial and error

# Initialize camera and background subtractor
cap = cv2.VideoCapture(0)
back_sub = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)


def detect_obstacle(frame):
    """Detect if there is an obstacle in front using background subtraction and contour detection."""
    fg_mask = back_sub.apply(frame)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        if area > OBSTACLE_THRESHOLD_AREA and y + h > frame.shape[0] // 2:
            return "obstacle_in_front"  # Obstacle detected
    return "clear_path"  # No obstacle detected


def choose_action(state):
    """Choose the best action based on Q-table or explore randomly."""
    if random.uniform(0, 1) < EPSILON:
        # Exploration: choose a random action
        return random.choice(ACTIONS)
    else:
        # Exploitation: choose the action with the highest Q-value
        return max(Q_table[state], key=Q_table[state].get)


def update_q_table(state, action, reward, next_state):
    """Update Q-value based on observed reward and maximum future reward."""
    best_next_action = max(Q_table[next_state], key=Q_table[next_state].get)
    td_target = reward + DISCOUNT_FACTOR * Q_table[next_state][best_next_action]
    Q_table[state][action] += LEARNING_RATE * (td_target - Q_table[state][action])


try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame for faster processing
        frame_resized = cv2.resize(frame, (320, 240))

        # Detect the current state (obstacle in front or clear path)
        current_state = detect_obstacle(frame_resized)

        # Choose an action based on Q-table
        action = choose_action(current_state)
        ACTION_FUNCTIONS[action]()  # Execute the chosen action

        # Observe the reward for the action
        if current_state == "obstacle_in_front" and action == "move_forward":
            reward = -10  # Penalize moving forward into an obstacle
        elif current_state == "clear_path" and action == "move_forward":
            reward = 10  # Reward moving forward when the path is clear
        else:
            reward = -1  # Small penalty for turning

        # Detect the new state after taking the action
        new_state = detect_obstacle(frame_resized)

        # Update Q-table with the observed reward
        update_q_table(current_state, action, reward, new_state)

        # Display the frame for debugging
        cv2.imshow("Robot View", frame_resized)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()








































































































