import socket
import pandas as pd
import ctypes

class PacketHeader(ctypes.LittleEndianStructure):
    _fields_ = [
        ('m_packet_format', ctypes.c_uint16), # 2021
        ('m_game_major_version', ctypes.c_uint8), # Game major version - "X.00"
        ('m_game_minor_version', ctypes.c_uint8), # Game minor version - "1.XX"
        ('m_packet_version', ctypes.c_uint8), # Version of this packet type, all start from 1
        ('m_packet_id', ctypes.c_uint8), # Identifier for the packet type, see below
        ('m_session_uid', ctypes.c_uint64), # Unique identifier for the session
        ('m_session_time', ctypes.c_float), # Session timestamp
        ('m_frame_identifier', ctypes.c_uint32), # Identifier for the frame the data was retrieved on
        ('m_player_car_index', ctypes.c_uint8), # Index of player's car in the array
        ('m_secondary_player_car_index', ctypes.c_uint8), # Index of secondary player's car in the array (splitscreen)
        # 255 if no second player
    ]

class CarMotionData(ctypes.LittleEndianStructure):
    _fields_ = [
        ('m_world_position_x', ctypes.c_float), # World space X position
        ('m_world_position_y', ctypes.c_float), # World space Y position
        ('m_world_position_z', ctypes.c_float), # World space Z position
        ('m_world_velocity_x', ctypes.c_float), # Velocity in world space X
        ('m_world_velocity_y', ctypes.c_float), # Velocity in world space Y
        ('m_world_velocity_z', ctypes.c_float), # Velocity in world space Z
        ('m_world_forward_dir_x', ctypes.c_int16), # World space forward X direction (normalised)
        ('m_world_forward_dir_y', ctypes.c_int16), # World space forward Y direction (normalised)
        ('m_world_forward_dir_z', ctypes.c_int16), # World space forward Z direction (normalised)
        ('m_world_right_dir_x', ctypes.c_int16), # World space right X direction (normalised)
        ('m_world_right_dir_y', ctypes.c_int16), # World space right Y direction (normalised)
        ('m_world_right_dir_z', ctypes.c_int16), # World space right Z direction (normalised)
        ('m_g_force_lateral', ctypes.c_float), # Lateral G-Force component
        ('m_g_force_longitudinal', ctypes.c_float), # Longitudinal G-Force component
        ('m_g_force_vertical', ctypes.c_float), # Vertical G-Force component
        ('m_yaw', ctypes.c_float), # Yaw angle in radians
        ('m_pitch', ctypes.c_float), # Pitch angle in radians
        ('m_roll', ctypes.c_float), # Roll angle in radians
    ]

ls_m_world_position_x = []
ls_m_world_position_y = []
ls_m_world_position_z = []
ls_m_world_velocity_x = []
ls_m_world_velocity_y = []
ls_m_world_velocity_z = []
ls_m_world_forward_dir_x = []
ls_m_world_forward_dir_y = []
ls_m_world_forward_dir_z = []
ls_m_world_right_dir_x = []
ls_m_world_right_dir_y = []
ls_m_world_right_dir_z = []
ls_m_g_force_lateral = []
ls_m_g_force_longitudinal = []
ls_m_g_force_vertical = []
ls_m_yaw = []
ls_m_pitch = []
ls_m_roll = []

UDP_IP = "127.0.0.1"
UDP_PORT = 20777

sock = socket.socket(
    socket.AF_INET, # Internet
    socket.SOCK_DGRAM
) # UDP


sock.bind(('', UDP_PORT))
df = pd.DataFrame(columns=['data'])

l = []
i = 0

