from pathlib import Path
from datetime import datetime

import numpy as np
import xarray as xr

from cadati.np_date import dt2jd

int8_nan_min = np.int8(-2**7)
int8_nan_max = np.int8(2**7 - 1)
int16_nan_min = np.int16(-2**15)
int16_nan_max = np.int16(2**15 - 1)
int32_nan_min = np.int32(-2**31)
int32_nan_max = np.int32(2**31 - 1)
uint8_nan_min = np.uint8(0)
uint8_nan_max = np.uint8(2**8 - 1)
uint16_nan_min = np.uint16(0)
uint16_nan_max = np.uint16(2**16 - 1)
uint32_nan_min = np.uint32(0)
uint32_nan_max = np.uint32(2**32 - 1)
float32_nan = np.int32(-2**31)
float64_nan = np.int32(-2**31)
dt_nan = np.datetime64("1970-01-01")

nan_dict = {
    "int8": int8_nan_min,
    np.dtype("int8"): int8_nan_min,
    np.dtype("int8").str: int8_nan_min,
    "uint8": uint8_nan_max,
    np.dtype("uint8"): uint8_nan_max,
    np.dtype("uint8").str: uint8_nan_max,
    "int16": int16_nan_min,
    np.dtype("int16"): int16_nan_min,
    np.dtype("int16").str: int16_nan_min,
    "uint16": uint16_nan_max,
    np.dtype("uint8"): uint16_nan_max,
    np.dtype("uint8").str: uint16_nan_max,
    "int32": int32_nan_min,
    np.dtype("int32"): int32_nan_min,
    np.dtype("int32").str: int32_nan_min,
    "uint32": uint32_nan_max,
    np.dtype("uint32"): uint32_nan_max,
    np.dtype("uint32").str: uint32_nan_max,
    "float32": float32_nan,
    np.dtype("float32"): float32_nan,
    np.dtype("float32").str: float32_nan,
    "float64": float64_nan,
    np.dtype("float64"): float64_nan,
    np.dtype("float64").str: float64_nan,
    "dt": dt_nan,
    np.dtype("<M8[ms]"): dt_nan,
    np.dtype("<M8[ms]").str: dt_nan,
}


def get_bit(a, bit_pos):
    """
    Returns 1 or 0 if bit is set or not.

    Parameters
    ----------
    a : int or numpy.ndarray
      Input array.
    bit_pos : int
      Bit position. First bit position is right.

    Returns
    -------
    b : numpy.ndarray
      1 if bit is set and 0 if not.
    """
    return np.clip(np.bitwise_and(a, 2**(bit_pos - 1)), 0, 1)


def mph_dtype():
    """
    ASPS Product Format 2.0 - Main Product Header

    Document: ERSE-GSEV-EOPG-RS-06-0002
    Table C: Main Product Header Detailed Description for all products
    """
    template = np.dtype([
        ("orig", np.dtype("S1")),
        ("orbit_nr", ">u4"),
        ("uniq_id", ">u1", 12),
        ("product_type", ">u1"),  # Type of product (Table B)
        ("spacecraft", ">u1"),  # 1: ERS-1, 2: ERS-2
        ("utc_time", np.dtype("S24")
         ),  # UTC time of subsatellite point at beginning of product
        ("station_id", ">u1"),  # Station ID, where data was processed
        ("product_conf_data", ">u2"),  # Product Confidence Data
        ("utc_generation", np.dtype("S24")),  # UTC time when MPH was generated
        ("sph_size",
         ">u4"),  # Size of Specific Product Header: Record in Bytes
        ("pdr_num", ">u4"),  # Number of Product Data Set Records
        ("pdr_size", ">u4"),  # Size of each Product Data Set Record in Bytes
        ("subsys", ">u1"),  # Subsystem that generated the product
        ("obrc_flg", ">u1"),  # OBRC flag used for SAR products only
        ("utc_reftime", np.dtype("S24")),  # UTC reference time.
        ("clock", ">u4", 2),  # Reference binary time of satellite clock
        ("software_version", ">u1",
         8),  # Processor software version used to generate product
        ("thr_table", ">u2"),  # Threshold table version number
        ("spare", ">u2"),  # Spare
        ("utc_asc_node",
         np.dtype("S24")),  # UTC time of ascending node state vector
        ("state_vector", ">u4", 6
         )  # Ascending node state vector in earth-fixed reference system
    ])

    return template


