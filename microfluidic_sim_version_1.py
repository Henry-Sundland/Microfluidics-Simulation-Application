import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

# Simulation class to handle the math and physics
class Simulation:
    def __init__(self, length, width, flow_rate, viscosity):
        self.length = length
        self.width = width
        self.flow_rate = flow_rate
        self.viscosity = viscosity

    # Poiseuille flow formula for a rectangular channel
    def calculate_velocity_rectangular(self):
        y = np.linspace(-self.width/2, self.width/2, 100)
        velocity_profile = (self.flow_rate / (2 * self.viscosity * self.length)) * (self.width**2 - y**2)
        return y, velocity_profile

    # Hagen-Poiseuille flow formula for a circular channel
    def calculate_velocity_circular(self, radius):
        r = np.linspace(0, radius, 100)  # radial distance from the center to the edge
        velocity_profile = (self.flow_rate / (4 * self.viscosity * self.length)) * (radius**2 - r**2)
        return r, velocity_profile

# GUI class to manage the interface
class GUI:
    def __init__(self, root):
        self.root = root
        self.simulation = None
        self.setup_widgets()

    def setup_widgets(self):
        # Input fields for user parameters
        tk.Label(self.root, text="Channel Length").grid(row=0)
        tk.Label(self.root, text="Channel Width/Radius").grid(row=1)  # Works for both rectangular and circular
        tk.Label(self.root, text="Flow Rate").grid(row=2)
        tk.Label(self.root, text="Viscosity").grid(row=3)

        self.length_entry = tk.Entry(self.root)
        self.width_entry = tk.Entry(self.root)
        self.flow_rate_entry = tk.Entry(self.root)
        self.viscosity_entry = tk.Entry(self.root)

        self.length_entry.grid(row=0, column=1)
        self.width_entry.grid(row=1, column=1)
        self.flow_rate_entry.grid(row=2, column=1)
        self.viscosity_entry.grid(row=3, column=1)

        # Dropdown menu for selecting flow model
        self.model_var = tk.StringVar(self.root)
        self.model_var.set("Poiseuille (Rectangular)")  # Default value
        model_dropdown = tk.OptionMenu(self.root, self.model_var, "Poiseuille (Rectangular)", "Hagen-Poiseuille (Circular)")
        model_dropdown.grid(row=4, column=0, columnspan=2)

        # Button to run the simulation
        self.simulate_button = tk.Button(self.root, text='Run Simulation', command=self.run_simulation)
        self.simulate_button.grid(row=5, column=0, columnspan=2)

        # Plot area for Matplotlib
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.grid(row=6, column=0, columnspan=2)

    def run_simulation(self):
        # Get user inputs
        length = float(self.length_entry.get())
        width_or_radius = float(self.width_entry.get())  # Can be width (rectangular) or radius (circular)
        flow_rate = float(self.flow_rate_entry.get())
        viscosity = float(self.viscosity_entry.get())

        # Create a Simulation object with inputs
        self.simulation = Simulation(length, width_or_radius, flow_rate, viscosity)

        # Get selected flow model
        selected_model = self.model_var.get()

        # Run different simulations based on the selected model
        if selected_model == "Poiseuille (Rectangular)":
            y, velocity_profile = self.simulation.calculate_velocity_rectangular()
            x_label = "Channel Width"
        elif selected_model == "Hagen-Poiseuille (Circular)":
            y, velocity_profile = self.simulation.calculate_velocity_circular(width_or_radius)
            x_label = "Radial Position"

        # Update the plot
        self.update_plot(y, velocity_profile, x_label)

    def update_plot(self, y, velocity_profile, x_label):
        # Clear previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Create figure and plot
        fig, ax = plt.subplots()
        ax.plot(y, velocity_profile)
        ax.set_title('Velocity Profile')
        ax.set_xlabel(x_label)
        ax.set_ylabel('Velocity')

        # Embed plot into Tkinter GUI
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Main application class (optional)
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Microfluidic Simulation Tool")
        self.gui = GUI(self.root)

    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = App()
    app.run()
