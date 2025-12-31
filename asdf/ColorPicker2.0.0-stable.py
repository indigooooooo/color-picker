import tkinter as tk
import subprocess
import sys
import os

# Auto install packages if needed
try:
    import pyautogui
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
    import pyautogui

try:
    from pynput import keyboard
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
    from pynput import keyboard

try:
    from screeninfo import get_monitors
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "screeninfo"])
    from screeninfo import get_monitors


class ColorPickerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Color Picker v1.2.0")
        self.window.geometry("400x900")
        self.window.resizable(False, False)
        self.window.attributes('-topmost', True)
        
        # Set window icon
        base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, 'icon.ico')
        if not os.path.exists(icon_path):
            exe_dir = os.path.dirname(sys.executable) if hasattr(sys, 'frozen') else os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(exe_dir, 'icon.ico')
        if os.path.exists(icon_path):
            try:
                self.window.iconbitmap(icon_path)
            except:
                pass
        
        self.window.configure(bg='#1e1e1e')
        self.current_rgb = None
        
        main_frame = tk.Frame(self.window, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="Color Picker", font=("Segoe UI", 20, "bold"), bg='#1e1e1e', fg='#ffffff').pack(pady=(0, 10))
        
        self.preview_canvas = tk.Canvas(main_frame, width=250, height=250, bg='#2d2d2d', highlightthickness=2, highlightbackground='#3d3d3d', relief=tk.FLAT)
        self.preview_canvas.pack(pady=15)
        
        tk.Label(main_frame, text="Press F11 to capture color\nPress F10 to clear", font=("Segoe UI", 10), bg='#1e1e1e', fg='#aaaaaa', justify=tk.CENTER).pack(pady=(10, 15))
        
        codes_frame = tk.Frame(main_frame, bg='#1e1e1e')
        codes_frame.pack(fill=tk.BOTH, expand=True)
        
        self.color_labels = {}
        for format_name, label_key in [("RGB", "rgb_label"), ("HEX", "hex_label"), ("HSV", "hsv_label"), ("HSL", "hsl_label"), ("CMYK", "cmyk_label")]:
            tk.Label(codes_frame, text=f"{format_name}:", font=("Segoe UI", 11, "bold"), bg='#1e1e1e', fg='#888888', anchor='w').pack(fill=tk.X, pady=(5, 2))
            value_label = tk.Label(codes_frame, text="Not captured", font=("Consolas", 11), bg='#2d2d2d', fg='#ffffff', anchor='w', padx=10, pady=5, relief=tk.FLAT)
            value_label.pack(fill=tk.X, pady=(0, 8))
            self.color_labels[label_key] = value_label
        
        tk.Button(main_frame, text="Exit (F12)", command=self.exit_app, font=("Segoe UI", 10), bg='#d32f2f', fg='#ffffff', activebackground='#b71c1c', activeforeground='#ffffff', relief=tk.FLAT, padx=20, pady=8, cursor='hand2').pack(pady=(15, 10))
        
        self.window.bind("<F12>", lambda event: self.exit_app())
        self.setup_hotkeys()
    
    def setup_hotkeys(self):
        def on_press(key):
            try:
                if key == keyboard.Key.f11:
                    self.capture_color()
                elif key == keyboard.Key.f10:
                    self.clear_color()
                elif key == keyboard.Key.f12:
                    self.exit_app()
            except AttributeError:
                pass
        
        self.keyboard_listener = keyboard.Listener(on_press=on_press)
        self.keyboard_listener.daemon = True
        self.keyboard_listener.start()
    
    def capture_color(self):
        try:
            x, y = pyautogui.position()
            self.current_rgb = self.get_color_at(x, y)
            self.update_display()
        except Exception as e:
            print(f"Error capturing color: {e}")
    
    def clear_color(self):
        self.current_rgb = None
        self.update_display()
    
    def get_color_at(self, x, y):
        for monitor in get_monitors():
            if monitor.x <= x < monitor.x + monitor.width and monitor.y <= y < monitor.y + monitor.height:
                adjusted_x, adjusted_y = x - monitor.x, y - monitor.y
                if 0 <= adjusted_x < monitor.width and 0 <= adjusted_y < monitor.height:
                    screenshot = pyautogui.screenshot(region=(monitor.x + adjusted_x, monitor.y + adjusted_y, 1, 1))
                    return screenshot.getpixel((0, 0))
        return (0, 0, 0)
    
    def rgb_to_hex(self, rgb):
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2]).upper()
    
    def rgb_to_hsv(self, rgb):
        r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
        max_val, min_val, delta = max(r, g, b), min(r, g, b), max(r, g, b) - min(r, g, b)
        h = 0 if delta == 0 else (60 * (((g - b) / delta) % 6) if max_val == r else (60 * (((b - r) / delta) + 2) if max_val == g else 60 * (((r - g) / delta) + 4)))
        return (round(h, 1), round((0 if max_val == 0 else delta / max_val) * 100, 1), round(max_val * 100, 1))
    
    def rgb_to_hsl(self, rgb):
        r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
        max_val, min_val, delta = max(r, g, b), min(r, g, b), max(r, g, b) - min(r, g, b)
        l = (max_val + min_val) / 2
        s = 0 if delta == 0 else delta / (1 - abs(2 * l - 1))
        h = 0 if delta == 0 else (60 * (((g - b) / delta) % 6) if max_val == r else (60 * (((b - r) / delta) + 2) if max_val == g else 60 * (((r - g) / delta) + 4)))
        return (round(h, 1), round(s * 100, 1), round(l * 100, 1))
    
    def rgb_to_cmyk(self, rgb):
        r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
        k = 1 - max(r, g, b)
        if k == 1:
            return (0, 0, 0, 100)
        return (round((1 - r - k) / (1 - k) * 100, 1), round((1 - g - k) / (1 - k) * 100, 1), round((1 - b - k) / (1 - k) * 100, 1), round(k * 100, 1))
    
    def update_display(self):
        if self.current_rgb is None:
            self.preview_canvas.delete("all")
            self.preview_canvas.create_rectangle(0, 0, 250, 250, fill='#2d2d2d', outline='')
            for label in self.color_labels.values():
                label.config(text="Not captured")
        else:
            hex_color = self.rgb_to_hex(self.current_rgb)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_rectangle(0, 0, 250, 250, fill=hex_color, outline='')
            self.color_labels["rgb_label"].config(text=f"({self.current_rgb[0]}, {self.current_rgb[1]}, {self.current_rgb[2]})")
            self.color_labels["hex_label"].config(text=hex_color)
            hsv = self.rgb_to_hsv(self.current_rgb)
            self.color_labels["hsv_label"].config(text=f"({hsv[0]}°, {hsv[1]}%, {hsv[2]}%)")
            hsl = self.rgb_to_hsl(self.current_rgb)
            self.color_labels["hsl_label"].config(text=f"({hsl[0]}°, {hsl[1]}%, {hsl[2]}%)")
            cmyk = self.rgb_to_cmyk(self.current_rgb)
            self.color_labels["cmyk_label"].config(text=f"({cmyk[0]}%, {cmyk[1]}%, {cmyk[2]}%, {cmyk[3]}%)")
    
    def exit_app(self, event=None):
        try:
            if hasattr(self, 'keyboard_listener'):
                self.keyboard_listener.stop()
        except:
            pass
        self.window.quit()
        self.window.destroy()


def main():
    app = ColorPickerApp()
    app.window.mainloop()


if __name__ == "__main__":
    main()