def sph_dtype():
    """
    ASPS Product Format 2.0 - Specific Product Header

    Document: ERSE-GSEV-EOPG-RS-06-0002
    Table 4: ASPS Level 2.0 Specific Product Header format
    """
    template = np.dtype([
        ("prod_desc", ">u1"),  # Product Description
        ("abs_orbit_nr", ">u4"),  # Absolute Orbit Number
        ("sig0_valid_n3", ">u2"),  # Number of nodes with 3 valid sigma noughts
        ("sig0_valid_n2", ">u2"),  # Number of nodes with 2 valid sigma noughts
        ("sig0_valid_n1", ">u2"),  # Number of nodes with 1 valid sigma noughts
        ("n_land_flag", ">u2"),  # Total number of nodes with Land Flag
        ("n_ice_flag", ">u2"),  # Total number of nodes with Ice Flag
        ("n_arc_flag", ">u2"),  # Total number of nodes with arcing flag set
        ("n_kp_flag", ">u2"),  # Total number of nodes with Kp flag set
        ("n_cksum_error_flag",
         ">u2"),  # Total Number of nodes with frame checksum error flag set
        ("n_noise_power_flag",
         ">u2"),  # Total number of nodes with Noise Power flag set
        ("n_int_calib_flag",
         ">u2"),  # Total number of nodes with Internal Calibration flag set
        ("n_dopp_comp_flag", ">u2"
         ),  # Total number of nodes with Doppler Compensation CoG flag set
        (
            "n_dopp_comp_std", ">u2"
        ),  # Total number of nodes with Doppler Compensation “standard deviation” flag set
        ("n_dopp_shift_flag",
         ">u2"),  # Total number of nodes with Doppler Shift flag set
        ("n_yaw_angle_flag",
         ">u2"),  # Total number of nodes with Yaw angle flag set
        ("n_wind_nodes", ">u2"),  # Total number of wind nodes
        ("n_lo_wind", ">u2"),  # Total number of low wind nodes
        ("n_hi_wind", ">u2"),  # Total number of high wind nodes
        ("n_mod_flag", ">u2"
         ),  # Total number of nodes with distance from C-BAND Model flag set
        ("n_wind_speed_bias_flag",
         ">u2"),  # Total number of nodes with wind speed bias flag set
        ("n_wind_dir_bias_flag",
         ">u2"),  # Total number of nodes with wind direction bias flag set
        ("mean_wind_speed_bias", ">u2"),  # Mean Wind Speed Bias 
        ("wind_speed_std", ">u2"),  # Wind speed standard deviation
        ("mean_wind_dir_bias", ">u2"),  # Mean Wind Direction Bias
        ("mean_dist_model", ">u4",
         41),  # Mean Distance from C-BAND Model node 1 to 41
        ("wsp_version", ">u2"),  # WSP version
        ("wsp_conf", ">u2"),  # WSP Configuration file version number
        ("meteo_table_id1", ">u2"),  # Meteo Table ID
        ("meteo_table_id2", ">u2"),  # Meteo Table ID
        ("meteo_table_id3", ">u2"),  # Meteo Table ID
        ("meteo_table_id4", ">u2"),  # Meteo Table ID
        ("meteo_table_type",
         ">u4"),  # Type of meteo table used in the processing:
        ("spare", ">u4", 2),  # Spare
    ])

    return template


def ds_header_dtype():
    """
    ASPS Product Format 2.0 - ASPS Level 2.0 Data Set Record
    (nominal or high resolution)

    Document: ERSE-GSEV-EOPG-RS-06-0002
    Table 5:  DSRHDR (Data Set Record Header)
    """
    template = np.dtype([
        ("rec_num", ">i4"),  # Data Record number, starting with 1
        ("utc_time",
         np.dtype("S24")),  # Mid beam acquisition time (UTC) node 10
        ("azi", ">i4"),  # Subsatellite Track Heading w.r. to North
    ])

    return template


def ds_dtype():
    """
    ASPS Product Format 2.0 - ASPS Level 2.0 Data Set Record
    (nominal or high resolution)

    Document: ERSE-GSEV-EOPG-RS-06-0002
    Table 5: Node
    """
    template = np.dtype([("lat", ">i4"), ("lon", ">i4"), ("time_fore", ">u2"),
                         ("time_mid", ">u2"), ("time_aft", ">u2"),
                         ("sigma_fore", ">i4"), ("inc_fore", ">i2"),
                         ("look_angle_fore", ">i2"), ("kp_fore", ">u2"),
                         ("n_samples_fore", ">i2"), ("sigma_mid", ">i4"),
                         ("inc_mid", ">i2"), ("look_angle_mid", ">i2"),
                         ("kp_mid", ">u2"), ("n_samples_mid", ">i2"),
                         ("sigma_aft", ">i4"), ("inc_aft", ">i2"),
                         ("look_angle_aft", ">i2"), ("kp_aft", ">u2"),
                         ("n_samples_aft", ">i2"), ("wind_speed_n1", ">i2"),
                         ("wind_dir_n1", ">i2"), ("dist_n1", ">i4"),
                         ("wind_speed_n2", ">i2"), ("wind_dir_n2", ">i2"),
                         ("dist_n2", ">i4"), ("wind_speed_n3", ">i2"),
                         ("wind_dir_n3", ">i2"), ("dist_n3", ">i4"),
                         ("wind_speed_n4", ">i2"), ("wind_dir_n4", ">i2"),
                         ("dist_n4", ">i4"), ("wind_speed_bias", ">i2"),
                         ("sea_ice_prob", ">i2"), ("wind_dir_bias", ">i2"),
                         ("ncd1", ">u2"), ("ncd2", ">u2"),
                         ("geophysical_pcd", ">u1")])

    return template


