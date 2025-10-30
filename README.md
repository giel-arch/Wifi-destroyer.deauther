# WiFi Deauther

A Python-powered graphical user interface for WiFi network analysis and deauthentication attacks.

## ⚠️ Disclaimer

This tool is for educational and testing purposes only. Unauthorized access to computer networks is illegal. Use this tool only on networks you own or have explicit permission to test. The developers are not responsible for any misuse or illegal activities conducted with this tool.

## 📋 Requirements

### System Requirements
- Linux operating system (tested on Ubuntu, Kali Linux, and Arch Linux)
- Python 3.6 or higher
- Root privileges (required for packet injection and monitor mode)

### Python Dependencies
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Required Packages
```bash
sudo apt install aircrack-ng
sudo apt install python3-tk
sudo apt install python3-pil
```

### Hardware Requirements
- WiFi adapter that supports monitor mode and packet injection
- Recommended adapters:
  - Alfa AWUS036H
  - Alfa AWUS036ACH
  - TP-Link TL-WN722N
  - Atheros AR9271 based adapters

## 🚀 Installation

1. Clone or download the script:
```bash
git clone <repository-url>
cd Wifi-destroyer.deauther
```

2. Make the script executable:
```bash
chmod +x deauth1.py
```

3. Install dependencies:
```bash
sudo apt install python3-tk python3-pil aircrack-ng
```

4. Run the script:
```bash
sudo python3 deauth1.py
```

## 📖 Usage

### Main Interface

#### 1. Interface Selection
- Click "Refresh Interfaces" to detect available WiFi interfaces
- Select an interface from the dropdown menu
- Click "Select Interface" to activate the selected interface

#### 2. Channel Selection
- Use the spinbox to select a channel (1-14)
- Click "Set Channel" to change the current channel

#### 3. Monitor Mode
- Click "Start Monitor Mode" to enable monitor mode on the selected interface
- Click "Stop Monitor Mode" to disable monitor mode

### Scan Tab

#### 1. Scan Options
- Choose between "Current Channel Only" or "All Channels"
- Click "Start Scan" to begin scanning for networks
- Click "Stop Scan" to stop the scanning process

#### 2. Scan Results
- View discovered networks in the table
- Columns: Network Name (ESSID), BSSID, Channel, Power
- Click "Select Target" to select a network for deauthentication
- Click "Clear Results" to clear the scan results

### Attack Tab

#### 1. Target Information
- View information about the selected target network
- Shows ESSID, BSSID, and Channel

#### 2. Attack Options
- Set the packet count (1-100) for the deauth attack
- Click "Start Attack" to begin the deauthentication attack
- Click "Stop Attack" to stop the attack

#### 3. Attack Log
- View real-time logs of the attack progress
- Shows timestamps and command outputs

### Tools Tab

#### 1. Interface Troubleshooter
- Click "Interface Troubleshooter" to diagnose interface issues
- Checks rfkill status, kernel messages, loaded modules, and service status
- Automatically unblocks rfkill devices

#### 2. Terminal
- Built-in terminal for running custom commands
- Type commands in the input field and click "Run Command"
- Click "Clear Terminal" to clear the terminal output

## 🔧 Troubleshooting

### Common Issues

#### 1. No WiFi Interfaces Found
- Ensure your WiFi adapter is properly connected
- Run `sudo rfkill unblock all` to unblock all wireless devices
- Try replugging your WiFi adapter
- Check if the required drivers are installed

#### 2. Monitor Mode Failed to Start
- Ensure NetworkManager and wpa_supplicant are stopped
- Run `sudo airmon-ng check kill` to kill interfering processes
- Try restarting your system
- Check if your adapter supports monitor mode

#### 3. Scan Returns No Results
- Ensure you're on the correct channel
- Try increasing the scan duration
- Check if your adapter is in monitor mode
- Move closer to the target networks

#### 4. Deauth Attack Fails
- Ensure you're on the same channel as the target network
- Check if your adapter supports packet injection
- Try increasing the packet count
- Ensure you have the correct target BSSID

### Getting Help

If you encounter issues:
1. Check the terminal output in the Tools tab for error messages
2. Run the Interface Troubleshooter to diagnose problems
3. Ensure all requirements are properly installed
4. Check online forums for common WiFi adapter issues

## 📚 Advanced Usage

### Command Line Arguments
The GUI can be launched with optional arguments:
```bash
sudo python3 deauth1.py [--help] [--version]
```

### Customizing the GUI
- Colors and styles can be modified in the Python script
- Additional features can be added by extending the WiFiDestroyerGUI class
- The terminal can be used to run custom commands and scripts

### Scripting and Automation
- The built-in terminal can be used to run custom scripts
- Commands can be automated using the command input field
- Output can be logged and analyzed for troubleshooting

## 🛡️ Security Considerations

### Legal and Ethical Use
- Only use this tool on networks you own or have explicit permission to test
- Respect all applicable laws and regulations
- Use responsibly and ethically

### Best Practices
- Always stop monitor mode when not in use
- Restart NetworkManager and wpa_supplicant after using the tool
- Keep your system and tools updated
- Use in a controlled environment for testing

### Privacy
- The tool does not collect or transmit any personal data
- All operations are performed locally on your system
- Scan results and logs are stored locally and can be cleared

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex functionality
- Include docstrings for functions and classes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Aircrack-ng for the powerful WiFi security tools
- Python and Tkinter for the GUI framework
- The open-source community for inspiration and feedback

## 📞 Support

For support, questions, or feature requests:
1. Check the troubleshooting section in this README
2. Search existing issues in the repository
3. Create a new issue with detailed information
4. Join our community discussions

---

**Remember: With great power comes great responsibility. Use this tool wisely and ethically.**
