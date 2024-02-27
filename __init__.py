bl_info = {
    "name": "Alan Wake 2 .binFBX Importer",
    "author": "Mike2023, erik945, DKDave, Volfix, riverence, Cheturbator",
    "version": (2, 0, 0),
    "blender": (3, 5, 0),
    "location": "File > Import > Alan Wake 2 Mesh (.binFBX)",
    "description": "Import binFBX meshes from Alan Wake 2",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}

import bpy
import struct
import math
from mathutils import Matrix, Quaternion, Vector
import os
import sys

icons_dir = os.path.join(os.path.dirname(__file__), "icons")
custom_icon_col = {}
    
def import_binfbx(context, file_path, import_rig, file_structure, smooth):
    print("reading mesh...")
    
    target_lod = 0  # Target LOD value
    
    if file_structure and import_rig:
        skel_path = file_path.replace('data_pc', 'data')
        skel_path = skel_path.replace('.binfbx', '.binskeleton')
    elif import_rig and not file_structure:
        skel_path = file_path.replace('.binfbx', '.binskeleton')

    # Define offset values based on filename
    MAGIC_SIG = 0x4C
    mltMsh = 5
    mesh_skeleton_offset = 0x10
#    table_offset = 0
#    lod0_offset = 0

#    # Check the file name and assign offset values
##    if "typewriter.binfbx" in file_path:
##        table_offset = 0x75FB
##        lod0_offset = 0x28D7CC
##        block_offset = 119
##        vertex_size = 12
#    
##    if "plaza_alice_wake_statue_a.binfbx" in file_path:
##        table_offset = 0xF0
##        lod0_offset = 
##        block_offset = 115
##        vertex_size = 8

##    if "typewriter.binfbx" in file_path:
##        table_offset = 0x75FB
##        lod0_offset = 0x28D7CC

#    if "subway_train_crush_sim.binfbx" in file_path:
#        table_offset = 0x523DCA
#        lod0_offset = 0x5242EF
#        mesh_skeleton_offset = 0x4AEE7C
#        
##    if "dark_presence_intro_paper_simulation.binfbx" in file_path:
##        table_offset = 0x5D8D1
##        lod0_offset = 0
#        
##    if "clicker_a.binfbnx" in file_path:
##        table_offset = 0xA0
##        lod0_offset =
#        
#    if "leadpipe_default_publish.binfbx" in file_path:
#        table_offset = 0x353
#        lod0_offset = 0xE685
#        
#    if "flashbang_default_publish.binfbx" in file_path:
#        table_offset = 0x68D
#        lod0_offset = 0x70C
#        
#    if "casey_pistol_default_publish.binfbx" in file_path:
#        table_offset = 0xB09
#        lod0_offset = 0xB8C
#        
#    if "crossbow_default_publish.binfbx" in file_path:
#        table_offset = 0x1D86
#        lod0_offset = 0x1FF5

#    if "crossbow_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x2CFC
#        lod0_offset = 0x2F6B
#        
#    if "crossbow_double_publish_physx.binfbx" in file_path:
#        table_offset = 0x41B1
#        lod0_offset = 0x149E93
#        
#    if "doublebarrelshotgun_default_publish.binfbx" in file_path:
#        table_offset = 0x1478
#        lod0_offset = 0x1576

#    if "fbiservicepistol_compensator_publish.binfbx" in file_path:
#        table_offset = 0x573
#        lod0_offset = 0x5F2

#    if "fbiservicepistol_default_publish.binfbx" in file_path:
#        table_offset = 0xD12
#        lod0_offset = 0xE10

#    if "fbiservicepistol_magazine_extended_publish.binfbx" in file_path:
#        table_offset = 0x613
#        lod0_offset = 0x709
#    
#    if "flare_default_publish.binfbx" in file_path:
#        table_offset = 0x4DE
#        lod0_offset = 0x561
#        
#    if "flaregun_default_publish.binfbx" in file_path:
#        table_offset = 0x6ED
#        lod0_offset = 0x76C

#    if "flashlight_default_publish.binfbx" in file_path:
#        table_offset = 0x1920D
#        lod0_offset = 0x193F1
#        mesh_skeleton_offset = 0x18C4C

#    if "lamp_default_publish.binfbx" in file_path:
#        table_offset = 0x40E
#        lod0_offset = 0x5F2

#    if "lamp_physx.binfbx" in file_path:
#        table_offset = 0x94A
#        lod0_offset = 0xB3E
#        
#    if "nightingale_treeweapon.binfbx" in file_path:
#        table_offset = 0x426
#        lod0_offset = 0x82CB4
#        
#    if "pumpactionshotgun_compensator_publish.binfbx" in file_path:
#        table_offset = 0x96C
#        lod0_offset = 0x9EB

#    if "pumpactionshotgun_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x2442
#        lod0_offset = 0x25BB

#    if "pumpactionshotgun_stock_pouch_publish.binfbx" in file_path:
#        table_offset = 0x8A4
#        lod0_offset = 0x923

#    if "revolver_default_publish.binfbx" in file_path:
#        table_offset = 0x1517
#        lod0_offset = 0x160D

