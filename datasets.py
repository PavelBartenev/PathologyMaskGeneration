from torch.utils.data import Dataset
import os
import nibabel as nib


class TrainPatchesDataset(Dataset):
    def __init__(self, dir_path, return_numpy=True):
        self.dir_path = dir_path
        self.filenames = os.listdir(f"{dir_path}/original")
        self.return_numpy = return_numpy
        self.getbyname_flag=False
        self.cur_filename = ''

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        filename = self.filenames[idx] if not self.getbyname_flag else self.cur_filename
        self.getbyname_flag = False
        
        orig = nib.load(f"{self.dir_path}/original/{filename}")
        label = nib.load(f"{self.dir_path}/labels/{filename}")
        opposite = nib.load(f"{self.dir_path}/opposite/{filename}")
        prob_mask = nib.load(f"{self.dir_path}/prob_mask/{filename}")

        if os.path.isfile(f"{self.dir_path}/flair/{filename}"):
            flair = nib.load(f"{self.dir_path}/flair/{filename}")
        else:
            flair = None

        if self.return_numpy:
            return {'patch' : orig.get_fdata(), 'mask' : label.get_fdata(), 'opposite_patch' : opposite.get_fdata(), 'flair': flair.get_fdata() if flair is not None else flair, 'filename' : filename, 'prob_mask': prob_mask}
        else:
            return {'patch' : orig, 'mask' : label, 'opposite_patch' : opposite, 'flair': flair, 'filename' : filename, 'prob_mask': prob_mask}

    def getbyname(self, filename):
        self.getbyname_flag=True
        self.cur_filename = filename
        return self[0]


class PathologicalMRIDataset(Dataset):
    def __init__(self, dir_path, return_numpy=True):
        self.dir_path = dir_path
        self.filenames = os.listdir(f"{dir_path}/mri")
        self.return_numpy = return_numpy
        
    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        filename = self.filenames[idx]
        maskname = filename.split('-')[1].split('_')[0] + ".nii.gz"
        orig = nib.load(f"{self.dir_path}/mri/{filename}")
        label = nib.load(f"{self.dir_path}/label/{maskname}")
        
        if self.return_numpy:
            return {'mri' : orig.get_fdata(), 'mask' : label.get_fdata(), 'filename' : filename}
        else:
            return {'mri' : orig, 'mask' : label, 'filename' : filename}


class HealthyMRIDataset(Dataset):
    def __init__(self, mri_path, mask_path=None, patch_mask_path=None, return_numpy=True):
        self.mri_path = mri_path
        self.mask_path = mask_path
        self.patch_mask_path = patch_mask_path
        self.filenames = os.listdir(mri_path)
        self.return_numpy = return_numpy

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        filename = self.filenames[idx] 
        maskname = filename.split('.')[0] + "-mask.nii.gz" 
        patchmaskname = filename.split('.')[0] + "-patch-mask.nii.gz" 
        
        if "_fl_" in filename: # in case of flair modality, masknames correspond to t1 filenames
            maskname = maskname.replace("_fl_", "_t1_")
            patchmaskname = patchmaskname.replace("_fl_", "_t1_")
            
        orig = nib.load(f"{self.mri_path}/{filename}")
        mask = nib.load(f"{self.mask_path}/{maskname}") if self.mask_path is not None else None
        patch_mask = nib.load(f"{self.patch_mask_path}/{patchmaskname}") if self.patch_mask_path is not None else None
            
        if self.return_numpy:
            return {'mri' : orig.get_fdata(), 'mask' : mask.get_fdata() if mask is not None else mask, 
                    'patch_mask' : patch_mask.get_fdata() if patch_mask is not None else patch_mask, 'filename' : filename}
        else:
            return {'mri' : orig, 'mask' : mask, 'patch_mask': patch_mask, 'filename' : filename}










        


            