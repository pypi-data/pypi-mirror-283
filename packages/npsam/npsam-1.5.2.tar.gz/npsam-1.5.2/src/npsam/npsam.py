# Standard library imports
import os, sys, warnings, gc
from pathlib import Path
from time import time

# Third-party imports

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import skimage
import math
import scipy
import tifffile
import torch
from ultralytics import FastSAM
from ultralytics.models.fastsam import FastSAMPrompt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.widgets import Button, RadioButtons, RangeSlider, Slider
from PyQt5.QtWidgets import QFileDialog, QApplication
from skimage.measure import label, regionprops_table
from datetime import datetime
from PIL import Image
from rsciio import emd, digitalmicrograph, tia

try:
    from .segment_anything import sam_model_registry, SamAutomaticMaskGenerator
    from .utils import *
except ImportError:
    from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
    from utils import *


def get_file_path(directory='./'):
    app = QApplication(sys.argv)
    fname = QFileDialog.getOpenFileNames(None, "Select a file...", directory,
                                         filter="Image files (*.png *.jpg *.jpeg *.tif *.tiff);;All files (*)")
    print(f'filepath = {fname[0]}'.replace(', ', ',\n'))
    return fname[0]


def get_directory_path(directory='./'):
    app = QApplication([])
    folder = QFileDialog.getExistingDirectory(None, "Select a folder...", directory)
    print(f'filepath = "{folder}"')
    return folder


def file_converter(filepath):
    filepath = Path(filepath).absolute()
    folder_path = os.path.dirname(filepath.as_posix())
    image_list = []
    try:
        if filepath.suffix == '.emd':
            file_dict = emd.file_reader(filepath.as_posix())
            for i in range(len(file_dict)):
                data_type = file_dict[i].get('metadata').get('General').get('title')

                if data_type in {'HAADF', 'Ceta'}:
                    title = file_dict[i].get('metadata').get('General').get('original_filename').split('.')[
                                0] + '_' + data_type
                    data = file_dict[i].get('data')
                    data = data.astype(np.uint16)
                    image = Image.fromarray(data)
                    image.save(Path(folder_path, f'{title}.png'))
                    image_list.append(str(Path(folder_path, f"{title}.png")))
                    try:
                        scale = round(file_dict[i].get('axes')[0].get('scale'), 3)
                        unit = file_dict[i].get('axes')[0].get('units')
                        dict = {"scale": scale, "unit": unit}
                        save_dictionary(str(Path(folder_path, f'{title}.png')), dict)
                    except:
                        print('Could not find scaling.')

        elif filepath.suffix in {'.dm3', '.dm4'}:
            file_dict = digitalmicrograph.file_reader(filepath.as_posix())
            for i in range(len(file_dict)):
                data_type = file_dict[i].get('metadata').get('General').get('title')
                title = file_dict[i].get('metadata').get('General').get('original_filename').split('.')[
                            0] + '_' + data_type
                data = file_dict[i].get('data')[0]
                data = data.astype(np.uint32)
                image = Image.fromarray(data)
                image.save(Path(folder_path, f'{title}.png'))
                image_list.append(str(Path(folder_path, f"{title}.png")))
                for j in range(len(file_dict[i].get('axes'))):
                    if file_dict[i].get('axes')[j].get('name') in {'y', 'x'}:
                        try:
                            scale = round(file_dict[i].get('axes')[j].get('scale'), 3)
                            unit = file_dict[i].get('axes')[j].get('units')
                            dict = {"scale": scale, "unit": unit}
                            save_dictionary(str(Path(folder_path, f'{title}.png')), dict)
                        except:
                            print('Could not find scaling.')

        elif filepath.suffix == '.emi':
            file_dict = tia.file_reader(filepath.as_posix())
            for i in range(len(file_dict)):
                title = file_dict[i].get('metadata').get('General').get('original_filename')
                data = file_dict[i].get('data')
                data = data.astype(np.uint16)
                image = Image.fromarray(data)
                image.save(Path(folder_path, f'{title}.png'))
                image_list.append(str(Path(folder_path, f"{title}.png")))
                try:
                    scale = round(file_dict[i].get('axes')[0].get('scale'), 3)
                    unit = file_dict[i].get('axes')[0].get('units')
                    dict = {"scale": scale, "unit": unit}
                    save_dictionary(str(Path(folder_path, f'{title}.png')), dict)
                except:
                    print('Could not find scaling.')
        plot_images(image_list)
        return print(f'The following image(s) were detected \nfilepath = {image_list}')

    except Exception as e:
        print(f'Could not extract image from file, please convert the file in other ways')


def SAM(filepath, device='cpu', SAM_model='auto', PPS=64, shape_filter=True,
        crop_and_enlarge=False, invert=False, double=False, min_mask_area=35, print_statement=True, **kwargs):
    '''SAM makes masks of the image
    Takes an image as input given as a filepath.
    Device can be default:'cpu' or 'cuda'
    PPS (points per side) number of sampling points default 64
    Saves the masks as a compressed numpy array file to easier load it later
    '''
    filepaths = process_filepath(filepath)
    try:
        sam_checkpoint, model_type, model_name = choose_SAM_model(SAM_model, device)
    except TypeError:
        return print('Cannot run SAM because no weight is chosen.')

    for n, filepath in enumerate(filepaths):
        files_folder = Path(filepath).parent / (Path(filepath).stem + '_files')
        files_folder.mkdir(exist_ok=True)
        if crop_and_enlarge or invert:
            image_filepaths = preprocess(filepath, crop_and_enlarge=crop_and_enlarge, invert=invert, double=double)
        else:
            image_filepaths = [filepath]

        if len(filepaths) > 1:
            print(f'{n + 1}/{len(filepaths)} - Now working on: {Path(filepath).stem}')

        for image_filepath in image_filepaths:
            if not Path(image_filepath).is_file():
                print(f'Error: {Path(image_filepath).as_posix()} was not found or is not a file.')
                return None

            image = load_image(image_filepath)

            if model_type == 'fast':
                start = time()
                fast_sam = FastSAM(sam_checkpoint)

                results = fast_sam(
                    source=image,
                    device=device,
                    retina_masks=True,  # imgsz=image.shape[0],
                    imgsz=int(np.ceil(max(image.shape[0], image.shape[1]) / 32) * 32),
                    conf=0.2,
                    iou=0.9,
                    verbose=False)

                prompt_process = FastSAMPrompt(image, results, device=device)

                masks = prompt_process.everything_prompt()[0].masks.data.cpu().numpy().transpose(1, 2, 0).astype(
                    np.uint8)

                list_of_masks = [masks[:, :, i] for i in range(masks.shape[2]) if masks[:, :, i][:, 0].sum() +
                                 masks[:, :, i][:, -1].sum() + masks[:, :, i][0, :].sum() + masks[:, :, i][-1,
                                                                                            :].sum() == 0]
            else:
                start = time()

                # set up model
                sam = sam_model_registry[model_type](checkpoint=sam_checkpoint).to(device=device)

                mask_generator = SamAutomaticMaskGenerator(sam, points_per_side=PPS, min_mask_region_area=min_mask_area,
                                                           **kwargs)

                masks = mask_generator.generate(image)

                list_of_masks = [mask['segmentation'].astype(np.uint8) for mask in masks if
                                 mask['segmentation'][:, 0].sum() +
                                 mask['segmentation'][:, -1].sum() + mask['segmentation'][0, :].sum() +
                                 mask['segmentation'][-1, :].sum() == 0]

            if shape_filter:
                list_of_filtered_masks = []
                for i in range(len(list_of_masks)):
                    labels_of_masks = skimage.measure.label(list_of_masks[i])
                    props = skimage.measure.regionprops_table(labels_of_masks, properties=['label', 'area', 'solidity'])
                    if len(props.get('label')) == 1 and (props.get('area') < 400 or props.get('solidity') > 0.95):
                        list_of_filtered_masks.append(list_of_masks[i])
                list_of_masks = list_of_filtered_masks

            if len(list_of_masks) == 0:
                elapsed_time = time() - start
                print(
                    f'{len(list_of_masks)} masks found for {Path(image_filepath).name}, so no masks were saved.\nIt took {format_time(elapsed_time)}')
            else:
                array_of_masks = np.stack(list_of_masks, axis=-1)
                file_p = files_folder / (Path(image_filepath).stem + '_array_of_masks.npz')
                np.savez_compressed(file_p, array=array_of_masks)
                segmentation = (model_name + f', PPS={PPS}' if model_name != 'fast' else model_name) + \
                               (', C&E' if crop_and_enlarge else '') + (', inverted' if invert else '')
                save_dictionary(filepath, {'segmentation': segmentation})
                elapsed_time = time() - start
                print(f'{len(list_of_masks)} masks found. It took {format_time(elapsed_time)}')
            if crop_and_enlarge:
                os.remove(image_filepath)
            if device in {'cuda', 'cuda:0'}:
                gc.collect()
                torch.cuda.empty_cache()

        if crop_and_enlarge:
            stitch_crops_together(filepath, image_filepaths)
        elif invert:
            if double:
                stitch_crops_together(filepath, image_filepaths, double=double, print_statement=print_statement)
            else:
                file_p = files_folder / (Path(image_filepath).stem + '_array_of_masks.npz')
                if (files_folder / (Path(filepath).stem + '_array_of_masks.npz')).is_file():
                    (files_folder / (Path(filepath).stem + '_array_of_masks.npz')).unlink()
                file_p.rename(files_folder / (Path(filepath).stem + '_array_of_masks.npz'))


