# Logging Info Meaning

Feature | Description
--- | ---|
mPci| base station identifier
mRegistered | Is device registered to corresponding base station
mTac | Area code
mMcc | Mobile Country Code - Country identifier
mMnc | Mobile Network Code - mobile network identifier
mEarFCN | Unique identifier for the LTE band and carrier frequency
ss | signal strength 
RSRP| Reference Signal Received Power - power of the LTE signals over the full bandwidth and narrow band
RSRQ| Reference Signal Received Quality - 
RSSNR | signal to noise
cqi | channel quality indicator
ta | length of time a signal takes to reach the base station from a mobile phone

# Resources
RSRP and RSRQ:
https://wiki.teltonika-networks.com/view/RSRP_and_RSRQ

# Directory Info
| Directory      | Description |
| ----------- | ----------- |
| datasets      | Newly Collected this Quarter      |
| original | from starter code |
| processed   | from starter code       |
| testingProcess | from starter code|

# Test Heuristic Based Approach
```
python3 test.py
```