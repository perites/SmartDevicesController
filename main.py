import tinytuya
import customtkinter as ctk

import constants
import logging
import sys

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] : %(message)s  ||[LOGGER:%(name)s] [FUNC:%(funcName)s] [FILE:%(filename)s]',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("main.log", mode='a', encoding='utf-8', )
    ]
)
logging.getLogger("tinytuya.core").setLevel(logging.ERROR)


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
        logging.info(f"Device {self.name} turned on")

    def turn_off(self):
        self.device.turn_off()
        logging.info(f"Device {self.name} turned off")

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
        logging.debug("Button pressed")
        device.toggle()

        texts = self.get_label_and_button_text(device)

        status_label.configure(text=texts["label"])
        toggle_button.configure(text=texts["button"])

    @staticmethod
    def get_label_and_button_text(device):
        label_text = f"{device.name} is {'active' if device.is_working() else 'not active'}"
        button_text = f"Turn {'off' if device.is_working() else 'on'}"

        return {"label": label_text, "button": button_text}


logging.debug("Creating devices")
guirlande_outlet = Device(
    "Guirlande Outlet",
    constants.DEV_ID,
    constants.SMART_OUTLET["ADDRESS"],
    constants.SMART_OUTLET["KEY"]
)

DEVICES = [
    guirlande_outlet,
]
logging.info(f"Succsesfully created {len(DEVICES)} devices")

if __name__ == "__main__":
    logging.info("Starting mainloop")
    try:
        app = StatusApp(DEVICES)
        app.mainloop()
    except Exception as e:
        logging.exception("Expedition occurred while in mainloop")
        input("Press Enter to exit")