def import_segmentation(filepath, seg_filepath=None):
    filepaths = process_filepath(filepath)
    if seg_filepath:
        seg_filepaths = process_filepath(seg_filepath)

    for n, filepath in enumerate(filepaths):
        files_folder = Path(filepath).parent / (Path(filepath).stem + '_files')
        file_p = files_folder / (Path(filepath).stem + '_array_of_masks.npz')
        if file_p.is_file():
            overwrite = input(
                f'Importing another segmentation will delete {file_p.name} (which is produced when running SAM()). Continue (y/n)?')
            if overwrite == 'y':
                file_p.unlink()
            else:
                print('import_segmentation() was interupted.')
                return None
        if seg_filepath:
            segmentation = load_image(seg_filepaths[n])
        else:
            print(f'Please select the segmentation image for {Path(filepath).name} in the dialogue window.', end=' ')
            app = QApplication(sys.argv)
            fname = QFileDialog.getOpenFileName(None, f'Select the segmentation image for {Path(filepath).name}...',
                                                './',
                                                filter="Image files (*.png *.jpg *.jpeg *.tif *.tiff);;All files (*)")
            segmentation = load_image(fname[0])
        segmentation = segmentation[:, :, 0] > 0
        labels = label(segmentation)
        array_of_masks = np.dstack([labels == n for n in range(1, labels.max() + 1)])
        file_p = files_folder / (Path(filepath).stem + '_array_of_masks.npz')
        np.savez_compressed(file_p, array=array_of_masks)
        segmentation = 'Imported from file'
        save_dictionary(filepath, {'segmentation': segmentation})
        print('Import completed.')


def mask_plot(filepath, label_cmap='default', figsize=[8, 4]):
    if label_cmap == 'default':
        label_cmap = make_randomized_cmap()

    filepaths = process_filepath(filepath)

    for filepath in filepaths:
        if not Path(filepath).is_file():
            print(f'Error: {Path(filepath).as_posix()} was not found or is not a file.')
            return None

        files_folder = Path(filepath).parent / (Path(filepath).stem + '_files')

        file_p = files_folder / (Path(filepath).stem + '_array_of_masks.npz')
        masks = np.load(file_p)['array']
        masks = np.moveaxis(masks, -1, 0)
        weights = np.arange(1, masks.shape[0] + 1)[:, np.newaxis, np.newaxis]
        weighted_masks = masks * weights
        labels = np.sum(weighted_masks, axis=0)

        img = load_image(filepath)
        if 'inverted' in load_dictionary(filepath).get('segmentation'):
            img_inverted = load_image((files_folder / (Path(filepath).stem + '_inverted.png')).as_posix())
            figsize[0] = 12
            fig, ax = plt.subplots(1, 3, figsize=figsize)

            ax[0].imshow(img, cmap='gray')
            ax[0].axis('off')

            ax[1].imshow(img_inverted, cmap='gray')
            ax[1].axis('off')

            ax[2].imshow(labels, cmap=label_cmap, interpolation='nearest')
            ax[2].axis('off')
        else:
            fig, ax = plt.subplots(1, 2, figsize=figsize)
            ax[0].imshow(img, cmap='gray')
            ax[0].axis('off')

            ax[1].imshow(labels, cmap=label_cmap, interpolation='nearest')
            ax[1].axis('off')

        plt.suptitle(Path(filepath).name)
        plt.tight_layout()
        plt.show()


