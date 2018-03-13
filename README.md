# CamBurglar: Detection of Hidden Wi-Fi Cameras

## Phase 1: Traffic Analysis
- Capture packet information using tshark 
- Analyze traffic for suspicious activity
- Look for small, constant stream of sent packets
- Return mac addr and rssi of suspicious device(s)

## Phase 2: RF Localization
- Gather (x,y) data for a room ahead of time
- Use sniffer to capture rssi and mac addr at each meter
- Filter by known mac addr of suspicious devices obtained from traffic analysis
- Localize using LDPL model given a mac addr 
- Return (x,y) coordinates of suspicious devices
- Plot map of room with localized (x,y) of camera

## Phase 3: Magnetic Confirmation
- Navigate to predicted (x,y) position in room
- Use magnetometer readings to check whether there is a camera or streaming device
