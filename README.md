# CamBurglar: Detection of Hidden Wi-Fi Cameras

## How to run our code:
1. After cloning the repository and cd-ing inside, run 'python3 app.py' in Terminal.
2. Navigate to http://127.0.0.1:5001/ in your browser.
3. Enter the length and width of the room you wish to scan and click submit.
4. Starting from a lefthand corner of the room (we will consider this (0,0)), walk along each wall of the room for 10 seconds.
5. After you have returned to the original corner, wait for results!

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
