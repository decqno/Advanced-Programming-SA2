import tkinter as tk
from tkinter import ttk
import requests

# API implemented inside an OOP
class WizardingWorldFilms:
    def __init__(self):
        self.hp_url = "https://api.potterdb.com/v1/movies"
        self.data = self.get_movies()

    def get_movies(self):
        response = requests.get(self.hp_url)
        response.raise_for_status()
        return response.json()

    def get_movie_titles(self):
        return [movie["attributes"]["title"] for movie in self.data["data"]]

    def get_movie_info(self, selected_title):
        for movie in self.data["data"]:
            details = movie["attributes"]
            if details["title"] == selected_title:
                return {
                    "Title": details.get("title", "N/A"),
                    "Release Date": details.get("release_date", "N/A"),
                    "Runtime": details.get("running_time", "N/A"),
                    "Rating": details.get("rating", "N/A"),
                    "Summary": details.get("summary", "No summary available")
                }
        return None

# Main Tkinter GUI
api = WizardingWorldFilms()

root = tk.Tk() 
root.title("Wizarding World Films")
root.geometry("700x500")
root.configure(bg="#2D3C59")

# Main Title Label
title = tk.Label(root, text="Wizarding World Films", justify="center", font=('Arial', 20, 'bold'), fg="#94B4C1", bg="#2D3C59")
title.grid(row=0, column=0, pady=(20, 5), sticky="nswe")

# Movie selection dropdown
movie_selector = ttk.Combobox(root, values=api.get_movie_titles(), state="readonly", width=50)
movie_selector.grid(row=1, column=0, pady=10)
movie_selector.current(0)

# Button to show details
def show_details():
    output.delete("1.0", tk.END)
    selected_movie = movie_selector.get()
    details = api.get_movie_info(selected_movie)
    if details:
        for key, value in details.items():
            output.insert(tk.END, f"{key}:\n{value}\n\n")
    else:
        output.insert(tk.END, "Movie details not found.")

view_button = tk.Button(root, text="View Details", command=show_details)
view_button.grid(row=2, column=0, pady=5)

# Output Text box
output = tk.Text(root, wrap="word")
output.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# Make text box expand with window
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()