#    if "rifle_cheek_pad_publish.binfbx" in file_path:
#        table_offset = 0xF75
#        lod0_offset = 0x1073

#    if "rifle_default_publish.binfbx" in file_path:
#        table_offset = 0x1536
#        lod0_offset = 0x1634

#    if "rifle_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x2471
#        lod0_offset = 0x256F

#    if "rifle_scope_publish.binfbx" in file_path:
#        table_offset = 0xF75
#        lod0_offset = 0x106B

#    if "sawnoffshotgun_default_publish.binfbx" in file_path:
#        table_offset = 0x1514
#        lod0_offset = 0x1612

#    if "sawnoffshotgun_physx.binfbx" in file_path:
#        table_offset = 0x260B
#        lod0_offset = 0x2709

#    if "abigail_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x2efe6
#        lod0_offset = 0xb30aae

#    if "ahti_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x379ef
#        lod0_offset = 0x5cb9dd

#    if "alan_brightfalls_noplaid_publish_physx.binfbx" in file_path:
#        table_offset = 0x253f9
#        lod0_offset = 0x20df985

#    if "alan_brightfalls_publish_physx.binfbx" in file_path:
#        table_offset = 0x303f2
#        lod0_offset = 0x218e521

#    if "alan_default_dirty_01_publish_physx.binfbx" in file_path:
#        table_offset = 0x2f5ff
#        lod0_offset = 0x2356e64

#    if "alan_default_dirty_02_no_satchel_publish_physx.binfbx" in file_path:
#        table_offset = 0x33bde
#        lod0_offset = 0x10188b4

#    if "alan_default_dirty_02_publish_physx.binfbx" in file_path:
#        table_offset = 0x351a5
#        lod0_offset = 0x10da56d

#    if "alan_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x2f5f3
#        lod0_offset = 0x232566a

#    if "alan_no_satchel_publish_physx.binfbx" in file_path:
#        table_offset = 0x2e028
#        lod0_offset = 0x2288458

#    if "alan_scratch_player_publish_physx.binfbx" in file_path:
#        table_offset = 0x2efcc
#        lod0_offset = 0x81A524

#    if "alan_wake_scratch_publish_physx.binfbx" in file_path:
#        table_offset = 0x6a541f
#        lod0_offset = 0x24ea0b5
#        mesh_skeleton_offset = 0x678968

#    if "alex_casey_dark_place_publish_physx.binfbx" in file_path:
#        table_offset = 0x2c6f4
#        lod0_offset = 0x1b6307e

#    if "alex_casey_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x2d08d
#        lod0_offset = 0x1eccaa0

#    if "alex_casey_suit_publish.binfbx" in file_path:
#        table_offset = 0x22e5f
#        lod0_offset = 0x1B59BE2

#    if "alex_casey_suit_rough_publish_physx.binfbx" in file_path:
#        table_offset = 0x26f90
#        lod0_offset = 0x628DAC

#    if "charlie_koskela_mascot_publish_physx.binfbx" in file_path:
#        table_offset = 0x223c2
#        lod0_offset = 0x2aae00

#    if "charline_koskela_mascot_publish_physx.binfbx" in file_path:
#        table_offset = 0x226c3
#        lod0_offset = 0x2955a9

#    if "cynthia_weaver_dead_publish_physx.binfbx" in file_path:
#        table_offset = 0x440ab
#        lod0_offset = 0xf0d180

#    if "cynthia_weaver_sweater_publish_physx.binfbx" in file_path:
#        table_offset = 0x2e966
#        lod0_offset = 0xbd7938

#    if "deputy_mulligan_cultist_publish_physx.binfbx" in file_path:
#        table_offset = 0x26411
#        lod0_offset = 0xbc6e74

#    if "deputy_mulligan_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x26ade
#        lod0_offset = 0xb64576

#    if "deputy_mulligan_guardian_publish_physx.binfbx" in file_path:
#        table_offset = 0x237e7
#        lod0_offset = 0xf45a19
#        mesh_skeleton_offset = 0x539e70

#    if "deputy_thorton_cultist_publish_physx.binfbx" in file_path:
#        table_offset = 0x2b112
#        lod0_offset = 0x1039915

#    if "deputy_thorton_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x2b24d
#        lod0_offset = 0xf9f308

#    if "deputy_thorton_guardian_publish_physx.binfbx" in file_path:
#        table_offset = 0x569ddc
#        lod0_offset = 0x1920a21

#    if "donna_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x241a8
#        lod0_offset = 0xa42115

#    if "ed_booker_deerfest_publish_physx.binfbx" in file_path:
#        table_offset = 0x2cfb2
#        lod0_offset = 0x74ff4b

#    if "ed_booker_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x42c370
#        lod0_offset = 0xa9b16a
#        mesh_skeleton_offset = 0x3ff308
#        
#    if "enemy_m_fadeout_01_publish.binfbx" in file_path:
#        table_offset = 0x1F9C9
#        lod0_offset = 0x3034C9
#        
#    if "ilmo_koskela_bikergang_publish_physx.binfbx" in file_path:
#        table_offset = 0x2594e
#        lod0_offset = 0x68d545

