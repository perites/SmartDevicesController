import tinytuya
import customtkinter as ctk

import constants


class Device:
    def __init__(self, name, dev_id, address, local_key):
        self.name = name
        self.device = tinytuya.OutletDevice(
            dev_id=dev_id,
            address=address,
            local_key=local_key,
            version=3.3)

    def turn_on(self):
        self.device.turn_on()

    def turn_off(self):
        self.device.turn_off()

    def is_working(self):
        result = self.device.status()
        if result.get("Error"):
            raise Exception(f"Error while checking status :\n{result}")

        return result['dps']['1']

    def toggle(self):
        if self.is_working():
            self.turn_off()
        else:
            self.turn_on()


class StatusApp(ctk.CTk):
    def __init__(self, devices):
        super().__init__()

        self.title("Smart Devices Control panel")
        self.geometry("600x600")

        self.devices_frame = ctk.CTkFrame(self)
        self.devices_frame.pack(pady=20, padx=20, fill="both", expand=True)

        for device in devices:
            self.add_device_widget(device)

    def add_device_widget(self, device):
        frame = ctk.CTkFrame(self.devices_frame)
        frame.pack(fill="x", pady=5)

        texts = self.get_label_and_button_text(device)

        status_label = ctk.CTkLabel(frame, text=texts["label"], font=("Arial", 18))
        status_label.pack(side="left", padx=10)

        toggle_button = ctk.CTkButton(frame, text=texts['button'],
                                      command=lambda: self.toggle_device(device, status_label, toggle_button))
        toggle_button.pack(side="right", padx=10)

    def toggle_device(self, device, status_label, toggle_button):
        device.toggle()

        texts = self.get_label_and_button_text(device)

        status_label.configure(text=texts["label"])
        toggle_button.configure(text=texts["button"])

    @staticmethod
    def get_label_and_button_text(device):
        label_text = f"{device.name} is {'active' if device.is_working() else 'not active'}"
        button_text = f"Turn {'off' if device.is_working() else 'on'}"

        return {"label": label_text, "button": button_text}


guirlande_outlet = Device(
    "Guirlande Outlet",
    constants.DEV_ID,
    constants.SMART_OUTLET["ADDRESS"],
    constants.SMART_OUTLET["KEY"]
)

DEVICES = [
    guirlande_outlet,
]

if __name__ == "__main__":
    app = StatusApp(DEVICES)
    app.mainloop()
