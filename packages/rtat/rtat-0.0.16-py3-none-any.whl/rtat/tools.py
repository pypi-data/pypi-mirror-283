import glob
import matplotlib.pyplot as plt
import netrc
import os
import numpy as np
import pydicom
import pymysql
import sys
import struct


verbose=0
rootDir="/data/projects/RCR03-400/experiments"
tempDir="/data/projects/RCR03-400/experiments"

########################################################################################################    
#
########################################################################################################    
def accumulate_dose_from_files(dicom_files):
    accumulated_dose = None
    slice_thickness = None

    for file in dicom_files:
        ds = pydicom.dcmread(file)

        # Get dose data
        dose_data = ds.pixel_array
        dose_grid_scaling = ds.DoseGridScaling
        dose_data = dose_data * dose_grid_scaling

        if accumulated_dose is None:
            accumulated_dose = dose_data
            slice_thickness = ds.GridFrameOffsetVector[1] - ds.GridFrameOffsetVector[0]
        else:
            accumulated_dose += dose_data

    return accumulated_dose, slice_thickness

########################################################################################################    
#
########################################################################################################    
def find_highest_dose_voxel(summed_dose_grid):
    # Find the index of the maximum dose value
    max_index = np.argmax(summed_dose_grid)
#   print("map_index ", max_index)
    # Convert the flat index to 3D indices
    max_coords = np.unravel_index(max_index, summed_dose_grid.shape)
    return max_coords

########################################################################################################    
#
########################################################################################################    
def find_plan_directory(apid,aplan):
#   expDir=rootDir+"/"+str(apid)+"-"+aplan
#   return expDir
# Construct the expected directory path
    expDir = os.path.join(rootDir, f"{apid}-{aplan}")

    # Check if the directory exists
    if not os.path.exists(expDir):
        # If the directory does not exist, create a temporary directory
        temp_expDir = expDir.replace(rootDir, tempDir)
        os.makedirs(temp_expDir, exist_ok=True)  # Create the directory
        expDir = temp_expDir  # Update expDir to the temp directory

    return expDir
########################################################################################################    
#
########################################################################################################    
def find_voxel_spectra_files(expDir,beam=None):
   if beam == None or beam == 'all' or beam == 'ALL' :
      search_pattern = expDir + "/SCANS/104/voxel_spectra/*voxel-spectra.bin"
      matching_files = glob.glob(search_pattern)
      if verbose > 2 : 
         print(" search_pattern ", search_pattern)
         for file_path in matching_files:
            print(file_path)
      return matching_files
   else:
      search_pattern = expDir + "/SCANS/104/voxel_spectra/fdc-beam_"+str(beam)+"*-voxel-spectra.bin"
      if verbose > 2 : 
         print(" search_pattern ", search_pattern)
      matching_files = glob.glob(search_pattern)
      if verbose > 0 and len(matching_files) == 0:
         print(" Voxel spectra not found ")
      return matching_files