def properties(filepath, scaling=True, unit='nm', stepsize=1, print_statement=True):
    filepaths = process_filepath(filepath)
    if unit == 'um':
        unit = 'µm'

    auto = False
    scalings = []
    if scaling is True:
        for filepath in filepaths:
            if 'scale' in load_dictionary(filepath):
                auto = True
    if auto and scaling is True:
        ask_for_auto_scaling = input(f'A scaling has been detected, do you want to use it? (y/n):')
        if ask_for_auto_scaling == 'y':
            for filepath in filepaths:
                if 'scale' in load_dictionary(filepath):
                    scalings.append(float(load_dictionary(filepath).get('scale')))
                    unit = load_dictionary(filepath).get('unit')
        if ask_for_auto_scaling == 'n':
            auto = False
    if type(scaling) == bool and auto is False:
        if scaling:
            if len(filepaths) > 1:
                ask_for_common_scaling = input(f'Is the scaling for all the images? (y/n):')
            elif len(filepaths) == 1:
                ask_for_common_scaling = 'n'
            else:
                print('Error: no filepaths in filepath.')
                return None
            while True:
                unit = input('Please provide the units of the image(s) (um (µm) / nm):')
                if unit == 'um':
                    unit = 'µm'
                if unit in {'µm', 'nm', 'px'}:
                    break

            if ask_for_common_scaling == 'y':
                scale_str = input(f'Insert the scaling for the images in pixels per {unit}:')
                scale_float = float(scale_str.split("/")[0]) / float(
                    scale_str.split("/")[1]) if "/" in scale_str else float(scale_str)
                scalings = len(filepaths) * [scale_float]
            elif ask_for_common_scaling == 'n':
                for filepath in filepaths:
                    scale_str = input(f'Insert the scaling for {Path(filepath).name} in pixels per {unit}:')
                    scale_float = float(scale_str.split("/")[0]) / float(
                        scale_str.split("/")[1]) if "/" in scale_str else float(scale_str)
                    scalings.append(scale_float)
            else:
                print('Invalid input. Try again.')
                return None
        else:
            unit = 'px'
            scalings = len(filepaths) * [1]

    elif type(scaling) == list and auto is False:
        if len(scaling) == len(filepaths):
            scalings = [float(scale_factor) for scale_factor in scaling]
        else:
            print('Error: The length of the scaling list is not equal to the number of images.')
            return None

    elif type(scaling) in {int, float} and auto is False:
        if len(filepaths) >= 1:
            scalings = len(filepaths) * [float(scaling)]
        else:
            print('Error: No filepaths in filepath.')
            return None

    if scaling:
        print('The following scalings will be used for the given image(s):')
        for (scale_factor, filepath) in zip(scalings, filepaths):
            print(f'{scale_factor} pixels per {unit} for {Path(filepath).name}')

    for n, filepath in enumerate(filepaths):
        start = time()
        if not Path(filepath).is_file():
            print(f'Error: {Path(filepath).as_posix()} was not found or is not a file.')
            return None

        image = load_image(filepath)

        files_folder = Path(filepath).parent / (Path(filepath).stem + '_files')

        file_p = files_folder / (Path(filepath).stem + '_array_of_masks.npz')
        masks = np.load(file_p)['array']

        print(f'Finding mask properties in {Path(filepath).name}:')
        dfs_properties = []
        for m, mask in enumerate(np.moveaxis(masks, -1, 0)):
            if print_statement:
                print(f'Mask {m + 1}/{masks.shape[-1]}', sep=',',
                  end='\r' if m + 1 < masks.shape[-1] else '\n', flush=True)
            dfs_properties.append(pd.DataFrame(regionprops_table(mask.astype('uint8'), image[:, :, 0], properties=
            ('area', 'area_convex', 'axis_major_length', 'axis_minor_length', 'bbox', 'centroid', 'centroid_local',
             'centroid_weighted', 'eccentricity', 'equivalent_diameter_area', 'euler_number', 'extent',
             'feret_diameter_max', 'inertia_tensor', 'inertia_tensor_eigvals', 'intensity_max', 'intensity_mean',
             'intensity_min', 'moments_hu', 'moments_weighted_hu', 'orientation', 'perimeter',
             'perimeter_crofton', 'solidity'))))
        df = pd.concat(dfs_properties)
        df['unit'] = unit
        df['mask'] = np.arange(df.shape[0])
        df['mask_index'] = np.arange(df.shape[0])
        column_to_move = df.pop("mask_index")
        df.insert(0, "mask_index", column_to_move)
        df = df.set_index('mask')

        pixels_per_unit = scalings[n]
        units_per_pixel = 1 / pixels_per_unit
        df['num_pixels'] = df['area'].astype(int)
        for property in ['equivalent_diameter_area', 'feret_diameter_max',
                         'perimeter', 'perimeter_crofton']:
            df[property] *= units_per_pixel
        for property in ['area', 'area_convex']:
            df[property] *= units_per_pixel ** 2
        df['scaling [px/unit]'] = pixels_per_unit

        df = df.round({
            'area': 1, 'area_convex': 1, 'axis_major_length': 1,
            'axis_minor_length': 1, 'centroid-0': 1, 'centroid-1': 1,
            'centroid_local-0': 1, 'centroid_local-1': 1,
            'centroid_weighted-0': 1, 'centroid_weighted-1': 1, 'eccentricity': 3,
            'equivalent_diameter_area': 1, 'extent': 3, 'feret_diameter_max': 1,
            'inertia_tensor-0-0': 1, 'inertia_tensor-0-1': 1,
            'inertia_tensor-1-0': 1, 'inertia_tensor-1-1': 1,
            'inertia_tensor_eigvals-0': 1, 'inertia_tensor_eigvals-1': 1,
            'intensity_max': 1, 'intensity_mean': 1, 'intensity_min': 1,
            'moments_hu-0': 3, 'moments_hu-1': 3, 'moments_hu-2': 3,
            'moments_hu-3': 3, 'moments_hu-4': 3, 'moments_hu-5': 3,
            'moments_hu-6': 3, 'moments_weighted_hu-0': 3,
            'moments_weighted_hu-1': 3, 'moments_weighted_hu-2': 3,
            'moments_weighted_hu-3': 3, 'moments_weighted_hu-4': 3,
            'moments_weighted_hu-5': 3, 'moments_weighted_hu-6': 3,
            'orientation': 3, 'perimeter': 1, 'perimeter_crofton': 1,
            'scaling [px/unit]': 2, 'solidity': 3})

        print('Detecting areas with overlap.')
        flattened_multiple_masks = masks[masks.sum(axis=-1) > 1]
        unique_multiple_masks = nb_unique_caller(flattened_multiple_masks[::stepsize])

        print('Processing areas with overlap:')

        df['overlap'] = 0
        df['overlapping_masks'] = [set() for _ in range(len(df))]

        overlap_counts = np.zeros(len(df), dtype=int)

        for n, unique in enumerate(unique_multiple_masks):
            if print_statement:
                print(f'Area {n + 1}/{len(unique_multiple_masks)}', sep=',',
                  end='\r' if n + 1 < len(unique_multiple_masks) else '\n', flush=True)

            mask_indices = np.where(unique)[0]

            for idx in mask_indices:
                df.at[idx, 'overlapping_masks'].update(mask_indices)

            summed_masks = masks[:, :, mask_indices].sum(axis=-1)
            overlaps = (summed_masks > 1).sum(axis=(0, 1))

            overlap_counts[mask_indices] += overlaps

        df['overlap'] = overlap_counts
        df['number_of_overlapping_masks'] = df['overlapping_masks'].apply(len)

        df['number_of_overlapping_masks'] = [len(masks) for masks in df['overlapping_masks'].to_list()]

        file_p = files_folder / (Path(filepath).stem + '_raw_dataframe.csv')
        df.to_csv(file_p, encoding='utf-8', header='true', index=False)
        save_dictionary(filepath, {'scale': pixels_per_unit, 'unit': unit})
        elapsed_time = time() - start
        print(f'Done. It took {format_time(elapsed_time)}.')