def dsr_dtype(n_nodes, n_lines):
    """
    ASPS Product Format 2.0 - ASPS Level 2.0 Data Set Record
    """
    line = np.dtype([("dsr_hdr", ds_header_dtype()),
                     ("node", ds_dtype(), n_nodes)])
    template = np.dtype([("line", line, n_lines)])

    return template


def ms_dsr_array(shape):
    """
    ASPS Product Format 2.0 - ASPS Level 2.0 Data Set Record
    Masked and scaled dtype.
    """
    num_beam = 3

    template = np.dtype([
        ("latitude", "<f4"),
        ("longitude", "<f4"),
        ("time", "<M8[ns]"),
        ("jd", "<f8"),
        ("as_des_pass", "<i1"),
        ("swath_indicator", "<i1"),
        ("backscatter", "<f4", num_beam),
        ("incidence_angle", "<f4", num_beam),
        ("azimuth_angle", "<f4", num_beam),
        ("kp", "<f4", num_beam),
        ("n_echos", "<i2", num_beam),
        ("f_usable", "<i1", num_beam),
        ("f_land", "<i1"),
        ("spacecraft_id", "<i1"),
    ])

    fill_value = (
        nan_dict["float32"],
        nan_dict["float32"],
        "1970-01-01",
        nan_dict["float64"],
        nan_dict["int8"],
        nan_dict["int8"],
        (nan_dict["float32"], ) * num_beam,
        (nan_dict["float32"], ) * num_beam,
        (nan_dict["float32"], ) * num_beam,
        (nan_dict["float32"], ) * num_beam,
        (nan_dict["uint16"], ) * num_beam,
        (nan_dict["int8"], ) * num_beam,
        nan_dict["int8"],
        nan_dict["int8"],
    )

    array = np.ma.empty(shape, dtype=template)
    array[:] = fill_value
    array[:] = np.ma.masked
    array.fill_value = np.array(fill_value, dtype=template)

    return array


def read_ers_asps_level2(filename, mask_and_scale=False, return_xr=False):
    """
    Read ERS ASPS Level 2 data.

    Parameters
    ----------
    filename : str
        ASPS Level 2 file.
    mask_and_scale : bool, optional
        Mask and scale data records.
    return_xr : bool, optional
        Return xarray.Dataset instead of dict.

    Returns
    -------
    data : dict or xarray.Dataset
        Main product header, specific product header and data records.
    """
    with open(filename, "rb") as fp:
        mph = np.fromfile(fp, mph_dtype(), count=1)
        sph = np.fromfile(fp, sph_dtype(), count=1)

        bits = np.unpackbits(sph["prod_desc"])
        n_nodes = {0: 19, 1: 41}[bits[-2]]
        n_lines = mph["pdr_num"][0]

        dsr = np.fromfile(fp, dsr_dtype(n_nodes, n_lines), count=1)

    if mask_and_scale or return_xr:
        dsr = mask_and_scale_ers_asps_level2(dsr, mph)

    if return_xr:
        data = asps_level2_xr(dsr)
    else:
        data = {"mph": mph, "sph": sph, "dsr": dsr}

    return data


