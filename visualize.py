import nkmodel as nk
import tkinter as tk
import math

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.canvas = tk.Canvas(self, width=800, height=670)
        self.canvas.pack()

        self.control_frame = tk.Frame(self, width=250, height=200)
        self.control_frame.pack(side=tk.RIGHT)

        self.n_label = tk.Label(self.control_frame, text="N:")
        self.n_label.pack()

        self.n_entry = tk.Entry(self.control_frame, width=10)
        self.n_entry.pack()

        self.k_label = tk.Label(self.control_frame, text="K:")
        self.k_label.pack()

        self.k_entry = tk.Entry(self.control_frame, width=10)
        self.k_entry.pack()

        self.new_network_button = tk.Button(self.control_frame, text="New Network", command=self.new_network)
        self.new_network_button.pack()

        self.new_state_button = tk.Button(self.control_frame, text="New State", command=self.new_state)
        self.new_state_button.pack(side=tk.LEFT)

        self.step_button = tk.Button(self.control_frame, text="Step", command=self.step)
        self.step_button.pack(side=tk.LEFT)

    def new_network(self):
        n = int(self.n_entry.get())
        k = int(self.k_entry.get())
        if n < k:
            return;

        self.nodes = nk.Network(n, k)
        self.canvas.delete("all")
        self.circles = []
        center_width = self.canvas.winfo_width()/2
        center_height = self.canvas.winfo_height()/2 - 20
        state = self.nodes.get_state()

        for i, b in enumerate(state):
            x = center_width + 300*math.sin(((2*math.pi)/n)*i)
            y = center_height + 300*math.cos(((2*math.pi)/n)*i)
            if b:
                color = "red"
            else:
                color = "white"
            self.circles.append(self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color))

        conns = self.nodes.get_conns()
        for i, l in enumerate(conns):
            start_coords = self.canvas.coords(self.circles[i])
            for c in l:
                end_coords = self.canvas.coords(self.circles[c]) 
                self.canvas.create_line(start_coords[0] + 20, start_coords[1] + 20, end_coords[0] + 20, end_coords[1] + 20, arrow=tk.FIRST)

    def new_state(self):
        self.nodes = nk.Network(self.nodes.get_n(), self.nodes.get_k(), start_conns=self.nodes.get_start_conns(), start_funcs=self.nodes.get_funcs()) 
        self.update_colors()

    def step(self):
        self.nodes.step()
        self.update_colors()
        
    def update_colors(self):
        state = self.nodes.get_state()
        for i, c in enumerate(self.circles):
            if state[i]:
                color = "red"
            else:
                color = "white"
            self.canvas.itemconfig(c, fill=color)

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