class ImageFilter:
    def __init__(self, filepath, image_number=1, label_cmap='default', app=False):
        if label_cmap == 'default':
            self.label_cmap = make_randomized_cmap()
        else:
            self.label_cmap = label_cmap

        self.image_number = image_number
        self.filepaths = process_filepath(filepath)
        self.app = app

        self.labels = None
        self.vmax = None
        self.image = None
        self.fig = None
        self.ax = None
        self.text = None
        self.filtered_label_image = None
        self.buttons = {}

        self.min_area = None
        self.max_area = None
        self.min_solidity = None
        self.max_solidity = None
        self.min_intensity = None
        self.max_intensity = None
        self.min_eccentricity = None
        self.max_eccentricity = None
        self.max_overlap = None
        self.overlapping_masks = None
        self.overlapping_masks_dict = {'All': "Not applied", '0': 0, '1': 2, '2': 3}

        self.ax_slider_area = None
        self.unit = None
        self.ax_slider_solidity = None
        self.ax_slider_intensity = None
        self.ax_slider_eccentricity = None
        self.ax_slider_overlap = None
        self.ax_radio_overlapping_masks = None
        self.ax_save = None
        self.ax_next = None
        self.ax_previous = None
        self.ax_return_all_removed = None
        self.ax_return_last_removed = None
        self.pressed_keys = set()
        self.last_interacted_slider = None

        self.slider_color = '#65B6F3'
        self.radio_color = '#387FBE'

        self.directory = Path(__file__).resolve().parent / 'button_images'

    def get_df_params(self):
        return ((self.df['area'] >= self.min_area) & (self.df['area'] <= self.max_area) &
                (self.df['solidity'] >= self.min_solidity) & (self.df['solidity'] <= self.max_solidity) &
                (self.df['intensity_mean'] >= self.min_intensity) & (self.df['intensity_mean'] <= self.max_intensity) &
                (self.df['eccentricity'] >= self.min_eccentricity) & (self.df['eccentricity'] <= self.max_eccentricity) &
                (~self.df['mask_index'].isin(self.removed_index)) &
                (self.df['number_of_overlapping_masks'] == self.overlapping_masks if type(self.overlapping_masks) == int
                 else self.df['number_of_overlapping_masks'] >= 0) & (self.df['overlap'] <= self.max_overlap))

    def plot_df(self, df):
        mask_indices = df.index.to_numpy().astype(np.uint16)

        selected_masks = self.weighted_masks_rebinned[mask_indices]

        self.filtered_label_image = np.sum(selected_masks, axis=0, dtype=np.uint16)

        self.fig.canvas.restore_region(self.background)
        self.im_lab.set_data(self.filtered_label_image)
        self.ax['left2'].draw_artist(self.im_lab)
        self.fig.canvas.blit(self.ax['left2'].bbox)
        
        self.text.set_text(f'{self.df.shape[0] - df.shape[0]} masks removed. {df.shape[0]} remain.')


    def create_button(self, x, y, w, h, default_img_path, hover_img_path, click_action, rotate=False):
        ax = plt.axes([x, y, w, h], frameon=False)
        ax.set_axis_off()

        default_img = mpimg.imread(self.directory / default_img_path)
        hover_img = mpimg.imread(self.directory / hover_img_path)
        if rotate:
            default_img = np.flipud(np.fliplr(default_img))
            hover_img = np.flipud(np.fliplr(hover_img))

        img_display = ax.imshow(default_img)

        self.buttons[ax] = {'default': default_img, 'hover': hover_img, 'display': img_display}
        ax.figure.canvas.mpl_connect('button_press_event', lambda event: self.on_button_click(event, ax, click_action))

    def on_hover(self, event):
        redraw_required = False
        for ax, img_info in self.buttons.items():
            if event.inaxes == ax:
                if not np.array_equal(img_info['display'].get_array(), img_info['hover']):
                    img_info['display'].set_data(img_info['hover'])
                    ax.draw_artist(img_info['display'])
                    redraw_required = True
            elif not np.array_equal(img_info['display'].get_array(), img_info['default']):
                img_info['display'].set_data(img_info['default'])
                ax.draw_artist(img_info['display'])
                redraw_required = True
        if redraw_required:
            if self.app is False:
                self.fig.canvas.update()
            else:
                self.fig.canvas.draw_idle()

    def on_button_click(self, event, ax, action):
        if event.inaxes == ax:
            action()

    def update_area(self, slider_area):
        self.last_interacted_slider = self.slider_area
        self.min_area = int(slider_area[0])
        self.max_area = int(slider_area[1])

        self.area_val_text.set_text(f"Area ({self.unit2}): ({self.min_area}, {self.max_area})")

        df_area = self.df.loc[self.get_df_params()]

        self.plot_df(df_area)

    def update_solidity(self, slider_solidity):
        self.last_interacted_slider = self.slider_solidity
        self.min_solidity = float(slider_solidity[0])
        self.max_solidity = float(slider_solidity[1])

        self.solidity_val_text.set_text(f"Solidity: ({self.min_solidity:.3f}, {self.max_solidity:.3f})")

        df_solidity = self.df.loc[self.get_df_params()]

        self.plot_df(df_solidity)

    def update_intensity(self, slider_intensity):
        self.last_interacted_slider = self.slider_intensity
        self.min_intensity = int(slider_intensity[0])
        self.max_intensity = int(slider_intensity[1])

        self.intensity_val_text.set_text(f"Intensity: ({self.min_intensity}, {self.max_intensity})")

        df_intensity = self.df.loc[self.get_df_params()]

        self.plot_df(df_intensity)

    def update_eccentricity(self, slider_eccentricity):
        self.last_interacted_slider = self.slider_eccentricity
        self.min_eccentricity = float(slider_eccentricity[0])
        self.max_eccentricity = float(slider_eccentricity[1])

        self.eccentricity_val_text.set_text(f"Eccentricity: ({self.min_eccentricity:.2f}, {self.max_eccentricity:.2f})")

        df_eccentricity = self.df.loc[self.get_df_params()]

        self.plot_df(df_eccentricity)

    def update_overlap(self, slider_overlap):
        self.last_interacted_slider = self.slider_overlap
        self.max_overlap = slider_overlap

        self.overlap_val_text.set_text(f"Overlap: {self.max_overlap}")

        df_overlap = self.df.loc[self.get_df_params()]

        self.plot_df(df_overlap)

    def update_overlapping_masks(self, label):
        self.overlapping_masks = self.overlapping_masks_dict[label]

        df_overlapping_masks = self.df.loc[self.get_df_params()]

        self.plot_df(df_overlapping_masks)

        self.fig.canvas.draw()

    def on_key_press(self, event):
        if self.last_interacted_slider == self.slider_overlap:
            high = self.last_interacted_slider.val
        else:
            low, high = self.last_interacted_slider.val
        self.pressed_keys.add(event.key)

        if self.last_interacted_slider == self.slider_eccentricity:
            step = 0.01
        elif self.last_interacted_slider == self.slider_solidity:
            step = 0.001
        else:
            step = 1
        if 'shift' in self.pressed_keys:
            if self.last_interacted_slider == self.slider_eccentricity:
                step = 0.1
            elif self.last_interacted_slider == self.slider_solidity:
                step = 0.005
            else:
                step = 10

        if event.key in {'left', 'right', 'up', 'down', 'shift+left', 'shift+right', 'shift+up', 'shift+down'}:
            if self.last_interacted_slider == self.slider_overlap:
                if event.key in {'up', 'shift+up'}:
                    val = high
                elif event.key in {'down', 'shift+down'}:
                    val = high
                elif event.key in {'right', 'shift+right'}:
                    val = high + step
                elif event.key in {'left', 'shift+left'}:
                    val = high - step
                self.last_interacted_slider.set_val(val)

            else:
                if event.key in {'up', 'shift+up'}:
                    val = (low + step, high)
                elif event.key in {'down', 'shift+down'}:
                    val = (low - step, high)
                elif event.key in {'right', 'shift+right'}:
                    val = (low, high + step)
                elif event.key in {'left', 'shift+left'}:
                    val = (low, high - step)
                self.last_interacted_slider.set_val(val)
        
        if event.key == 'z':
            self.return_last_removed()

        if event.key == 'a':
            self.return_all_removed()

        if event.key == 'enter':
            if self.image_number < len(self.filepaths):
                self.update_next()
            else:
                self.final_save()

        if event.key == 'backspace':
            if self.image_number != 1:
                self.update_previous()

    def on_key_release(self, event):
        if event.key in self.pressed_keys:
            self.pressed_keys.remove(event.key)

    def on_click(self, event):
        df = self.df.loc[self.get_df_params()]
        if event.inaxes == self.ax['left2']:
            for idx, row in df.iterrows():
                if row['bbox-1'] <= event.xdata <= row['bbox-3'] and row['bbox-0'] <= event.ydata <= row['bbox-2']:
                    self.removed_index.append(idx)

                    df_removed = self.df.loc[self.get_df_params()]

                    self.fig.canvas.draw_idle()

                    self.plot_df(df_removed)
                    break

    def return_all_removed(self):
        self.removed_index = []

        df_removed = self.df.loc[self.get_df_params()]

        self.fig.canvas.draw_idle()

        self.plot_df(df_removed)

    def return_last_removed(self):
        try:
            self.removed_index.pop()

            df_removed = self.df.loc[self.get_df_params()]

            self.fig.canvas.draw_idle()

            self.plot_df(df_removed)
        except IndexError:
            pass

    def update_button(self):
        df_filtered = self.df.loc[self.get_df_params()]
        self.plot_df(df_filtered)

        filters = {
            'min_area': self.min_area,
            'max_area': self.max_area,
            'min_solidity': self.min_solidity,
            'max_solidity': self.max_solidity,
            'min_intensity': self.min_intensity,
            'max_intensity': self.max_intensity,
            'min_eccentricity': self.min_eccentricity,
            'max_eccentricity': self.max_eccentricity,
            'scaling': self.df['scaling [px/unit]'].to_list()[0],
            'overlap': self.max_overlap,
            'overlapping_masks': self.overlapping_masks,
            'removed_list': self.removed_index,
            'removed': self.df.shape[0] - df_filtered.shape[0],
            'remain': df_filtered.shape[0],
            }

        self.file_p = self.files_folder / (Path(self.filepath).stem + '_filtered_dataframe.csv')
        df_filtered.to_csv(self.file_p, encoding='utf-8', header='true', index=False)
        save_dictionary(str(self.filepath), filters)

        self.filtered_label_image = np.zeros(self.weighted_masks[0].shape)
        for n in df_filtered.index.to_list():
            self.filtered_label_image += self.weighted_masks[n]
        self.file_p = self.files_folder / (Path(self.filepath).stem + '_filtered_masks.png')
        plt.imsave(self.file_p, self.filtered_label_image, cmap=self.label_cmap)
        self.file_p = self.files_folder / (Path(self.filepath).stem + '_filtered_masks.tif')
        tifffile.imwrite(self.file_p, self.filtered_label_image.astype('uint16'))
        self.file_p = self.files_folder / (Path(self.filepath).stem + '_filtered_binary_labels.tif')
        tifffile.imwrite(self.file_p, ((self.filtered_label_image > 0) * 255).astype('uint8'))

        plt.close()

    def final_save(self):
        self.update_button()

    def update_next(self):
        self.update_button()

        self.image_number += 1

        self.filter()

    def update_previous(self):
        self.update_button()

        self.image_number -= 1

        self.filter()

    def create_area_slider(self, ax):
        self.unit = self.df.loc[0, 'unit']
        self.unit2 = self.unit + "$^2$" if self.unit != "px" else self.unit

        self.slider_area = RangeSlider(ax, '', valmin=self.min_area, valmax=self.max_area, valstep=1,
                                       valinit=(self.min_area_init, self.max_area_init))
        self.slider_area.on_changed(self.update_area)

        self.area_val_text = ax.text(0, 1.12, f"Area ({self.unit2}): ({self.min_area}, {self.max_area})",
                                     fontsize=14, ha='left', va='center', transform=ax.transAxes)
        self.slider_area.valtext.set_visible(False)
        self.update_area((self.min_area_init, self.max_area_init))

    def create_solidity_slider(self, ax):
        self.slider_solidity = RangeSlider(ax, "", valmin=self.min_solidity, valmax=self.max_solidity, valstep=0.001,
                                           valinit=(self.min_solidity_init, self.max_solidity_init))
        self.slider_solidity.on_changed(self.update_solidity)

        self.solidity_val_text = ax.text(0, 1.12, f"Solidity: ({self.min_solidity:.3f}, {self.max_solidity:.3f})",
                                         fontsize=14, ha='left', va='center', transform=ax.transAxes)
        self.slider_solidity.valtext.set_visible(False)
        self.update_solidity((self.min_solidity_init, self.max_solidity_init))

    def create_intensity_slider(self, ax):
        self.slider_intensity = RangeSlider(ax, "", valmin=self.min_intensity, valmax=self.max_intensity,
                                            valstep=1, valinit=(self.min_intensity_init, self.max_intensity_init))
        self.slider_intensity.on_changed(self.update_intensity)

        self.intensity_val_text = ax.text(0, 1.12, f"Intensity slider: ({self.min_intensity}, {self.max_intensity})",
                                          fontsize=14, ha='left', va='center', transform=ax.transAxes)
        self.slider_intensity.valtext.set_visible(False)
        self.update_intensity((self.min_intensity_init, self.max_intensity_init))

    def create_eccentricity_slider(self, ax):
        self.slider_eccentricity = RangeSlider(ax, "", valmin=self.min_eccentricity, valmax=self.max_eccentricity,
                                               valstep=0.01,
                                               valinit=(self.min_eccentricity_init, self.max_eccentricity_init))
        self.slider_eccentricity.on_changed(self.update_eccentricity)

        self.eccentricity_val_text = ax.text(0, 1.12,
                                             f"Eccentricity: ({self.min_eccentricity:.2f}, {self.max_eccentricity:.2f})",
                                             fontsize=14, ha='left', va='center', transform=ax.transAxes)
        self.slider_eccentricity.valtext.set_visible(False)
        self.update_eccentricity((self.min_eccentricity_init, self.max_eccentricity_init))

    def create_overlap_slider(self, ax):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            self.slider_overlap = Slider(ax, '', valmin=0, valmax=self.max_overlap, valstep=1,
                                         valinit=self.max_overlap_init)
            self.slider_overlap.on_changed(self.update_overlap)

            self.overlap_val_text = ax.text(0, 1.12, f"Overlap: {self.max_overlap}",
                                            fontsize=14, ha='left', va='center', transform=ax.transAxes)
            self.slider_overlap.valtext.set_visible(False)
            self.slider_overlap.vline._linewidth = 0
            self.update_overlap(self.max_overlap_init)

    def create_overlapping_masks_radio(self, ax):
        ax.set_aspect('equal')
        if type(self.overlapping_masks_init) == str:
            self.overlapping_masks_init = -1
        elif self.overlapping_masks_init > 2:
            self.overlapping_masks_init = -1
        self.radio_overlapping_masks = RadioButtons(ax, ('All', '0', '1', '2'),
                                                    active=self.overlapping_masks_init + 1,
                                                    activecolor=self.radio_color)

        dists = [0, 0.12, 0.2245, 0.325]
        for i, (circle, label) in enumerate(
                zip(self.radio_overlapping_masks.circles, self.radio_overlapping_masks.labels)):
            new_x = 0.53 + dists[i]
            new_y = 0.5
            circle.set_center((new_x, new_y))
            circle.set_radius(0.02)
            label.set_position((new_x + 0.03, new_y))
            label.set_fontsize(14)

        self.overlapping_masks_val_text = ax.text(0, 0.5, "Number of overlapping masks:",
                                                  fontsize=14, ha='left', va='center', transform=ax.transAxes)

        self.radio_overlapping_masks.on_clicked(self.update_overlapping_masks)
        self.update_overlapping_masks(['All', '0', '1', '2'][self.overlapping_masks_init + 1])

    def initiate_filter_values(self):
        self.min_area_init = self.min_area
        self.max_area_init = self.max_area
        self.min_solidity_init = self.min_solidity
        self.max_solidity_init = self.max_solidity
        self.min_intensity_init = self.min_intensity
        self.max_intensity_init = self.max_intensity
        self.min_eccentricity_init = self.min_eccentricity
        self.max_eccentricity_init = self.max_eccentricity
        self.max_overlap_init = self.max_overlap
        self.overlapping_masks_init = self.overlapping_masks
        self.removed_index = []
        if 'min_area' in self.filters_init.keys():
            self.min_area_init = self.filters_init['min_area']
            self.max_area_init = self.filters_init['max_area']
            self.min_solidity_init = self.filters_init['min_solidity']
            self.max_solidity_init = self.filters_init['max_solidity']
            self.min_intensity_init = self.filters_init['min_intensity']
            self.max_intensity_init = self.filters_init['max_intensity']
            self.min_eccentricity_init = self.filters_init['min_eccentricity']
            self.max_eccentricity_init = self.filters_init['max_eccentricity']
            self.max_overlap_init = self.filters_init['overlap']
            self.overlapping_masks_init = self.filters_init['overlapping_masks']
            self.removed_index = self.filters_init['removed_list']

        df_init = self.df.loc[self.get_df_params()]

        self.plot_df(df_init)

    def start_plot(self, image, labels):
        self.fig, self.ax = plt.subplot_mosaic([['left', 'right'], ['left2', 'right2'], ['.', '.']],
                                               gridspec_kw=dict(height_ratios=[1, 1, 0.1]),
                                               constrained_layout=True, figsize=(12, 10))

        self.ax['left'].imshow(image, cmap='gray')
        self.vmax = labels.max()
        self.ax['right'].imshow(labels, cmap=self.label_cmap, interpolation='nearest', vmin=0, vmax=self.vmax)
        self.im_lab = self.ax['left2'].imshow(self.filtered_masks_rebinned, cmap=self.label_cmap,
                                              interpolation='nearest', vmin=0, vmax=self.vmax)

        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.ax['left2'].bbox)

        for axis in self.ax:
            self.ax[axis].axis('off')

        self.ax_slider_area = plt.axes([0.525, 0.430, 0.45, 0.03], facecolor=self.slider_color, zorder=1)
        self.ax_slider_solidity = plt.axes([0.525, 0.375, 0.45, 0.03], facecolor=self.slider_color, zorder=1)
        self.ax_slider_intensity = plt.axes([0.525, 0.320, 0.45, 0.03], facecolor=self.slider_color, zorder=1)
        self.ax_slider_eccentricity = plt.axes([0.525, 0.265, 0.45, 0.03], facecolor=self.slider_color, zorder=1)
        self.ax_slider_overlap = plt.axes([0.525, 0.210, 0.45, 0.03], facecolor=self.slider_color, zorder=1)
        self.ax_radio_overlapping_masks = plt.axes([0.525, -0.12, 0.5, 0.6], frameon=False)

        self.create_button(0.835, 0.01, 0.14, 0.085, 'Save_close.png', 'Save_close_dark.png', self.final_save)

        if self.image_number < len(self.filepaths):
            self.create_button(0.68, 0.01, 0.14, 0.085, 'arrow.png', 'arrow_dark.png', self.update_next)

        if self.image_number != 1:
            self.create_button(0.525, 0.01, 0.14, 0.085, 'arrow.png', 'arrow_dark.png', self.update_previous,
                               rotate=True)

        self.create_button(0.1, 0.0, 0.10, 0.05, 'plus_one.png', 'plus_one_dark.png', self.return_last_removed)

        self.create_button(0.3, 0.0, 0.10, 0.05, 'plus_all.png', 'plus_all_dark.png', self.return_all_removed)

        self.min_area = math.floor(self.df['area'].min())
        self.max_area = math.ceil(self.df['area'].max())

        self.min_intensity = math.floor(self.df['intensity_mean'].min())
        self.max_intensity = math.ceil(self.df['intensity_mean'].max())

        self.max_overlap = math.ceil(self.df['overlap'].max())

        self.text = self.fig.text(0.752, 0.12, '', fontsize=16, horizontalalignment='center')

        self.min_solidity = self.df['solidity'].min()
        self.max_solidity = self.df['solidity'].max()

        self.min_eccentricity = self.df['eccentricity'].min()
        self.max_eccentricity = self.df['eccentricity'].max()

        self.overlapping_masks = "Not applied"

        self.initiate_filter_values()

        self.create_solidity_slider(self.ax_slider_solidity)
        self.create_intensity_slider(self.ax_slider_intensity)
        self.create_eccentricity_slider(self.ax_slider_eccentricity)
        self.create_overlap_slider(self.ax_slider_overlap)
        self.create_area_slider(self.ax_slider_area)
        self.create_overlapping_masks_radio(self.ax_radio_overlapping_masks)

        string_title = f'{self.image_number}/{len(self.filepaths)} - {Path(self.filepath).stem}' if len(
            self.filepaths) > 1 else Path(self.filepath).stem

        plt.suptitle(string_title, fontsize=16)

        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_hover)
        if self.app is True:
            matplotlib.use('tkagg')
        plt.show()

    def filter(self):
        self.filepath = self.filepaths[self.image_number - 1]
        self.files_folder = Path(self.filepath).parent / (Path(self.filepath).stem + '_files')
        self.file_p = self.files_folder / (Path(self.filepath).stem + '_raw_dataframe.csv')
        self.df = pd.read_csv(self.file_p)
        self.removed_rows = pd.DataFrame(columns=self.df.columns)

        self.file_p = self.files_folder / (Path(self.filepath).stem + '_array_of_masks.npz')

        self.masks = np.load(self.file_p)['array']
        self.masks = np.moveaxis(self.masks, -1, 0)

        self.weights = (np.arange(1, self.masks.shape[0] + 1)[:, np.newaxis, np.newaxis]).astype(np.uint16)

        self.weighted_masks = self.masks * self.weights

        self.weighted_masks_rebinned = self.weighted_masks[:, ::4, ::4]

        self.labels = np.sum(self.weighted_masks, axis=0, dtype=np.uint16)

        self.filtered_masks_rebinned = self.labels

        self.image = load_image(self.filepath)

        self.filters_init = load_dictionary(str(self.filepath))

        self.start_plot(self.image, self.labels)


