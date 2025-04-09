"""
This is a Python script for automating the simulation process using QuestaSim.
If you don't know much about Python, read the comments (lines starting with #)
to learn where to change things.

How to use:
  Save this file as sim.py.
  Open a terminal and run:
      python sim.py simulate
  Other commands:
      simulate_gui  : Run simulation in GUI mode.
      view_wave     : Open the generated waveform.
      clean         : Remove generated simulation files.
      help          : Show this help message.
"""

import os            # Used for file and directory operations.
import subprocess    # Used to run external commands.
import sys           # Used for command-line arguments.
import shutil        # Used for removing directories.

# ========================================
# SECTION: Configuration Variables
# ========================================

# Set the source directory where your Verilog files are located.
# Change this path if your Verilog files are somewhere else.
SRC_DIR = "../src"

# Set the simulation directory where temporary simulation files will be stored.
# Change this path if you want simulation files to be stored in a different location.
SIM_DIR = "../sim"

# List the Verilog files you want to compile.
# Modify this list to include additional or different source files.
VERILOG_FILES = [
    os.path.join(SRC_DIR, "d1_design.v"),
    os.path.join(SRC_DIR, "d1_test.v")
]

# Define the top-level module for simulation.
# Change TOP_MODULE if your top module is named differently.
TOP_MODULE = "d1_test"

# Define options for vsim.
# If you need to change or remove options, modify this list.
VSIM_OPTIONS = ["-vopt", "-voptargs=+acc"]

# ========================================
# SECTION: Utility Functions
# ========================================

def ensure_dirs():
    """
    Create required directories if they do not exist.
    Change directory names here if needed.
    """
    if not os.path.exists("../quartus"):
        os.makedirs("../quartus")
    if not os.path.exists(SIM_DIR):
        os.makedirs(SIM_DIR)

def run_command(cmd):
    """
    Runs an external command.
    If you want to add logging or change how commands are run, modify this function.
    """
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)

# ========================================
# SECTION: Simulation Commands
# ========================================

def simulate():
    """
    Run the simulation in batch mode (non-interactive).
    Change the commands inside if you want to alter the simulation flow.
    """
    ensure_dirs()  # Make sure necessary directories exist.
    
    # Create the simulation library.
    run_command(["vlib", SIM_DIR])
    
    # Compile the Verilog files.
    run_command(["vlog", "-work", SIM_DIR] + VERILOG_FILES)
    
    # Build the vsim command.
    cmd = [
        "vsim"
    ] + VSIM_OPTIONS + [
        "-c",                           # Run in command-line (batch) mode.
        "-do", "log -r /* ; run -all; quit",  # Commands: log all signals recursively, run simulation, then quit.
        TOP_MODULE,                     # Top-level module to simulate.
        "-work", SIM_DIR,               # Specify the simulation library location.
        "-l", os.path.join(SIM_DIR, "simulation.log"),  # Log file path.
        "-wlf", os.path.join(SIM_DIR, "waveform.wlf")     # Waveform file path.
    ]
    run_command(cmd)

def simulate_gui():
    """
    Run the simulation in GUI mode for interactive debugging.
    Modify the vsim command if you need additional GUI options.
    """
    ensure_dirs()
    run_command(["vlib", SIM_DIR])
    run_command(["vlog", "-work", SIM_DIR] + VERILOG_FILES)
    cmd = [
        "vsim"
    ] + VSIM_OPTIONS + [
        "-do", "log -r /*",  # Start logging recursively.
        TOP_MODULE,
        "-work", SIM_DIR
    ]
    run_command(cmd)

def view_wave():
    """
    Open the waveform viewer to inspect the simulation results.
    Change the command if your waveform viewer is different.
    """
    run_command(["vsim", "-view", os.path.join(SIM_DIR, "waveform.wlf")])

def clean():
    """
    Clean the simulation directory by removing all generated files.
    Modify this function if you want to clean additional directories.
    """
    shutil.rmtree(SIM_DIR, ignore_errors=True)
    print("Cleaned simulation directory.")

def print_help():
    """
    Print help information about how to use this script.
    """
    help_text = """
Usage: python sim.py [command]

Commands:
  simulate       : Run simulation in batch mode.
  simulate_gui   : Run simulation in GUI mode.
  view_wave      : View the generated waveform.
  clean          : Clean the simulation directory.
  help           : Display this help message.
"""
    print(help_text)

# ========================================
# SECTION: Main Execution Block
# ========================================

if __name__ == "__main__":
    # If no command is provided, show help.
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    
    # Get the command from command-line arguments.
    cmd = sys.argv[1]
    
    # Execute the corresponding function.
    if cmd == "simulate":
        simulate()
    elif cmd == "simulate_gui":
        simulate_gui()
    elif cmd == "view_wave":
        view_wave()
    elif cmd == "clean":
        clean()
    elif cmd == "help":
        print_help()
    else:
        print("Unknown command:", cmd)
        print_help()

