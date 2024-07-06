import multiprocessing
import time
import panel as pn

# Initialize Panel extension
pn.extension()

class LongRunningProcess:
    def __init__(self):
        self.stop_event = multiprocessing.Event()
        self.process = None

    # Long-running process
    def long_running_process(self, stop_event):
        count = 0
        while not stop_event.is_set():
            print(f"Processing {count}")
            count += 1
            time.sleep(1)  # Simulate long process
        print("Process stopped")
        print("Process completed")

    # Function to start the long-running process
    def start_process(self):
        self.stop_event.clear()
        self.process = multiprocessing.Process(target=self.long_running_process, args=(self.stop_event,))
        self.process.start()

    # Function to stop the long-running process
    def stop_process(self):
        self.stop_event.set()
        self.process.join()

class LongRunningProcessUI:
    def __init__(self, process):
        self.process = process
        
        # Create start and stop buttons
        self.start_button = pn.widgets.Button(name='Start Process')
        self.stop_button = pn.widgets.Button(name='Stop Process')

        # Assign functions to button click events
        self.start_button.on_click(self.start_process)
        self.stop_button.on_click(self.stop_process)

    # Function to start the process
    def start_process(self, event):
        self.process.start_process()

    # Function to stop the process
    def stop_process(self, event):
        self.process.stop_process()

    # Method to get the Panel layout
    def get_layout(self):
        return pn.Column(self.start_button, self.stop_button)

# Create an instance of the LongRunningProcess
long_running_process = LongRunningProcess()

# Create an instance of the LongRunningProcessUI with the process instance
long_running_process_ui = LongRunningProcessUI(long_running_process)

# Display the buttons in a Panel layout
long_running_process_ui.get_layout().servable()
