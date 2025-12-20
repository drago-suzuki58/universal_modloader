import datetime
import hashlib
import tkinter as tk
import uuid


class PyToolsApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("PyTool - Demo App")
        self.root.geometry("780x520")
        self.root.resizable(False, False)

        self._build_layout()

    def _build_layout(self) -> None:
        self.main_frame = tk.Frame(self.root, padx=12, pady=12)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.main_frame.grid_columnconfigure(0, weight=1, uniform="half")
        self.main_frame.grid_columnconfigure(1, weight=1, uniform="half")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self._build_text_analyzer()
        self._build_hash_generator()
        self._build_epoch_converter()
        self._build_uuid_generator()

    def _build_text_analyzer(self) -> None:
        frame = tk.LabelFrame(self.main_frame, text="Text Analyzer", padx=10, pady=10)
        frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        self.text_input = tk.Text(frame, height=10, width=40, wrap=tk.WORD)
        self.text_input.pack(fill=tk.BOTH, expand=True)

        action_frame = tk.Frame(frame)
        action_frame.pack(fill=tk.X, pady=(8, 0))

        analyze_button = tk.Button(
            action_frame, text="Analyze", command=self._analyze_text
        )
        analyze_button.pack(side=tk.LEFT)

        clear_button = tk.Button(
            action_frame,
            text="Clear",
            command=lambda: self._clear_text(self.text_input),
        )
        clear_button.pack(side=tk.LEFT, padx=(8, 0))

        self.text_result = tk.Label(
            frame, text="Characters: 0 | Words: 0 | Lines: 0", anchor="w"
        )
        self.text_result.pack(fill=tk.X, pady=(8, 0))

    def _build_hash_generator(self) -> None:
        frame = tk.LabelFrame(self.main_frame, text="Hash Gen", padx=10, pady=10)
        frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

        self.hash_input = tk.Text(frame, height=10, width=40, wrap=tk.WORD)
        self.hash_input.pack(fill=tk.BOTH, expand=True)

        generate_button = tk.Button(
            frame, text="Generate Hashes", command=self._generate_hashes
        )
        generate_button.pack(pady=(8, 0))

        self.md5_label = tk.Label(frame, text="MD5: -", anchor="w", justify=tk.LEFT)
        self.md5_label.pack(fill=tk.X, pady=(8, 0))

        self.sha_label = tk.Label(frame, text="SHA256: -", anchor="w", justify=tk.LEFT)
        self.sha_label.pack(fill=tk.X, pady=(4, 0))

    def _build_epoch_converter(self) -> None:
        frame = tk.LabelFrame(self.main_frame, text="Epoch Converter", padx=10, pady=10)
        frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)

        epoch_label = tk.Label(frame, text="Epoch Seconds:")
        epoch_label.pack(anchor="w")
        self.epoch_entry = tk.Entry(frame)
        self.epoch_entry.pack(fill=tk.X)

        datetime_label = tk.Label(frame, text="Datetime (UTC, YYYY-MM-DD HH:MM:SS):")
        datetime_label.pack(anchor="w", pady=(8, 0))
        self.datetime_entry = tk.Entry(frame)
        self.datetime_entry.pack(fill=tk.X)

        buttons_frame = tk.Frame(frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))

        to_datetime_button = tk.Button(
            buttons_frame, text="Epoch To Datetime", command=self._epoch_to_datetime
        )
        to_datetime_button.pack(side=tk.LEFT)

        to_epoch_button = tk.Button(
            buttons_frame, text="Datetime To Epoch", command=self._datetime_to_epoch
        )
        to_epoch_button.pack(side=tk.LEFT, padx=(8, 0))

        self.epoch_status = tk.Label(frame, text="Awaiting conversion...", anchor="w")
        self.epoch_status.pack(fill=tk.X, pady=(10, 0))

    def _build_uuid_generator(self) -> None:
        frame = tk.LabelFrame(self.main_frame, text="UUID Gen", padx=10, pady=10)
        frame.grid(row=1, column=1, sticky="nsew", padx=8, pady=8)

        description = tk.Label(
            frame,
            text="Press the button to get a UUID v4.\nIt will be copied to the clipboard.",
        )
        description.pack(anchor="w")

        generate_button = tk.Button(
            frame, text="Generate UUID", command=self._generate_uuid
        )
        generate_button.pack(pady=(10, 0))

        self.uuid_value = tk.Label(
            frame,
            text="-",
            font=("Courier", 12),
            anchor="w",
            justify=tk.LEFT,
            wraplength=320,
        )
        self.uuid_value.pack(fill=tk.X, pady=(10, 0))

        self.uuid_status = tk.Label(frame, text="Nothing generated yet.", anchor="w")
        self.uuid_status.pack(fill=tk.X, pady=(6, 0))

    def _analyze_text(self) -> None:
        raw_text = self.text_input.get("1.0", tk.END)
        cleaned_text = raw_text.rstrip("\n")
        characters = len(cleaned_text)
        words = len(cleaned_text.split())
        lines = cleaned_text.count("\n") + 1 if cleaned_text else 0
        self.text_result.config(
            text=f"Characters: {characters} | Words: {words} | Lines: {lines}"
        )

    def _clear_text(self, widget: tk.Text) -> None:
        widget.delete("1.0", tk.END)
        self.text_result.config(text="Characters: 0 | Words: 0 | Lines: 0")

    def _generate_hashes(self) -> None:
        content = self.hash_input.get("1.0", tk.END).rstrip("\n")
        if not content:
            self.md5_label.config(text="MD5: (enter text first)")
            self.sha_label.config(text="SHA256: (enter text first)")
            return

        md5_value = hashlib.md5(content.encode("utf-8")).hexdigest()
        sha_value = hashlib.sha256(content.encode("utf-8")).hexdigest()

        self.md5_label.config(text=f"MD5: {md5_value}")
        self.sha_label.config(text=f"SHA256: {sha_value}")

    def _epoch_to_datetime(self) -> None:
        raw_value = self.epoch_entry.get().strip()
        if not raw_value:
            self.epoch_status.config(text="Please provide an epoch value.")
            return
        try:
            epoch_value = float(raw_value)
            dt = datetime.datetime.fromtimestamp(epoch_value, tz=datetime.timezone.utc)
            formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
            self.datetime_entry.delete(0, tk.END)
            self.datetime_entry.insert(0, formatted)
            self.epoch_status.config(text="Converted epoch to UTC datetime.")
        except (ValueError, OSError):
            self.epoch_status.config(text="Invalid epoch value.")

    def _datetime_to_epoch(self) -> None:
        raw_value = self.datetime_entry.get().strip()
        if not raw_value:
            self.epoch_status.config(text="Please provide a datetime value.")
            return
        try:
            dt = datetime.datetime.strptime(raw_value, "%Y-%m-%d %H:%M:%S")
            dt = dt.replace(tzinfo=datetime.timezone.utc)
            epoch_value = int(dt.timestamp())
            self.epoch_entry.delete(0, tk.END)
            self.epoch_entry.insert(0, str(epoch_value))
            self.epoch_status.config(text="Converted datetime to epoch.")
        except ValueError:
            self.epoch_status.config(text="Invalid datetime format.")

    def _generate_uuid(self) -> None:
        new_uuid = str(uuid.uuid4())
        self.uuid_value.config(text=new_uuid)
        self.root.clipboard_clear()
        self.root.clipboard_append(new_uuid)
        self.uuid_status.config(text="UUID copied to clipboard.")

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = PyToolsApp()
    app.run()
