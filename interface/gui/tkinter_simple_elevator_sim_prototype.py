"""Simple Full Elevator Simulator"""
import time
import threading
import tkinter as tk
from tkinter import messagebox


class ElevatorSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Elevator Simulator")
        
        # size: "widthxheight+X+Y"
        self.root.geometry("400x500")
        
        # background color:
        self.root.configure(bg="#2c3e50")

        # Simulator States:
        self.current_floor = 1
        self.target_floors = []
        self.is_moving = False
        self.total_floors = 8

        # Build the Interface
        self.create_widgets()

    def create_widgets(self):
        # Title Label:
        title = tk.Label(
            self.root, 
            text="ELEVATOR SIMULATOR", 
            font=("Arial", 16, "bold"), 
            fg="#ecf0f1", 
            bg="#2c3e50",
        )
        title.pack(pady=15)

        # Main Layout Frame:
        main_frame = tk.Frame(
            self.root, 
            bg="#2c3e50",
        )
        main_frame.pack(
            pady=10, 
            padx=20, 
            fill="both", 
            expand=True,
        )

        # Left Side: 
        # Elevator Shaft Display:
        self.shaft_frame = tk.Frame(
            main_frame, 
            bg="#34495e", 
            bd=2, 
            relief="sunken", 
            width=120,
        )
        self.shaft_frame.pack(
            side="left", 
            fill="y", 
            padx=10,
        )
        self.shaft_frame.pack_propagate(False)

        # Create Visual Floor Indicators in the shaft
        self.floor_displays = {}
        for floor in range(self.total_floors, 0, -1):
            lbl = tk.Label(
                self.shaft_frame, 
                text=f"Floor {floor}", 
                font=("Arial", 10), 
                bg="#34495e", 
                fg="#bdc3c7", 
                height=2,
            )
            lbl.pack(
                fill="x", 
                pady=2,
            )
            self.floor_displays[floor] = lbl

        # Highlight starting floor
        self.update_elevator_visual(self.current_floor)

        # Right Side: 
        # Control Panels:
        control_frame = tk.Frame(
            main_frame, 
            bg="#2c3e50",
        )
        control_frame.pack(
            side="right", 
            fill="both", 
            expand=True, 
            padx=10,
        )

        # Status Display Panel
        status_panel = tk.Frame(
            control_frame, 
            bg="#16a085", 
            bd=2, 
            relief="groove",
        )
        status_panel.pack(
            fill="x", 
            pady=(0, 15),
        )

        self.lbl_display = tk.Label(
            status_panel, 
            text="[ 1 ]", 
            font=("Courier New", 24, "bold"), 
            fg="#2ecc71", 
            bg="#111",
        )
        self.lbl_display.pack(
            fill="x", 
            pady=5, 
            padx=5,
        )

        self.lbl_status = tk.Label(
            status_panel, 
            text="State: IDLE", 
            font=("Arial", 10, "bold"), 
            fg="#ffffff", 
            bg="#16a085",
        )
        self.lbl_status.pack(pady=2)

        # Inside/Outside Call Panel Buttons
        btn_label = tk.Label(
            control_frame, 
            text="Call / Floor Buttons", 
            font=("Arial", 11, "bold"), 
            fg="#ecf0f1", 
            bg="#2c3e50",
        )
        btn_label.pack(
            anchor="w", 
            pady=(0, 5),
        )

        # Generate buttons dynamically for each floor
        for floor in range(self.total_floors, 0, -1):
            btn = tk.Button(
                control_frame, 
                text=f"Floor {floor}", 
                font=("Arial", 10, "bold"),
                bg="#ecf0f1", 
                activebackground="#3498db",
                command=lambda f=floor: self.call_elevator(f)
            )
            btn.pack(fill="x", pady=4)

    def update_elevator_visual(self, active_floor):
        # Reset colors of all floors in the shaft graphical view
        for floor, widget in self.floor_displays.items():
            if floor == active_floor:
                widget.configure(
                    bg="#e74c3c", 
                    fg="#ffffff", 
                    font=("Arial", 11, "bold"),
                ) # Red indicator for elevator car
            else:
                widget.configure(
                    bg="#34495e", 
                    fg="#bdc3c7", 
                    font=("Arial", 10),
                )

    def call_elevator(self, floor):
        if floor in self.target_floors or floor == self.current_floor:
            return  # Ignore duplicate requests or immediate arrivals
        
        self.target_floors.append(floor)
        
        # If the elevator is not currently tracking a sequence, start the processing thread
        if not self.is_moving:
            self.is_moving = True
            # Movement loop is run in a separate thread so the GUI remains active and clickable
            threading.Thread(target=self.process_queue, daemon=True).start()

    def process_queue(self):
        while self.target_floors:
            # Basic queue logic: Go to the oldest requested floor first
            next_floor = self.target_floors[0]
            
            # Move towards the destination step-by-step
            while self.current_floor != next_floor:
                if self.current_floor < next_floor:
                    self.current_floor += 1
                    direction_text = "State: MOVING UP ▲"
                else:
                    self.current_floor -= 1
                    direction_text = "State: MOVING DOWN ▼"

                # Update safe Tkinter UI elements inside the thread loop using .configure
                self.lbl_display.configure(text=f"[ {self.current_floor} ]")
                self.lbl_status.configure(text=direction_text)
                self.update_elevator_visual(self.current_floor)
                
                # Travel time between floors (1 second)
                time.sleep(1)

            # Destination floor reached
            self.target_floors.pop(0)
            self.lbl_status.configure(text="State: DOORS OPENING")
            time.sleep(1.5)  # Simulate passengers getting off/on

        # All requests cleared
        self.lbl_status.configure(text="State: IDLE")
        self.is_moving = False


if __name__ == "__main__":
    root = tk.Tk()
    app = ElevatorSimulator(root)
    root.mainloop()
    