#    if "ilmo_koskela_cultist_publish_physx.binfbx" in file_path:
#        table_offset = 0x3ba099
#        lod0_offset = 0xafa914
#        mesh_skeleton_offset = 0x3911a0

#    if "ilmo_koskela_deerfest_publish_physx.binfbx" in file_path:
#        table_offset = 0x25801
#        lod0_offset = 0x9e9c96

#    if "jaakko_koskela_bikergang_publish_physx.binfbx" in file_path:
#        table_offset = 0x2f92b
#        lod0_offset = 0xd1080f

#    if "jaakko_koskela_cultist_publish_physx.binfbx" in file_path:
#        table_offset = 0x454c4e
#        lod0_offset = 0x10076b9
#        mesh_skeleton_offset = 0x42b998

#    if "kiran_estevez_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x2ab4c
#        lod0_offset = 0x97e866

#    if "kiran_estevez_healed_publish.binfbx" in file_path:
#        table_offset = 0x254d7
#        lod0_offset = 0x970eaf

#    if "kiran_estevez_wounded_jacket_publish_physx.binfbx" in file_path:
#        table_offset = 0x2ab44
#        lod0_offset = 0x4E94AA

#    if "kiran_estevez_wounded_publish.binfbx" in file_path:
#        table_offset = 0x2549f
#        lod0_offset = 0x94af5a

#    if "mandy_may_nursinghome_publish_physx.binfbx" in file_path:
#        table_offset = 0x26357
#        lod0_offset = 0x9f24d5
#        
#    if "nightingale_guardian_publish.binfbx" in file_path:
#        table_offset = 0x20494
#        lod0_offset = 0x101707D
#        
#    if "norman_deerfest_publish.binfbx" in file_path:
#        table_offset = 0x2069d
#        lod0_offset = 0x8aa9d7

#    if "norman_default_publish.binfbx" in file_path:
#        table_offset = 0x239d4
#        lod0_offset = 0x76fee3

#    if "odin_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x24487
#        lod0_offset = 0x87b739

#    if "odin_rocker_publish_physx.binfbx" in file_path:
#        table_offset = 0x296d2
#        lod0_offset = 0x8c35c5

#    if "pat_maine_default_publish.binfbx" in file_path:
#        table_offset = 0x23c97
#        lod0_offset = 0x828564

#    if "rose_marigold_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x32a33
#        lod0_offset = 0xd96181

#    if "rose_marigold_nursinghome_publish_physx.binfbx" in file_path:
#        table_offset = 0x2d0ff
#        lod0_offset = 0xd1b5ed

#    if "saga_alt_publish_physx.binfbx" in file_path:
#        table_offset = 0x40ed2
#        lod0_offset = 0x19990ED

#    if "saga_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x3e394
#        lod0_offset = 0x16E23CC

#    if "saga_no_jacket_publish_physx.binfbx" in file_path:
#        table_offset = 0x34e35
#        lod0_offset = 0x18f6e73

#    if "saga_raincoat_publish_physx.binfbx" in file_path:
#        table_offset = 0x40d66
#        lod0_offset = 0x158ac0c

#    if "steven_lin_default_publish.binfbx" in file_path:
#        table_offset = 0x24d73
#        lod0_offset = 0xb58c24

#    if "tammy_booker_cultist_publish_physx.binfbx" in file_path:
#        table_offset = 0x25d85
#        lod0_offset = 0x50feb6

#    if "tammy_booker_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x3ebedd
#        lod0_offset = 0x8758c7
#        mesh_skeleton_offset = 0x3c6190

#    if "tim_breaker_darkplace_publish_physx.binfbx" in file_path:
#        table_offset = 0x286c3
#        lod0_offset = 0xd766e0

#    if "tim_breaker_sheriff_publish_physx.binfbx" in file_path:
#        table_offset = 0x2851d
#        lod0_offset = 0xb25aab

#    if "tor_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x2d8be
#        lod0_offset = 0xe73bad

#    if "vladimir_blum_cultist_publish_physx.binfbx" in file_path:
#        table_offset = 0x35b527
#        lod0_offset = 0x83b7ea
#        mesh_skeleton_offset = 0x3330b8

