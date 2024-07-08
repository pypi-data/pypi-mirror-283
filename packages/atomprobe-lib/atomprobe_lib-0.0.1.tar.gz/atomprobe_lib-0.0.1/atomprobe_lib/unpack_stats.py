import struct

LEN_TOTAL_PEAK_RATIOS = 10  # Not sure what the actual length is, but this is the max that fits the bytes that I received.

def unpack_event_stats(data, offset):
    event_stats_format = 'QIdIdd'
    event_stats_size = struct.calcsize(event_stats_format)
    event_stats_data = struct.unpack_from(event_stats_format, data, offset)
    event_stats = {
        "qwPulses": event_stats_data[0],
        "dwTotalEvents": event_stats_data[1],
        #"dwUnused1": event_stats_data[2], - ignored, uncomment if read needed
        "dEventRate": event_stats_data[2],
        "dwTotalIons": event_stats_data[3],
        #"dwUnused2": event_stats_data[5], - ignored, uncomment if read needed
        "dGoldenPercent": event_stats_data[4],
        "dMultiplePercent": event_stats_data[5]
    }
    return event_stats, offset + event_stats_size

def unpack_acq_hvs(data, offset):
    acq_hvs_format = 'dddddd'
    acq_hvs_size = struct.calcsize(acq_hvs_format)
    acq_hvs_data = struct.unpack_from(acq_hvs_format, data, offset)
    acq_hvs = {
        "dSpecimen": acq_hvs_data[0],
        "dReflectron": acq_hvs_data[1],
        "dAccel2": acq_hvs_data[2],
        "dBias": acq_hvs_data[3],
        "dMcpBack": acq_hvs_data[4],
        "dPulseAmp": acq_hvs_data[5]
    }
    return acq_hvs, offset + acq_hvs_size

def unpack_davis_acq_stats(data):
    offset = 0

    # Unpack first line
    davis_acq_format = 'd'
    davis_acq_size = struct.calcsize(davis_acq_format)
    dElapsedTimeSec = struct.unpack_from(davis_acq_format, data, offset)[0]
    offset += davis_acq_size

    # Unpack the EVENT_STATS structure
    event_stats, offset = unpack_event_stats(data, offset)

    # Unpack the ACQ_HVS structure
    acq_hvs, offset = unpack_acq_hvs(data, offset)

    # Unpack the dPeakRatios array
    dPeakRatios_format = 'd' * LEN_TOTAL_PEAK_RATIOS
    dPeakRatios_size = struct.calcsize(dPeakRatios_format)
    dPeakRatios = struct.unpack_from(dPeakRatios_format, data, offset)
    offset += dPeakRatios_size

    # Unpack the remaining fields
    remaining_format = 'd' * 12
    remaining_size = struct.calcsize(remaining_format)
    remaining_data = struct.unpack_from(remaining_format, data, offset)
    offset += remaining_size

    remaining_fields = [
        "dBackground", "dLaserPosX", "dLaserPosY", "dLaserPosZ",
        "dAmbientTemp", "dSpecimenPosX", "dSpecimenPosY", "dSpecimenPosZ",
        "dLinearFov", "dSpecimenTemp", "dAnalysisPressure", "dPulseRate"
    ]

    davis_acq_stats = {
        "dElapsedTimeSec": dElapsedTimeSec,
        "sEventStats": event_stats,
        "sHvs": acq_hvs,
        "dPeakRatios": dPeakRatios,
    }

    for i, field in enumerate(remaining_fields):
        davis_acq_stats[field] = remaining_data[i]

    return davis_acq_stats

def start(binary_data):
    return_string = ''''''
    davis_acq_stats = unpack_davis_acq_stats(binary_data)
    for key, value in davis_acq_stats.items():
        if isinstance(value, dict):
            return_string += f"{key}:\n"
            for sub_key, sub_value in value.items():
                return_string += f"\t{sub_key}: {sub_value}\n"
        elif isinstance(value, (list, tuple)):
            return_string += f"{key}:\n"
            for i, sub_value in enumerate(value):
                return_string += f"\t{key}[{i}]: {sub_value}\n"
        else:
            return_string += f"{key}: {value}\n"

    return return_string

if __name__ == "__main__":
    res = start(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x91C\x11@\x00\x00\x00`>X\x19@\x00\x00\x00\xa08\xb8\x08\xc0\x00\x00\x00 r\xa8\xfa?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\xbf\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00j\x08A')
    print(res)