def mask_and_scale_ers_asps_level2(dsr, mph):
    """
    Mask and scale ERS ASPS Level 2 data.

    Parameters
    ----------
    dsr : numpy.ndarray
        Original ERS ASPS Level 2 data array.
    mph : numpy.ndarray
        Main product header.

    Returns
    -------
    arr : numpy.ndarray
        Masked and scaled ERS ASPS Level 2 data array.
    """
    arr = ms_dsr_array(dsr["line"]["node"].shape[1:])

    beams = ["fore", "mid", "aft"]

    arr["longitude"] = dsr["line"]["node"]["lon"][0] * 1e-3
    invalid = (arr["longitude"] > 360) | (arr["longitude"] < 0)
    arr["longitude"][invalid] = np.ma.masked
    # modify longitudes from (0, 360) to (-180, 180)
    arr["longitude"][arr["longitude"] > 180] -= 360.

    arr["latitude"] = dsr["line"]["node"]["lat"][0] * 1e-3
    invalid = (arr["latitude"] > 90) | (arr["latitude"] < -90)
    arr["latitude"][invalid] = np.ma.masked

    for i, beam in enumerate(beams):
        arr["backscatter"][...,
                           i] = dsr["line"]["node"][f"sigma_{beam}"][0] * 1e-7
    invalid = (arr["backscatter"] < -50) | (arr["backscatter"] > 50)
    arr["backscatter"][invalid] = np.ma.masked

    for i, beam in enumerate(beams):
        arr["incidence_angle"][
            ..., i] = dsr["line"]["node"][f"inc_{beam}"][0] * 1e-1
    invalid = (arr["incidence_angle"] < 10) | (arr["incidence_angle"] > 80)
    arr["incidence_angle"][invalid] = np.ma.masked

    for i, beam in enumerate(beams):
        arr["azimuth_angle"][
            ..., i] = dsr["line"]["node"][f"look_angle_{beam}"][0] * 1e-1
    invalid = (arr["azimuth_angle"] > 360) | (arr["azimuth_angle"] < 0)
    arr["azimuth_angle"][invalid] = np.ma.masked

    for i, beam in enumerate(beams):
        arr["kp"][..., i] = dsr["line"]["node"][f"kp_{beam}"][0] * 1e-3
    invalid = (arr["kp"] > 10) | (arr["kp"] < 0)
    arr["kp"][invalid] = np.ma.masked

    for i, beam in enumerate(beams):
        arr["n_echos"][..., i] = dsr["line"]["node"][f"n_samples_{beam}"][0]

    format_str = "%d-%b-%Y %H:%M:%S.%f"
    time = np.array([
        np.datetime64(datetime.strptime(t.decode("utf-8"), format_str))
        for t in dsr["line"]["dsr_hdr"]["utc_time"][0]
    ],
                    dtype="<M8[ns]")
    arr["time"][:, ...] = time[:, np.newaxis]
    arr["jd"] = dt2jd(arr["time"])

    arr["as_des_pass"][:, ...] = (dsr["line"]["dsr_hdr"]["azi"][0] * 1e-3
                                  > 270).astype("<i1")[:, np.newaxis]

    # ERS-1 and ERS-2 only have a right beam
    arr["swath_indicator"][:] = 1

    # Bit 1 Land-Sea Flag
    arr["f_land"] = get_bit(dsr["line"]["node"]["geophysical_pcd"][0], 1)

    # f_usable:  0, 1 or 2  indicating nominal, slightly degraded
    # or severely degraded data
    for i, beam in enumerate(beams):
        bit_sum = get_bit(dsr["line"]["node"]["ncd1"][0], i + 3)
        # bit_sum = (get_bit(dsr["line"]["node"]["ncd1"][0], i + 3) +
        #            get_bit(dsr["line"]["node"]["ncd1"][0], (i * 2) + 6) +
        #            get_bit(dsr["line"]["node"]["ncd1"][0], (i * 2) + 7) +
        #            get_bit(dsr["line"]["node"]["ncd1"][0], i + 12))
        # get_bit(dsr["line"]["node"]["ncd1"][0], 15))

        arr["f_usable"][..., i] = np.int8(bit_sum > 0) * 2

    arr["spacecraft_id"] = mph["spacecraft"][0]

    return arr


def asps_level2_xr(dsr):
    """
    Conversion to xr.Dataset.

    Parameters
    ----------
    dsr : numpy.ndarray
        Data records.

    Returns
    -------
    ds : xarray.Datast
        Data records as xarray.Dataset.
    """
    dims = ("line", "node")
    dims_beam = ("line", "node", "beam")

    ds = xr.Dataset({
        "latitude": (dims, dsr["latitude"]),
        "longitude": (dims, dsr["longitude"]),
        "time": (dims, dsr["time"]),
        "as_des_pass": (dims, dsr["as_des_pass"]),
        "swath_indicator": (dims, dsr["swath_indicator"]),
        "backscatter": (dims_beam, dsr["backscatter"]),
        "incidence_angle": (dims_beam, dsr["incidence_angle"]),
        "azimuth_angle": (dims_beam, dsr["azimuth_angle"]),
        "kp": (dims_beam, dsr["kp"]),
        "n_echos": (dims_beam, dsr["n_echos"]),
        "f_usable": (dims_beam, dsr["f_usable"]),
        "f_land": (dims, dsr["f_land"]),
        "spacecraft_id": (dims, dsr["spacecraft_id"]),
    })

    return ds