#    if "vladimir_blum_default_publish_physx.binfbx" in file_path:
#        table_offset = 0x243a2
#        lod0_offset = 0xaaed1d


    # Auxiliary functions\
    def read_char(file):
        return struct.unpack('<B', file.read(1))[0]
    
    def read_long(file):
        return struct.unpack('<I', file.read(4))[0]

    def read_short(file):
        return struct.unpack('<h', file.read(2))[0]

    def read_float(file):
        return struct.unpack('<f', file.read(4))[0]
    
    def read_float_array(count, file):
        return [float(read_float(file)) for _ in range(count)]
    
    def read_string(file):
        result = ""
        while True:
            byte = file.read(1)
            if not byte or byte == b'\x00':
                break
            result += byte.decode('utf-8')  # Assuming the string is encoded in UTF-8

        return result
    def read_sofl(file):
        length = read_long(file) - 1
        string = file.read(length).decode('utf-8')
        return string, length
    
    def find_byte_sequence(file, byte_sequence):
        byte_data = file.read()

        # Convert the byte sequence into a list of integers
        byte_sequence_int = [int(byte, 16) for byte in byte_sequence.split()]

        # Search for the byte sequence
        index = byte_data.find(bytes(byte_sequence_int))

        return index

    def read_value_at_offset(file, offset):
        file.seek(offset)
        value = file.read(1)
        value = int.from_bytes(value, byteorder='little')

        return value


    # Mesh info structure
    class MeshInfo:
        def __init__(self, lodId, vertCount, faceCount, byteForFace, face_offset, name, bonesPerVertex, bbox, vertex_size):
            self.lodId = lodId
            self.vertCount = vertCount
            self.faceCount = faceCount
            self.byteForFace = byteForFace
            self.face_offset = face_offset
            self.name = name
            self.bonesPerVertex = bonesPerVertex
            self.bbox = bbox
            self.vertex_size = vertex_size
            
    class SkelInfo:
        def __init__(self, weightcount, bonecount, bonenames, weightnames,bone_dict):
            self.weightcount = weightcount
            self.bonecount = bonecount
            self.bonenames = bonenames
            self.weightnames = weightnames
            self.bone_dict = bone_dict



    def find_offset(file):
        byte_sequence_1 = b"\x00\x01\x0F\x01\x00\x01\x07\x02"
        total_entries = 0
        
        signature = read_long(file)
        if signature != MAGIC_SIG:
            print("Invalid file signature:", hex(signature))
            return None
        
        file.seek(0)

        byte_data = file.read()
        
        index = byte_data.find(byte_sequence_1)
        
        if index != -1:
            # Jump 54 bytes back and read the value
            offset_54 = index - 54
            value_54 = read_value_at_offset(file, offset_54)
            
            if value_54 > 5:
                total_entries += 1
                print("\ntable_offset:", hex(offset_54), "count:", value_54, "\n")
            else:
                # Jump 84 bytes back and read the value
                offset_84 = index - 84
                value_84 = read_value_at_offset(file, offset_84)
                print("\ntable_offset:", hex(offset_84), "count:", value_84, "\n")
                total_entries += 1
        
        if total_entries == 0:
            print("\nByte sequence not found.")
        table_offset = offset_84
        lod = 0
        mesh_infos = read_mesh_data(file, table_offset)
        lod = mesh_infos[0].lodId - 1
        # Search function for the second byte sequence
        byte_sequence_2 = b"\x00\x00\x00\x02\x00\x00\x00"
        consecutive_bytes = 12
        offset_shift = 7
        print("Possible offsets:")    
        index = byte_data.find(byte_sequence_2)
        
        while index != -1:
            # Check the following bytes
            consecutive_values = byte_data[index + len(byte_sequence_2):index + len(byte_sequence_2) + consecutive_bytes]
            if not any(byte == 0 for byte in consecutive_values):
                offset_shifted = index + offset_shift
                print(f"lod{lod}_offset: {hex(offset_shifted)}")
                lod -= 1
            
            # Search for the next occurrence of the byte sequence
            index = byte_data.find(byte_sequence_2, index + 1)
    
        if index == -1:
            print("\nByte sequence not found.")
            
    # Read mesh data for mesh info structure
    def read_mesh_data(file, table_offset):
        mesh_infos = []
        file.seek(table_offset)
        mesh_id = read_long(file)
        dir, full = os.path.split(file_path)
        name, ext = os.path.splitext(full)
        bbox = dict()

        for i in range(mesh_id):
            cur_offset = file.tell()
#            print(cur_offset)
            lodId = read_long(file)
            vertCount = read_long(file)
            faceCount = read_long(file)
            
            file.seek(8, 1) 

            byteForFace = read_long(file)
            face_offset = read_long(file)
            bonesPerVertex = read_long(file)
            if bonesPerVertex == 8:
                block_offset = 127
                vertex_size = 32
            elif bonesPerVertex == 4:
                block_offset = 123
                vertex_size = 16
            elif bonesPerVertex == 1:
                block_offset = 119
                vertex_size = 12
            elif bonesPerVertex == 0:
                block_offset = 115
                vertex_size = 8
#            print(f"Vertex Size: {vertex_size}")
            bbox[i] = read_float_array(10, file)
            
            for n in range(10):
                bbox[i][n] *= 5
                

            # Go to the next block
            if block_offset == 127:
                file.seek(cur_offset + block_offset, 0)
                countBlock = read_long(file)
                file.seek(countBlock * 36, 1)
            else:
                file.seek(cur_offset + block_offset, 0)
            mesh_infos.append(MeshInfo(lodId, vertCount, faceCount, byteForFace, face_offset, name, bonesPerVertex, bbox, vertex_size))

        
        return mesh_infos

    # Function for outputting mesh info structure (console)
    def print_mesh_infos(mesh_infos):
        for i, mesh_info in enumerate(mesh_infos, start=1):  # Starts counting at 1
            print(f"Mesh ID {i}: LOD ID: {mesh_info.lodId}, Vertex Count: {mesh_info.vertCount}, Face Count: {mesh_info.faceCount}, Bytes per Face: {mesh_info.byteForFace}, Bones per Vertex: {mesh_info.bonesPerVertex}, Face Offset: {mesh_info.face_offset}")


    def read_skel_data(skel, mesh):
        skel_infos = []
        mesh.seek(mesh_skeleton_offset)
        skel.seek(0x30, 0)
        weightcount = read_long(mesh)
        bonecount = read_long(skel)
        bonenames = []
        weightnames = []
        bone_dict = dict()
        skel.seek(0x50, 0)
        offset = (bonecount * 32) + (bonecount * 2) + 80
        while offset % 16 != 0:
            offset += 1
        
        offset += bonecount * 4
        while offset % 16 != 0:
            offset += 1
        
        offset += 16 + (bonecount * 4)
        while offset % 16 != 0:
            offset += 1
        
        offset += 16 + (bonecount * 8)
        
        skel.seek(offset, 0)
        for i in range(bonecount):
            bonename = read_string(skel)
            bonenames.append(bonename)
            bone_dict[i] = bonename