########################################################################################################    
#
########################################################################################################    
def get_dose_files ( apid, aplan, engine, beam ):
    
    scan="1104"
    if   engine == "TPS":   scan="104"
    elif engine == "DoseW": scan="1104"
    
    expDir = find_plan_directory(apid,aplan)
    bm=beam.lower()
    search_pattern = expDir + "/SCANS/"+scan+"*/DICOM"
    #print("search_pattern ", search_pattern)
    dose_dirs = glob.glob(search_pattern)
    
    if len(dose_dirs) == 1 :
        search_pattern = expDir + "/SCANS/"+scan+"*/DICOM/*.dcm"
        dose_files = glob.glob(search_pattern)
        #print("dose_files ", dose_files)
        
        if beam != None and bm != "all":
            selected_files=[]
            #print("dose_files ", dose_files)
            for dose_file in dose_files:
                #print("dose_file ",dose_file)
                ds = pydicom.dcmread(dose_file)
                referenced_beam_number = None
                if 'ReferencedRTPlanSequence' in ds:
                    rt_plan_sequence = ds.ReferencedRTPlanSequence
    
                    if rt_plan_sequence and len(rt_plan_sequence) > 0:
                       referenced_rt_plan = rt_plan_sequence[0]  # Assuming there's only one referenced RT plan
        
                       if 'ReferencedFractionGroupSequence' in referenced_rt_plan:
                          fraction_group_sequence = referenced_rt_plan.ReferencedFractionGroupSequence
            
                          if fraction_group_sequence and len(fraction_group_sequence) > 0:
                             referenced_fraction_group = fraction_group_sequence[0]  # Assuming there's only one referenced fraction group
                
                             if 'ReferencedBeamSequence' in referenced_fraction_group:
                                 beam_sequence = referenced_fraction_group.ReferencedBeamSequence
                    
                                 if beam_sequence and len(beam_sequence) > 0:
                                    referenced_beam = beam_sequence[0]  # Assuming there's only one referenced beam
                        
                                    if 'ReferencedBeamNumber' in referenced_beam:
                                        referenced_beam_number = referenced_beam.ReferencedBeamNumber
                                        #print("Ref_beam ",referenced_beam_number,"  beam ", beam)
                                        if referenced_beam_number == beam:
                                            selected_files.append(dose_file)
            
            return selected_files
            #print(dose_file)
        else:
            return dose_files
    else:
        print("Get_dose_files, multiple directories found for ",engine)
        return None

########################################################################################################    
#
########################################################################################################    
def get_dose (apid,aplan,engine,beams):
    dose_files = get_dose_files(apid,aplan,engine,beams)
    print("AAAA dose_files engine", dose_files, engine) 
    summed_dose_grid = None
    for dose_file in dose_files:
        ds = pydicom.dcmread(dose_file)
        if ds.Modality != "RTDOSE":
            raise ValueError("The provided DICOM file is not an RTDose file.")
        dose_grid = ds.pixel_array
        dose_grid_scaling = ds.DoseGridScaling
        
        dose_grid = dose_grid * dose_grid_scaling
        
        if summed_dose_grid is None:
            summed_dose_grid = np.zeros_like(dose_grid, dtype=np.float64)
        summed_dose_grid += dose_grid
    return summed_dose_grid    

########################################################################################################    
#
########################################################################################################    
def get_files_by_scan_type(xnat_session, project, experiment, xnat_url, scan_type):

 # Select project and experiment
    project_obj = xnat_session.projects[project]
    experiment_obj = project_obj.experiments[experiment]
    if verbose>1 : print("proj obj ",project_obj," exp_obj ", experiment_obj)

     # Iterate over scans to find the correct scan type
    for scan in experiment_obj.scans.values():
         if scan.type == scan_type:
             # Retrieve all files for this scan
             files = scan.files.values()
             return files


########################################################################################################    
#
########################################################################################################    
def get_dose_at_voxel(summed_dose_grid, ix, iy, iz):
    if ix < 0 or ix >= summed_dose_grid.shape[2] or iy < 0 or iy >= summed_dose_grid.shape[1] or iz < 0 or iz >= summed_dose_grid.shape[0]:
        raise IndexError("Voxel coordinates are out of bounds.")
        return 0
    return summed_dose_grid[iz, iy, ix]
    
