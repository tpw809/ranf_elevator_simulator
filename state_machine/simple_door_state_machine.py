"""Floor Elevator Door State Machine

nominal state is closed_idle

"""
from enum import Enum, auto


class DoorState(Enum):
    CLOSED_IDLE = auto()
    OPEN_FOR_CAB = auto()
    CLOSING = auto()
    OPENING = auto()
    OVERRIDE_OPEN = auto()


class ElevatorDoorStateMachine:
    def __init__(self):
        self.state = DoorState.CLOSED_IDLE

    # -----------------------------
    # External events
    # -----------------------------

    def cab_arrived(self):
        """
        Cab arrives at the floor → door must open.
        """
        if self.state == DoorState.CLOSED_IDLE:
            print("Cab arrived — opening door")
            self.state = DoorState.OPENING
        else:
            print("Cab arrival ignored — door already active")

    def door_fully_open(self):
        """
        Sensor event: door has finished opening.
        """
        if self.state in (DoorState.OPENING, DoorState.OVERRIDE_OPEN):
            print("Door is fully open")
            self.state = DoorState.OPEN_FOR_CAB
        else:
            print("Open event ignored — wrong state")

    def door_fully_closed(self):
        """
        Sensor event: door has finished closing.
        """
        if self.state == DoorState.CLOSING:
            print("Door is fully closed — returning to idle")
            self.state = DoorState.CLOSED_IDLE
        else:
            print("Close event ignored — wrong state")

    def command_close(self):
        """
        Hallway or cab controller requests door to close.
        """
        if self.state == DoorState.OPEN_FOR_CAB:
            print("Closing door")
            self.state = DoorState.CLOSING
        else:
            print("Close command ignored — door not in open state")

    def obstruction_detected(self):
        """
        Safety override: door must reopen immediately.
        """
        print("Obstruction detected — forcing door open")
        self.state = DoorState.OVERRIDE_OPEN

    def command_open(self):
        """
        Manual open command (e.g., door-open button).
        """
        if self.state == DoorState.CLOSED_IDLE:
            print("Opening door manually")
            self.state = DoorState.OPENING
        elif self.state == DoorState.CLOSING:
            print("Interrupting closing — reopening")
            self.state = DoorState.OPENING
        else:
            print("Open command ignored — door already open or opening")

    def __repr__(self):
        return f"<ElevatorDoorStateMachine state={self.state.name}>"


def main() -> None:
    # -------------------------
    # Example usage
    # -------------------------
    print(DoorState)
    pairs = [(member.name, member.value) for member in DoorState]
    print(pairs)
    
    door = ElevatorDoorStateMachine()
    print(door)
    
    door.cab_arrived()
    print(door)
    
    door.door_fully_open()
    print(door)
    
    door.command_close()
    print(door)
    
    door.obstruction_detected()
    print(door)
    
    door.door_fully_open()
    print(door)
    
    door.command_close()
    print(door)
    
    door.door_fully_closed()
    print(door)


if __name__ == "__main__":
    main()
    