#            print("bone_dict:", bone_dict)
        
        for i in range(weightcount):
            cur_offset = mesh.tell()
#            print("mesh name offset:", cur_offset)
            weightname, wlength = read_sofl(mesh)
#            print("weight name:", weightname, "current offset:", cur_offset, "weight number", i)
            mesh.seek(cur_offset + (73 + wlength), 0)
#            print("cur_offset (weights):", cur_offset + (73 + wlength))
            weightnames.append(weightname)
            
        skel_infos.append(SkelInfo(weightcount, bonecount, bonenames, weightnames, bone_dict))
        
        return skel_infos
    
    def print_skel_infos(skel_infos):
        for i, skel_info in enumerate(skel_infos, start=1):
            print(f"Weight Count: {skel_info.weightcount}, Bone Count: {skel_info.bonecount}")
            
    def read_mesh_skel(skel, mesh, skel_info, name, objArray):
        boneArray = []
        parents = []
        dir, full = os.path.split(file_path)
        name, ext = os.path.splitext(full)
        bpy.ops.object.add(
        type='ARMATURE', 
        enter_editmode=True,)
        arm_obj = bpy.context.object
        bpy.data.collections[name].objects.link(arm_obj)
        bpy.data.scenes['Scene'].collection.objects.unlink(arm_obj)
        bpy.context.view_layer.objects.active = arm_obj
        arm = arm_obj.data
        skel.seek(0x50 + (skel_info.bonecount * 32), 0)
        for i in range(0, skel_info.bonecount):
            pid = read_short(skel)
            parents.append(pid)
        skel.seek(0x50, 0)
        for i in range(0, skel_info.bonecount):
            bpy.ops.object.mode_set(mode='EDIT')
#            print("edit mode on")
            cur_offset = skel.tell()
#            print(f"cur skel offset: {cur_offset}")
            bnVal = read_float_array(8, skel)
            
            quat = Quaternion(Vector((bnVal[3], bnVal[0], bnVal[1], bnVal[2])))
#            print(quat)
#            print(skel_info.bone_dict)
            bonename = skel_info.bone_dict.get(i, "key not found")
#            print(f"{bonename} quat: {quat}")
#            print(f"{bonename} transform: {transform}")
            transform = [bnVal[4] * mltMsh, bnVal[5] * mltMsh, bnVal[6] * mltMsh]
            tfm = Matrix.LocRotScale(transform, quat, None)
#            print(f"{bonename} tfm matrix: {tfm}")
            bone = arm.edit_bones.new(bonename)
            bone.use_relative_parent = True
            bone.head = Vector(transform)
            bone.matrix = tfm
            bone.length = 0.1

#            bone.use_connect = True
            if parents[i] >= 0:
                bone.parent = arm.edit_bones[skel_info.bone_dict[parents[i]]]
                bone.head += bone.parent.head
            
            bone.tail = bone.head + Vector((.0, .0, .115))
            if parents[i] == -1:
                bone.head = Vector([.0, .0, .01]) #prevent zero length
            
            
            if bone.parent:
                bone.matrix = bone.parent.matrix @ tfm
            else:
                bone.matrix = tfm
#            bpy.ops.object.mode_set(mode='POSE')
##            print("pose mode on")
#        
#            pbone = arm_obj.pose.bones[bonename]
#            
#        
#            pbone.matrix_basis.identity()
#            
#        
#            if pbone.parent:
#                pbone.matrix = pbone.parent.matrix @ tfm
#            else:
#                pbone.matrix = tfm
#            
#            bpy.ops.pose.armature_apply()

                    
       
            
        bpy.ops.object.mode_set(mode='OBJECT')
        arm_obj.rotation_euler[0] = math.radians(90)
        arm_obj.scale = (-1.0, 1.0, 1.0)
        
        for i in range(len(objArray)):
            mod = objArray[i].modifiers.new('Armature', 'ARMATURE')
            mod.object = arm_obj
            mod.use_bone_envelopes = False
            mod.use_vertex_groups = True
            if bpy.app.version[1] > 71:
                context.view_layer.objects.active = objArray[i]
                bpy.ops.object.vertex_group_sort(sort_type='BONE_HIERARCHY')
            objArray[i].parent = arm_obj