########################################################################################################    
#
########################################################################################################    
def get_lattice_info ( apid, aplan ):
    expDir=rootDir+"/"+str(apid)+"-"+aplan
    search_pattern = expDir + "/SCANS/104/voxel_spectra/lattice-info.txt"
    matching_files = glob.glob(search_pattern)
    if verbose > 2 : 
         print(" search_pattern ", search_pattern)
         for file_path in matching_files:
            print(file_path)
    if len(matching_files) == 0 :
        print("get_voxel_info, lattice-info not found")
        return
    if len(matching_files) > 1 :
        print("get_voxel_info, multiple lattice-info files found")
        return 
    
    lattice_info={}
    try:
        with open(matching_files[0], 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split()
                i = 0
                while i < len(parts):
                    key = parts[i]
                    if key in ['nx', 'ny', 'nz', 'nTot']:
                        lattice_info[key] = int(parts[i + 1])
                        i += 2
                    elif key in ['xmi', 'ymi', 'zmi', 'xma', 'yma', 'zma', 'dx', 'dy', 'dz']:
                        lattice_info[key] = float(parts[i + 1])
                        i += 2
                    else:
                        i += 1  # Move to the next part if key is not recognized
    except e:
        print("get_lattice_info ", e)
    return lattice_info
########################################################################################################    
#
########################################################################################################    
def get_scan_numbers(xnat_session, project, experiment, xnat_url, scan_type):
 # Select project and experiment
    project_obj    = xnat_session.projects[project]
    experiment_obj = project_obj.experiments[experiment]

     # Iterate over scans to find the correct scan type
    scan_ids = []
    for scan in experiment_obj.scans.values():
         #print("scan ", scan, "scan.type ", scan.type, ' scan.id ', scan.id )
         if scan.type == scan_type:
             # Retrieve all files for this scan
             scan_ids.append(scan.id)
    return scan_ids
########################################################################################################    
#
########################################################################################################    
def get_voxel_index(apid,aplan,indices):
    lattice_info = get_lattice_info(apid,aplan)
    
    if lattice_info == None:
        print("get_voxel_indices, lattice_info not found ")
        return (-1,-1,-1)
    
    nx   = int(lattice_info['nx'])
    ny   = int(lattice_info['ny'])
    nz   = int(lattice_info['nz'])

    if len(indices)!= 3:
        print("Wrong dimensions of indices ", indices )        
    index = indices[2]*(nx*ny)+indices[1]*nx+indices[0] ;
    return index

########################################################################################################    
#
########################################################################################################    
def get_voxel_indices(apid,aplan,voxel):
    lattice_info = get_lattice_info(apid,aplan)
    
    if lattice_info == None:
        print("get_voxel_indices, lattice_info not found ")
        return (-1,-1,-1)
    
    nx   = int(lattice_info['nx'])
    ny   = int(lattice_info['ny'])
    nz   = int(lattice_info['nz'])
    nxny = int(lattice_info['nx'])*int(lattice_info['ny'])
    #print(" voxel ", voxel, "nxny ",nxny)
    iz      = int(int(voxel)/nxny);
    oIndex2 = int(int(voxel)-iz*nxny);
    iy = int(oIndex2/nx);
    ix = int(oIndex2-iy*nx);
    return (ix,iy,iz)

########################################################################################################    
#
########################################################################################################    
def get_voxel_indices_bare(lattice_info,voxel):
    
    nx   = int(lattice_info['nx'])
    ny   = int(lattice_info['ny'])
    nz   = int(lattice_info['nz'])
    nxny = int(lattice_info['nx'])*int(lattice_info['ny'])
    #print(" voxel ", voxel, "nxny ",nxny)
    iz      = int(int(voxel)/nxny);
    oIndex2 = int(int(voxel)-iz*nxny);
    iy = int(oIndex2/nx);
    ix = int(oIndex2-iy*nx);
    return (ix,iy,iz)


########################################################################################################    
#
########################################################################################################    
def get_voxel_position(apid,aplan,voxel):
    
    lattice_info = get_lattice_info(apid,aplan)
    if lattice_info == None:
        print("get_voxel_indices, lattice_info not found ")
        return (-1,-1,-1)
    indices = get_voxel_indices_bare(lattice_info,voxel)
    
    xmi = float(lattice_info['xmi'])
    ymi = float(lattice_info['ymi'])
    zmi = float(lattice_info['zmi'])
    dx  = float(lattice_info['dx'])
    dy  = float(lattice_info['dy'])
    dz  = float(lattice_info['dz'])

    x  = xmi + (indices[0]+0.5)*dx
    y  = ymi + (indices[1]+0.5)*dy
    z  = zmi + (indices[2]+0.5)*dz
     
    return (x,y,z)
########################################################################################################    
#
########################################################################################################    
   
def get_voxel_spectra ( fileName, voxel=None, beam=None ):
    if voxel == None :
       voxel=1000
    histos, delta_e = read_bin_spectra(fileName)
    #print("after calling find_voxel_spectra len ", len(histos))
    if voxel<0 or voxel >= len(histos):
       print("voxel ", voxel," out of range")
       return None, None
    return histos[voxel], delta_e
########################################################################################################    
#
########################################################################################################    

def get_voxel_spectra_histos ( apid, aplan, voxel=None, beam=None ):
    expDir=find_plan_directory(apid,aplan)
    files = find_voxel_spectra_files(expDir,beam)
    if len(files) > 0 :
        sum_histos = None  
        for file_path in files:
            histograms, delta_e = get_voxel_spectra(file_path,3400)
            if verbose > 0: 
               print(file_path)
               print("histograms ", histograms)

            if sum_histos is None:
               sum_histos = histograms
            else:
               if verbose > 1: print("lengh histos ",len(histograms))
               max_length = max(len(sum_histos), len(histograms))
               sum_histos = tuple(sum(x) for x in zip(
                   sum_histos + (0,) * (max_length - len(sum_histos)),
                   histograms + (0,) * (max_length - len(histograms))
               ))
    return sum_histos
########################################################################################################    
#
########################################################################################################    

def plot_dose_slice(dicom_file, slice_index):
    # Load the DICOM RTDOSE file
    ds = pydicom.dcmread(dicom_file)

    # Get dose data
    dose_data = ds.pixel_array  # Assuming dose values are stored as pixel_array

    # Get slice thickness (assuming it's along the z-axis)
    slice_thickness = ds.GridFrameOffsetVector[1] - ds.GridFrameOffsetVector[0]

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.imshow(dose_data[:, :, slice_index], cmap='jet', interpolation='nearest', origin='lower')
    plt.colorbar(label='Dose (Gy)')
    plt.title(f"Dose Distribution - Slice {slice_index} (z = {slice_index * slice_thickness} mm)")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
########################################################################################################    
#
########################################################################################################    

def plot_accumulated_dose(dicom_files, slice_index):
    accumulated_dose, slice_thickness = accumulate_dose_from_files(dicom_files)

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.imshow(accumulated_dose[:, :, slice_index], cmap='jet', interpolation='nearest', origin='lower')
    plt.colorbar(label='Accumulated Dose (Gy)')
    plt.title(f"Accumulated Dose Distribution - Slice {slice_index} (z = {slice_index * slice_thickness} mm)")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
########################################################################################################    
#
########################################################################################################    
def read_bin_spectra(file_name):
    histos = []
    delta_e = 0

    with open(file_name, 'rb') as fin:
        # Read the number of voxels in structures
        n_voxels_in_structures = struct.unpack('i', fin.read(4))[0]
        if verbose>1: print(f'nVoxelsInStructures: {n_voxels_in_structures}')


        # Read deltaE
        delta_e = struct.unpack('f', fin.read(4))[0]
        if verbose>1: print(f'deltaE: {delta_e}')
        # Read arrayStruct
        array_struct = struct.unpack(f'{n_voxels_in_structures}i', fin.read(n_voxels_in_structures * 4))
        # Read spectraPointers
        spectra_pointers = struct.unpack(f'{n_voxels_in_structures}i', fin.read(n_voxels_in_structures * 4))
        # Read histograms
        for i in range(n_voxels_in_structures):
            if spectra_pointers[i] > 0:
                fin.seek(spectra_pointers[i])
                n_bins = struct.unpack('i', fin.read(4))[0]
                if n_bins < 1:
                    continue
                entries = struct.unpack(f'{n_bins}i', fin.read(n_bins * 4))
                histos.append(entries)

    return histos, delta_e
################################################################################################
#
################################################################################################
def upload_file_to_xnat(xnat_session, project_id, experiment_id, scan_id, resource, file_name):
    #scan = xnat_session.projects[project_id].subjects[subject_id].experiments[experiment_id].scans[scan_id]
    scan = xnat_session.projects[project_id].experiments[experiment_id].scans[scan_id]

    file_resource = scan.resources.get(resource)
    if file_resource is None:
        try:
           file_resource = scan.create_resource(resource)
        except Exception as e:
            try:
                file_resource = scan.resources.get(resource)
            except Exception as e:
               print(" problem creating resource ", e )

    try: 
       file_resource.upload(file_name, os.path.basename(file_name))
    except Exception as e:
       print(" problem ", e )