def manual_filter(filepath, conditions, label_cmap='default'):
    if label_cmap == 'default':
        label_cmap = make_randomized_cmap()
    filepaths = process_filepath(filepath)

    if type(conditions) == dict:
        conditions = [conditions] * len(filepaths)
        if len(filepaths) > 1:
            print('The filtering conditions will be used for all images.')
    elif type(conditions) == list:
        if len(conditions) == len(filepaths):
            for entry in conditions:
                if type(entry) != dict:
                    print('The list entries must be dictionaries containing the filter conditions.')
                    return None
        elif len(conditions) == 1:
            conditions = conditions * len(filepaths)
            print('The filtering conditions will be used for all images.')
        else:
            print(
                'The length of the list with filtering conditions does not have the same length as the list with image filepaths.')
            return None

    for filter_conditions, filepath in zip(conditions, filepaths):
        files_folder = Path(filepath).parent / (Path(filepath).stem + '_files')
        file_p = files_folder / (Path(filepath).stem + '_raw_dataframe.csv')
        df = pd.read_csv(file_p)

        file_p = files_folder / (Path(filepath).stem + '_array_of_masks.npz')
        masks = np.load(file_p)['array']
        masks = np.moveaxis(masks, -1, 0)
        weighted_masks = (masks * np.arange(1, masks.shape[0] + 1)[:, np.newaxis, np.newaxis])

        filters = {'min_area': math.floor(df['area'].min()),
                   'max_area': math.ceil(df['area'].max()),
                   'min_solidity': math.floor(df['solidity'].min()),
                   'max_solidity': math.ceil(df['solidity'].max()),
                   'min_intensity': math.floor(df['intensity_mean'].min()),
                   'max_intensity': math.ceil(df['intensity_mean'].max()),
                   'min_eccentricity': math.floor(df['eccentricity'].min()),
                   'max_eccentricity': math.ceil(df['eccentricity'].max()),
                   'overlap': math.ceil(df['overlap'].max()),
                   'overlapping_masks': "Not applied",
                   'scaling': df['scaling [px/unit]'].to_list()[1]}

        filters.update(filter_conditions)

        filtered_df = df[((df['area'] >= filters['min_area']) & (df['area'] <= filters['max_area']) &
                          (df['solidity'] >= filters['min_solidity']) & (df['solidity'] <= filters['max_solidity']) &
                          (df['intensity_mean'] >= filters['min_intensity']) & (
                                      df['intensity_mean'] <= filters['max_intensity']) &
                          (df['eccentricity'] >= filters['min_eccentricity']) & (
                                      df['eccentricity'] <= filters['max_eccentricity']) &
                          (df['number_of_overlapping_masks'] == filters['overlapping_masks'] if type(
                              filters['overlapping_masks']) == int
                           else df['number_of_overlapping_masks'] >= 0) & (df['overlap'] <= filters['overlap']))]

        filters.update({'removed': df.shape[0] - filtered_df.shape[0], 'remain': filtered_df.shape[0]})

        filtered_label_image = np.zeros(weighted_masks[0].shape)
        for n in filtered_df.index.to_list():
            filtered_label_image += weighted_masks[n]

        file_p = files_folder / (Path(filepath).stem + '_filtered_dataframe.csv')
        filtered_df.to_csv(file_p, encoding='utf-8', header='true', index=False)
        save_dictionary(filepath, filters)
        file_p = files_folder / (Path(filepath).stem + '_filtered_masks.png')
        plt.imsave(file_p, filtered_label_image, cmap=label_cmap)
        file_p = files_folder / (Path(filepath).stem + '_filtered_masks.tif')
        tifffile.imwrite(file_p, filtered_label_image.astype('uint16'))
        file_p = files_folder / (Path(filepath).stem + '_filtered_binary_labels.tif')
        tifffile.imwrite(file_p, ((filtered_label_image > 0) * 255).astype('uint8'))