while True:
    data, addr = sock.recvfrom(4096) # buffer size is 1024 bytes
    print("received message: %s" % data)


    i = i + 1

    d = {'data':data}
    
    m_header = PacketHeader.from_buffer_copy(data)
    if m_header.m_packet_id == 0:
        
        m_motion = CarMotionData.from_buffer_copy(data[24:])
        m_world_position_x = m_motion.m_world_position_x
        m_world_position_y = m_motion.m_world_position_y
        m_world_position_z = m_motion.m_world_position_z
        m_world_velocity_x = m_motion.m_world_velocity_x
        m_world_velocity_y = m_motion.m_world_velocity_y
        m_world_velocity_z = m_motion.m_world_velocity_z
        m_world_forward_dir_x = m_motion.m_world_forward_dir_x
        m_world_forward_dir_y = m_motion.m_world_forward_dir_y
        m_world_forward_dir_z = m_motion.m_world_forward_dir_z
        m_world_right_dir_x = m_motion.m_world_right_dir_x
        m_world_right_dir_y = m_motion.m_world_right_dir_y
        m_world_right_dir_z = m_motion.m_world_right_dir_z
        m_g_force_lateral = m_motion.m_g_force_lateral
        m_g_force_longitudinal = m_motion.m_g_force_longitudinal
        m_g_force_vertical = m_motion.m_g_force_vertical
        m_yaw = m_motion.m_yaw
        m_pitch = m_motion.m_pitch
        m_roll = m_motion.m_roll
        
        ls_m_world_position_x.append(m_world_position_x)
        ls_m_world_position_y.append(m_world_position_y)
        ls_m_world_position_z.append(m_world_position_z)
        ls_m_world_velocity_x.append(m_world_velocity_x)
        ls_m_world_velocity_y.append(m_world_velocity_y)
        ls_m_world_velocity_z.append(m_world_velocity_z)
        ls_m_world_forward_dir_x.append(m_world_forward_dir_x)
        ls_m_world_forward_dir_y.append(m_world_forward_dir_y)
        ls_m_world_forward_dir_z.append(m_world_forward_dir_z)
        ls_m_world_right_dir_x.append(m_world_right_dir_x)
        ls_m_world_right_dir_y.append(m_world_right_dir_y)
        ls_m_world_right_dir_z.append(m_world_right_dir_z)
        ls_m_g_force_lateral.append(m_g_force_lateral)
        ls_m_g_force_longitudinal.append(m_g_force_longitudinal)
        ls_m_g_force_vertical.append(m_g_force_vertical)
        ls_m_yaw.append(m_yaw)
        ls_m_pitch.append(m_pitch)
        ls_m_roll.append(m_roll)
        

    if i % 1000 == 0:
        df_car_motion_data = pd.DataFrame()

        df_car_motion_data['m_world_position_x'] = ls_m_world_position_x
        df_car_motion_data['m_world_position_y'] = ls_m_world_position_y
        df_car_motion_data['m_world_position_z'] = ls_m_world_position_z
        df_car_motion_data['m_world_velocity_x'] = ls_m_world_velocity_x
        df_car_motion_data['m_world_velocity_y'] = ls_m_world_velocity_y
        df_car_motion_data['m_world_velocity_z'] = ls_m_world_velocity_z
        df_car_motion_data['m_world_forward_dir_x'] = ls_m_world_forward_dir_x
        df_car_motion_data['m_world_forward_dir_y'] = ls_m_world_forward_dir_y
        df_car_motion_data['m_world_forward_dir_z'] = ls_m_world_forward_dir_z
        df_car_motion_data['m_world_right_dir_x'] = ls_m_world_right_dir_x
        df_car_motion_data['m_world_right_dir_y'] = ls_m_world_right_dir_y
        df_car_motion_data['m_world_right_dir_z'] = ls_m_world_right_dir_z
        df_car_motion_data['m_g_force_lateral'] = ls_m_g_force_lateral
        df_car_motion_data['m_g_force_longitudinal'] = ls_m_g_force_longitudinal
        df_car_motion_data['m_g_force_vertical'] = ls_m_g_force_vertical
        df_car_motion_data['m_yaw'] = ls_m_yaw
        df_car_motion_data['m_pitch'] = ls_m_pitch
        df_car_motion_data['m_roll'] = ls_m_roll
        
        df_car_motion_data.to_csv(r'C:\Users\jules\OneDrive\F1 2021 Telemetry\Python Script\motion_data.csv', index=False)