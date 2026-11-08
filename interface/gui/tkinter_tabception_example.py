"""Example of left hand side tab notebook, 
each with an upper tab notebook
"""
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


def create_app():
    # Initialize the main window:
    root = tk.Tk()
    
    # Fetch and configure the internal default font
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(
        #family="Antonio", 
        family="Lexend",
        size=12,
        weight="bold",
        # slant="italic",
        # underline=0,
        # overstrike=0,
    )

    root.title("Nested Tab GUI")
    
    # size: "widthxheight+X+Y"
    root.geometry("800x500")

    # Create and configure custom styles for the left-side tabs:
    style = ttk.Style()
    # "west" positioning ('w') places the tab bar on the left side
    style.configure("LeftTabs.TNotebook", tabposition="wn") 

    # Create the Main (Outer) Left-Side Notebook:
    main_notebook = ttk.Notebook(
        root, 
        style="LeftTabs.TNotebook",
    )
    main_notebook.pack(
        fill="both", 
        expand=True, 
        padx=5, 
        pady=5,
    )

    # --- SIDE TAB 1 ---
    # Create a frame to act as the first left-side tab container
    side_tab1 = ttk.Frame(main_notebook)
    main_notebook.add(
        side_tab1, 
        text="  Dashboard  ",
    )

    # Inner upper tabs for Side Tab 1
    inner_notebook1 = ttk.Notebook(side_tab1) # Default layout is upper tabs
    inner_notebook1.pack(
        fill="both", 
        expand=True, 
        padx=5, 
        pady=5,
    )

    sub_tab1_a = ttk.Frame(inner_notebook1)
    sub_tab1_b = ttk.Frame(inner_notebook1)
    inner_notebook1.add(sub_tab1_a, text="Overview")
    inner_notebook1.add(sub_tab1_b, text="Analytics")

    # Add content to Inner Tab A
    ttk.Label(
        sub_tab1_a, 
        text="Dashboard Overview Content Goes Here", 
        # font=("Antonio", 14),
    ).pack(pady=40)
    
    # Add content to Inner Tab B
    ttk.Label(
        sub_tab1_b, 
        text="Analytics Visualizations & Graphs", 
        # font=("Antonio", 14),
    ).pack(pady=40)


    # --- SIDE TAB 2 ---
    # Create a frame to act as the second left-side tab container
    side_tab2 = ttk.Frame(main_notebook)
    main_notebook.add(side_tab2, text="  Settings   ")

    # Inner upper tabs for Side Tab 2
    inner_notebook2 = ttk.Notebook(side_tab2)
    inner_notebook2.pack(
        fill="both", 
        expand=True, 
        padx=5, 
        pady=5,
    )

    sub_tab2_a = ttk.Frame(inner_notebook2)
    sub_tab2_b = ttk.Frame(inner_notebook2)
    
    inner_notebook2.add(
        sub_tab2_a, 
        text="Profile Settings",
    )
    
    inner_notebook2.add(
        sub_tab2_b, 
        text="Application Settings",
    )

    # Add content to Inner Tabs
    ttk.Label(
        sub_tab2_a, 
        text="Modify User Account & Preferences", 
        # font=("Antonio", 14),
        # bg="#5588ee",
    ).pack(pady=40)
    
    ttk.Label(
        sub_tab2_b, 
        text="System & Theme Configurations", 
        # font=("Antonio", 14),
    ).pack(pady=40)

    # Start the application loop:
    root.mainloop()


if __name__ == "__main__":
    create_app()
    