#!/usr/bin/env python

import sys
import re

line_counter = 0
onstage_id=None

# [modules/UI/videolayout/LargeVideoManager.js] <>:  hover in %s 8189ee8b
onstage_pattern = re.compile(".*LargeVideoManager.js] <>:  hover in %s (.*)")

# [modules/connectivity/ParticipantConnectionStatus.js] <e.value>: Figure out conn status for cf16f893, is video muted: true is active(jvb): true video track frozen: false p2p mode: false is in last N: true currentStatus => newStatus: active => active
status_pattern = re.compile(".*Figure out conn status for (.*), is video muted: (true|false) is active\\(jvb\\): true video track frozen: (true|false) p2p mode: (true|false) is in last N: (true|false).*")

# [modules/RTC/BridgeChannel.js] <e.value>:  sending selected changed notification to the bridge for endpoints f15f7b75
selected_pattern = re.compile(".*sending selected changed notification to the bridge for endpoints (.*)")

for line in sys.stdin:
    line_counter = line_counter + 1
    onstage_match = onstage_pattern.match(line)
    if onstage_match:
        onstage_id = onstage_match.group(1)
        continue

    selected_match = selected_pattern.match(line)
    if selected_match:
        selected_id = selected_match.group(1)
        continue

    status_match = status_pattern.match(line)
    if status_match:
        participant_id = status_match.group(1)
        if participant_id == onstage_id:
            in_lastn = status_match.group(5)
            if in_lastn == 'false':
                print("%r,%r,%r,%r,%r" % (onstage_id, selected_id, participant_id, in_lastn, line_counter))
        continue