def overview(filepath, property_list=['area'], bin_list=None, timestamp=False):
    filepaths = process_filepath(filepath)

    if property_list == ['all']:
        property_list = ['area', 'area_convex', 'axis_major_length', 'axis_minor_length',
                         'eccentricity', 'equivalent_diameter_area', 'extent', 'feret_diameter_max',
                         'intensity_max', 'intensity_mean', 'intensity_min', 'orientation',
                         'perimeter', 'perimeter_crofton', 'solidity', 'overlap']

    for n, property in enumerate(property_list):
        if property == 'intensity':
            property_list[n] = 'intensity_mean'
        elif property == 'diameter':
            property_list[n] = 'equivalent_diameter_area'
        elif property == 'max diameter':
            property_list[n] = 'feret_diameter_max'
        elif property == 'crofton perimeter':
            property_list[n] = 'perimeter_crofton'
        elif property == 'convex area':
            property_list[n] = 'area_convex'

    dfs = []
    imagenumber = 1
    for filepath in filepaths:
        files_folder = Path(filepath).parent / (Path(filepath).stem + '_files')
        file_p = files_folder / (Path(filepath).stem + '_filtered_dataframe.csv')
        df_filtered = pd.read_csv(file_p)
        df_filtered['imagename'] = Path(filepath).name
        df_filtered['imagenumber'] = imagenumber
        imagenumber += 1
        dfs.append(df_filtered)
    master_df = pd.concat(dfs)
    if len(filepaths) > 1:
        file_p = Path(filepaths[0]).parent / (Path(filepaths[0]).parent.name + '_overview_filtered_dataframe.csv')
        first_column = master_df.pop('imagename')
        second_column = master_df.pop('imagenumber')
        master_df.insert(0, 'imagename', first_column)
        master_df.insert(1, 'imagenumber', second_column)
        master_df.to_csv(file_p, encoding='utf-8', header='true', index=False)

    if bin_list is None:
        bin_list = ['auto'] * len(property_list)

    def save_image():
        if timestamp:
            d = datetime.now()
            stamp = str(d.year) + str(d.month) + str(d.day) + '-' + str(d.hour) + str(d.minute) + str(d.second)
            if len(filepaths) > 1:
                file_p = Path(filepaths[0]).parent / (Path(filepaths[0]).parent.name + '_overview' + stamp + '.pdf')
            else:
                file_p = files_folder / (Path(filepath).stem + '_overview' + stamp + '.pdf')
        else:
            if len(filepaths) > 1:
                file_p = Path(filepaths[0]).parent / (Path(filepaths[0]).parent.name + '_overview' + '.pdf')
            else:
                file_p = files_folder / (Path(filepath).stem + '_overview' + '.pdf')

        p = PdfPages(file_p)

        fig_nums = plt.get_fignums()
        figs = [plt.figure(n) for n in fig_nums]

        for fig in figs:
            fig.savefig(p, format='pdf')

        p.close()

    unit = master_df['unit'].to_list()[0]
    unit2 = unit + '$^2$' if unit != 'px' else unit
    name_dict = {'area': f'area ({unit2})', 'area_convex': f'convex area ({unit2})', 'eccentricity': 'eccentricity',
                 'solidity': 'solidity', 'intensity_mean': 'mean intensity', 'overlap': 'overlap (px)',
                 'equivalent_diameter_area': f'area equivalent diameter ({unit})',
                 'feret_diameter_max': f'Max diameter (Feret) ({unit})', 'orientation': 'orientation',
                 'perimeter': f'perimeter ({unit})', 'perimeter_crofton': f'crofton perimeter ({unit})',
                 'axis_major_length': f'Major axis length ({unit})', 'axis_minor_length': f'Minor axis length ({unit})',
                 'extent': 'Ratio of pixels in the mask the pixels in the bounding box',
                 'intensity_max': 'Max intensity of the mask',
                 'intensity_min': 'minimum intensity of the mask', 'overlap': f'amount of overlap ({unit2})'}
    for n, prop in enumerate(property_list):
        fig, ax = plt.subplots(figsize=(12, 9))
        ax.set_xlabel(name_dict.get(prop).capitalize(), fontsize=16)
        ax.set_title(f'Histogram of {name_dict.get(prop)} for all images', fontsize=18)
        master_df[prop].hist(bins=bin_list[n], ax=ax, edgecolor='k', color='#0081C6')
        ax.grid(False)
        ax.set_ylabel('Count', fontsize=16)
        ax.tick_params(axis='both', which='major', labelsize=14)
        data = master_df[prop]
        mean = np.mean(data)
        median = np.median(data)
        std_dev = np.std(data)
        variance = np.var(data)
        skewness = scipy.stats.skew(data)
        kurtosis = scipy.stats.kurtosis(data)
        data_range = np.ptp(data)
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = scipy.stats.iqr(data)
        minimum = np.min(data)
        maximum = np.max(data)
        count = len(data)
        total_sum = np.sum(data)
        coeff_variation = std_dev / mean

        def format_value(val):
            if val == 0:
                return 0
            elif val < 10:
                return f"{val:.2f}"
            elif 10 <= val < 100:
                return f"{val:.1f}"
            elif 100 <= val:
                return f"{int(val)}"

        x_r = 1 - len(f'Upper quantile: {format_value(q3)}') * 0.0108
        x_m = x_r - 0.025 - len(f'Sum: {format_value(total_sum)}') * 0.0108 if total_sum > 100000000 else x_r - 0.155
        x_l = x_m - 0.055 - len(f'Sum: {format_value(variance)}') * 0.0108 if variance > 1000000000000 else x_m - 0.22

        stats_text_left = (f"Mean: {format_value(mean)}\nStd Dev: {format_value(std_dev)}\n"
                           f"Median: {format_value(median)}\nVariance: {format_value(variance)}\n"
                           f"Coeff of Variation: {format_value(coeff_variation)}\n"
                           f"Total number of masks: {len(master_df['area'].to_list())}")

        stats_text_middle = (f"Skewness: {format_value(skewness)}\nKurtosis: {format_value(kurtosis)}\n"
                             f"Count: {count}\nSum: {format_value(total_sum)}\nIQR: {format_value(iqr)}")

        stats_text_right = (f"Lower quantile: {format_value(q1)}\nUpper quantile: {format_value(q3)}\n"
                            f"Min: {format_value(minimum)}\nMax: {format_value(maximum)}\n"
                            f"Range: {format_value(data_range)}")
        n = 'i' * int((194 * (1 - x_l + 0.011)))

        text = f"{n}\n{n}\n{n}\n{n}\n{n}\n{n}"
        text_properties = {
            'fontsize': 12,
            'color': 'none',
            'verticalalignment': 'top',
            'bbox': dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white", alpha=0.5)
        }

        plt.text(x_l, 0.98, text, transform=plt.gca().transAxes, **text_properties)
        plt.text(x_l, 0.98, stats_text_left, horizontalalignment='left',
                 verticalalignment='top', transform=plt.gca().transAxes, fontsize=12)
        plt.text(x_m, 0.98, stats_text_middle, horizontalalignment='left',
                 verticalalignment='top', transform=plt.gca().transAxes, fontsize=12)
        plt.text(x_r, 0.98, stats_text_right, horizontalalignment='left',
                 verticalalignment='top', transform=plt.gca().transAxes, fontsize=12)

        plt.show()

    for filepath in filepaths:
        img = load_image(filepath)
        files_folder = Path(filepath).parent / (Path(filepath).stem + '_files')
        file_p = files_folder / (Path(filepath).stem + '_filtered_dataframe.csv')
        df_filtered = pd.read_csv(file_p)
        file_p = files_folder / (Path(filepath).stem + '_filtered_masks.png')
        labels = load_image(file_p.as_posix())

        fig, ax = plt.subplot_mosaic([['left', 'right'], ['left2', 'right2']],
                                     constrained_layout=True, figsize=(12, 9))
        ax['left'].imshow(img, cmap='gray')
        ax['left'].axis('off')

        ax['right'].imshow(labels, interpolation='nearest')
        ax['right'].axis('off')

        ax['right2'].axis('off')

        plt.suptitle(Path(filepath).name, fontsize=18)

        df_filtered['area'].hist(bins='auto', ax=ax['left2'], edgecolor='k', color='#0081C6')
        ax['left2'].set_title(f'Histogram of area ({unit})')
        ax['left2'].set_xlabel(f'area ({unit})')
        ax['left2'].grid(False)
        ax['left2'].set_ylabel('Count')

        filters = load_dictionary(filepath)
        min_area = round(filters['min_area'], 1)
        max_area = round(filters['max_area'], 1)
        min_solidity = round(filters['min_solidity'], 3)
        max_solidity = round(filters['max_solidity'], 3)
        min_intensity = filters['min_intensity']
        max_intensity = filters['max_intensity']
        min_eccentricity = round(filters['min_eccentricity'], 3)
        max_eccentricity = round(filters['max_eccentricity'], 3)
        overlap = filters['overlap']
        overlapping_masks = filters['overlapping_masks']
        scaling = round(filters['scaling'], 3)
        removed = filters['removed']
        remain = filters['remain']
        segmentation = filters['segmentation']

        x1 = 0.5845
        x2 = 0.8
        fig.text(x1, 0.495, 'Used parameter values:', fontsize=18)

        fig.text(x1, 0.455, 'Segmentation:', fontsize=18)
        fig.text(0.75, 0.455, segmentation, fontsize=18)

        fig.text(x1, 0.415, f'Area ({unit2}):', fontsize=18)
        fig.text(x2, 0.415, f'({round(min_area, 1)}, {round(max_area, 1)})', fontsize=18)

        fig.text(x1, 0.375, 'Solidity:', fontsize=18)
        fig.text(x2, 0.375, f'({min_solidity}, {max_solidity})', fontsize=18)

        fig.text(x1, 0.335, 'Intensity:', fontsize=18)
        fig.text(x2, 0.335, f'({min_intensity}, {max_intensity})', fontsize=18)

        fig.text(x1, 0.295, 'Eccentricity:', fontsize=18)
        fig.text(x2, 0.295, f'({min_eccentricity}, {max_eccentricity})', fontsize=18)

        fig.text(x1, 0.255, 'Overlap:', fontsize=18)
        fig.text(x2, 0.255, f'{overlap}', fontsize=18)

        fig.text(x1, 0.185, 'Number of \noverlapping masks:', fontsize=18)
        fig.text(x2, 0.185, f'{overlapping_masks}', fontsize=18)

        fig.text(x1, 0.145, f'Scaling (px/{unit}):', fontsize=18)
        fig.text(x2, 0.145, f'{scaling}', fontsize=18)
        fig.text(0.63, 0.055, f'{removed} masks removed.\n {remain} remain.', fontsize=18, multialignment='center')

        plt.show()

    save_image()
