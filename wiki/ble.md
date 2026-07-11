# BLE Protocol & Wireless Communication Interface

## 1. Environment Broadcast Target
- **Target System MAC Address:** `F4:4E:FC:44:84:FF`
- **Status:** CONFIRMED
- **Evidence Reference:** `[E003]` (Plain-text verification sequences from developer trace arrays).

## 2. Mapped BLE Service Mappings

| Service UUID | Characteristic UUID | Operational Properties | Intended System Mapping Usage |
| :--- | :--- | :--- | :--- |
| `00001800-0000-1000-8000-00805f9b34fb` | `00002a00-0000-1000-8000-00805f9b34fb` | Read | Transmits the static ASCII device profile name string down to client radios. |
| `00001801-0000-1000-8000-00805f9b34fb` | `00002a05-0000-1000-8000-00805f9b34fb` | Indicate | Triggers background state change alerts when internal firmware tables shift. |

## 3. Outstanding Wireless Questions Matrix
- What specific characteristic UUID handles incoming SDFS update files during active over-the-air firmware flashes?
- What are the exact structural hex patterns used for Bluetooth connection commands to initiate handshakes, verify encryption states, and request sync information?
- Does the device enforce hardware pairing limits or require secure bonding protocols before accepting raw binary configuration updates over Bluetooth?