from enum import Enum, auto


class CallState(Enum):
    IDLE = auto()
    CALL_UP = auto()
    CALL_DOWN = auto()


class ElevatorCallStateMachine:
    def __init__(self):
        self.state = CallState.IDLE

    def press_up(self):
        if self.state == CallState.IDLE:
            self.state = CallState.CALL_UP
            print("Call registered: UP")
        else:
            print("Ignoring UP press — call already active")

    def press_down(self):
        if self.state == CallState.IDLE:
            self.state = CallState.CALL_DOWN
            print("Call registered: DOWN")
        else:
            print("Ignoring DOWN press — call already active")

    def cab_arrived(self, direction):
        """
        direction: "up" or "down"
        """
        if self.state == CallState.IDLE:
            print("Cab arrived but no call was active")
            return

        if direction == "up" and self.state == CallState.CALL_UP:
            print("Cab arrived going UP — clearing call")
            self.state = CallState.IDLE

        elif direction == "down" and self.state == CallState.CALL_DOWN:
            print("Cab arrived going DOWN — clearing call")
            self.state = CallState.IDLE

        else:
            print("Cab arrived in wrong direction — call remains active")

    def set_state_to_idle(self):
        self.state = CallState.IDLE

    def __repr__(self):
        return f"<ElevatorCallStateMachine: state={self.state.name}>"


def main() -> None:
    # -------------------------
    # Example usage
    # -------------------------
    
    # CallStates:
    print(CallState)
    pairs = [(member.name, member.value) for member in CallState]
    print(pairs)
    
    floor_x_call_sm = ElevatorCallStateMachine()
    print(floor_x_call_sm)
    
    floor_x_call_sm.press_up()
    print(floor_x_call_sm)
    
    floor_x_call_sm.cab_arrived("down")   # wrong direction
    print(floor_x_call_sm)
    
    floor_x_call_sm.cab_arrived("up")     # correct direction
    print(floor_x_call_sm)
    
    floor_x_call_sm.press_down()
    print(floor_x_call_sm)
    
    floor_x_call_sm.set_state_to_idle()
    print(floor_x_call_sm)
    
    floor_x_call_sm.press_down()
    print(floor_x_call_sm)
    
    floor_x_call_sm.cab_arrived("up")
    print(floor_x_call_sm)
    
    floor_x_call_sm.cab_arrived("down")
    print(floor_x_call_sm)


if __name__ == "__main__":
    main()
    