#        arm_obj.location.z += 3.12317
        
    # Read UV data for the entire mesh with the corresponding LOD value
    def read_mesh_uvs(file, mesh_info, uv_offset):
        UV_array = []
        file.seek(uv_offset)
        uvCount = mesh_info.vertCount
        # Assumption: UVs present for every vertex and consist of two 'short' values
        for _ in range(uvCount):
            u = struct.unpack('<H', file.read(2))[0] / 65535.0 * 16 # scaling factor [0,1]
            v = struct.unpack('<H', file.read(2))[0] / 65535.0 * 16
            UV_array.append((u,-v +1))  # Invert V for Blender
            
            file.read(4)  # Skipping bytes (padding)
            
        return UV_array



    smax = 1 / 65535
    # Read vertex data for the entire mesh with the corresponding LOD value
    def read_mesh_vertices(file, mesh_info, vertex_offset, minv, maxv, meshnum):
        vertArray = []
        lva = []
        # Navigate to the start of the vertex data
        file.seek(vertex_offset)
        vertCount = mesh_info.vertCount
        xMin = 9000000
        yMin = 9000000
        zMin = 9000000
        xMax = 0
        yMax = 0
        zMax = 0
        for _ in range(vertCount):
            cur_offset = file.tell()
            
            lx = read_short(file) * smax
            ly = read_short(file) * smax
            lz = read_short(file) * smax
            lva.append((lx, ly, lz))
            file.seek(cur_offset + mesh_info.vertex_size, 0)
            
            
#        print(f"min vertex: {minv}")
#        print(f"max vertex: {maxv}")
        for vi in range(minv, maxv):
            if xMin > lva[vi][0]:
                xMin = lva[vi][0]
            if xMax < lva[vi][0]:
                xMax = lva[vi][0]

            if yMin > lva[vi][1]:
                yMin = lva[vi][1]
            if yMax < lva[vi][1]:
                yMax = lva[vi][1]

            if zMin > lva[vi][2]:
                zMin = lva[vi][2]
            if zMax < lva[vi][2]:
                zMax = lva[vi][2]

#        minv -= 1
        
#        print(f"bbox: {mesh_info.bbox[meshnum]}")
#        print(f"x min: {xMin}, y min: {yMin}, z min: {zMin}")
#        print(f"x max: {xMax}, y max: {yMax}, z max: {zMax}")
        
        xsca = (mesh_info.bbox[meshnum][7] - mesh_info.bbox[meshnum][4]) / (xMax - xMin)
        ysca = (mesh_info.bbox[meshnum][8] - mesh_info.bbox[meshnum][5]) / (yMax - yMin)
        zsca = (mesh_info.bbox[meshnum][9] - mesh_info.bbox[meshnum][6]) / (zMax - zMin)
        
        
        
        # avert your eyes, shitty handling for when one of the max or mins is 0 because it fucks up the submesh's scale.... :(
        if xMax == 0 or xMin == 0:
            xsca = ysca
            if yMax == 0 or yMin == 0:
                xsca = zsca
                ysca = zsca
                if zMax == 0 or zMin == 0:
                    print(f"Couldn't scale submesh {meshnum + 1} properly.")
        elif yMax == 0 or yMin == 0:
            ysca = xsca
            if zMax == 0 or zMin == 0:
                zsca = xsca
        elif zMax == 0 or zMin == 0:
            zsca = xsca
         
        print(f"xsca: {xsca}")
        print(f"ysca: {ysca}")
        print(f"zsca: {zsca}")
        for i in range(vertCount):
            vx = ((lva[i][0] - xMin) * xsca + mesh_info.bbox[meshnum][4])
            vy = ((lva[i][1] - yMin) * ysca + mesh_info.bbox[meshnum][5])
            vz = ((lva[i][2] - zMin) * zsca + mesh_info.bbox[meshnum][6])
            
            vertArray.append((vx, vy, vz))
        

    
        return vertArray


    def read_mesh_weights(file, mesh_info, skel_info, vertex_offset, vertcount):
        file.seek(vertex_offset, 0)
        print(f"vertex size in weights func: {mesh_info.vertex_size}")
        bdrev = dict((v, k) for k, v in skel_info.bone_dict.items())
        vrts = []

        for i in range(vertcount):
            vrt = []
            cur_offset = file.tell()

            if mesh_info.lodId == 0:
                    vbids = []
                    vweights = []
                    file.seek(cur_offset + 8, 0)
                    for _ in range(mesh_info.bonesPerVertex):
                        if mesh_info.vertex_size == 32:
                            lbid = read_short(file)
                        elif mesh_info.vertex_size == 16 or mesh_info.vertex_size == 12:
                            lbid = read_char(file)
                        vbids.append(lbid)

                    file.seek(cur_offset + (3 * mesh_info.bonesPerVertex), 0)
                    for _ in range(mesh_info.bonesPerVertex):
                        lweight = read_char(file)
                        vweights.append(lweight)

                    for bdat in range(mesh_info.bonesPerVertex):
                        lbid = vbids[bdat]
                        if lbid != 0:
                            weightname = skel_info.weightnames[lbid]
                            nbid = bdrev[weightname]
                            vrt.append(nbid)
                            vrt.append(vweights[bdat] / 255.0)
                        else:
                            vrt.append(0)
                            vrt.append(vweights[bdat] / 255.0)

                    vrts.append(vrt)
                    
                    

            file.seek(cur_offset + mesh_info.vertex_size, 0)

        print(f"number of weight verts: {len(vrts)}")
        return vrts

                            
                               
    # Read face data for each Submesh
    def read_mesh_faces(file, mesh_info, face_offset):
        faceArray = []
        minv = 9000000
        maxv = 0 
        # Go to the start point of the face data for this Submesh
        file.seek(face_offset)
        # Reading the face data (indices)
        for _ in range(mesh_info.faceCount):
            f1 = f2 = f3 = 0
            if mesh_info.byteForFace == 4:
                # The indices must be correct and within the bounds of the vertex array
                f1, f2, f3 = struct.unpack('<III', file.read(12))
                
            elif mesh_info.byteForFace == 2:
                # The indices must be correct and within the bounds of the vertex array
                f1, f2, f3 = struct.unpack('<HHH', file.read(6))
            faceArray.append((f1, f2, f3))
            
            if f1 < minv:
                minv = f1 + 1
            if f2 < minv:
                minv = f2 + 1
            if f3 < minv:
                minv = f3 + 1

            if f1 > maxv:
                maxv = f1 + 1
            if f2 > maxv:
                maxv = f2 + 1
            if f3 > maxv:
                maxv = f3 + 1
        
        return faceArray, minv, maxv

        
    
    # Create mesh in Blender
    def create_mesh_in_blender(vertArray, faceArray, UV_array, mesh_name, name, objArray):
        # Create new mesh and new object
        mesh_data = bpy.data.meshes.new(mesh_name)
        mesh_obj = bpy.data.objects.new(mesh_name, mesh_data)

        # Link scene and position mesh object
        bpy.data.collections[name].objects.link(mesh_obj)
        bpy.context.view_layer.objects.active = mesh_obj
        mesh_obj.select_set(True)
        if not import_rig:
            bpy.context.active_object.rotation_euler[0] = math.radians(90)
        

        # Assign mesh data
        mesh_data.from_pydata(vertArray, [], faceArray)
        mesh_data.update()  # Mesh update to apply the changes
        
        
        
        # Assign UV data
        if UV_array:
            # Check if UV map already exists, if not, create a new one
            if "UVMap" not in mesh_data.uv_layers:
                mesh_data.uv_layers.new(name='UVMap')
            uv_layer = mesh_data.uv_layers['UVMap'].data

            # Delete old UV map if there is one
            if "UVMap" in mesh_data.uv_layers:
                mesh_data.uv_layers.remove(mesh_data.uv_layers["UVMap"])

            # Create new UV map
            uv_layer = mesh_data.uv_layers.new(name="UVMap")

            # Assignment of the UV coordinates to the new UV map
            for poly in mesh_data.polygons:  # Go through each polygon
                poly.use_smooth = True
                for loop_index, loop_vert in zip(poly.loop_indices, poly.vertices):  # Go through each loop and vertex of the polygon
                    # Access the UV loop to set the UV coordinates
                    loop_uv = uv_layer.data[loop_index]
                    # Assign UV values (assumption: UV_array contains pairs of UV values)
                    loop_uv.uv = UV_array[loop_vert]  # Assigning the UV coordinates according to the vertices
            
            
            # Clean up mesh
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.delete_loose()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.editmode_toggle()
            
        mesh_data.update() # Mesh update to apply the changes
        objArray.append(mesh_obj)
        return objArray



    # Constants
    UV_SIZE = 8  # A UV pair consists of two floats
    #FACE_SIZE = 3  # A face consists of three indices and each index is an integer
    HEADER_SIZE = 4 # The first 4 bytes from lod0_offset must be skipped

    # Main function               
    def main():
        print("binfbx path (main):", file_path)
        objArray = []
        msh = -1
        verts = 0
        with open(file_path, "rb") as file:     
            find_offset(file)
            mesh_infos = read_mesh_data(file, table_offset)
            print_mesh_infos(mesh_infos)

            for mesh_info in mesh_infos:
                collection_name = mesh_info.name
                
                # check if the collection already exists
                if collection_name not in bpy.data.collections:
                    bpy.ops.collection.create(name=collection_name)
                    bpy.context.scene.collection.children.link(bpy.data.collections[collection_name])
            if import_rig:    
                with open(skel_path, "rb") as skel:     
                    print("reading skel...")
                    skel_infos = read_skel_data(skel, file)
                    print_skel_infos(skel_infos)
            for i, mesh_info in enumerate(mesh_infos, start=1):
                if mesh_info.lodId == target_lod:
                    msh += 1
                    vrtwgt = None
#                            for n in range(i)
                    uv_offset = lod0_offset + HEADER_SIZE
                    vertex_offset = (uv_offset + (mesh_info.vertCount * UV_SIZE) - HEADER_SIZE)
                    print(f"Vertex Size: {mesh_info.vertex_size}")
                    submeshvert_offset = vertex_offset + (verts * mesh_info.vertex_size)
                    print(f"Vertex Offset in DEC for Submesh {i} (LOD{mesh_info.lodId}): {submeshvert_offset}")
                    face_offset = vertex_offset + (mesh_info.vertCount * mesh_info.vertex_size) + (mesh_info.face_offset * mesh_info.byteForFace)
                    print(f"Face Offset in DEC for Mesh ID {i} (LOD{mesh_info.lodId}): {face_offset}")
                    
                    UV_array = read_mesh_uvs(file, mesh_info, uv_offset)
                    faceArray, minv, maxv = read_mesh_faces(file, mesh_info, face_offset)
                    vertArray = read_mesh_vertices(file, mesh_info, vertex_offset, minv, maxv, i - 1)
                    if len(faceArray) != mesh_info.faceCount:
                        print(f"Warning: Number of faces loaded ({len(faceArray)}) does not match expected number ({mesh_info.faceCount}) agree!")
                
                    mesh_name = f"{mesh_info.name}_LOD{mesh_info.lodId}__ID_{i}"
                    objArray = create_mesh_in_blender(vertArray, faceArray, UV_array, mesh_name, mesh_info.name, objArray)
                    print(f"submesh number {msh}")
                    vertcount = len(objArray[msh].data.vertices)
                    verts += vertcount
                    print(f"number of verts for submesh {msh}: {vertcount}")
                    obj = objArray[msh]
                    if import_rig:    
                        with open(skel_path, "rb") as skel:     
                            # assigning weight groups
                            for _, skel_info in enumerate(skel_infos, start=1):
                                vrtwgt = read_mesh_weights(file, mesh_info, skel_info, submeshvert_offset, vertcount)
                                for vrt in range(vertcount):   
                                    wgt = vrtwgt
                                    boneid = wgt[vrt][0]
                                    bonename = skel_info.bone_dict[boneid]
                                    grp = None
                                    if bonename in obj.vertex_groups.keys():
                                        grp = obj.vertex_groups[bonename]
                                    if grp == None:
                                        grp = obj.vertex_groups.new(name=bonename)
                                        
                                    wgt = vrtwgt
    #                                    print(f"boneid: {vrtwgt[vrt][0]}")
    #                                    print(f"current bone: {n}")
                                    grp.add([vrt],
                                    wgt[vrt][1], 
                                    'ADD')
                                if smooth:
                                    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
                                    bpy.ops.active_object = obj
                                    bpy.ops.object.vertex_group_smooth(group_select_mode='ALL', factor=0.5, repeat=2, expand=0.0)
                                    if mesh_info.vertex_size == 32:
                                        bpy.ops.object.mode_set(mode='EDIT')
                                        bpy.ops.mesh.remove_doubles(use_unselected=True, use_sharp_edge_from_normals=True)
                                    bpy.ops.object.mode_set(mode='OBJECT')                         
                        
                        
                        
                        
                    

                    if i+1 < len(mesh_infos) and mesh_info.lodId != mesh_infos[i+1].lodId:
                        print("Move to next LOD or additional processing")

                    elif i+1 == len(mesh_infos):
                        print("Last mesh reached, additional processing or move on to the next block")
                    
            if import_rig:    
                with open(skel_path, "rb") as skel:     
                    for _, skel_info in enumerate(skel_infos, start=1):
                        print("creating armature...")
                        read_mesh_skel(skel, file, skel_info, collection_name, objArray)
#                        print(weightArray)
                                    
                                    
                                
    
    
    main()
    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class read_binfbx(Operator, ImportHelper):
    """Import Alan Wake 2 binFBX"""
    bl_idname = "import_scene.binfbx"
    bl_label = "Import binFBX"

    # ImportHelper mixin class uses this
    filename_ext = ".binfbx"

    filter_glob: StringProperty(
        default="*.binfbx",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    import_rig: BoolProperty(
        name="Import Rig",
        description="Import the binfbx rig from the binskeleton file (either next to the binfbx or in the original directory structure)",
        default=True,
    )
    
    file_structure: BoolProperty(
        name="Original Directory Structure",
        description="When enabled, looks for the binskeleton file in /data/objects/. If disabled, looks for the skeleton file next to the mesh file",
        default=True,
    )
    smooth: BoolProperty(
        name="Smooth Weights",
        description="Whether or not to 'smooth' the imported vertex groups, giving them a cleaner and smoother deform.",
        default=True,
    )
    def execute(self, context):
        print("file path:", self.filepath)
        return import_binfbx(context, self.filepath, self.import_rig, self.file_structure, self.smooth)


# Only needed if you want to add into a dynamic menu.
def menu_func_import(self, context):
    self.layout.operator(read_binfbx.bl_idname, text="Alan Wake 2 Mesh (.binFBX)", icon_value=custom_icon_col["import"]['AW2'].icon_id)


# Register and add to the "file selector" menu
def register():
    import bpy.utils.previews
    bpy.utils.register_class(read_binfbx)
    custom_icon = bpy.utils.previews.new()
    custom_icon.load("AW2", os.path.join(icons_dir, "aw2.png"), 'IMAGE')
    custom_icon_col["import"] = custom_icon
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(read_binfbx)
    bpy.utils.previews.remove(custom_icon_col["import"])
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()